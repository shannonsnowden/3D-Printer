# Handoff: approved Christmas v6 art, for matching CAD/STL

**Approval:** Shannon approved all four v6 images on Mon Nov 9, 2026 at 1:23 PM ET. His words: "yes, these look good. go ahead and create them".
That approval covers making STLs that match these images. It does not cover printing, uploading, publishing or claiming physical fit. Physical fit has not been tested.

## Contract (do not redesign)
- Panel size is 77.5 × 105 × 1.8 mm, the same outline, frame and slot-fit dimensions as the v5 panels.
- Thickness comes from the image colours:
  - cream (192,180,120): 0.7 mm
  - amber (168,96,36): 1.1 mm
  - dark brown (48,24,0): 1.8 mm
- **Tree (1) and wreath (4):** the approved images are pixel-identical to v5. Reuse the v5 tree and wreath meshes unchanged.
- **Snowman (2):** the side-of-head spike and its amber band are removed. The head circle and the scarf's top-right corner are restored. The centred nose dot below the eyes is kept. There is no side nose, and the two extra dots removed earlier must stay removed. Nothing else changed.
- **Reindeer (3):** below y=700 px (head, muzzle, round nose, eye, mouth, neck), it is identical to v5. Above that, the old antlers are gone, and so are the ear-like spikes and the left curved branch. They must not come back. The new antlers are the APPROVED image's dark pixels. That equals `vectors/reindeer_antlers_v6_mask.png`, which has the exact dilation already applied.
  - **Do NOT build from the raw `vectors/reindeer_antlers_v6.svg`.** It has no offset. The approved art adds 3 px (about 0.21 mm) around it, then smooths the edge and drops specks under 3000 px.
  - Either trace the mask or the approved PNG, or offset the SVG by +0.214 mm and run the overlay test below.
- Geometry must match the approved images. Any change goes back to Shannon as an image first.

## Coordinates
- Each panel PNG is 1086 × 1471 px and covers the full 77.5 × 105 mm panel.
  - x: 1086 / 77.5 = 14.013 px/mm. y: 1471 / 105 = 14.010 px/mm.
  - Pixel (0,0) is the top-left corner of the panel outline. Image y runs down, so mesh Y = 105 − y/14.01.
- The tiny light pixels at the outer corners are sheet background at the corner notches, not panel material. Some 1-px white slivers carried over from v5 are render artefacts. Use the v5 frame/notch geometry for both.
- The SVG viewBox is in the same panel pixels, so 1 unit = 1 px.
- Fitted shapes in px:
  - reindeer head ellipse: centre (627,760), rx 241, ry 188
  - snowman head circle: centre (542.75,483.4), r 140

## What each file is
- `approved/`: the four-up sheet and the four approved panels. These are the only geometry authority.
- `derived/*_thickness_classes.png`: each pixel snapped to the nearest palette colour. 0 = cream 0.7 mm, 127 = amber 1.1 mm, 254 = dark 1.8 mm. Anti-aliased edges are snapped too.
- `derived/*_changed_vs_v5_mask.png`: 255 where the approved image differs from v5.
  - snowman: 8,297 px, inside x675–850, y440–545
  - reindeer: 114,347 px, inside x396–988, y113–699
- `vectors/reindeer_antlers_v6_mask.png`: the final antler coverage (255 = dark, 1.8 mm), after the dilation.
- `vectors/reindeer_antlers_v6.svg`: the unoffset clipped PhyloPic path. Reference only.
- `vectors/old_antler_erase_mask.png`: the area where the old v5 antlers were painted to cream.
- `vectors/reindeer_head_old_antlers_removed.png`: the v5 reindeer with the old antlers erased and no new ones.
- `vectors/snowman_spike_edit_region_mask.png`: the first spike-erase pass only. Use `derived/christmas_2_snowman_v6_changed_vs_v5_mask.png` for the full edit.
- `scripts/` and `vectors/reindeer_build_args.txt`: these reproduce the images.
  - Run `build_reindeer.py 600 608 1.1 240 0 3` and `build_snowman.py` from a folder holding `vectors/`, `refs/<phylopic svg>`, and `v5_unchanged_crops/v5_2_snowman.png` and `v5_3_reindeer.png` (both are in `repro_inputs/`).
  - In `build_reindeer.py`, the SRC path points to the v5 reindeer PNG; use `repro_inputs/v5_3_reindeer.png`.
  - The scripts need numpy, scipy, Pillow and cairosvg.
- `repro_inputs/`: the v5 base crops the edits started from. They are not approved art.
- `source_vector/`: the original PhyloPic SVG and its license metadata. It is under the Public Domain Mark 1.0, contributor Ando, image e60cd072-d9ce-4d13-a79c-aa3d8086d37a.

## Recommended check after export (independent overlay test)
1. Take the exported mesh or slicer output and render a top-down orthographic view at 14.01 px/mm. Map local thickness to the three classes, using thresholds of about 0.9 and 1.45 mm.
2. Align it to the panel outline and compare against `derived/*_thickness_classes.png`.
3. Report the mismatch percentage and an XOR image for each panel.
4. Mismatch should sit only in a 1–2 px band along edges. Look specifically for:
   - old antler fragments or spikes in the reindeer above y≈575
   - any snowman spike or extra dots
   - thin antler tines lost (the thinnest are about 1.1 mm)
5. Tree and wreath should match the v5 meshes exactly.
