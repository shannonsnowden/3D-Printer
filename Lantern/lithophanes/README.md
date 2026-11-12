# Lithophane print settings (OrcaSlicer)

This folder is an OrcaSlicer **project template** for printing photo lithophanes that fit the lantern panel slots (77.5 × 105 mm) on a **Creality K1 Max** with a **0.4 mm nozzle**.

## How to use the template

1. Open `orcaslicer-lithophane-settings.3mf` in OrcaSlicer.
2. Delete the placeholder object on the plate if there is one. The template currently includes the dog lithophane (`PLACEHOLDER_dog_lithophane_v1`), already laid flat with the back down. Keep it only if you want to print that panel.
3. Import your lithophane `.stl` (drag the file onto the plate, or use File → Import).
4. Lay the panel **flat with the back down** (flat back on the bed, relief facing up).
5. Keep the project / **Global** settings. Do not switch to per-object settings, and do not reset the profile back to the stock defaults.
6. Slice and print.

## Print settings

The project starts from the official **0.20mm Standard @Creality K1Max (0.4 nozzle)** process, the **Creality K1 Max (0.4 nozzle)** printer, and **Generic PLA @Creality**, then applies these lithophane settings:

- Layer height **0.12 mm**, first layer **0.2 mm**
- **Arachne** wall generator, **6 walls**
- **0** top shell layers and **0** bottom shell layers
- Sparse infill **100% rectilinear**
- Speeds: outer wall **50 mm/s**, inner wall **80 mm/s**, sparse and internal solid infill **80 mm/s**, first layer **30 mm/s**
- Default acceleration about **3000 mm/s²**
- **No supports**, **no brim**
- Nozzle **210 °C** (first layer the same), bed / hot plate **60 °C**, fan **100%**
- Print **flat with the back down**

A machine-readable copy of the same settings is in `orcaslicer-lithophane-settings.json`. The complete flattened project settings live inside the `.3mf` file at `Metadata/project_settings.config`.

Official OrcaSlicer process profiles spell the printer as `K1Max` (no space) in the process name, and `K1 Max` in the printer name.

## Notes

- **Physical fit in the lantern is untested.** Confirm the first panel slides into a 78 mm slot before printing more. Do not force it.
- Printing **vertically** can give a sharper image, but the frame may come out about 0.05–0.1 mm thicker, which can affect fit. The recommended orientation is flat, back down.
