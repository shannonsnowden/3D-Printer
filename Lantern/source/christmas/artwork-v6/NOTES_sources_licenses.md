# Christmas v6 — IMAGES FOR APPROVAL (no new STL)
Artwork concept only. Nothing here is an exported mesh. No CAD, repo, STL or ZIP was touched or made.

## Files
- CHRISTMAS_v6_FOUR_UP_IMAGES_FOR_APPROVAL.png: the labelled four-panel sheet
- christmas_1_tree_v6_unchanged.png / christmas_4_wreath_v6_unchanged.png: exact pixel crops of the v5 four-up sheet (0 pixels differ)
- christmas_2_snowman_v6.png: v5 snowman with the side spike and its amber band removed. 8,297 px changed, all inside x675-850, y440-545
- christmas_3_reindeer_v6.png: v5 head, muzzle, nose, eye, mouth and neck kept. Pixels at y>=700 are identical. The old antlers were erased and the new outline was composited on
- CLOSEUPS_v5_vs_v6.png: v5 and v6 side by side for the antlers and the snowman head
- check_fourup_quarter_scale.png: quarter-scale thumbnail used to check legibility
- vectors/reindeer_antlers_v6.svg: the antler vector in panel pixel coordinates (1086x1471 px = 77.5x105 mm, 14.01 px/mm). It is the PhyloPic path, clipped above the skull with the brow shovel removed
  - IMPORTANT: the PNG adds a 3 px (about 0.21 mm) outward offset to the SVG, then smooths it and drops specks under 3000 px. CAD must apply the same offset, or trace vectors/reindeer_antlers_v6_mask.png, so the STL matches the approved image
  - Approx antler stroke width: p10 1.1 mm, median 2.2 mm, p90 3.2 mm
- vectors/reindeer_antlers_v6_mask.png, old_antler_erase_mask.png, reindeer_head_old_antlers_removed.png, snowman_spike_edit_region_mask.png: masks for rebuilding
- Head ellipse used for the reindeer erase: centre (627,760), rx 241, ry 188 px. Snowman head circle: centre (542.75,483.4), r 140 px
- build_reindeer.py (args in vectors/reindeer_build_args.txt: 600 608 1.1 240 0 3), build_snowman.py, make_sheets.py: these reproduce every image

## Sources and licenses
- Antler outline: PhyloPic image e60cd072-d9ce-4d13-a79c-aa3d8086d37a, "Rangifer tarandus", contributor Ando. License: Public Domain Mark 1.0 (https://creativecommons.org/publicdomain/mark/1.0/). No attribution needed
  - SVG: https://images.phylopic.org/images/e60cd072-d9ce-4d13-a79c-aa3d8086d37a/vector.svg
  - Page: https://www.phylopic.org/images/e60cd072-d9ce-4d13-a79c-aa3d8086d37a
- Other PhyloPic Rangifer silhouettes I looked at (refs/phylopic_rangifer_contact_sheet.png) are CC0 or PDM. For example, 09c5d6bf and 19864ae2 are CC0 by Laura Barbero-Palacios. They were not used
- Photo reference (left-facing bull, pose check only, not copied into the art): "Reinbukken på frisk grønt beite. - panoramio.jpg" by Are G Nilsen, CC BY-SA 3.0. https://commons.wikimedia.org/wiki/File:Reinbukken_p%C3%A5_frisk_gr%C3%B8nt_beite._-_panoramio.jpg
- Base art: v5 four-up sheet 01M70N7DK0YPKGWA3WN5PGBECH.png and v5 reindeer panel 01M70N7DK1508RZ8XW86JZMFMW.png. Both were read only
