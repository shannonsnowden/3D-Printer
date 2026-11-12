#!/usr/bin/env python3
"""Render flat and simulated-backlit previews from exported STL meshes.

Colors come from the top surface height of the same mesh that is printed:
  under 0.95 mm  field  (0.7 mm sheet)
  under 1.30 mm  detail (1.1 mm groove floor)
  otherwise      silhouette and rails (1.8 mm)

The backlit palette is a simulation of thickness, not a photograph.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
XMAS = ROOT / "holidays" / "christmas" / "stl"
PREVIEW = ROOT / "holidays" / "christmas" / "previews"

PANELS = [
    ("tree", "lantern_panel_christmas_tree.stl", "Christmas tree"),
    ("snowman", "lantern_panel_christmas_snowman.stl", "Snowman"),
    ("reindeer", "lantern_panel_christmas_reindeer.stl", "Reindeer"),
    ("wreath", "lantern_panel_christmas_wreath.stl", "Wreath"),
]

FLAT = {
    "bg": (247, 246, 244),
    "field": (192, 192, 180),
    "mid": (156, 132, 108),
    "dark": (120, 60, 24),
    "ink": (62, 42, 32),
}
BACKLIT = {
    "bg": (244, 241, 234),
    "field": (192, 180, 120),
    "mid": (168, 96, 36),
    "dark": (48, 24, 0),
    "ink": (48, 28, 16),
}

FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


def load_mesh(path: Path) -> trimesh.Trimesh:
    mesh = trimesh.load_mesh(path)
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))
    return mesh


def raster_panel(mesh: trimesh.Trimesh, ppm: float, palette: dict) -> Image.Image:
    xmin, ymin, _ = mesh.bounds[0]
    xmax, ymax, _ = mesh.bounds[1]
    width = int(np.ceil((xmax - xmin) * ppm)) + 2
    height = int(np.ceil((ymax - ymin) * ppm)) + 2
    image = Image.new("RGB", (width, height), palette["bg"])
    draw = ImageDraw.Draw(image)
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.faces)
    ordered = []
    for index, tri in enumerate(faces):
        points = vertices[tri]
        normal = np.cross(points[1] - points[0], points[2] - points[0])
        if normal[2] <= 0.2:
            continue
        ordered.append((float(points[:, 2].max()), index))
    ordered.sort()
    for zmax, index in ordered:
        points = vertices[faces[index]]
        if zmax < 0.95:
            color = palette["field"]
        elif zmax < 1.30:
            color = palette["mid"]
        else:
            color = palette["dark"]
        polygon = [
            (float((x - xmin) * ppm) + 1.0, float((ymax - y) * ppm) + 1.0)
            for x, y, _ in points
        ]
        draw.polygon(polygon, fill=color)
    return image


_RAY_Z = {}


def ray_panel(mesh: trimesh.Trimesh, ppm: float, palette: dict) -> Image.Image:
    """Pixel-center rays. Used when a boolean mesh is too slivered to paint."""
    xmin, ymin, _ = mesh.bounds[0]
    xmax, ymax, _ = mesh.bounds[1]
    width = max(1, int(round((xmax - xmin) * ppm)))
    height = max(1, int(round((ymax - ymin) * ppm)))
    cache_key = (len(mesh.faces), round(float(mesh.volume), 3), width, height)
    cached = _RAY_Z.get(cache_key)
    if cached is not None:
        zz = cached
        rgb = np.empty((height, width, 3), dtype=np.uint8)
        rgb[:] = palette["bg"]
        covered = np.isfinite(zz)
        rgb[covered] = palette["field"]
        rgb[covered & (zz >= 0.95) & (zz < 1.30)] = palette["mid"]
        rgb[covered & (zz >= 1.30)] = palette["dark"]
        return Image.fromarray(rgb)
    yy, xx = np.mgrid[0:height, 0:width]
    xs = xmin + (xx.ravel() + 0.5) / ppm
    ys = ymax - (yy.ravel() + 0.5) / ppm
    origins = np.column_stack([xs, ys, np.full(xs.shape, 4.0)])
    directions = np.tile([0.0, 0.0, -1.0], (len(xs), 1))
    z = np.full(len(xs), np.nan, dtype=np.float64)
    step = 50000
    for start in range(0, len(xs), step):
        loc, idx, _ = mesh.ray.intersects_location(
            origins[start : start + step],
            directions[start : start + step],
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
    zz = z.reshape(height, width)
    _RAY_Z[cache_key] = zz
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[:] = palette["bg"]
    covered = np.isfinite(zz)
    rgb[covered] = palette["field"]
    rgb[covered & (zz >= 0.95) & (zz < 1.30)] = palette["mid"]
    rgb[covered & (zz >= 1.30)] = palette["dark"]
    return Image.fromarray(rgb)


def render_one(path: Path, ppm: float, palette: dict) -> Image.Image:
    mesh = load_mesh(path)
    # Row-box booleans (the v6 reindeer) leave sliver triangles that a painter streaks.
    if len(mesh.faces) > 6000:
        return ray_panel(mesh, ppm, palette)
    supersampled = raster_panel(mesh, ppm * 2.0, palette)
    return supersampled.resize(
        (max(1, supersampled.width // 2), max(1, supersampled.height // 2)),
        Image.Resampling.LANCZOS,
    )


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size)


def four_up(mode: str, ppm: float, dest: Path) -> None:
    palette = FLAT if mode == "flat" else BACKLIT
    panels = [(label, render_one(XMAS / filename, ppm, palette)) for _, filename, label in PANELS]
    panel_w = max(image.width for _, image in panels)
    panel_h = max(image.height for _, image in panels)
    margin = 72
    gap = 40
    label_h = 64
    title_h = 132
    width = margin * 2 + panel_w * 2 + gap
    height = margin + title_h + (panel_h + label_h) * 2 + gap + margin
    canvas = Image.new("RGB", (width, height), palette["bg"])
    draw = ImageDraw.Draw(canvas)
    title = "Christmas panels — flat relief review" if mode == "flat" else "Christmas panels — SIMULATED backlighting"
    subtitle = "Not a photograph. Color shows thickness: cream 0.7 mm, amber 1.1 mm, dark 1.8 mm."
    if mode == "flat":
        subtitle = "Same exported meshes as the STLs. 77.5 × 105 × 1.8 mm. Graphics approved 9 Nov 2026."
    draw.text((margin, 36), title, fill=palette["ink"], font=font(42, bold=True))
    draw.text((margin, 92), subtitle, fill=palette["ink"], font=font(24))
    if mode == "backlit":
        draw.text(
            (margin, 124),
            "SIMULATED illumination, not a photo. Approved 9 Nov 2026. The 77.5 × 105 × 1.8 mm panels have been printed and fit the lantern well (confirmed by Shannon, Nov 2026).",
            fill=palette["ink"],
            font=font(22),
        )
    origin_y = margin + title_h
    for index, (label, image) in enumerate(panels):
        col = index % 2
        row = index // 2
        x = margin + col * (panel_w + gap) + (panel_w - image.width) // 2
        y = origin_y + row * (panel_h + label_h + gap)
        canvas.paste(image, (x, y))
        label_x = margin + col * (panel_w + gap)
        label_y = y + image.height + 12
        draw.text((label_x, label_y), label, fill=palette["ink"], font=font(32, bold=True))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest)
    print(dest, canvas.size)


def individuals(ppm: float) -> None:
    for key, filename, _label in PANELS:
        for mode, palette in (("flat", FLAT), ("backlit", BACKLIT)):
            image = render_one(XMAS / filename, ppm, palette)
            dest = PREVIEW / f"{key}_{mode}.png"
            image.save(dest)
            print(dest, image.size)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ppm", type=float, default=16.0, help="Pixels per millimetre in the output")
    parser.add_argument("--individuals", action="store_true")
    args = parser.parse_args()
    PREVIEW.mkdir(parents=True, exist_ok=True)
    four_up("flat", args.ppm, PREVIEW / "christmas_panels_flat_4up.png")
    four_up("backlit", args.ppm, PREVIEW / "christmas_panels_backlit_SIMULATED_4up.png")
    if args.individuals:
        individuals(args.ppm)


if __name__ == "__main__":
    main()
