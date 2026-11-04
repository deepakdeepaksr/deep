# STAGE_TRACKER — MoriShield Carrier Rev C

| | |
|---|---|
| **Document** | ST-CAR-4L-RevC-01 |
| **Date** | 2026-11-02 (measured numbers refreshed 22:45) |
| **Board** | `pcb\MoriShield_Carrier.kicad_pcb` |
| **Single contact and signatory** | Aswin |
| **Companions** | `TASK_TRACKER.md` (the 76 items), `REPLY_TO_CTO.md` (what goes to Serigreen) |
| **Status** | Working plan. Rev C is **not released for fabrication**. |

Gate criteria below are quoted from the source documents, not paraphrased. Where a stage has
more than one binding clause, every clause is quoted and the stage is only complete when all of
them pass.

---

## Current measured numbers

Refreshed after every verification run. Last refresh: 2026-11-01.

| Measure | Value | Command or file |
|---|---|---|
| ERC | **0 errors, 0 warnings** | `kicad-cli sch erc --severity-all --format json` — re-run independently 2026-11-01 and reproduced |
| DRC violations | **0** | `kicad-cli pcb drc --refill-zones --schematic-parity --severity-all --all-track-errors --format json` — reproduced |
| DRC errors | **0** | same |
| DRC warnings | **0** | same |
| Unconnected items | **0** | same |
| Schematic parity | **0** | same |
| Census | **159 footprints · 1178 segments · 315 vias · 6 zones · 134 nets** (2026-11-03: J26 moved, J5 moved, 8 capacitor relocations, 2 +5V segments moved to F.Cu) | `pcb\_census.ps1` |
| Suppressed checks | **0** — all nine re-enabled, nothing ignored | `.kicad_pro` |
| **DRC items the nine suppressions hid** | **0** — was 15; all fixed (courtyards added to U4 and SW1, 13 track ends centred) | `revC\_drc_b3.json` |
| **ERC against the release-layout library** | **0 `lib_symbol_issues`** — was 336 against the stale 153,623 B copy; the copy was refreshed to 157,936 B and the package stages it | `revC\_work\scratch\libtest_after` |
| **ERC when the footprint library does not travel** | **0 `footprint_link_issues`** — was 124; `pack.ps1` now stages the `.pretty` beside the project | `revC\pack.ps1` |
| **Package build** | **stops at GATE 5 PRODUCTION** — the response sheet exists and the derived files are current, so the build reaches the production gate and refuses: no release Gerber set at `revC\gerber`. Correct for this stage | `revC\pack.ps1` |
| **`pack.ps1` stages** | `MoriShield_Carrier.kicad_sym`, `MoriShield_Carrier.kicad_dru` and the whole `MoriShield_Carrier.pretty` into `project\libraries\`, with `${KIPRJMOD}/libraries/...` tables in forward slashes — so the receiver can re-run our width floors and resolve the footprints | `revC\pack.ps1` |
| Vias in SMD pads | **67 of 315** (was 65 of 314); `revC\vias_in_pads.txt` and `revC\FAB_NOTES.md` regenerated 2026-11-03 and agree with the board | `revC\vias_in_pads.txt`, `revC\FAB_NOTES.md` |
| Track on In2.Cu | **431.40 mm / 61 segments / 7 nets** (was 448.41 / 63 / 8; the +5V feed moved to F.Cu) | `pcbnew` |
| ESD distance, field ports | 11.3–27.6 mm (J11–J23); none at J24/J25/J26 | `revC\_esd_measure.json` |
| Title block | `Rev C`, `2026-11-01`, A0 sheet | `.kicad_sch` |
| Silk verification plot | 12,128 strokes; J18 marks Δ0.05 mm; name/Rev/S-N present. Save 22:31:44, DRC 22:45:13, plot 22:45:15 | `revC\silk_check\` |
| Decoupling verdict | **36 supply pins (21 connector, 6 MOSFET, 6 IC, 3 diode): 1 meets both (J13.1), 3 meet local, 3 meet bulk, 33 fail local, 33 fail bulk.** Measured with the CTO's verbatim 100 nF / 10 uF thresholds; the earlier 31-fail-bulk figure used 1 uF as bulk and mis-parsed "100nF/16V" as 10 uF | `revC\decoupling_map.csv` |
| Release gate | Gate tally, counted from the rows above: 4 met (C1, C2, C5, C12), 1 partly (C9), 8 not met (C3, C4, C6, C7, C8, C10, C11, C13). | `TASK_TRACKER.md` Part 2, `gate_truth.py` |
| Table 11 pre-send ticks | 2 of 16 | `TASK_TRACKER.md` Part 3 |
| **LoRa socket orientation** | J6 is numbered for a **180-degree insertion** and all seven nets line up that way - it is **not** mis-wired. But nothing marks it: no silk, pads named 1-7 only, header unkeyed | `pcb` J6 pad nets; Ebyte E22-900T22D manual section 3; Aswin's pin-1 reading 2026-11-02 |
| **microSD, measured** | slot owns **GPIO10, 11, 12, 13** (CS, MOSI, CLK, MISO). **GPIO9 and GPIO14 are not on the slot**, so `/I2C0_SCL` on GPIO9 is safe. CHK-001 C11 is right about 10-13, wrong to include 14 | Aswin's continuity test 2026-11-02 |
| **Open design changes not yet in the board** | T-55 strap E22 M0/M1 to GND through 0 ohm (frees the microSD); T-56 move the reed from GPIO41 to **GPIO39** (J2.9); T-57 print port labels on F.SilkS; T-58 keyed header | `TASK_TRACKER.md` Part 5 |
| **Port labels do not print** | 9 items on F.SilkS; every port name is on **F.Fab**, which is not in the Gerber set. J21 is the FDC1004 (channel 5); J17 and J20 have no identified sensor | text dump by layer 2026-11-02 |
| **ESP32 antenna** | identified as the **J1/J2 pin-1 end** (left row 3V3/3V3/RST, right row GND/TX/RX). The outline gives only 2.5 mm past that row where the board has about 11.6 mm, so the outline is short and the keep-out is not yet drawn. **Awaiting Aswin's tip-to-pin measurement** | vendor photo and board geometry 2026-11-02 |
| GND plane distance to a ground link | max **10.00 mm**, **0.0 %** beyond 10 mm, **146 links** in both pours (was 144 / 11.16 mm / 0.1 % after the 2026-11-03 moves; restored by two GND vias at (277.00, 90.00) and (164.00, 186.00)) | `revC\E1_stitching_plot.png` |
| `/+5V_SENS` series resistance | **156.6 mΩ** (313 → 177.4 → 156.6); 25 segments at 0.80 mm, 12 capped at 0.60 mm | `revC\EVIDENCE_RevC.md` §7 |
| **Derived files vs the design** | Regenerated from the saved board: BOM 23:51:39, POS front/back 23:51:40, `vias_in_pads.txt` 23:51:32, `FAB_NOTES.md` rewritten; board saved 23:50:46. Gate 4 passes | timestamps |
| **J18 power chain, pad nets (re-read today)** | `+5V_IN` J18.1 → F1 → `+5V_F` → Q9 → `+5V` → J5.1; D2, ESD16 and C13 on `+5V`; **U10 has no net on any of its six pads** | `pcb\_evidence\power_chain_pads.json` from `_cto_extract\power_chain_now.py` |
| **Converter audit (XL4015 5 A module with LED voltmeter)** | **No-Go, written up.** 8–36 V operating / 40 V absolute input against condition 1's "40 V or more"; no TVS holds off at 22–25 V and clamps under 36 V; +65 °C display and 85 °C electrolytics in a +70 °C box; 7 A limit against F1's 8 A trip. Incumbent LM2596HVS kept, with its die marking (LM2596 vs LM2596HV) still unverified | `revC\BUCK_AUDIT_XL4015_20261101.md`; `_cto_extract\XL4015_datasheet.txt`; `_cto_extract\SMBJ_series.txt` |

---

## Stages

| Stage | What ships | Gate criteria (verbatim) | Status | Evidence file | Date | Blocked by |
|---|---|---|---|---|---|---|
| **S1** Schematic-only review package | Schematic PDF, ERC report, response sheet, cover message, six-condition plan, pin map and truth table | CHK-001 §3: *"If you want a look at the schematic before you lay out the board, send the schematic, the ERC report and the response sheet on their own."* · C1: *"ERC reports 0 errors and 0 warnings on the saved schematic, and the title block carries the right revision."* · Table 2, Schematic PDF: *"Plotted from the same schematic, with the revision in the title block."* · Table 2, Reports: *"Run on the saved files, after the plot settings of check C3. ERC 0 errors and 0 warnings; DRC 0 errors, 0 warnings, 0 unconnected items, parity clean."* · Table 14 row 1: *"A response sheet against the 59 items and R1 to R17: what changed and the evidence. Every P0 designed in and evidenced (for A2, B10 and C1 to C4, the bench result or the agreed plan to take it on the first boards); each P1 closed or deferred in writing with Serigreen's agreement; each P2 closed or listed for Rev C; any rejection with its reason."* | **Partly** | `revC\MoriShield_Carrier_RevC_schematic.pdf`, `revC\erc_RevC.json`, `REPLY_TO_CTO.md`, `TASK_TRACKER.md` | — | Table 14 row 1 (no signed statuses); the schematic PDF predates the last schematic edits |
| **S2** Power protection and interface close-out | Revised schematic and board, updated response sheet | C8: *"The three input events are written up with the simulation; stand-off and clamp voltages are stated against the rail; every ESD part is within 5 mm of its pin; the PE bond is on the board and described."* · C11: *"The signed pin map is in the package and matches the schematic; no pin is double-used; every control line has one driver and a defined reset state in the truth table; the watchdog survives reset and download; the bus recovery is designed and described."* · Condition 2: *"Reverse-polarity protection, and an over-voltage cut-off that disconnects the board before its 5 V rail reaches 5.5 V and survives 12 V or 24 V on J18 indefinitely; current limit near 3.5 A."* | **Not started** | `revC\BUCK_AUDIT_XL4015_20261101.md` (condition 1 analysis) | — | R4 (controller search and Serigreen's deviation signature); **the converter decision, now question 8a: the XL4015 module is audited and rejected, and condition 1 cannot be closed until Serigreen either supplies a 40 V-or-more converter or signs the deviation**; A1, A2 (modem polarity); E22 pinout (B1) |
| **S3** Layout completion | Board, renders, maps, fresh ERC and DRC | C2: *"0 unconnected items, 0 parity differences, no dangling track or via, on the saved file."* · C5: *"No footprint mismatch, no courtyard overlap, no silk over pads, no via in a pad without a fab note, constraints met."* · C9: *"The decoupling map shows every supply pin inside the distance; the 3D check shows every module on its right socket with the box closed; nothing reachable sits under a module."* · C10: *"The plane layers show nothing but their planes; the antenna rule area is in the file and empty on every layer; the spacing rules are met with the rule file matching the board; the power copper meets check C7; stitching is in."* · C12: *"Every polarity mark sits beside the right pad on the plotted Gerber; the board carries name, revision and serial box; no silk over copper."* | **In progress** | `revC\erc_RevC.json`, `revC\drc_RevC.json`, `revC\render_*.png`, `revC\EVIDENCE_RevC.md` | — | R12 (63 In2.Cu items, needs rerouting); E3 (antenna position unknown, awaiting Aswin's photo); condition-3 copper (3 mm pour and via arrays at J18, blocked on R4); C8 (no ESD at J24/J25/J26) |
| **S4** Fabrication release package | Gerbers, drill, job file, IPC-356, placement, BOM, fab drawing, response sheet, checksums | 004 §7: *"Rev B goes to fabrication only on Serigreen's written release, which names the exact file set by its checksum, so the board ordered is the board reviewed."* · 004 §7 row 2: *"KiCad project and schematic PDF; ERC 0 errors and 0 warnings; DRC 0 on the saved file with zones refilled."* · C3: *"DRC on the saved file is clean, the Gerbers were plotted after that DRC, and the plot dialog's zone check was on. State the three times (save, DRC, plot) in the response sheet."* · C4: *"Every copper layer, mask, paste, silk, outline and drill file matches the board, inner-layer clearances included, and the IPC-D-356 file is in the package."* · C6: *"Every BOM line has manufacturer, part number, quantity, rating and temperature range; the placement file has every fitted part; the job file shows revision, finish and the real stack; the fab drawing is in the package."* · Table 11: *"Tick each line on the files in the zip, not on the files on screen."* | **Not started** | — | — | S3; fab capability sheet (D-7); stack-up dielectric data; BOM part numbers |
| **S5** First-article bench evidence | Evidence pack: bench results, EMC, 72-hour runs | 004 §7 row 6: *"Power: G1 results (modem connector 4.75 V or more in the worst case; clamps; thermal), supply-path resistances or a DC solve for every load, and the decoupling map with copper distances (B7, B10, B12); the B10 bench trace and the modem registering on the network (A2), or the agreed plan to take them on the first Rev B boards."* · 004 §7 row 8: *"Interfaces: schematic and layout for RS485, the microSD archive, the FDC1004 port and the event button (C1 to C4), with their bench results or the agreed plan to close them on the first Rev B boards."* · C13: *"Each document is in the package and the response sheet points at it from the items it closes."* | **Not started** | — | — | Boards; bench access (modem, SIM, LTE coverage); Serigreen's written allowance for items that close on first boards |

---

## What each stage can honestly claim

| Stage | Can claim | Cannot claim |
|---|---|---|
| S1 | Schematic is drawn and ERC-clean apart from one placeholder warning; parity and unconnected are zero; the response sheet exists | Release, fabrication readiness, or that any P0 is evidenced |
| S2 | Protection and pin map designed; the converter candidates audited against condition 1 | Bench survival of reverse, 12 V and 24 V; a named converter that satisfies condition 1 while its die marking and surge coordination are unverified |
| S3 | Layout complete, DRC clean, silk clean | That the antenna keep-out is right, that the vias in pads are acceptable to the fab |
| S4 | Package complete and internally consistent | That the board works |
| S5 | The board works on the bench | That it passes EMC until the plan is run |

**No stage in this file authorises fabrication.** Release is Serigreen's, in writing, naming the
files by checksum.
