# Easter lantern panels v1: IMAGES FOR APPROVAL, NO STL
These are 2D artwork only. The backlighting is simulated, with each colour simply standing for a thickness. The 77.5 × 105 × 1.8 mm panels have been printed and fit the lantern well (confirmed by Shannon, Nov 2026).

Started on Shannon's "do it" (Nov 10, 2026, 1:00 PM ET). Every earlier holiday folder is unchanged.

## Panels
1. **Easter bunny:** a sitting European rabbit facing left, from a CC0 silhouette. It is 930 px tall (about 66 mm).
   - My additions:
     - a 4 px dark outline, so no edge is a hairline
     - an amber eye
     - an amber inner-ear stripe
   - Around it: a dark grass strip, two small decorated eggs at the feet (zigzag and dots), an amber tulip, three amber five-petal flowers and two sparkles.
2. **Basket of decorated eggs:** all my own geometry.
   - The basket:
     - a tapered bowl woven from staggered amber rounded bars on dark
     - a thick dark rim with an amber diagonal twist
     - a tall dark arch handle with a dashed amber centre line
   - Four eggs poke above the rim with their own patterns (wavy lines, zigzag, stripes with dots, dots). Each has a cream separation halo. Grass blades sit between them.
   - Grass and two flowers are at the base.
3. **Decorated Easter egg:** one big dark egg (690 × 940 px, about 49 × 67 mm). It is my own parametric egg shape.
   - The bands, top to bottom:
     - a row of amber dots
     - a bold amber zigzag
     - a wide amber flower band, edged with dark rules, holding dark five-petal flowers and leaf pairs
     - an amber wave
     - a row of amber dots
   - The egg sits in grass between two amber tulips, with sparkles.
4. **Chick hatching from an egg:** a cartoon chick (round head, big eyes, beak, small wings) rising out of a cracked shell, with the broken top of the shell lying beside it. It comes from a CC0 cartoon.
   - My colouring and changes:
     - the chick is amber with a thick dark outline
     - the eyes are cream with dark pupils and cream highlights, with the eye rings thickened
     - the beak is dark
     - the shell is dark with amber zigzag and dot Easter-egg decoration
     - a cream halo marks the crack line
   - I dropped the tiny wing-tip feather marks and the beak and nostril hairlines.
   - The loose shell cap is tilted −38° (`CAPR`, default −38) so its jagged edge faces up and it reads as a broken shell rather than a spiky blob.
   - Grass, two flowers and sparkles complete it.

No text, no year, no through-holes.

## Sources and licenses
- **Bunny:** PhyloPic image d71fcd12-90f6-40c4-b918-0dac0ba3e809, *Oryctolagus cuniculus* (European rabbit) silhouette by Anthony Caravaggi. License: CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/). No attribution required; credit given as a courtesy.
  - Page: https://www.phylopic.org/images/d71fcd12-90f6-40c4-b918-0dac0ba3e809
  - SVG: https://images.phylopic.org/images/d71fcd12-90f6-40c4-b918-0dac0ba3e809/vector.svg, saved as `refs/phylopic_d71fcd12-…_oryctolagus_cuniculus.svg`.
- **Chick:** Openclipart #131089, "Funny Chick Cartoon Newborn Coming Out from the Egg" by palomaironique. The file's metadata says Public Domain, and Openclipart releases all its art under CC0 1.0.
  - Page: https://openclipart.org/detail/131089
  - SVG: https://openclipart.org/download/131089, saved as `refs/openclipart_131089_chick_from_egg.svg`.
  - I flattened its paths (transforms applied) and recoloured them into the three-tone palette.
- **Panels 2 and 3 and all added details:** my own simple geometry. This covers the eggs, basket, grass, tulips, flowers, sparkles and patterns.
- **Frame and template:** copied unchanged from Valentine's v2 and New Year's v1, which in turn came from Christmas v6.

## Dimensions and registration
- Each panel PNG is 1086 × 1471 px for the full 77.5 × 105 mm panel, at 14.01 px/mm. Pixel (0,0) is the top-left corner of the panel outline.
  - X_mm = x/14.0129. Y_mm = 105 − y/14.0095.
  - See `vectors/pixel_to_mm_transform.json`.
- Thickness by colour: cream = 0.7 mm continuous backing, amber = 1.1 mm, dark = 1.8 mm.
- `vectors/easter_*.svg` is the exact final art in panel px. The reference paths are flattened and embedded, so each SVG stands alone.
- `vectors/easter_*_thickness_classes.png`: 0 = 0.7 mm, 127 = 1.1 mm, 254 = 1.8 mm. These cover the full panel, frame included.
- The approved bitmap decides any difference.
- All art stays at least about 25 px (1.8 mm) clear of the frame.
- Motif coverage inside the frame:

| Panel | Total | Dark | Amber |
|---|---|---|---|
| Bunny | 34% | 32% | 2% |
| Basket | 39% | 28% | 11% |
| Egg | 45% | 33% | 12% |
| Chick | 32% | 20% | 12% |

- **Reproducing:** run `python3 scripts/build_easter_v1.py`, then `python3 scripts/make_sheet.py`.
  - The paths are relative to this folder.
  - The scripts need numpy, scipy (checks only), Pillow, cairosvg, svgelements, and the DejaVu fonts at `/usr/share/fonts/truetype/dejavu/`.
  - The grass uses fixed random seeds, so rebuilds are deterministic.

## Geometry caveats (checked with 0.43 mm and 0.57 mm morphological opening)
- No amber or dark feature is under 0.57 mm, apart from these tapered tips and wedges:
  - **Grass:** blade tips, and the cream wedges between blade bases and nearby objects (eggs, paws, tulip leaves, the basket handle), taper to about 0.3–0.4 mm at the very ends.
  - **Tulips:** leaf tips and the three petal points taper to about 0.4 mm.
  - **Sparkles:** points taper to about 0.4 mm.
  - **Chick shell:** the jagged shell points narrow to about 0.3–0.4 mm at the tips.
  - **Chick eyes:** the two eye rings meet, leaving a small tapering amber wedge between them.
- **Bunny:** the paw and toe notches in the silhouette are about 0.5 mm.
- **Basket:** a grass blade beside the handle leaves a thin cream wedge.
- All of this sits on the continuous 0.7 mm backing; nothing is freestanding.
