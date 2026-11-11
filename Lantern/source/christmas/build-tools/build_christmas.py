#!/usr/bin/env python3
"""Export the four Christmas panels from OpenSCAD at final size.

No post-export scaling. OpenSCAD writes the mesh directly at 77.5 x 105 x 1.8.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import trimesh
import manifold3d as md

ROOT = Path(__file__).resolve().parents[1]
SCAD = ROOT / "holidays" / "christmas" / "source" / "christmas.scad"
OUT = ROOT / "holidays" / "christmas" / "stl"
PARTS = {
    "tree": "lantern_panel_christmas_tree.stl",
    "snowman": "lantern_panel_christmas_snowman.stl",
    "reindeer": "lantern_panel_christmas_reindeer.stl",
    "wreath": "lantern_panel_christmas_wreath.stl",
}
# v6 meshes are already exported. Tree and wreath are frozen bytes.
# Snowman and reindeer come from tools/build_v6_panels.py.
DEFAULT_PARTS = []
FROZEN = {"tree", "snowman", "reindeer", "wreath"}


def seal_if_needed(dest: Path) -> None:
    """Drop a non-manifold CGAL sliver without moving the artwork."""
    mesh = trimesh.load_mesh(dest)
    if mesh.is_watertight and mesh.is_winding_consistent:
        return
    solid = md.Manifold(md.Mesh64(
        np.asarray(mesh.vertices, dtype=np.float64),
        np.asarray(mesh.faces, dtype=np.uint64),
    ))
    if solid.status() != md.Error.NoError:
        raise SystemExit(f"{dest.name} manifold status {solid.status()}")
    sealed_mesh = solid.to_mesh64()
    sealed = trimesh.Trimesh(
        vertices=sealed_mesh.vert_properties[:, :3],
        faces=sealed_mesh.tri_verts,
        process=False,
    )
    if not sealed.is_watertight:
        raise SystemExit(f"{dest.name} still not watertight after seal")
    if abs(sealed.volume - mesh.volume) > 1e-3:
        raise SystemExit(f"{dest.name} seal changed volume by {sealed.volume - mesh.volume}")
    dest.write_text(trimesh.exchange.stl.export_stl_ascii(sealed))
    print(f"sealed {dest.name}", flush=True)


def export_part(part: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "openscad",
        "-o",
        str(dest),
        "-D",
        f'part="{part}"',
        str(SCAD),
    ]
    print(" ".join(cmd), flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    if result.returncode != 0:
        raise SystemExit(f"OpenSCAD failed for {part} (exit {result.returncode})")
    if not dest.is_file() or dest.stat().st_size < 1000:
        raise SystemExit(f"OpenSCAD did not write a mesh for {part}")
    seal_if_needed(dest)


def main(argv: list[str]) -> None:
    selected = argv[1:] or list(DEFAULT_PARTS)
    frozen = [name for name in selected if name in FROZEN]
    if frozen:
        raise SystemExit(
            "Refusing to overwrite frozen Christmas meshes from OpenSCAD: "
            + ", ".join(frozen)
            + ". Snowman and reindeer v6 are built by tools/build_v6_panels.py."
        )
    unknown = [name for name in selected if name not in PARTS and name != "blank"]
    if unknown:
        raise SystemExit(f"Unknown part(s): {unknown}")
    for part in selected:
        if part == "blank":
            export_part("blank", ROOT / "build" / "panel_blank.stl")
        else:
            export_part(part, OUT / PARTS[part])
    print("exported", ", ".join(selected))


if __name__ == "__main__":
    main(sys.argv)
