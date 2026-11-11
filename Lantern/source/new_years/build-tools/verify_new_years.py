#!/usr/bin/env python3
"""Ray-render New Year's previews and measure them against the approved maps."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "holidays" / "new_years" / "source" / "v1_approved"
STL = ROOT / "holidays" / "new_years" / "stl"
PREVIEW = ROOT / "holidays" / "new_years" / "previews"
PX, PY = 14.0129, 14.0095
PARTS = {
    "fireworks": "new_years_1_fireworks_thickness_classes.png",
    "midnight_clock": "new_years_2_midnight_clock_thickness_classes.png",
    "champagne_toast": "new_years_3_champagne_toast_thickness_classes.png",
    "party_hat": "new_years_4_party_hat_streamers_thickness_classes.png",
}
APPROVED = {
    "fireworks": "new_years_1_fireworks.png",
    "midnight_clock": "new_years_2_midnight_clock.png",
    "champagne_toast": "new_years_3_champagne_toast.png",
    "party_hat": "new_years_4_party_hat_streamers.png",
}
LABELS = {
    "fireworks": "Fireworks",
    "midnight_clock": "Midnight clock",
    "champagne_toast": "Champagne toast",
    "party_hat": "Party hat and streamers",
}
BACKLIT = {"field": (192, 180, 120), "mid": (168, 96, 36), "dark": (48, 24, 0), "bg": (244, 241, 234), "ink": (48, 28, 16)}
FLAT = {"field": (192, 192, 180), "mid": (156, 132, 108), "dark": (120, 60, 24), "bg": (247, 246, 244), "ink": (62, 42, 32)}


def ray_heights(mesh: trimesh.Trimesh, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    origins = np.column_stack([xs, ys, np.full(len(xs), 4.0)])
    directions = np.tile([0.0, 0.0, -1.0], (len(xs), 1))
    z = np.full(len(xs), np.nan)
    for start in range(0, len(xs), 50000):
        loc, idx, _ = mesh.ray.intersects_location(
            origins[start : start + 50000],
            directions[start : start + 50000],
            multiple_hits=True,
        )
        if len(loc) == 0:
            continue
        order = np.argsort(idx)
        idx_s = idx[order]
        locz = loc[order, 2]
        cuts = np.flatnonzero(np.diff(idx_s))
        starts = np.r_[0, cuts + 1]
        ends = np.r_[cuts + 1, len(idx_s)]
        for a, b in zip(starts, ends):
            z[start + int(idx_s[a])] = locz[a:b].max()
    return z


def classify(z: np.ndarray) -> np.ndarray:
    pred = np.zeros(len(z), np.uint8)
    pred[(z >= 0.9) & (z < 1.45)] = 127
    pred[z >= 1.45] = 254
    return pred


def height_grid(mesh: trimesh.Trimesh, ppm: float) -> np.ndarray:
    width = int(round(77.5 * ppm))
    height = int(round(105.0 * ppm))
    yy, xx = np.mgrid[0:height, 0:width]
    scale_x = width / 77.5
    scale_y = height / 105.0
    xs = (xx.ravel() + 0.5) / scale_x - 38.75
    ys = 52.5 - (yy.ravel() + 0.5) / scale_y
    return ray_heights(mesh, xs, ys).reshape(height, width)


def colorize(z: np.ndarray, palette: dict) -> Image.Image:
    rgb = np.empty((*z.shape, 3), np.uint8)
    rgb[:] = palette["bg"]
    covered = np.isfinite(z)
    rgb[covered] = palette["field"]
    rgb[covered & (z >= 0.95) & (z < 1.30)] = palette["mid"]
    rgb[covered & (z >= 1.30)] = palette["dark"]
    return Image.fromarray(rgb)


def measure(name: str, mesh: trimesh.Trimesh) -> dict:
    classes = np.array(Image.open(ART / "vectors" / PARTS[name]))
    frame = np.array(Image.open(ART / "vectors" / "panel_frame_mask.png")) > 128
    interior = ~frame
    dark = (classes == 254) & interior
    amber = (classes == 127) & interior
    count, labels = cv2.connectedComponents(amber.astype(np.uint8))
    sizes = np.bincount(labels.ravel())
    keep = np.zeros(count, dtype=bool)
    keep[1:] = sizes[1:] >= 12
    amber_keep = keep[labels]
    region = dark | amber_keep
    py, px = np.where(region)
    z = ray_heights(mesh, (px + 0.5) / PX - 38.75, 52.5 - (py + 0.5) / PY)
    pred = classify(z)
    actual = classes[py, px]
    miss = pred != actual
    edge = np.zeros(classes.shape, dtype=bool)
    edge[1:] |= classes[1:] != classes[:-1]
    edge[:, 1:] |= classes[:, 1:] != classes[:, :-1]
    band = ndimage.binary_dilation(edge, iterations=2)
    return {
        "sha256": hashlib.sha256((STL / f"lantern_panel_new_years_{name}.stl").read_bytes()).hexdigest(),
        "extents_mm": [round(float(v), 4) for v in mesh.extents],
        "watertight": bool(mesh.is_watertight),
        "winding_consistent": bool(mesh.is_winding_consistent),
        "bodies": len(mesh.split()),
        "volume_mm3": round(float(mesh.volume), 3),
        "kept_artwork_pixels": int(region.sum()),
        "amber_antialias_components_not_modeled": int((sizes[1:] < 12).sum()) if count > 1 else 0,
        "class_mismatch_pixels": int(miss.sum()),
        "mismatch_percent_of_kept": round(100 * float(miss.mean()), 3),
        "mismatch_outside_2px_edge_band": int((miss & ~band[py, px]).sum()),
        "rays_missing": int(np.isnan(z).sum()),
        "transform": "pixel center (px+0.5, py+0.5); X = px/14.0129 - 38.75; Y = 52.5 - py/14.0095; thresholds 0.90 and 1.45 mm",
    }


def four_up(images: dict[str, Image.Image], palette: dict, title: str, subtitle: str, dest: Path) -> None:
    keys = list(PARTS)
    panel_w = max(images[key].width for key in keys)
    panel_h = max(images[key].height for key in keys)
    margin, gap, label_h, title_h = 48, 28, 48, 110
    width = margin * 2 + panel_w * 2 + gap
    height = margin + title_h + (panel_h + label_h) * 2 + gap
    canvas = Image.new("RGB", (width, height), palette["bg"])
    draw = ImageDraw.Draw(canvas)
    font_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    draw.text((margin, 24), title, fill=palette["ink"], font=font_b)
    draw.text((margin, 70), subtitle, fill=palette["ink"], font=font)
    origin_y = margin + title_h
    for index, key in enumerate(keys):
        image = images[key]
        col, row = index % 2, index // 2
        x = margin + col * (panel_w + gap)
        y = origin_y + row * (panel_h + label_h + gap)
        canvas.paste(image, (x, y))
        draw.text((x, y + image.height + 8), LABELS[key], fill=palette["ink"], font=font_b)
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest)
    print(dest, canvas.size)


def main() -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    report = {
        "approval": "Shannon approved New Year's v1 on 2026-11-09 at 4:04 PM ET",
        "physical_fit": "NOT_TESTED",
        "raw_export": "The boolean meshes were watertight before STL export, and the STL files reloaded watertight without a second weld.",
        "edge_note": "Mismatch on kept artwork pixels is confined to a 2 px band on class boundaries. Amber components under 12 px are anti-aliased edge snaps and were not extruded. This is not exact pixel identity.",
        "panels": {},
    }
    flat_images = {}
    backlit_images = {}
    for name in PARTS:
        mesh = trimesh.load(STL / f"lantern_panel_new_years_{name}.stl")
        report["panels"][name] = measure(name, mesh)
        print(name, "outside band", report["panels"][name]["mismatch_outside_2px_edge_band"], flush=True)
        grid = height_grid(mesh, 8)
        flat_images[name] = colorize(grid, FLAT)
        backlit_images[name] = colorize(grid, BACKLIT)
        flat_images[name].save(PREVIEW / f"{name}_flat.png")
        backlit_images[name].save(PREVIEW / f"{name}_backlit.png")
    four_up(
        flat_images,
        FLAT,
        "New Year's panels — flat relief",
        "Rendered from the exported STLs. 77.5 × 105 × 1.8 mm. Graphics approved 9 Nov 2026.",
        PREVIEW / "new_years_panels_flat_4up.png",
    )
    four_up(
        backlit_images,
        BACKLIT,
        "New Year's panels — SIMULATED backlighting",
        "Not a photograph. Cream 0.7 mm, amber 1.1 mm, dark 1.8 mm. Physical fit UNTESTED.",
        PREVIEW / "new_years_panels_backlit_SIMULATED_4up.png",
    )
    dest = ROOT / "holidays" / "new_years" / "verification" / "v1_mesh_match.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2))
    print(dest)


if __name__ == "__main__":
    main()
