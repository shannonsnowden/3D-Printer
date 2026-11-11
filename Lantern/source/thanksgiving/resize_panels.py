"""Width-only lantern correction. Requires numpy, trimesh, manifold3d.
Run: /workspace/lantern-analysis-venv/bin/python resize_panels.py
Never writes to source STL directory. X scale=77.5/84.4; Y/Z scale=1.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import trimesh
import manifold3d as md
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'stls'
DESIGNS=['turkey','cornucopia','pumpkin','leaves','pilgrim_hat','pumpkin_pie']
SCALE=77.5/84.4

def solid(mesh):
    result=md.Manifold(md.Mesh64(np.asarray(mesh.vertices,dtype=np.float64),np.asarray(mesh.faces,dtype=np.uint64)))
    if result.status()!=md.Error.NoError:raise ValueError(result.status())
    return result

def from_solid(obj):
    m=obj.to_mesh64()
    return trimesh.Trimesh(vertices=m.vert_properties[:,:3],faces=m.tri_verts,process=False)

originals=[SOURCE/f'lantern_panel_{n}.stl' for n in DESIGNS]+[SOURCE/'lantern_panel_blank.stl',SOURCE/'lantern_base.stl',SOURCE/'lantern_roof.stl',ROOT.parent/'lantern.scad',ROOT.parent/'lantern_v2_backup.scad']
report={'source_width_mm':84.4,'target_width_mm':77.5,'user_slot_span_mm':78,'nominal_total_clearance_mm':0.5,'scale_xyz':[SCALE,1,1],'original_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in originals},'panels':{}}
for n in DESIGNS:
    source=trimesh.load_mesh(SOURCE/f'lantern_panel_{n}.stl')
    scaled=source.copy();scaled.vertices[:,0]*=SCALE
    needs_normalization=not scaled.is_watertight
    # Three originals contain one four-face edge at a near-coincident artwork boundary.
    # Normalize topology in float64, without remeshing or smoothing the artwork.
    result=from_solid(solid(scaled)) if needs_normalization else scaled
    assert result.is_watertight and result.is_winding_consistent
    dest=ROOT/f'lantern_panel_{n}_78mm_slots.stl'
    dest.write_text(trimesh.exchange.stl.export_stl_ascii(result))
    reloaded=trimesh.load_mesh(dest)
    np.testing.assert_allclose(reloaded.extents,[77.5,105,1.8],atol=1e-7,rtol=0)
    # Set equality in volume vs normalized original after the same affine transform.
    ideal=solid(scaled);actual=solid(reloaded)
    symmetric_difference=abs((ideal-actual).volume())+abs((actual-ideal).volume())
    assert symmetric_difference<1e-6
    expected_volume=source.volume*SCALE
    assert abs(reloaded.volume-expected_volume)<1e-3
    # All emitted vertices originate in the width-only-transformed input; no Y/Z shift.
    from scipy.spatial import cKDTree
    vertex_delta=float(cKDTree(scaled.vertices).query(reloaded.vertices)[0].max())
    assert vertex_delta<1e-7
    report['panels'][n]={'file':dest.name,'bounds':reloaded.bounds.tolist(),'extents':reloaded.extents.tolist(),'watertight':bool(reloaded.is_watertight),'winding_consistent':bool(reloaded.is_winding_consistent),'original_watertight':bool(source.is_watertight),'inherited_nonmanifold_edge_normalized':needs_normalization,'volume_mm3':float(reloaded.volume),'volume_difference_from_pure_affine_mm3':float(reloaded.volume-expected_volume),'symmetric_difference_vs_normalized_affine_mm3':float(symmetric_difference),'max_vertex_distance_from_affine_input_mm':vertex_delta,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
# Diagnostic: exact width-transformed blank-panel middle strip.
# Preserves side rails, their bevel, and the .7mm connecting glow sheet.
blank=trimesh.load_mesh(SOURCE/'lantern_panel_blank.stl');blank.vertices[:,0]*=SCALE
crop=trimesh.creation.box(extents=[100,8,10]);crop.apply_translation([0,0,0.9])
strip=from_solid(solid(blank)^solid(crop))
dest=ROOT/'diagnostic_fit_strip_77p5x8mm.stl';dest.write_text(trimesh.exchange.stl.export_stl_ascii(strip))
strip=trimesh.load_mesh(dest)
np.testing.assert_allclose(strip.extents,[77.5,8,1.8],atol=1e-7,rtol=0)
assert strip.is_watertight
# Same X/Z side edge section as the complete blank (crop only removed distant Y).
report['diagnostic_strip']={'file':dest.name,'extents':strip.extents.tolist(),'watertight':bool(strip.is_watertight),'volume_mm3':float(strip.volume),'side_profile':'Exact middle slice of X-scaled original blank; 0.7mm field + 1.8mm rails; unchanged Y/Z.'}
assert all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in report['original_sha256'].items())
(ROOT/'evidence/build_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
