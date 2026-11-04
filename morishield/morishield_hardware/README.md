# MoriShield Carrier — Hardware

KiCad 10 designs for the **MoriShield Carrier** board (SERIGREEN) — a
carrier/backplane PCB that hosts the field node's plug-in modules and
distributes power, I²C and protection:

- ESP32-S3 DevKit (S3-WROOM-1 N16R8) on J1 + J2
- EBYTE E22-900T22D (SX1262) LoRa 868 MHz module on J6
- A7672S 4G/GSM modem (Parry board) on J3 + J4 + J5 feed
- Sensor headers: SPS30 (JST-ZH-5), I²C mux ports (JST-XH-4) for
  SHT45 / SGP41 / BME688 probes, soil moisture, FSR406 force pad,
  AS5600 wind sensor, FDC1004 capacitive electrodes
- Support ICs: TCA9548A I²C mux, TCA9535 GPIO expander, TPS3823-33
  watchdog, TPS7A2033 LDO, SRV05-4 ESD arrays, LED/buzzer drivers

Schematic rev: **Proto-Simple Rev 0.2** ("Post-RS485 Stripped"),
2026-10-22. Both variants share the same schematic and differ only in
stackup and routing.

## Variants

| Folder | PCB file | Layers | DRC errors | Unconnected |
|--------|----------|--------|------------|-------------|
| [`4L/`](4L/README.md) | `MoriShield_Carrier.kicad_pcb`    | 4 (F/In1/In2/B)    | 0 | 1 (`/WDT_WDI`) |
| [`6L/`](6L/README.md) | `MoriShield_Carrier_6L.kicad_pcb` | 6 (F/In1..In4/B)   | 0 | 0 — complete |

The 4-layer variant is the cost-optimised build; the 6-layer variant
adds two inner signal layers (In3/In4) and is fully routed.

## Repository layout

```
4L/                     4-layer KiCad project + docs + fab outputs + reports
6L/                     6-layer KiCad project + docs + fab outputs + reports
libraries/
  MoriShield_Carrier.kicad_sym    shared symbol library (49 symbols)
  MoriShield_Carrier.pretty/      shared footprint library (39 footprints)
```

Each project is self-contained: its `fp-lib-table` and `sym-lib-table`
resolve to `../libraries/` inside this repo — no external KiCad
libraries are required to open either project.

## Opening a project

1. Install **KiCad 10** (files use the 20260306 format).
2. Open `4L/MoriShield_Carrier.kicad_pro` or
   `6L/MoriShield_Carrier_6L.kicad_pro`.
3. Board outline: **178 x 118 mm**, 1.6 mm stackup.

## Fabrication

- Gerber X2 + Excellon drill files: `<variant>/fabrication/`
  (generated 2026-10-26).
- DRC/ERC JSON reports: `<variant>/reports/`.
- Order notes: min track/clearance 0.2 mm, min via 0.8/0.45 mm,
  1 oz copper, ENIG or HASL, solder mask both sides, e-test.
- Custom clearance rules ship as `*.kicad_dru` next to each project
  (relaxed-clearance areas `LOOSE5V` / `LOOSE_U7`; see the file header
  comments). Gerbers were generated 2026-10-26 — regenerate them from
  the PCB if the board is edited after that date.

## Design status

See the per-variant READMEs for the full status tables. Summary:
both boards pass DRC with **0 electrical errors**; remaining items are
134 cosmetic warnings per board (silkscreen overlaps etc.) and one
unconnected net on the 4-layer board.

## History

This repository previously contained the earlier **MoriShield V2**
controller design (OrCAD/EDIF conversion, IPC-2581 data, audit docs).
Those files were removed in the 2026-10-27 cleanup and remain
recoverable from the git history (`git log --all`).
