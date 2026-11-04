# Session report - MoriShield Carrier Rev C - 2026-11-03 (repair pass: E1, via evidence, decoupling)

Board saved 2026-11-03 20:48:19. Schematic untouched this pass (no Value or netlist edit).

## 1. The four numbers after every task

| Point | ERC | DRC viol / unconn / parity | Census (fp / seg / via / zone / net) |
|---|---|---|---|
| On entry (re-confirmed) | 0 | 0 / 0 / 0 | 159 / 1178 / 313 / 6 / 134 |
| After Task 1 (E1 vias) | 0 | 0 / 0 / 0 | 159 / 1178 / **315** / 6 / 134 |
| Task 2 (via list + fab note) | 0 | 0 / 0 / 0 | unchanged - no board edit |
| Task 3 (decoupling classification) | 0 | 0 / 0 / 0 | unchanged - no board edit |
| Task 4 / 5 (checks and report) | 0 | 0 / 0 / 0 | unchanged |
| Final | **0** | **0 / 0 / 0**, `ignored_checks []` | 159 / 1178 / 315 / 6 / 134 |

Vias in SMD pads: **67 of 315**.

## 2. Task 1 - E1 restored

**Before:** 144 links, worst **11.16 mm**, **0.1 %** beyond 10 mm. Thirteen 1 mm cells were over:

| cluster | cells | worst cell | worst distance |
|---|---|---|---|
| top-right corner | 12, x 276-279 / y 88-92 | **(277, 90)** | 11.16 mm |
| R11/D6 area | 1, (169, 180) | (169, 180) | 10.07 mm |

Cause: the four +5V 100 nF capacitors left the top-right corner in the earlier pass and took their GND
vias with them; the J26 reroute removed a GND link near (169, 180).

**Fix:** two GND stitching vias, 0.6 mm / 0.3 mm drill, at **(277.00, 90.00)** and **(164.00, 186.00)**.
Both were measured to sit inside both pours before being placed, so each connects In1 and B.Cu rather
than stub-ending in one. DRC stayed 0/0/0.

**After:** **146 links, worst 10.00 mm, 0.0 % beyond 10 mm.** `revC\E1_stitching_plot.png` regenerated.
E1 set back to **Done** in `TASK_TRACKER.md` and `REPLY_TO_CTO.md`, and the stitching row in
`STAGE_TRACKER.md` updated. The standing rule (re-run the metric after every copper or via change) is
recorded in finding 41 and was applied again after Task 3.

## 3. Task 2 - via-in-pad evidence

`revC\vias_in_pads.txt` regenerated from the saved board: **67 rows of 315 vias**, one row per via, with
reference, pad, pad net, footprint, via net, x, y, **via size** and drill. The count rose from 65 to 67 in
the 2026-11-03 reroutes; the denominator moved 314 -> 315 because Task 1 added two vias.

`revC\FAB_NOTES.md` updated everywhere (65 -> 67, 314 -> 315), including the "move all 67 off the pads"
option row, and it now states that the count rose during the reroutes. The IPC-4761 plug/fill/cap
requirement is unchanged.

**C5 still reads Met, and its evidence line now matches the board** (`67 of 315`, same pad set as
`vias_in_pads.txt`). R16 stays open - that is Serigreen's agreement and the price, a different obligation.

## 4. Task 3 - the 20 failing connector pins

Every row in `revC\decoupling_map.csv` now carries a `verdict` (MOVE / ADD / NONE) and a
`verdict_reason`; **no blank verdicts**. Totals: **3 MOVE, 13 ADD, 20 NONE** of 36 supply pins.

Counts by class, before and after (no copper moved in this task, so they are identical):

| class | pins | meet both | meet local | meet bulk | MOVE | ADD | NONE |
|---|---|---|---|---|---|---|---|
| connector | 21 | 1 (J13.1) | 1 | 1 | 1 | 12 | 8 |
| IC | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| MOSFET | 6 | 0 | 1 | 1 | 1 | 0 | 5 |
| diode | 3 | 0 | 1 | 1 | 1 | 1 | 1 |
| **total** | **36** | **1** | **3** | **3** | **3** | **13** | **20** |

