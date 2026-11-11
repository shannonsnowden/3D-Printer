# St Patrick's Day lantern panels v1: IMAGES FOR APPROVAL, NO STL
These are 2D artwork only. No STL, CAD, repo change, ZIP, cloud agent, upload, print or contact. The backlighting is simulated, with each colour simply standing for a thickness. Physical fit is untested.

Started on Shannon's "do it" (Nov 10, 2026, 4:42 PM ET). Every earlier holiday folder is unchanged.

## Panels
1. **Four-leaf clover:** all my own geometry.
   - Four dark heart-shaped leaves with their tips meeting at a central boss.
   - Thin cream separation lines between the leaves; the stem fills the lower gap.
   - Each leaf has an amber inset heart outline and an amber midrib.
   - A thick, gently S-curved dark stem.
   - Around it: four small amber three-leaf shamrocks and three sparkles.
2. **Leprechaun hat:** all my own geometry.
   - A tapered dark crown with a soft domed top.
   - A dark band edged with two amber lines.
   - A bold amber square buckle with a dark opening, a centre post and a tongue.
   - An amber shamrock tucked in the band.
   - A wide upturned dark brim with an amber rim line and an amber highlight stroke on the crown.
   - Below: a stack of four gold coins and four flat coins (amber faces, dark rims). Shamrocks and sparkles fill the background.
3. **Pot of gold at the rainbow's end:** all my own geometry.
   - A tall rainbow of four bands, alternating dark and amber, with about 0.7 mm cream gaps between them.
   - The left foot rests in an amber cloud with a dark outline. The right foot disappears into a heap of gold coins.
   - The coins sit in a dark cauldron with a rim, ring handles, small legs, and amber highlight strokes.
   - Two coins on the ground, plus shamrocks and sparkles.
4. **Celtic harp:** the traditional Irish harp emblem, from a CC0 drawing.
   - My recolouring:
     - the frame (pillar, neck and soundbox) is solid dark
     - the seven strings are dark
     - the Celtic chain-link ornament on the pillar and soundbox is amber
     - the seven tuning-peg dots on the neck are amber
   - I added one amber shamrock and two sparkles.

No text, no year, no through-holes.

## Sources and licenses
- **Harp:** Openclipart #8526, "Celtic Harp" by Gerald_G. The file's metadata says Public Domain (http://creativecommons.org/licenses/publicdomain/), and Openclipart releases all its art under CC0 1.0. No attribution required; credit given as a courtesy.
  - Page: https://openclipart.org/detail/8526
  - SVG: https://openclipart.org/download/8526, saved as `refs/openclipart_8526_celtic_harp.svg`.
  - I flattened its paths with svgelements, kept the even-odd fill so the string openings and rings stay open, recoloured it, and placed it at 1040 px tall (about 74 mm), centred, top at y = 200.
- **Panels 1–3 and every added shamrock, coin and sparkle:** my own simple geometry. This covers the parametric hearts and shamrocks, hat, buckle, rainbow arcs, cloud, cauldron and coins.
- I also looked at Openclipart's shamrock, leprechaun-hat and pot-of-gold clipart (#189385, #3477, #244303) for proportions only. None of their geometry is used.
- **Frame and template:** copied unchanged from Easter v1, Valentine's v2 and New Year's v1, which in turn came from Christmas v6.

## Dimensions and registration
- Each panel PNG is 1086 × 1471 px for the full 77.5 × 105 mm panel, at 14.01 px/mm. Pixel (0,0) is the top-left corner of the panel outline.
  - X_mm = x/14.0129. Y_mm = 105 − y/14.0095.
  - See `vectors/pixel_to_mm_transform.json`.
- Thickness by colour: cream = 0.7 mm continuous backing, amber = 1.1 mm, dark = 1.8 mm.
- `vectors/st_patricks_*.svg` is the exact final art in panel px. The harp paths are flattened and embedded, so each SVG stands alone.
- `vectors/st_patricks_*_thickness_classes.png`: 0 = 0.7 mm, 127 = 1.1 mm, 254 = 1.8 mm. These cover the full panel, frame included.
- All art stays at least about 25 px (1.8 mm) clear of the frame.
- Motif coverage inside the frame:

| Panel | Total | Dark | Amber |
|---|---|---|---|
| Clover | 24% | 17% | 7% |
| Hat | 31% | 21% | 10% |
| Pot of gold | 29% | 16% | 13% |
| Harp | 37% | 30% | 7% |

- **Reproducing:** run `python3 scripts/build_st_patricks_v1.py`, then `python3 scripts/make_sheet.py`.
  - The paths are relative to this folder.
  - The scripts need numpy, Pillow, cairosvg, svgelements, and the DejaVu fonts at `/usr/share/fonts/truetype/dejavu/`.
  - A second run gave byte-identical images.

## Geometry caveats (checked with 0.43 mm and 0.57 mm morphological opening)
- Amber and dark features are at least about 0.57 mm, with these exceptions:
  - **Sparkles:** points taper to about 0.4 mm.
  - **Shamrocks:** the notches between the small leaves taper to about 0.4 mm.
  - **Gaps:**
    - Clover: where the stem meets the lower leaves.
    - Hat: between the band shamrock and the crown edge.
    - Pot: between the heaped coins.
    - These cream gaps and wedges narrow to about 0.3–0.4 mm at their ends.
- **Rainbow:** the cream gaps between bands are 10 px (about 0.7 mm).
- **Harp:** the strings are about 9 px (0.65 mm) and the amber chain rings are about 9–10 px. The small curl where the neck meets the pillar is kept from the source.
- All detail sits on the continuous 0.7 mm backing; nothing is freestanding.
