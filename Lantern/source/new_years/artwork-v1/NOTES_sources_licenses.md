# New Year's lantern panels v1: IMAGES FOR APPROVAL, NO STL
These are 2D artwork only. The backlighting is simulated: each colour simply stands for a thickness. The 77.5 × 105 × 1.8 mm panels have been printed and fit the lantern well (confirmed by Shannon, Nov 2026).

## Final motifs (no year number anywhere)
1. **Fireworks:** three radial bursts. The large one is at the top centre, with a smaller one lower left and lower right.
   - Each burst has 18 or 14 tapered rays in alternating long and short lengths, a dark dot on each ray tip, and an amber centre.
   - Amber spark dots sit between the rays.
   - Three curved, dotted launch trails rise from the bottom.
   - Six amber four-point sparkles fill the gaps.
   - There are no side branches, so the bursts don't read as snowflakes.
2. **Midnight clock:** an alarm clock with a heavy dark rim, a top knob and two feet.
   - The face has a thin amber ring, amber minute dots, dark hour dots, and dark 12, 3, 6 and 9.
   - The numerals are upright, cut from DejaVu Sans Bold outlines and converted to paths.
   - A broad spade hour hand and a slim minute hand both point to 12, with an amber hub and an amber inset on the hand.
   - Amber sparkles sit in the corners.
3. **Champagne toast:** two tall tulip-shaped flutes tilted ±12° so their rims touch at the centre.
   - Each has a dark wall, a stem with a knot, and a broad foot.
   - The amber champagne level stays horizontal even though the glasses tilt, and it has cream bubbles.
   - Above the clink there is a dark sparkle with an amber centre and a few rising bubble dots, plus amber sparkles.
4. **Party hat and streamers:** a striped cone tilted −10°, made of dark and amber diagonal bands.
   - It has a dark brim with amber dots and a scalloped pompom with amber highlights.
   - Three broad wavy streamers end in open spiral curls: two dark at 34 px (2.4 mm) and one amber at 30 px.
   - A handful of chunky confetti rectangles and dots stay well apart.
   - The straight cone, stripes and brim keep it from reading as a Christmas tree or a floppy Santa hat.

## Sources and licenses
- All motif geometry was drawn for this project from simple geometric and Bézier forms in `scripts/build_new_years.py`. No third-party clip art or vector files were used, so no attribution is needed.
- Numeral glyph outlines come from DejaVu Sans Bold, under the Bitstream Vera / DejaVu font license. It is free to use and embed; converting glyphs into artwork is allowed. Only "12", "3", "6" and "9" were used.
- The panel frame and template come from the approved Christmas v6 panel (`../artwork-concept-v6/`), which is our own artwork.

## Dimensions and registration
- Each panel PNG is 1086 × 1471 px for the full 77.5 × 105 mm panel, at 14.01 px/mm, using the same frame as Christmas v6. Total thickness is 1.8 mm.
- Thickness classes: cream 0.7 mm backing, amber 1.1 mm, dark 1.8 mm.
- Coordinates and transform: `vectors/pixel_to_mm_transform.json`.
- Every panel keeps at least 25 px (about 1.8 mm) of clear cream between the art and the frame.
- `vectors/new_years_*.svg` is the exact final art in panel pixels.
- Each PNG is that SVG rendered with cairosvg over `vectors/panel_template_blank.png`, with `vectors/panel_frame_mask.png` laid on top.
- `vectors/new_years_*_thickness_classes.png` maps each pixel to a thickness class: 0 = 0.7 mm, 127 = 1.1 mm, 254 = 1.8 mm.
- After approval, build the STL from the class maps or the SVGs plus this transform. The approved PNG decides any difference.

## Geometry caveats
- Sparkle tips and firework ray tips taper to rounded points. The narrowest dark features are about 0.9 mm, and the amber sparkle centres about 0.6 mm. Smallest dots: amber clock minute dots about 1.1 mm across, and firework spark dots about 1.2–1.4 mm.
- Amber areas are either inset into dark shapes or stand alone on the 0.7 mm cream backing. Everything sits on a continuous backing sheet, with no through-holes.
- The cream bubbles in the champagne are 0.7 mm windows in the 1.1 mm amber area.
- These are images only (simulated backlighting, not a photo of a print). The 77.5 × 105 × 1.8 mm panels have been printed and fit the lantern well (confirmed by Shannon, Nov 2026).