**Why no further board-only move exists.** The blocker is the bulk half, and it is structural:

- **3V3_C has no 10 uF capacitor anywhere on the rail.** Every capacitor on it is 100 nF (C4, C7, C8,
  C9, C10, C30, C36). Ten of the 36 pins are on 3V3_C, so ten can never meet "bulk 10 uF within 10 mm"
  by moving an existing part.
- **/+5V_SENS, /+5V_E22, /+5V_ESP, +5V and /3V3_SENS_SW each have exactly one bulk capacitor**, and on
  /3V3_SENS_SW that one (C51 at 186, 173) already gives Q2.3 a bulk pass at 5.83 mm. Moving it to a port
  trades one pass for another - not a gain.
- The five connector pins with a rot-0 100 nF site (J1.1, J4.3, J7.2, J7.8, J24.1) are all on 3V3_C or
  +5V, so even a perfect local move leaves the bulk half failing. J24.1's site is additionally
  unroutable: the track crosses `/LED1_K` from (132.975, 144.75) to (136.705, 148.48).

**ADD list for Aswin (T-59 in `TASK_TRACKER.md` Part 5, also in `revC\FAB_NOTES.md`):**

| pin | net | value | footprint | site |
|---|---|---|---|---|
| J1.1 | 3V3_C | 100 nF (+10 uF bulk on the rail) | C_0805_2012Metric | (210.50, 157.75) rot 0 |
| J4.3 | 3V3_C | 100 nF (+bulk) | C_0805_2012Metric | (273.50, 117.39) rot 0 |
| J7.2 | 3V3_C | 100 nF (+bulk) | C_0805_2012Metric | (215.65, 163.00) rot 0 |
| J7.8 | 3V3_C | 100 nF (+bulk) | C_0805_2012Metric | (229.14, 169.00) rot 0 |
| J8.5 | 3V3_C | 100 nF (+bulk) | C_0805_2012Metric | (166.06, 157.25) rot 90 |
| J26.1 | 3V3_C | 100 nF (+bulk) | C_0805_2012Metric | (129.75, 152.50) rot 90 |
| J11.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (171.75, 195.00) rot 90 |
| J12.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (187.75, 193.50) rot 90 |
| J15.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (146.13, 193.50) rot 90 |
| J16.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (163.94, 189.50) rot 90 |
| J17.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (266.75, 194.25) rot 90 |
| J24.1 | +5V | 100 nF | C_0805_2012Metric | (138.97, 147.25) rot 0 |
| D7.1 | /+5V_ESP | 100 nF | C_0805_2012Metric | (215.60, 97.50) rot 90 |

The rot-90 rows need a rotated part; rotating a placed footprint raises `lib_footprint_mismatch`, so
they must be added as new parts.

**NONE (20), with the blocking copper** - the 8 connector ones first, then the rest:

| pin | net | what blocks it |
|---|---|---|
| J1.2 | 3V3_C | B.Cu /I2C1_SDA 1.8 mm, J1.3 pad 2.5 mm, B.Cu /I2C1_SCL 4.0 mm |
| J1.21 | /+5V_ESP | J1.20 and J1.22 pads 2.5 mm, B.Cu /UART2_MOD_RX 4.0 mm |
| J20.1 | /3V3_SENS_SW | J20.2 pad 2.5 mm, F.Cu /I2C0_SCL_CH6 4.5 mm, ESD19.1 4.9 mm |
| J5.1 | +5V | J5.2 pad 5.0 mm, GND via 5.3 mm (no room around the terminal body) |
| J6.2 | /+5V_E22 | F.Cu /PWR_EN 1.2 mm and 1.6 mm |
| J14.1 | /3V3_SENS_SW | J14.2 pad 2.5 mm, B.Cu PE 3.8 mm, F.Cu /I2C0_SCL_CH3 4.5 mm |
| J21.1 | /3V3_SENS_SW | B.Cu /I2C0_SDA_CH3 1.5 mm, J21.2 pad 2.5 mm |
| J25.1 | +5V | B.Cu /BZ_NEG 2.1-2.2 mm |
| U4.5 | 3V3_C | F.Cu /WDT_WDI 1.3 mm, WDT_WDI via 1.8 mm |
| U6.1, U6.3, U6.5 | +5V, +5V, /3V3_SENS | U6 pads 1.0 mm, GND vias 1.0 mm, /SENS_GATE 1.1 mm |
| U7.24, U8.24 | 3V3_C | neighbouring pads 0.6 mm, /I2C0_SDA 0.8-0.9 mm |
| Q2.2, Q2.3 | /3V3_SENS, /3V3_SENS_SW | /SENS_GATE 1.0-1.8 mm, Q2 pads 1.9-2.1 mm |
| Q3.2, Q3.3 | +5V, /+5V_SENS | /SENS_GATE 1.3 mm, /3V3_SENS 2.0 mm |
| Q7.2 | +5V | /+5V_E22_IN 1.0 mm, /E22_GATE 1.2 mm |
| D7.2 | +5V | B.Cu /UART2_MOD_RX 4.7 mm, GND via 5.3 mm |

