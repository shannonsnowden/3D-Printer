#!/usr/bin/env python3
"""Build Christmas v6 snowman and reindeer meshes from the approved art.

Tree and wreath STLs are not rewritten. Edits are boolean changes inside the
approved changed-pixel masks. Rails outside those masks stay on the v5 mesh.
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import trimesh
import manifold3d as md

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "holidays" / "christmas" / "source" / "v6_approved"
STL = ROOT / "holidays" / "christmas" / "stl"
W, H = 1086, 1471
SX, SY = W / 77.5, H / 105.0
XMIN, YMAX = -38.75, 52.5


def to_manifold(mesh: trimesh.Trimesh) -> md.Manifold:
    return md.Manifold(md.Mesh64(
        np.asarray(mesh.vertices, dtype=np.float64),
        np.asarray(mesh.faces, dtype=np.uint64),
    ))


def from_manifold(solid: md.Manifold) -> trimesh.Trimesh:
    # A second manifold pass plus merge_vertices is required. The raw boolean
    # mesh reloads from STL with open edges until those coincident vertices weld.
    healed = md.Manifold(solid.to_mesh64())
    out = healed.to_mesh64()
    mesh = trimesh.Trimesh(out.vert_properties[:, :3], out.tri_verts, process=True)
    return mesh


def components(mask: np.ndarray, min_pixels: int) -> np.ndarray:
    count, labels = cv2.connectedComponents(mask.astype(np.uint8))
    if count <= 1:
        return mask.astype(bool)
    sizes = np.bincount(labels.ravel())
    keep = np.zeros(count, dtype=bool)
    keep[1:] = sizes[1:] >= min_pixels
    return keep[labels]


def union_all(parts: list[md.Manifold]) -> md.Manifold:
    solid = parts[0]
    for part in parts[1:]:
        solid = solid + part
    return solid


def runs(mask: np.ndarray) -> list[tuple[int, int, int]]:
    """Return (y, x0, x1) inclusive pixel runs."""
    found = []
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return found
    order = np.lexsort((xs, ys))
    ys, xs = ys[order], xs[order]
    start = 0
    for index in range(1, len(ys) + 1):
        end_run = index == len(ys) or ys[index] != ys[start] or xs[index] != xs[index - 1] + 1
        if end_run:
            found.append((int(ys[start]), int(xs[start]), int(xs[index - 1])))
            start = index
    return found


def boxes_for_runs(mask: np.ndarray, z0: float, z1: float, pad: float = 0.02) -> list[md.Manifold]:
    solids = []
    dx, dy = 1.0 / SX, 1.0 / SY
    for y, x0, x1 in runs(mask):
        width = (x1 - x0 + 1) * dx + 2 * pad
        height = dy + 2 * pad
        cx = XMIN + ((x0 + x1 + 1) / 2) / SX
        cy = YMAX - (y + 0.5) / SY
        box = trimesh.creation.box(extents=[width, height, z1 - z0])
        box.apply_translation([cx, cy, (z0 + z1) / 2])
        solids.append(to_manifold(box))
    return solids


def edit_mesh(source: Path, change_mask: np.ndarray, dark: np.ndarray, amber: np.ndarray) -> trimesh.Trimesh:
    original = trimesh.load(source)
    if not change_mask.any():
        raise SystemExit(f"no edit pixels for {source.name}")
    cutter = union_all(boxes_for_runs(change_mask, -0.2, 2.6, pad=0.015))
    kept = to_manifold(original) - cutter
    sheet = change_mask & ~dark & ~amber
    additions = [kept]
    additions.extend(boxes_for_runs(sheet, 0.0, 0.7, pad=0.02))
    if dark.any():
        additions.extend(boxes_for_runs(dark, 0.0, 1.8, pad=0.02))
    if amber.any():
        additions.extend(boxes_for_runs(amber, 0.0, 1.1, pad=0.02))
    solid = union_all(additions)
    if solid.status() != md.Error.NoError:
        raise SystemExit(f"manifold status {solid.status()} for {source.name}")
    mesh = from_manifold(solid)
    return mesh


def seal_export(mesh: trimesh.Trimesh, dest: Path) -> trimesh.Trimesh:
    """Write an STL that reloads watertight. merge_vertices after a manifold pass is required."""
    mesh.export(dest)
    loaded = trimesh.load(dest)
    if loaded.is_watertight and loaded.is_winding_consistent and len(loaded.split()) == 1:
        return loaded
    solid = to_manifold(loaded)
    if solid.status() != md.Error.NoError:
        raise SystemExit(f"manifold status {solid.status()} while sealing {dest.name}")
    healed = from_manifold(solid)
    healed.export(dest)
    loaded = trimesh.load(dest)
    parts = loaded.split()
    if not loaded.is_watertight or not loaded.is_winding_consistent or len(parts) != 1:
        raise SystemExit(
            f"{dest.name} still open after seal watertight={loaded.is_watertight} "
            f"winding={loaded.is_winding_consistent} bodies={len(parts)}"
        )
    return loaded


def build_snowman() -> None:
    art = ART
    change = np.array(Image_open(art / "derived/christmas_2_snowman_v6_changed_vs_v5_mask.png")) > 0
    classes = np.array(Image_open(art / "derived/christmas_2_snowman_v6_thickness_classes.png"))
    dark = components(change & (classes == 254), 1)
    amber = np.zeros_like(dark)
    sheet_region = change & ~dark
    mesh = edit_mesh(STL / "lantern_panel_christmas_snowman.stl", sheet_region | dark, dark, amber)
    dest = STL / "lantern_panel_christmas_snowman.stl"
    sealed = seal_export(mesh, dest)
    print("snowman", dest.name, sealed.extents.tolist(), sealed.is_watertight, "merge_vertices_required", True)


def Image_open(path: Path):
    from PIL import Image
    return Image.open(path)


def build_reindeer() -> None:
    art = ART
    change = np.array(Image_open(art / "derived/christmas_3_reindeer_v6_changed_vs_v5_mask.png")) > 0
    classes = np.array(Image_open(art / "derived/christmas_3_reindeer_v6_thickness_classes.png"))
    dark = components(change & (classes == 254), 1)
    amber = np.zeros_like(dark)
    mesh = edit_mesh(STL / "lantern_panel_christmas_reindeer.stl", change, dark, amber)
    dest = STL / "lantern_panel_christmas_reindeer.stl"
    sealed = seal_export(mesh, dest)
    print("reindeer", dest.name, sealed.extents.tolist(), sealed.is_watertight, "merge_vertices_required", True)


def main() -> None:
    which = sys.argv[1:] or ["snowman", "reindeer"]
    if "snowman" in which:
        build_snowman()
    if "reindeer" in which:
        build_reindeer()


if __name__ == "__main__":
    main()
