# Valentine's Day lantern panels v2: IMAGES FOR APPROVAL, NO STL
These are 2D artwork only. No STL, CAD, repo change, ZIP, upload, print or contact. The backlighting is simulated, with each colour simply standing for a thickness. Physical fit is untested.

Shannon's v1 review (Nov 10, 2026, 11:52 AM ET): "change the love letter for a box of chocolates and change the lovebirds for a cupid with arrow". The v1 folder is unchanged.

## Panels
1. **Heart and Cupid's arrow:** a byte-identical copy of v1. The PNG, SVG and thickness map are copied from `../artwork-valentines-v1/`.
2. **Rose bouquet:** a byte-identical copy of v1, the same way.
3. **Box of chocolates (new):** an open heart-shaped box.
   - The box has a dark rim and an amber tray. It holds nine chocolates, each in a scalloped cream paper cup:
     - round truffles with an amber swirl
     - heart chocolates with an amber drizzle
     - square bonbons with amber stripes
   - The heart-shaped lid is propped up behind it, tilted −22°. The lid has an amber inner outline, an amber ribbon band and an amber bow with tails.
   - A thin cream gap separates the box from the lid.
   - Floating hearts and amber sparkles fill the background.
4. **Cupid with bow and arrow (new):** a flying cherub (chubby child, curly hair, feathered wings) drawing a bow, from a CC0 silhouette.
   - My changes to it:
     - added a 5 px dark outline, so feather tips and curls aren't hairlines
     - removed two pointed hair tufts that read as horns, replaced with round curls
     - drew a thicker bowstring (12 px) and arrow shaft (14 px)
     - added a heart-shaped arrowhead (dark with an amber centre) and an amber eye
   - Floating hearts and sparkles fill the background.

## Sources and licenses
- **Cupid:** "Martin74's Cupid Silhouette" by GDJ, Openclipart #244366, CC0 1.0 public domain (https://creativecommons.org/publicdomain/zero/1.0/). No attribution required; credit given as a courtesy.
  - Page: https://openclipart.org/detail/244366/martin74s-cupid-silhouette
  - SVG: https://openclipart.org/download/244366, saved as `refs/openclipart_244366_martin74s_cupid_silhouette.svg`.
  - Placement: 1 px of a 900 px-wide reference render = 1 panel px, origin at panel (75, 250).
- **Roses (panel 2, unchanged from v1):** "Rose Silhouette" by GDJ, Openclipart #221383, CC0 1.0 (https://openclipart.org/detail/221383/rose-silhouette), saved in `refs/`.
- **Panels 1 and 3 and all added details:** my own simple geometry, including the parametric hearts, box, cups, chocolates, ribbon, bow, sparkles and bowstring.
- **Frame and template:** the same as Christmas v6, New Year's v1 and Valentine's v1. They are our own artwork.

## Dimensions and registration
- Each panel PNG is 1086 × 1471 px for the full 77.5 × 105 mm panel, at 14.01 px/mm. Pixel (0,0) is the top-left corner of the panel outline.
  - X_mm = x/14.0129. Y_mm = 105 − y/14.0095.
  - See `vectors/pixel_to_mm_transform.json`.
- Thickness by colour: cream = 0.7 mm continuous backing, amber = 1.1 mm, dark = 1.8 mm. There are no through-holes.
- `vectors/valentines_*.svg` is the exact final art in panel px; the cupid's source path is embedded.
- `vectors/valentines_*_thickness_classes.png`: 0 = 0.7 mm, 127 = 1.1 mm, 254 = 1.8 mm.
- The approved bitmap decides any difference.
- All art stays at least 25 px (about 1.8 mm) clear of the frame. Coverage: box 31%, cupid 21%.
- **Reproducing:**
  - Panels 3 and 4: run `scripts/build_valentines_v2.py`, then `scripts/make_sheet.py`, from this folder.
  - Panels 1 and 2: these come from v1 and are not rebuilt here. `scripts/build_valentines_v1_reference_panels_1_2.py` is a reference copy; it needs the v1 `refs/` folder, including the PhyloPic lovebird file.
  - The scripts need the DejaVu fonts at `/usr/share/fonts/truetype/dejavu/`.

## Geometry caveats
- **Box of chocolates:** small tapered points (heart-chocolate tips, ribbon tails, sparkle points) narrow to about 0.3–0.4 mm at the very tips. The amber swirls and drizzles are 10 px (about 0.7 mm). The cream cup ruffles are at least about 0.9 mm.
- **Cupid:** a few narrow cream gaps between wing feathers, between fingers on the bow hand, and at the toes are about 0.3 mm. The dark features are at least about 0.57 mm.
- **Rose bouquet:** the v1 caveat still applies; it has fine stencil detail of about 0.3–0.6 mm.
- All detail sits on the continuous 0.7 mm backing.