## 5. Task 4 - serviceability of the two moves

**J5 at (222.00, 91.40), rot 0.** Courtyard **217.65-226.54 x 87.86-99.44**. The board's top edge line
is at y 87.425-87.575 (centre 87.50), so the courtyard is **0.36 mm** from it and the part body about
0.61 mm. Pads at y 91.40 and 96.40 (5 mm pitch, 2.8 mm pads).
- Screwdriver: the screws sit over the pads, 3.9 mm and 8.9 mm in from the edge. Access is from above
  and the board is horizontal, so a driver reaches both without obstruction. **Fits.**
- Wire bend: the pads are stacked in y, so the wire entry is along **±x**. To the left the courtyard is
  **5.1 mm** from the ESP32 outline (212.55) and to the right **1.91 mm** from the modem outline
  (228.45). A bend on the modem side does **not** fit; the lead must be dressed to the left or brought
  in from above. **The entry side itself is not verified** - it depends on the MX126 part, and the
  datasheet for that specific terminal is not in the workspace.

**J26 at (134.00, 153.50), rot 0.** Courtyard **131.00-144.50 x 150.60-157.44**. It does not overlap
the DS3231 (144.70-182.80 x 162.95-185.05), the GY-521 or the ESP32 outline; nothing sits above it in
the XY plane, so it is reachable from the top with the RTC module fitted. The four nets read back
connected: 3V3_C 200 items, GND 310, /I2C1_SCL 48, /I2C1_SDA 40, and DRC unconnected is 0.
**Lid clearance is not verified**: the board carries no 3D model for the modules or the enclosure, so
"fits under the lid" cannot be measured, only reasoned from the absence of anything above it.

**Under-module re-test over all five outlines:** modem J3/J4 only; ESP32 J1/J2 only; GY-521 R31/R32;
E22 J6 only; DS3231 seven passives (Q2, Q3, C26, C27, R20, R21, R26). **Nothing new is inside any
outline, and J26 is out of the DS3231.**

## 6. Task 5 - report only

In2.Cu: **61 segments, 431.40 mm, 7 nets.** No net has a free outer corridor:

| net | seg | mm | F.Cu corridor | B.Cu corridor | blocker |
|---|---|---|---|---|---|
| /LED_DRV2 | 14 | 109.84 | -0.30 | -0.30 | /I2C0_MUX_SC1 F.Cu, 3V3_C B.Cu at x 233.5 |
| /LED_DRV1 | 8 | 100.95 | -0.30 | -0.30 | /I2C0_SDA F.Cu, 3V3_C B.Cu at 165-168 |
| /+5V_SENS | 13 | 76.73 | -0.60 | -0.60 | /I2C_SW_RST F.Cu, 3V3_C B.Cu at 237-243 |
| 3V3_C | 10 | 63.07 | -0.35 | -0.35 | /+5V_E22 F.Cu at x 257.5, /E22_AUX B.Cu |
| /SENS_EN | 7 | 52.62 | -0.35 | -0.35 | R32.2 pad, /I2C0_SDA_CH2 B.Cu |
| /I2C0_SCL | 7 | 22.53 | -0.30 | -0.30 | U8.17 pad, /BUZZER_EN B.Cu |
| /I2C0_MUX_SC0 | 2 | 5.68 | -0.30 | -0.30 | /I2C0_MUX_SC1 F.Cu, /I2C0_SDA_CH3 B.Cu |

