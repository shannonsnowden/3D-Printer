from pathlib import Path
import sys, unittest, hashlib, json
import numpy as np
import trimesh
from shapely.geometry import Polygon
ROOT=Path(__file__).resolve().parent
DESIGNS=['turkey','cornucopia','pumpkin','leaves','pilgrim_hat','pumpkin_pie']
ORIGINAL='--original' in sys.argv
class DimensionContract(unittest.TestCase):
    def test_all_six_width_height_thickness(self):
        for n in DESIGNS:
            with self.subTest(design=n):
                f=ROOT.parent/'stls'/f'lantern_panel_{n}.stl' if ORIGINAL else ROOT/f'lantern_panel_{n}_78mm_slots.stl'
                self.assertTrue(f.is_file(),str(f))
                m=trimesh.load_mesh(f)
                np.testing.assert_allclose(m.extents,[77.5,105,1.8],atol=1e-5,rtol=0)
    def test_all_six_watertight(self):
        for n in DESIGNS:
            with self.subTest(design=n):
                f=ROOT.parent/'stls'/f'lantern_panel_{n}.stl' if ORIGINAL else ROOT/f'lantern_panel_{n}_78mm_slots.stl'
                self.assertTrue(f.is_file(),str(f))
                m=trimesh.load_mesh(f)
                self.assertTrue(m.is_watertight,n)
                self.assertTrue(m.is_winding_consistent,n)
    @unittest.skipIf(ORIGINAL,'New-output preservation checks only')
    def test_continuous_sheet_and_unchanged_thickness(self):
        for n in DESIGNS:
            with self.subTest(design=n):
                m=trimesh.load_mesh(ROOT/f'lantern_panel_{n}_78mm_slots.stl')
                original=trimesh.load_mesh(ROOT.parent/'stls'/f'lantern_panel_{n}.stl')
                np.testing.assert_allclose(m.bounds[:,1:],original.bounds[:,1:],atol=1e-5,rtol=0)
                np.testing.assert_allclose(np.unique(m.vertices[:,2]),np.unique(original.vertices[:,2]),atol=1e-5,rtol=0)
                for z in [0.01,0.35,0.69]:
                    s=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
                    loops=s.discrete
                    self.assertEqual(len(loops),1,(n,z,'sheet must have one outer loop and no holes'))
                    poly=Polygon(loops[0][:,:2]); self.assertTrue(poly.is_valid); self.assertGreater(poly.area,8000)
                # Uniform grid rays through the sheet: solid from bed to at least .7mm everywhere sampled.
                xy=np.array([(x,y) for x in np.linspace(-33,33,15) for y in np.linspace(-44,44,17)])
                origins=np.column_stack([xy,np.full(len(xy),-1.)]); directions=np.tile([0,0,1.],(len(xy),1))
                pts,idx,_=m.ray.intersects_location(origins,directions,multiple_hits=True)
                for i in range(len(xy)):
                    # Rays tangent to artwork boundaries can have extra hits ABOVE the sheet.
                    heights=np.sort(pts[idx==i,2]); self.assertGreaterEqual(len(heights),2,(n,i,heights))
                    self.assertAlmostEqual(heights[0],0,places=5); self.assertGreaterEqual(heights[1],0.7-1e-5)
    @unittest.skipIf(ORIGINAL,'New diagnostic only')
    def test_fit_strip(self):
        f=ROOT/'diagnostic_fit_strip_77p5x8mm.stl';self.assertTrue(f.is_file())
        m=trimesh.load_mesh(f);np.testing.assert_allclose(m.extents,[77.5,8,1.8],atol=1e-5,rtol=0)
        self.assertTrue(m.is_watertight)
        blank=trimesh.load_mesh(ROOT.parent/'stls/lantern_panel_blank.stl');blank.vertices[:,0]*=77.5/84.4
        def profile(mesh):
            sec=mesh.section(plane_origin=[0,0,0],plane_normal=[0,1,0])
            return Polygon(sec.discrete[0][:,[0,2]])
        self.assertLess(profile(m).symmetric_difference(profile(blank)).area,1e-8)
    @unittest.skipIf(ORIGINAL,'Original hash manifest after build')
    def test_originals_unchanged(self):
        data=json.loads((ROOT/'evidence/build_verification.json').read_text())
        for f,h in data['original_sha256'].items():
            self.assertEqual(hashlib.sha256(Path(f).read_bytes()).hexdigest(),h)
if __name__=='__main__':unittest.main(argv=[sys.argv[0]],verbosity=2)
