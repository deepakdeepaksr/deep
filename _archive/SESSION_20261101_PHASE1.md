# Phase 1 Session Record — 1 November 2026

| | |
|---|---|
| **Files changed** | `pcb\MoriShield_Carrier.kicad_pcb`, `pcb\MoriShield_Carrier.kicad_sch`, `pcb\MoriShield_Carrier.kicad_pro` |
| **Backup** | `pcb\_snap\pre_S3run_20261101_162916\` — board, schematic, project, symbol library, both lib tables, plus `census.json` |
| **Verification** | `revC\erc_RevC.json`, `revC\drc_RevC.json`, produced by `kicad-cli` on the saved files |

---

## 1. Verified numbers, before → after

| Measure | Before this session | After | |
|---|---|---|---|
| DRC total | 145 | **140** | −5 |
| DRC errors | 16 | **16** | unchanged — all `track_width` |
| `track_dangling` | 2 | **0** | ✅ |
| `via_dangling` | 3 | **0** | ✅ |
| `silk_overlap` | 46 | **46** | one added by me, then relocated |
| `silk_over_copper` | 78 | **78** | untouched |
| Unconnected | 0 | **0** | held |
| Schematic parity | 0 | **0** | held |
| ERC | 0 errors / 1 warning | **0 / 1** | held |
| Copper census | 1175 seg / 233 via / 159 fp | **1172 / 230 / 159** | −3 seg, −3 via, **no footprint lost** |

The census is the important line: **159 footprints before and after.** Five dangling items and three dead-copper fragments were removed; nothing that carries a signal was lost.

---

## 2. What was actually done

### 2.1 Release-gate items closed

| Check | What was missing | Now |
|---|---|---|
| **C2** "no dangling track or via" | 2 dangling tracks, 3 dangling vias — the same five items the CTO names in C2's own "Seen so far" | **0.** Removed by UUID from DRC's own report, then chased the dead branch to its end |
| **C6 / Table 14 row 3** "placement in mm **with U4 in it**" | U4 carried `board_only` **and** `exclude_from_pos_files` — the watchdog supervisor was invisible to the assembler | **Both flags cleared.** Placement files generated and U4 is in them |
| **C12** "board name, revision and a blank serial box on the silkscreen" | none of the three existed | **Added on F.SilkS**: `MoriShield Carrier`, `Rev C`, `S/N` with a 20 × 2.2 mm box |
| **C11 / A3** modem orientation | two unkeyed 1×12 sockets, no orientation mark, GND pins asymmetric between the rows | **Added** `1` marks at J3 pin 1 and J4 pin 1, and `MODEM THIS WAY UP` between the rows |
| **C1 / D2** title block | `rev "Proto-Simple Rev 0.2 (Post-RS485 Stripped)"`, `date 2026-10-22` — the exact string the CTO quotes | **`Rev C`, `2026-11-01`**, comment rewritten as a Rev C change note; mirrored in the project file |

### 2.2 Dead copper removed, and how each piece was justified

Five items were deleted. Each was checked before removal, because "dangling" from a script is not the same as "dead":

| Item | Where | Why it is dead |
|---|---|---|
| `3V3_C` track 13.00 mm | (169.00,129.25) → (182.00,129.25) | one end on a via, the other in free air |
| `3V3_C` via | (169.00, 129.25) | orphaned by the track above |
| `3V3_C` track 1.00 mm | (168.00,129.25) → (169.00,129.25) | orphaned by the via |
| `3V3_C` track 0.78 mm | (167.45,129.80) → … | **measured**: floats 0.325 mm below R10.1's pad edge (pad centre 131.00, half-height 0.875 → edge 130.125). Touches nothing |
| `/EVENT_BTN` track 1.05 mm | from (170.55, 131.00) | stub off R10.2 with a free end |

The first removal exposed the second, the second the third — a four-segment dead branch off R10.1. It was chased to completion rather than stopped at the number DRC first reported.

### 2.3 Net classes

`3V3` floor set 0.50 → 0.20 mm, with the reason written into the project:
> *3V3_C carries the MPU-6050 socket, the DS3231 socket, the I2C pull-ups and the modem VDD_UART level-translator reference — worst case under 50 mA.*

**It did not take effect, and that is reported rather than hidden.** See §4.1.

### 2.4 Files generated into `revC\`

| File | Status |
|---|---|
| `MoriShield_Carrier_RevC_schematic.pdf` | ✅ 451 KB, plotted from the current schematic with the Rev C title block |
| `erc_RevC.json`, `drc_RevC.json` | ✅ from the saved files, `--schematic-parity --refill-zones` |
| `render_top.png`, `render_bottom.png`, `render_iso.png` | ✅ 1800 × 1000, high quality, isometric with floor and perspective |
| `MoriShield_Carrier_RevC_bom.csv` | ⚠ generated **with empty Manufacturer / MPN / Rating / Temp / Variant columns** — deliberately, so the C6 gap is visible rather than assumed away |
| `MoriShield_Carrier_RevC_pos_front.csv` | ✅ 12.9 KB, mm |
| `MoriShield_Carrier_RevC_pos_back.csv` | ⚠ 36 bytes — the board is single-sided assembly, so this is expected, but it must be checked against the BOM at S4 |
| `preview_do_not_ship\` | 9 Gerbers + drill + job file. **Labelled as preview and excluded from the release zip** — the board is mid-S3 and R1's whole lesson is that stale production files are the expensive mistake |

---

## 3. Two regressions I caused, and fixed

Being explicit, because the same thing will be tempting to gloss over:

1. **A silkscreen overlap.** My first silk pass placed the serial box at x 153.0, overlapping the new `S/N` label — `silk_overlap` went 46 → 47. Moved the box to x 156.5; back to 46.
2. **An invalid s-expression.** My `(justify right center)` token ordering is not accepted by KiCad's parser and **the board stopped loading entirely** — `Expecting left, right, top, bottom, or mirror`. Repaired to `(justify right bottom)` and re-verified by a full DRC run.

Both were caught because the loop was *edit → reload → DRC*, not *edit → assume*. The backup in `_snap\` was available and was not needed.

---

## 4. What is still wrong, including one thing I cannot explain

### 4.1 Unresolved — the 3V3 class floor is not the rule being applied

13 `3V3_C` tracks are still flagged `track_width`, at **0.200 mm (10, all In2.Cu) and 0.250 mm (3, F.Cu/B.Cu)** — at or above the 0.20 mm floor I set. The count was **also exactly 13 when the floor was 0.50 mm**, at which width the 24 tracks at 0.30 mm should also have failed.

So the floor in force on `3V3_C` is **0.30 mm**, and it is not the value in `net_settings.classes.3V3`. Candidates: the pattern `3V3_C` is not binding and some other class is; or an inner-layer half-etch correction is applied; or the board caches the class table until a GUI save.

**This needs 60 seconds in Board Setup → Net Classes, where the binding is visible.** I am not going to guess at it and write a number I cannot defend.

**Until it is resolved, "16 DRC errors" is not attributable to copper that is genuinely too thin** — 13 of them may be a rule-engine artefact.

### 4.2 Deliberately not attempted — the four schematic net changes

These are the highest-value remaining items and I stopped short of them on purpose:

| Item | Change needed | Why it was not attempted blind |
|---|---|---|
| **A7, C2, C5, R11** | `/E22_M0` GPIO11 → GPIO15, `/E22_M1` GPIO10 → GPIO38, `/REED_PULSE_F` GPIO41 → GPIO39 | Each is a global label moving between two pins of a 22-pin connector, plus adding/removing `no_connect` flags. Schematic connectivity is carried by wires and label instances, not by per-pin net fields — text surgery can silently break a neighbouring connection and **would put the parity-0 state at risk** |
| **R7, A11** | remove U8.16 from `/PWR_EN`, R16 4.7 k → 100 k | Same class of edit. Also **blocked on D-1**: the enable polarity decides whether the pull-down is the safe state |
| **`/MODEM_RST` pull** | 100 kΩ pull, direction unknown | **Blocked on D-2** — pulling the wrong way holds the modem in reset |
| **`3V3_C` off J1.1 / J1.2** | de-link our rail from the ESP32 board's 3V3 *output* | Same surgery risk; and the Edgehax doc is explicit that those pins are outputs, so the fix is right but must be made where it can be seen |

**The honest trade-off:** I would rather hand over four precisely-specified edits than a broken schematic with a plausible-looking report. The parity-0 state took the last two sessions to reach and is the single strongest thing in the package.

### 4.3 Stack-up — deliberately not written

A stack-up needs the fab's dielectric constants and core/prepreg thicknesses. We do not have them (dependency **D-7**, the capability sheet, is unanswered). Writing plausible numbers into `board.design_settings.stackup` would produce a job file that **looks** specified and is **invented**. The stack-up goes in at S4 with the fab's real data, and until then the copper weights are stated as assumptions in `revC\FAB_NOTES.md`: *1 oz outer, 0.5 oz inner, 1.6 mm, 4 layers — to be confirmed.*

### 4.4 R16 is not partly done — it is untouched, and DRC cannot see it

Every via centre was tested against every SMD pad:

> **65 vias sit inside an SMD pad.**

Rev B was cited for *"65 vias sat inside solder pads"*. **The number is identical.** Nothing about this finding has changed since the review, and it is invisible to DRC because KiCad does not flag via-in-pad by default — which is precisely how it survived a full DRC run at 0 clearance errors.

| Footprint family | Vias inside pads |
|---|---|
| `C_0805` hand-solder | 23 |
| `R_1206` hand-solder | 19 |
| `SOT-23-6` (U10, the eFuse placeholder) | 9 |
| `R_0805` hand-solder | 4 |
| `SOT-23` / `SOT-23-5` | 6 |
| `C_1206` | 2 |
| `D_SMB` | 2 |

All 65 are listed with coordinates in **`revC\vias_in_pads.txt`**.

**This does not need 65 routing changes.** With hand assembly, the correct answer is one line on the fab drawing: *plug, fill and cap all vias under SMD pads per IPC-4761 Class B or C.* That is a cost decision for Serigreen, not a week of re-routing, and it is now written into `revC\FAB_NOTES.md`. **It needs your agreement to specify filled-and-capped, and Serigreen's to price it.**

### 4.5 The 124 silk items are 25 parts, and three of them are half the problem

| Violation | Kind | Count |
|---|---|---|
| `silk_over_copper` | F.Silkscreen graphics over copper | 52 |
| `silk_overlap` | Reference fields overlapping each other | 46 |
| `silk_over_copper` | Reference fields over copper | 26 |

Only **25 distinct parts** appear, and **U7 (26), U8 (25) and C31 (18) account for 69 of the 124** — 56 % of the whole item in three components. The estimate of 3–4 hours was pessimistic; clearing U7, U8 and C31 first is roughly 45 minutes of work and would take the count from 124 to about 55.

---

## 5. Register rows this session moved

| Row | Before | After |
|---|---|---|
| **C2** (CHK) | not met — 5 dangling | **met** |
| **C6** (CHK) | not met | **partly** — U4 restored, placement generated; BOM fields and fab drawing still missing |
| **C12** (CHK) | partly | **partly, much closer** — name/rev/serial and orientation marks added; 124 silk items remain |
| **D2** | open | **partly** — revision and date correct, sheet still A0 |
| **H2** | new/regressed | **improved** — U4 now in BOM and placement; the push-pull supervisor and the cabled-bus watchdog remain |
| **R5** | partly | **improved** — no footprint mismatch anywhere on the board |
| Table 14 row 3 | 0 % | **partly** — placement with U4 exists; Gerbers deliberately withheld until S4 |

Rows **not** moved: A7, C2 (59-item), C5, R11, R7, A11, R4, R17, C8, E7, R12, E3, G1, G2, G3, and every evidence document.

---

## 6. Next actions, in the order that unblocks the most

| # | Action | Who | Time |
|---|---|---|---|
| 1 | **Open Board Setup → Net Classes and confirm which class `3V3_C` is bound to and what floor is live** (§4.1) | you or Deepak, GUI, 60 s | resolves the meaning of 13 of the 16 remaining errors |
| 2 | **Agree "filled and capped" for the 65 vias in pads** (§4.4), then put it in the Serigreen message | you | 5 min; it replaces 65 routing changes |
| 3 | **Send the Serigreen message** — D-3 deviation, D-5 SD/PSRAM, D-6 RS485, D-7 capability sheet + fill cost, D-9 fifth pin, and now R16 | you | 20 min to send; **everything from S2 onward is downstream of it** |
| 4 | Clear silk on **U7, U8, C31** first — 69 of 124 items in one pass | me, DRC after each | 45 min |
| 5 | The four schematic net changes in §4.2, done in the GUI where the wires are visible, or by me with you watching the screen | you + me | ~90 min |
| 6 | BOM fields Manufacturer / MPN / Rating / Temp on all 159 parts via Edit Symbol Fields | me, then you check | 90 min |
| 7 | ESD arrays to ≤5 mm at the 14 field connectors; add protection to J24 / J25 | me with DRC after each | 3 h |
| 8 | Antenna keep-out rule area; In2 nets to outer layers; 47 Ω on the 10 missing cabled I2C lines | me | 3 h |
| 9 | Response sheet, reply, six-condition budget, pin map, truth table, decoupling map, FMEA, bring-up plan | me | 5 h |
| 10 | `revC\pack.ps1` — run it last. It refuses to build the zip if the ERC or DRC report is older than the file it describes | you | 1 min |

---

## 7. Files this session produced

| File | What it is |
|---|---|
| `revC\MoriShield_Carrier_RevC_schematic.pdf` | The drawing, with the Rev C title block |
| `revC\erc_RevC.json`, `revC\drc_RevC.json` | Tool output on the saved files |
| `revC\render_top.png`, `render_bottom.png`, `render_iso.png` | Evidence renders |
| `revC\vias_in_pads.txt` | **All 65 via-in-pad locations with coordinates** — the R16 evidence |
| `revC\FAB_NOTES.md` | Stack-up, minimum features, via-fill requirement, assembly notes — assumptions labelled |
| `revC\MoriShield_Carrier_RevC_bom.csv` | BOM, with the missing columns visible rather than hidden |
| `revC\MoriShield_Carrier_RevC_pos_front.csv` | Placement, mm, now including U4 |
| `revC\pack.ps1` | Builds the release zip and **refuses** if the reports are stale |
| `revC\preview_do_not_ship\` | Gerbers and drill for review only, excluded from the release |
| `pcb\_snap\pre_S3run_20261101_162916\` | Full restore point with `census.json` |