Each needs real rerouting on the target layer, not a layer-token change. Nothing moved.

Keep-outs: **not drawn.** The ESP32 antenna tab length and the modem U.FL position are still owed by
Aswin. The E22 area (x 296.00-304.57, y 163.00-177.00) is still crossed by `/3V3_SENS_SW` and the
CH3/CH6 runs; the corridor is reported, not drawn over.

## 7. Final state of the checks

| Check | State | Note |
|---|---|---|
| C1 | Met | ERC 0, `ignored_checks []`, title block `Rev C` |
| C2 | **Met** | 0 unconnected, 0 parity, no dangling, on the saved file |
| C5 | **Met** | 0 footprint mismatch, 0 courtyard overlap, 0 silk over pads; fab note now reads **67 of 315** and matches `vias_in_pads.txt` |
| C9 | **Not met** | 1 of 36 pins meets both (J13.1); 3 MOVE / 13 ADD / 20 NONE; 3V3_C has no bulk capacitor |
| C10 | **Not met** | 61 In2 items across 7 nets, all corridors negative; no antenna rule area |
| C12 | **Met** | labels and marks verified in the plotted Gerber last pass; silk DRC 0 |

Gate tally: **4 met (C1, C2, C5, C12), 2 partly (C9, C10), 7 not met.** `pack.ps1` stops at **GATE 5
PRODUCTION**. `trace2.py`: 76 / 76 / 76, **0** status disagreements, **0** priority mismatches.
S3 is **not** declared complete.

## 8. Items changed, with evidence

| Change | Evidence |
|---|---|
| Two GND stitching vias at (277.00, 90.00) and (164.00, 186.00) | `pcb\_work_20261103\T1_drc.json` (0/0/0), metric 146 / 10.00 / 0.0 %, `revC\E1_stitching_plot.png` |
| `revC\vias_in_pads.txt` regenerated: 67 rows of 315, with via size | file header and row count |
| `revC\FAB_NOTES.md` 65 -> 67 and 314 -> 315, with the "rose during the reroutes" note | grep of the file |
| `revC\decoupling_map.csv`: `verdict` and `verdict_reason` on all 36 rows | `pcb\_work_20261103\task3_classify.py` output, 0 blanks |
| E1 back to Done in the tracker and the reply; stitching row in the stage tracker | `trace2.py` 0 disagreements |
| Response sheet regenerated | 76 rows, generator reports 0 mismatches |

## 9. Still open, with reasons

- **13 ADD capacitors** (T-59): need symbols, so a GUI job. The 3V3_C rows additionally need a 10 uF
  bulk on that rail, which does not exist today.
- **20 NONE pins**: no legal site inside the CTO radius; the blocking copper is listed in section 4.
- **C10**: 61 In2 items; the E22 keep-out needs `/3V3_SENS_SW` and CH3/CH6 moved first.
- **Aswin**: ESP32 tab length, modem U.FL position, J17/J20 purpose, module heights.
- **Not verified**: J5's wire-entry side (no MX126 datasheet in the workspace); lid clearance in 3D (no
  models); the 3D check of modules on sockets.

## 10. Newly found

- **3V3_C has no bulk capacitor at all** - ten supply pins can never pass C9 by moving parts.
- **E1's two failing clusters were both caused by the previous pass**: the +5V capacitor bank left the
  top-right corner and took its GND vias, and the J26 reroute removed a link near (169, 180).
- The via-in-pad denominator moved from 314 to 315 because of the two new stitching vias; the in-pad
  count itself stayed at 67.

## 11. Files and rollback

Snapshot before Task 1: `pcb\_snap\T1_E1_20261103_204817` (with `census.json`). Rollback is a copy of
`MoriShield_Carrier.kicad_pcb` from that directory. Working scripts: `pcb\_work_20261103\`
(`e1_probe.py`, `e1_check.py`, `task1_stitch.py`, `task2_vias.py`, `task3_classify.py`,
`task4_checks.py`, `taskE_in2.py`).

---

