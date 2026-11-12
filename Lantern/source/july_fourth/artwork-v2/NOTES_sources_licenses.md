# Fourth of July lantern panels v2: IMAGES FOR APPROVAL, NO STL
These are 2D artwork only. The backlighting is simulated, with each colour simply standing for a thickness. The 77.5 × 105 × 1.8 mm panels have been printed and fit the lantern well (confirmed by Shannon, Nov 2026).

Started on Shannon's "go ahead" (Nov 10, 2026, 5:02 PM ET). This v2 follows Shannon's v1 feedback (5:08 PM ET): "the stars on the flag should be 50". The v1 folder and every earlier holiday folder are unchanged.

## What changed in v2
- **Panel 1 only.** The canton now has exactly 50 amber five-point stars in the real US layout: 9 staggered rows of 6-5-6-5-6-5-6-5-6, on an 11 × 9 half-grid. Each star follows the flag's ripple.
- To keep the stars printable I enlarged the flag and the canton:
  - Flag: hoist 572 px (41 mm, was 36 mm). Width unchanged at 785 px (56 mm). Ripple amplitude 30 px (was 34).
  - Canton: 440 × 308 px (31.4 × 22.0 mm, was 23.5 × 19.3 mm).
- **Stars:**
  - 17.5 px outer radius, with a 4 px round-joined stroke.
  - About 37 × 36 px (2.6 mm) tip to tip. Area about 658 px (3.4 mm²) each.
  - Solid core about 1.5 mm across. Points taper to about 0.3–0.4 mm at the very tips; about 7% of each star's area is narrower than 0.5 mm.
  - Neighbouring stars are at least about 1 mm apart, and at least about 0.6 mm from the canton edges.
- **Star count check:** the amber connected components in `vectors/july_fourth_1_waving_flag_thickness_classes.png` inside the canton number exactly **50**, all 653–662 px in area. The other amber regions are the stripes, bunting, finial, sparkles and border stars, plus 1–20 px anti-alias edge specks.
- **Panels 2–4 and the shared files:** the PNGs, SVGs, thickness maps, template, mask, transform and `refs/` are byte-identical copies of v1.
- Panel 1's motif coverage is now 52% (35% dark, 17% amber).

## Panels
1. **Waving flag and bunting:** all my own geometry.
   - The flag ripples outward from the pole:
     - (v2) a 50-star canton; see "What changed in v2" above
     - 13 stripes, alternating dark and amber; the dark stripes are about 3.1 mm and the amber stripes about 2.3 mm wide
   - A dark pole with an amber ball finial and two flag clips.
   - Below it, a patriotic half-fan bunting:
     - ten alternating dark and amber pleats
     - a dark rim and top rail
     - a dark medallion with a large amber star
   - Small stars and sparkles fill the background.
2. **Fireworks over a small town:** all my own geometry, and different in style from the New Year's spoke bursts.
   - A large "peony" burst of four concentric dot rings, alternating amber and dark, with a dark star centre.
   - A "star-spangled" burst: dark spokes ringed by ten amber stars.
   - A small amber spoke ring with a dotted rising trail.
   - A town skyline silhouette along the bottom:
     - gabled houses
     - a domed hall with a flag on top
     - a tree
     - two flat-roofed buildings
     - amber lit windows throughout
3. **Soaring bald eagle:** from a CC0 silhouette, wings spread on a diagonal.
   - The white head and tail from the source are amber, with a firm dark outline.
   - The eye is dark; the hooked beak is part of the amber head.
   - The silhouette has a 5 px dark outline added.
   - Amber five-point stars sit in the empty corners.
4. **Liberty Bell:** all my own geometry, a simple drawing of the bell.
   - A heavy wooden yoke with amber grain lines and end posts.
   - A crown strap.
   - The classic bell profile (domed shoulder, waist, flared lip) with amber bands at the shoulder and lip, plus a highlight stroke.
   - The famous jagged crack as an 18 px (1.3 mm) cream cut rising from the lip, right of centre.
   - A clapper below, and stars and sparkles around it.

No text, no year, no through-holes.

## Sources and licenses
- **Eagle:** PhyloPic image 3002e4de-eb9b-48a4-8921-57dfe0d2e169, *Haliaeetus leucocephalus* (bald eagle) by Andy Wilson. License: CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/). No attribution required; credit given as a courtesy.
  - Page: https://www.phylopic.org/images/3002e4de-eb9b-48a4-8921-57dfe0d2e169
  - SVG: https://images.phylopic.org/images/3002e4de-eb9b-48a4-8921-57dfe0d2e169/vector.svg, saved in `refs/`.
  - I flattened the paths with svgelements. Subpath 0 is the dark body; subpaths 1–2 (head and tail) are filled amber.
  - Placement: 1130 px tall (about 81 mm), roughly centred, top at y = 165.
- **Panels 1, 2 and 4 and every added star, sparkle and burst:** my own simple geometry.
- I also looked at Openclipart's Liberty Bell engravings (#221329, #242333) for proportions only. None of their geometry is used.
- **Frame and template:** copied unchanged from St Patrick's v1, Easter v1, Valentine's v2 and New Year's v1, which in turn came from Christmas v6.

## Dimensions and registration
- Each panel PNG is 1086 × 1471 px for the full 77.5 × 105 mm panel, at 14.01 px/mm. Pixel (0,0) is the top-left corner of the panel outline.
  - X_mm = x/14.0129. Y_mm = 105 − y/14.0095.
  - See `vectors/pixel_to_mm_transform.json`.
- Thickness by colour: cream = 0.7 mm continuous backing, amber = 1.1 mm, dark = 1.8 mm.
- `vectors/july_fourth_*.svg` is the exact final art in panel px. The eagle paths are flattened and embedded, so each SVG stands alone.
- `vectors/july_fourth_*_thickness_classes.png`: 0 = 0.7 mm, 127 = 1.1 mm, 254 = 1.8 mm. These cover the full panel, frame included.
- All art stays at least about 25 px (1.8 mm) clear of the frame.
- Motif coverage inside the frame:

| Panel | Total | Dark | Amber |
|---|---|---|---|
| Flag (v2) | 52% | 35% | 17% |
| Fireworks | 24% | 16% | 7% |
| Eagle | 25% | 22% | 3% |
| Bell | 28% | 22% | 6% |

- **Reproducing:** run `python3 scripts/build_july_fourth_v2.py 1_waving_flag`, then `python3 scripts/make_sheet.py`. Running it with no arguments also rebuilds panels 2–4, which come out identical to v1.
  - The defaults are `CANTON_W=440` and `STAR_R=17.5`.
  - The paths are relative to this folder.
  - The scripts need numpy, Pillow, cairosvg, svgelements, and the DejaVu fonts at `/usr/share/fonts/truetype/dejavu/`.
  - A second run gave byte-identical images.

## Geometry caveats (checked with 0.43 mm and 0.57 mm morphological opening)
- **Panels 1, 2 and 4:** no amber, dark or cream feature is under 0.57 mm, apart from the very tips of sparkles and star points, which taper to about 0.4 mm.
- **Eagle:** a few cream gaps between the separated primary wing feathers, and between the tail and wing, are about 0.3–0.4 mm. They come from the source silhouette and are kept as drawn. The feather tips themselves are dark and at least about 0.5 mm.
- All detail sits on the continuous 0.7 mm backing; nothing is freestanding.
