# Halloween v1 — sources, licenses, checks (IMAGES ONLY, not approved yet)

Template: 1086×1471 px = 77.5×105 mm, frame/rails/transform copied unchanged (byte-identical to earlier holidays).
Thickness classes: 0 = cream 0.7 mm, 127 = amber 1.1 mm, 254 = dark 1.8 mm, all on a continuous backing with no through-holes. No text or years.

## Panels
1. halloween_1_jack_o_lantern: ribbed pumpkin with stem, curly vine and leaf. Carved triangle eyes, nose and crescent grin with two teeth. The carved areas are cream (thinnest, so they glow) with an amber rim. Original geometry. It differs from the Thanksgiving pumpkin because of the carved face.
2. halloween_2_witch_moon: witch on a broomstick across a full amber moon, with two bats and sparkles. Ref: Openclipart 306877 "Broom Riding Witch Silhouette", GDJ, Public Domain/CC0, https://openclipart.org/detail/306877
3. halloween_3_black_cat_fence: black cat with amber eyes and slit pupils sitting on a picket fence, crescent moon, sparkles. Ref: Openclipart 26514 "black cat", kattekrab, Public Domain, https://openclipart.org/detail/26514. The eyes, fence and moon are original.
4. halloween_4_haunted_house_bats: gabled house with a tower, chimney, lit windows, a boarded window, an arched door, gravestones, a full moon and four bats. The house is original geometry. Bat ref: Openclipart 242212 "Bat Silhouette", GDJ, Public Domain, https://openclipart.org/detail/242212. It is also used on panel 2.

## Checks (final build)
- Thickness maps contain only {0,127,254}. PNG and map agree on 100% of the art window.
- Speck rule: 0 amber components under 12 px, and also 0 dark and 0 cream components under 12 px. Edge fragments under 12 px are merged into the neighbouring class at build time.
- Backing: every pixel is in a class of at least 0.7 mm. There are no transparent pixels or holes, and the base plate is continuous.
- Art-to-frame clearance (px): jack 41, witch 71, cat 28, house 24.
- Thin features under 0.57 mm, all inherent tapered tips: the leaf/vine tip on the jack, the crescent-moon horns on the cat, and bat wing tips on the house and witch panels. Bats and the witch use an 8 px outline stroke to round off the tips and broom bristles.
- Coverage of the art window: jack 39%, witch 32%, cat 38%, house 49%.
- Deterministic: a rebuild gives byte-identical PNGs, SVGs, maps and four-up.
- Reviewed at full, 1/4 and 1/8 scale. All four panels are recognizable at 1/8.
