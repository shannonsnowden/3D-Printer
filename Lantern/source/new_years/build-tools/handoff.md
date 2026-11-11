# Handoff: approved New Year's v1 art for matching STL creation

**Approval:** Shannon approved all four New Year's v1 images on Mon Nov 9, 2026 at 4:04 PM ET ("looks good. go ahead").
- This approval covers only making matching STLs.
- It does not cover printing, slicing for print, uploading, publishing or contacting anyone.
- Physical fit is untested.

## Exact approved versions (New Year's v1, final)
- The four approved panels are `new_years_1_fireworks.png`, `new_years_2_midnight_clock.png`, `new_years_3_champagne_toast.png` and `new_years_4_party_hat_streamers.png`.
- `NEW_YEARS_v1_FOUR_UP_IMAGES_FOR_APPROVAL.png` is the sheet Shannon reviewed.
- Their hashes are in `MANIFEST_sha256.txt`.
- These come byte-for-byte from `/workspace/lantern/artwork-new-years-v1/` as of 4:02 PM ET, Nov 9, 2026.

## Contract (implement exactly, do not reinterpret)
- **Motifs:** the four approved motifs exactly as drawn: Fireworks, Midnight clock, Champagne toast, Party hat and streamers.
  - No year numbers.
  - No added, removed, moved or restyled elements.
- **Precedence:** the approved bitmaps win over everything else. If an SVG, thickness map, script or any suggestion here disagrees with an approved PNG, follow the PNG.
- **Panel size:** 77.5 × 105 mm, 1.8 mm total thickness.
- **Thickness from colour:**
  - **Cream (192,180,120):** a continuous, solid 0.7 mm base over the whole panel, with no through-holes. The champagne bubbles are 0.7 mm cream windows inside 1.1 mm amber.
  - **Amber (168,96,36):** 1.1 mm.
  - **Dark (48,24,0):** 1.8 mm.
- **Frame and side rails:** reuse the exact existing frame, side rail, slot-fit edge and corner-notch geometry from the authoritative resized Thanksgiving/Christmas panel CAD source. That is the 78 mm-slot, 77.5 mm panel version used for Christmas v6.
  - Do NOT trace the frame from `vectors/panel_frame_mask.png` or any screenshot or PNG edge.
  - That mask came from a rendered preview and is only for registration and comparison.
- **Library:** Christmas v6 (4 panels) and the six Thanksgiving panels stay unchanged.
  - The finished library is 6 Thanksgiving + 4 Christmas + 4 New Year's, plus the optional fit strip.
  - Do not start another holiday.

## Coordinate mapping
- Each panel PNG and SVG is 1086 × 1471 px and covers the full panel outline, 77.5 × 105 mm.
  - x scale: 14.0129 px/mm. y scale: 14.0095 px/mm.
  - Pixel (0,0) is the top-left corner of the panel outline.
  - X_mm = x / 14.0129. Y_mm = 105 − y / 14.0095, because image y points down.
  - See `vectors/pixel_to_mm_transform.json`.
- The SVG viewBox is `0 0 1086 1471` in panel pixels: 1 unit = 1 px.
- The cream window inside the frame is about x 54–1032, y 58–1412 px, with rounded inner corners.
- All art stays at least 25 px (about 1.8 mm) clear of the frame.

## Files
- `vectors/new_years_*.svg`: the exact final art geometry (dark and amber fills, plus cream bubble windows in the champagne). It includes no frame.
- `vectors/new_years_*_thickness_classes.png`: per-pixel classes for the full approved panel, frame included. 0 = 0.7 mm, 127 = 1.1 mm, 254 = 1.8 mm.
  - Anti-aliased edge pixels are snapped to the nearest class.
  - The tiny light corner pixels are the sheet background at the corner notches, not material.
- `vectors/panel_template_blank.png` and `vectors/panel_frame_mask.png`: the blank v6 panel render and its frame mask. Use them for registration only; see "Frame and side rails" above.
- `scripts/`: reference only. These are 2D authoring scripts, not CAD. Running `python3 scripts/build_new_years.py` and then `python3 scripts/make_sheet.py` from this folder's root reproduces every PNG, SVG and map byte-identically. I verified this in a separate copy.
  - They need numpy, scipy, Pillow, cairosvg and fontTools.
  - **Path changes may be needed:**
    - The DejaVu font paths are hardcoded as `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` and `DejaVuSans.ttf`. Change them if your machine's fonts are elsewhere.
    - The scripts expect `vectors/` next to `scripts/`.
    - `contact.py` is a preview helper that runs from the folder root and writes to the path you give it.
    - The template was made once from `../artwork-concept-v6/christmas_*` PNGs by a one-off command that isn't in the scripts. The template is included, so you don't need to make it again.
- `NOTES_sources_licenses.md`: motif decisions, sources and licenses.
  - All geometry is original.
  - The clock numerals are DejaVu Sans Bold outlines under the free DejaVu/Bitstream Vera license.
  - No third-party clip art was used.

## Implementation caveats and required checks
- **Small features:**
  - Sparkle points and firework ray tips taper to small rounded tips. The narrowest dark ones are about 0.9 mm; amber sparkle centres are about 0.6 mm.
  - The smallest dots are about 1.1–1.4 mm.
  - All of them sit on the solid 0.7 mm backing, so none is freestanding. Keep them; do not remove or simplify them without Shannon's approval.
- **After export, verify each panel:**
  - Actual mesh dimensions: 77.5 × 105 × 1.8 mm, with the same frame and rails as Christmas v6.
  - Topology: watertight and manifold, one connected body with a continuous base.
  - Rendered images.
- **Overlay test, per panel:**
  1. Render a top-down orthographic view at 14.01 px/mm.
  2. Classify height using thresholds of about 0.9 and 1.45 mm.
  3. Register it to the frame and XOR it against `vectors/new_years_*_thickness_classes.png`.
  4. Report the mismatch percentage. Differences should appear only along a 1–2 px edge band.
  5. Check specifically for missing tips or dots, merged streamer curls, clock numerals that are wrong or upside down, and changed champagne levels.
- Physical fit is untested. Make no fit or print claim.
