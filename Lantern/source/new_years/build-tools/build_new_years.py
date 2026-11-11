#!/usr/bin/env python3
"""Build New Year's v1 panels from the approved thickness maps.

The mechanical frame is the OpenSCAD blank used for Christmas v6.
Artwork is extruded from the approved class maps inside that frame.
The frame mask is used only to keep artwork off the rails. It is not traced.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import trimesh
import manifold3d as md
from shapely.geometry import Polygon

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "holidays" / "new_years" / "source" / "v1_approved"
STL = ROOT / "holidays" / "new_years" / "stl"
BLANK = ROOT / "build" / "panel_blank.stl"
SCAD = ROOT / "holidays" / "christmas" / "source" / "christmas.scad"

# Documented panel transform. Pixel (0,0) is the top-left of the outline.
PX_PER_MM_X = 14.0129
PX_PER_MM_Y = 14.0095
XMIN = -38.75
YMAX = 52.5

# Amber crumbs smaller than this are anti-aliased edge snaps, not dots.
# A 0.6 mm sparkle centre is about 55 px, so 12 px still keeps it.
AMBER_MIN_PX = 12

PARTS = {
    "fireworks": "new_years_1_fireworks_thickness_classes.png",
    "midnight_clock": "new_years_2_midnight_clock_thickness_classes.png",
    "champagne_toast": "new_years_3_champagne_toast_thickness_classes.png",
    "party_hat": "new_years_4_party_hat_streamers_thickness_classes.png",
}


def to_manifold(mesh: trimesh.Trimesh) -> md.Manifold:
    return md.Manifold(md.Mesh64(
        np.asarray(mesh.vertices, dtype=np.float64),
        np.asarray(mesh.faces, dtype=np.uint64),
    ))


def from_manifold(solid: md.Manifold) -> trimesh.Trimesh:
    out = solid.to_mesh64()
    return trimesh.Trimesh(out.vert_properties[:, :3], out.tri_verts, process=False)


def ensure_blank() -> trimesh.Trimesh:
    if not BLANK.is_file():
        BLANK.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["openscad", "-o", str(BLANK), "-D", 'part="blank"', str(SCAD)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 or not BLANK.is_file():
            raise SystemExit(result.stderr or "OpenSCAD did not write the blank")
    mesh = trimesh.load(BLANK)
    if not mesh.is_watertight or len(mesh.split()) != 1:
        raise SystemExit("panel blank is not a single watertight body")
    return mesh


def to_world(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=np.float64)
    return np.column_stack([
        pts[:, 0] / PX_PER_MM_X + XMIN,
        YMAX - pts[:, 1] / PX_PER_MM_Y,
    ])


def keep_components(mask: np.ndarray, min_px: int) -> tuple[np.ndarray, int]:
    count, labels = cv2.connectedComponents(mask.astype(np.uint8))
    if count <= 1:
        return mask.astype(bool), 0
    sizes = np.bincount(labels.ravel())
    keep = sizes >= min_px
    keep[0] = False
    dropped = int((~keep).sum() - 1)
    return keep[labels], dropped


def polygons_from_mask(mask: np.ndarray) -> list[Polygon]:
    image = mask.astype(np.uint8) * 255
    contours, hierarchy = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy is None:
        return []
    hierarchy = hierarchy[0]
    polygons = []
    for index, contour in enumerate(contours):
        if hierarchy[index][3] != -1:
            continue
        outer = contour[:, 0, :]
        if len(outer) < 3:
            continue
        holes = []
        child = hierarchy[index][2]
        while child != -1:
            hole = contours[child][:, 0, :]
            if len(hole) >= 3:
                holes.append(to_world(hole))
            child = hierarchy[child][0]
        poly = Polygon(to_world(outer), holes)
        if not poly.is_valid:
            poly = poly.buffer(0)
        if poly.is_empty:
            continue
        if poly.geom_type == "MultiPolygon":
            polygons.extend(part for part in poly.geoms if part.area > 1e-6)
        elif poly.area > 1e-6:
            polygons.append(poly)
    return polygons


def extrude(poly: Polygon, height: float) -> md.Manifold:
    mesh = trimesh.creation.extrude_polygon(poly, height=height)
    return to_manifold(mesh)


def union_all(parts: list[md.Manifold]) -> md.Manifold:
    solid = parts[0]
    for part in parts[1:]:
        solid = solid + part
    return solid


def build_one(name: str, blank: md.Manifold) -> trimesh.Trimesh:
    classes = np.array(Image_open(ART / "vectors" / PARTS[name]))
    frame = np.array(Image_open(ART / "vectors" / "panel_frame_mask.png")) > 128
    interior = ~frame
    dark_mask, dark_dropped = keep_components((classes == 254) & interior, 1)
    amber_mask, amber_dropped = keep_components((classes == 127) & interior, AMBER_MIN_PX)
    # Amber insets must stay 1.1 mm, so they are removed from the dark solid.
    dark_only = dark_mask & ~amber_mask
    dark_polys = polygons_from_mask(dark_only)
    amber_polys = polygons_from_mask(amber_mask)
    if not dark_polys and not amber_polys:
        raise SystemExit(f"{name} has no artwork polygons")
    parts = [blank]
    parts.extend(extrude(poly, 1.8) for poly in dark_polys)
    parts.extend(extrude(poly, 1.1) for poly in amber_polys)
    solid = union_all(parts)
    if solid.status() != md.Error.NoError:
        raise SystemExit(f"{name} manifold status {solid.status()}")
    mesh = from_manifold(solid)
    print(
        f"{name} dark_polys={len(dark_polys)} amber_polys={len(amber_polys)} "
        f"amber_aa_dropped={amber_dropped} dark_dropped={dark_dropped} "
        f"raw_watertight={mesh.is_watertight} faces={len(mesh.faces)}",
        flush=True,
    )
    return mesh


def Image_open(path: Path):
    from PIL import Image
    return Image.open(path)


def seal_export(mesh: trimesh.Trimesh, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    raw_watertight = bool(mesh.is_watertight)
    mesh.export(dest)
    loaded = trimesh.load(dest)
    reloaded = bool(loaded.is_watertight and loaded.is_winding_consistent and len(loaded.split()) == 1)
    if not reloaded:
        # Coincident vertices from the boolean do not survive STL until they are welded.
        healed_solid = to_manifold(loaded)
        if healed_solid.status() != md.Error.NoError:
            raise SystemExit(f"{dest.name} manifold status {healed_solid.status()}")
        healed = trimesh.Trimesh(
            healed_solid.to_mesh64().vert_properties[:, :3],
            healed_solid.to_mesh64().tri_verts,
            process=True,
        )
        healed.merge_vertices()
        healed.export(dest)
        loaded = trimesh.load(dest)
    parts = loaded.split()
    if not loaded.is_watertight or not loaded.is_winding_consistent or len(parts) != 1:
        raise SystemExit(
            f"{dest.name} watertight={loaded.is_watertight} winding={loaded.is_winding_consistent} "
            f"bodies={len(parts)} raw_was_watertight={raw_watertight} reloaded_before_weld={reloaded}"
        )
    extents = [round(float(v), 4) for v in loaded.extents]
    print(
        f"saved {dest.name} extents={extents} watertight={loaded.is_watertight} "
        f"raw_watertight={raw_watertight} stl_watertight_before_weld={reloaded}",
        flush=True,
    )


def main() -> None:
    selected = sys.argv[1:] or list(PARTS)
    blank_mesh = ensure_blank()
    blank = to_manifold(blank_mesh)
    for name in selected:
        if name not in PARTS:
            raise SystemExit(f"unknown panel {name}")
        mesh = build_one(name, blank)
        seal_export(mesh, STL / f"lantern_panel_new_years_{name}.stl")


if __name__ == "__main__":
    main()
