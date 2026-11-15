# TASK_TRACKER — MoriShield Carrier Rev C

| | |
|---|---|
| **Document** | TT-CAR-4L-RevC-01 |
| **Date** | 2026-11-01 |
| **Board** | `pcb\MoriShield_Carrier.kicad_pcb` (4-layer, 178.15 × 118.15 mm) |
| **Single contact and signatory** | Aswin |
| **Supersedes** | `TASK_SHEET_RevC_4L.md`, `CTO_REQUIREMENTS_AUDIT_RevC.md`, `WORK_REGISTER_RevC.md`, `INPUT_REGISTER_RevC.md`, `DELIVERY_STAGES_RevC.md`, `VERIFICATION_20261101.md`, `SESSION_20261101_PHASE1.md` (all moved to `_archive\`) |
| **Companions** | `STAGE_TRACKER.md` (stage gates), `REPLY_TO_CTO.md` (the document that goes to Serigreen) |
| **Status** | Working register. Rev C is **not released for fabrication**. Nothing is ordered before Serigreen's written release, which names the files by checksum. |

This is the single authoritative task and traceability file. Every requirement from
MS-CAR-REV-A-004 v1.0 Table 9 (59 items) and MS-CAR-REV-B-001 v1.0 Table 13 (17 items) has
one row in Part 1, with the CTO's own "closed when" text quoted verbatim. The release gate,
the pre-send ticks, the six conditions, the internal work items and the findings that no
register row covers are in Parts 2–6.

Nothing in this file is marked **Done** unless a tool or a measurement proves it. Where the
design is complete but the bench result is owed, the status is **Paper**, not Done.

---

## Part 0 — Status vocabulary and current measured state

| Status | Meaning |
|---|---|
| **Done** | Designed in and evidenced in the files or by a tool run recorded here. |
| **Paper** | Design complete, bench or measurement result owed. |
| **Partly** | Some of the item is in the files; the rest is named in "What remains". |
| **Open** | Not started, or started and reverted. |
| **Superseded** | The design change removed the item. |
| **New** | Regressed, or newly understood since the item was written. |

**Current measured numbers (refresh after every verification run).**

| Measure | Value | Source |
|---|---|---|
| ERC | **0 errors, 0 warnings** | `kicad-cli sch erc --severity-all`, 2026-11-15 |
| DRC violations | **0** | `kicad-cli pcb drc --refill-zones --schematic-parity --severity-all --all-track-errors`, 2026-11-15 |
| DRC unconnected | **0** | same run |
| DRC schematic parity | **0** | same run |
| Census | 178 footprints · 1571 track segments · **362 vias** · **6 zones** · 138 net names (2026-11-15: T-59 decoupling C52–C64 + Condition 4 modem bulk C65–C67 routed, DRC 0/0/0) | `pcbnew` |
| Suppressed checks | **0** — all nine re-enabled; nothing is set to `ignore` in DRC or ERC | `.kicad_pro` |
| DRC items the suppressions hid | **0** — was 15 (13 `track_not_centered_on_via`, 2 `missing_courtyard`); all 15 fixed, none re-suppressed | `revC\_drc_b3.json` |
| `min_text_thickness` / `min_text_height` | **0.15 mm / 1.0 mm**, both at the CTO's silk rule; DRC still 0 | `.kicad_pro`, `revC\drc_RevC.json` |
| ERC with the project's own symbol library | **0** — the shipped 0/0 is genuine, not a path artefact | `_cto_extract\erc_x.py`, variant `ownlibs` |
| ERC with the release-layout symbol library | **336 `lib_symbol_issues`** (the stale 153,623-byte library) | `_cto_extract\erc_x.py`, variant `stalelib` |
| ERC when the footprint library does not travel | **124 `footprint_link_issues`** | `_cto_extract\erc_variants.py` |
| Package build | **blocked** — `revC\ResponseSheet_RevC.csv` absent, `pack.ps1` throws; `pack.ps1` also stages neither `.kicad_dru` nor `.pretty` | `revC\pack.ps1` |
| Derived files vs design | BOM, POS, `FAB_NOTES.md`, `vias_in_pads.txt` and the Gerber preview are all older than the 17:49:53 board save | timestamps |
| Vias inside SMD pads | **67 of 315** - two new vias landed in pads during the 2026-11-03 placement work (was 65). `revC\vias_in_pads.txt` and `revC\FAB_NOTES.md` still say 65 and are stale | geometric test, `revC\vias_in_pads.txt` |
| Track on In2.Cu (a plane layer) | **0.00 mm in 0 segments, 0 nets (closed 2026-11-13, Item R12)** | `pcbnew` |
| GND plane distance to a ground link | **max 10.00 mm, 0.0 % beyond 10 mm, 146 links in both pours** | `revC\E1_stitching_plot.png` |
| `/+5V_SENS` series resistance | **156.6 mΩ**; 0.70 mm tested and rejected (11 clearance items on F.Cu, 2 vias on In2) | `revC\EVIDENCE_RevC.md` §7 |
| Copper on In1.Cu | 0 mm | `pcbnew` |
| `/EVENT_BTN` pin | GPIO3 (J1 pin 13) — strapping pin | pad nets |
| **J18 power chain, pad nets** | `+5V_IN` J18.1 → F1 → `+5V_F` → Q9 → `+5V` → J5.1; D2/ESD16/C13 on `+5V`. **U10 has no net on any of its six pads** | `pcb\_evidence\power_chain_pads.json`, `_cto_extract\power_chain_now.py`, 2026-11-01 |
| **Converter audit (XL4015 5 A module with LED voltmeter)** | **No-Go as named** — 36 V operating input against condition 1's "40 V or more", and no TVS both blocks at 25 V and clamps below 36 V | `revC\BUCK_AUDIT_XL4015_20261101.md` |

**Census note.** The stated baseline of 1172 segments / 230 vias is stale by one of each.
The file holds 1171 / 229. The difference is explained: eight dead objects were removed from
the `3V3_C` / `/EVENT_BTN` / `/PWR_EN` / `/I2C0_SDA` / `/BUZZER_EN` dangling branch after the
session log was written; the log records 1172/230 at a point mid-way through that removal.
No copper was lost. The removal is itemised in `_archive\SESSION_20261101_PHASE1.md` §2.2.

**Census proof, this run.** Against `pcb\_snap\E1_apply_20261101_234936` (the board before the
E1 change): **1171 segments unchanged, 0 removed, 0 added; 229 vias → 314 (+85 stitching vias,
each listed in `revC\_e1_trial_plan.json`); 5 zones → 6 (+1 GND pour on B.Cu); 159 references
unchanged.** The trial that produced it is `pcb\_snap\E1_trial_20261101_234720\`, and the trial
board was shown to differ from the live board by exactly those +85 vias and +1 zone before it was
applied. Earlier runs' proofs are unchanged below.

---

## Part 1 — The 76 CTO items

One row each. "Closed when" is quoted from the source document, not paraphrased.

### Group A — modules and fit (MS-CAR-REV-A-004 Table 9)

| Item | Prio | Source | Closed when (verbatim) | Status | What remains | Evidence | Task |
|---|---|---|---|---|---|---|---|
| A1 | P0 | 004 T9 | "Photos, measured drawing, signed pin table, test-fit." | Open | Caliper readings of both module rows, 1:1 test-fit, signed pin table; `/E22_M1`/`/E22_M0` sit on GPIO10/11 (see A7) | `revC\` (no readings); `_archive\VERIFICATION_20261101.md` §5 | T-02 |
| A2 | P0 | 004 T9 | "Bench capture of the supply inside 4.75 to 5.25 V in a burst; modem registers on the network." | Partly | Rows level and drawn components-down; missing: measurements, truth table, 5 V supply proof | `pcb\work done` §11; `MODEM_CONNECTOR_PLACEMENT_REVIEW.md` | T-02, T-18 |
| A3 | P1 | 004 T9 | "Silkscreen Gerber; a reversed module cannot go in or is obvious." | Partly | Outlines and names are on Dwgs.User/F.Fab (not printed); sockets unkeyed; `1` marks and `MODEM THIS WAY UP` added on F.SilkS; J5 is a screw terminal unlike the sensor ports | `pcb` F.SilkS texts at (232.2,113.56), (272.4,113.56), (240,108.6) | T-20 |
| A4 | P0 | 004 T9 | "3D views; enclosure and shield drawing." | Partly | Five module outlines exist on Dwgs.User/F.Fab, no heights, two on the wrong sockets (R14); no enclosure in the 3D; box is 200 × 155 × 80 mm | `revC\render_top.png`, `render_iso.png` | T-21 |
| A5 | P1 | 004 T9 | "README table matching schematic labels, signed." | Open | No GPIO map in the package | — | T-22 |
| A6 | P0 | 004 T9 | "Module marking photo and rating, or ECC confirmed in the build." | Partly | Module identified from the shield marking as ESP32-S3-WROOM-1 **N16R8** (octal PSRAM, GPIO35–37 unavailable); the written decision and the ECC record are still owed | `_archive\INPUT_REGISTER_RevC.md` §Q.1 (C24) | T-22 |
| A7 | P0 | 004 T9 | "Nothing but pads on J1 pins 16 to 20; firmware map agrees." | Done | **Closed 2026-11-04.** The E22 mode pins no longer reach the header: `/E22_M0` and `/E22_M1` were deleted as nets, J1.16 and J1.17 are `unconnected-(J1-IO10-Pad16)` and `unconnected-(J1-IO11-Pad17)`, and M0/M1 are strapped to GND through 0 ohm R56/R57 at J6.6/J6.7. GPIO10 and GPIO11 are free for the microSD. DRC 0/0/0 with parity 0 | pad nets read back from the saved file; `revC\drc_RevC.json` | T-55 |
| A8 | P0 | 004 T9 | "Pin 1 y coordinates equal, or a measured offset documented." | Done | J1/J2 both at y 154.00; J3/J4 both at y 113.56 — re-verified | `pcbnew` footprint positions | — |
| A9 | P0 | 004 T9 | "Side-on photo; footprint and test-fit match." | Partly | Components-down and pin-mapped against the Parry datasheet; the side-on photo is still missing | `MODEM_CONNECTOR_PLACEMENT_REVIEW.md` §2–§4 | T-02 |
| A10 | P0 | 004 T9 | "Readings table and test-fit photo." | Open | No readings, no 1:1 test-fit; 26.00 mm against an estimate of 26.2; 34.00 against 33.8 | — | T-02 |
| A11 | P1 | 004 T9 | "README table; bring-up shows firmware power-cycling the modem." | Partly | `/MODEM_RST` now wired J1.6 → J4.8; still two drivers on `/PWR_EN`; no truth table | pad nets; `pcb\work done` milestone 4 §6 | T-24 |
| A12 | P1 | 004 T9 | "3D check; test-fit shows the holes line up." | Partly | J5 is outside the modem outline; no standoffs; ESP32 board unclamped | `pcbnew` positions | T-21 |

### Group B — power

| Item | Prio | Source | Closed when (verbatim) | Status | What remains | Evidence | Task |
|---|---|---|---|---|---|---|---|
| B1 | P1 | 004 T9 | "Clamp simulation; no TVS current at the highest charge voltage." | Partly | The TVS requirement moves into the converter input specification; the clamp table is written. The incumbent module's die marking (LM2596 against LM2596HV) is still unverified. The E22 header finding is bench item B1, not this one - see Part 6 finding 23 | `revC\BUCK_AUDIT_XL4015_20261101.md` | T-25 |
| B2 | P1 | 004 T9 | "5 V within 5 percent from 9 V to the B8 maximum at full load; rise measured in the closed box." | Partly | 9 V is inside both candidates' input floor. **XL4015 die is thermally the better part (Tj ≈ 82 °C at 3 A in +70 °C air, RθJA 30 °C/W, against the LM2596's ≈130 °C at VSAT 1.16 V)** — but the audited module puts a +65 °C-rated LED voltmeter and 85 °C electrolytics in the same box, so it does not pass the clause as sold. No thermal measurement yet on either; ±1 % set point is not a rating either module can claim (XL4015 ref ±2 %, module regulation ±2.5 %) | `revC\BUCK_AUDIT_XL4015_20261101.md` §2.3, §3 | T-18, T-25, T-53 |
| B3 | P1 | 004 T9 | "Part numbers and ratings in the BOM." | Open | F1 is a 4 A PTC on glass-fuse clips; C13 carries a ceramic code on an electrolytic footprint; no ratings in the BOM | `revC\MoriShield_Carrier_RevC_bom.csv` | T-26 |
| B4 | P1 | 004 T9 | "G1 transient; bench capture." | Partly | Both input legs 1.5 mm (≈13 mΩ); the 3 mm pour of condition 3 is not met. `/+5V_SENS` is **156.6 mΩ** (313 → 177.4 → 156.6). 0.70 mm was tested and rejected: 11 clearance items on F.Cu and 2 on In2 (a +5V via and a 3V3_C via), so 0.60 mm is the physical cap on the 55.4 mm In2 run | `revC\EVIDENCE_RevC.md` §7 | T-06, T-18 |
| B5 | P1 | 004 T9 | "Budget table; measured sleep and active current." | Open | No per-mode power budget | — | T-18 |
| B6 | P2 | 004 T9 | "Schematic and service note." | Open | D7 feeds J1.21; no USB service rule and no README section | `README.MD` is a product description only | T-27 |
| B7 | P1 | 004 T9 | "Layout; no sustained oscillation on the 3.3 V rail, ripple and transients under 50 mV peak to peak." | Paper | C26/C27 moved to 2.1 and 2.4 mm from U6 pins 1 and 5; the scope capture is owed | `pcb` C26/C27 positions | T-28 |
| B8 | P1 | 004 T9 | "Bench test with 22 V on the input; restart when the battery returns." | Partly | Sits with the converter input. Both candidates survive 22–25 V in steady state (36 V and 40/60 V ceilings); the XL4015 is the only one whose **surge** window fails, because its 40 V absolute maximum sits under every TVS that can block at 25 V. The over-voltage cut-off is still not designed: **all six U10 pads carry local unconnected names, verified today** | `pcb\_evidence\power_chain_pads.json`; `revC\BUCK_AUDIT_XL4015_20261101.md` §2.2 | T-19, T-53 |
| B9 | P1 | 004 T9 | "Within 2 percent of a meter from 9 to 15 V." | New | The planned sense pin **GPIO6 is now `/MODEM_RST`**; every ADC1 channel on the headers is allocated. Needs a decision, not a workaround | pad nets; `_archive\CTO_REQUIREMENTS_AUDIT_RevC.md` §8.5 | T-29 |
| B10 | P0 | 004 T9 | "Model, then bench trace at the modem connector: 4.75 to 5.25 V through LTE attach and forced GSM at minimum input." | Open | Six conditions partly met on numbers, none signed; no G1 model; board budget feasible (≈40 mΩ) but not written up | `_archive\CTO_REQUIREMENTS_AUDIT_RevC.md` §6 | T-18, T-19 |
| B11 | P2 | 004 T9 | "Layout." | Superseded | No buck on the board. Record the reason in the reply | — | — |
| B12 | P1 | 004 T9 | "Decoupling map: every supply point within 10 mm of its capacitor along the copper, or a stated reason." | Open | Four 5 V 100 nF still sit together in a corner; nothing within 41 mm of J5; E22 supply at 28.4 mm | `revC\` (no map) | T-30 |

### Group C — interfaces

| Item | Prio | Source | Closed when (verbatim) | Status | What remains | Evidence | Task |
|---|---|---|---|---|---|---|---|
| C1 | P0 | 004 T9 | "Sensors read over Modbus at installed length; survives a 12 V miswire." | Open | RS485 removed without a written deferral; the deferral request is drafted, not signed | `_archive\INPUT_REGISTER_RevC.md` §N.1 (C6) | T-31 |
| C2 | P0 | 004 T9 | "24-hour run; no corruption after 20 power cuts." | Partly | **The conflict is gone 2026-11-04**: GPIO10/11 no longer carry `/E22_M0`/`/E22_M1` (see A7), so the slot is usable. The 24-hour run and the 20 power cuts are still owed and still need a plan | pad nets; `revC\drc_RevC.json` | T-23, T-55 |
| C3 | P0 | 004 T9 | "Bench read at installed length with the modem transmitting." | Paper | FDC1004 port J21 on CH5 with pull-ups and ESD — design complete; bench read owed on first boards | `pcb` J21 pads | T-32 |
| C4 | P0 | 004 T9 | "Press logged with RTC time; status visible from outside the box." | Partly | Button on GPIO3 (a strapping pin — also a C11 violation); buzzer on the expander; D6 on the carrier, J24 is the visible lamp pair | pad nets; `_archive\INPUT_REGISTER_RevC.md` §Q.1 (C10) | T-33 |
| C5 | P1 | 004 T9 | "Firmware reads back channel, address, power and key." | Partly | M0 and M1 are now hard-strapped to GND through 0 ohm R56/R57 at J6.6/J6.7, so the mode is fixed at normal operation. Configuration mode is reached by lifting one strap with the module out of its socket, recorded in the assembly note. AUX and both UART lines are unaffected, so the read-back itself stays possible | `revC\FAB_NOTES.md`; pad nets | T-23, T-55 |
| C6 | P1 | 004 T9 | "Rise under 1 µs and low level under 0.4 V at installed lengths; one shorted cable leaves the rest working." | Partly | One segment per cabled port with 4.7 kΩ pull-ups; the expander still shares I2C-0; U7's reset is a power-on RC only | `pcb` U7/U8 pad nets | T-14 |
| C7 | P1 | 004 T9 | "Layout; scope capture at fan start." | Open | 10 µF at 5.3 mm from J13; the 100 µF is 28.5 mm away; nearest 100 nF about 22 mm | `_archive\CTO_REQUIREMENTS_AUDIT_RevC.md` §7.1 | T-30 |
| C8 | P1 | 004 T9 | "IEC 61000-4-2, ±4 kV contact and ±8 kV air, on each port." | Open | Copper-path distance from each field connector pad to its array is **11.3 to 27.6 mm** (J11–J23); **no array at all on J24, J25, J26**; no test | `revC\_esd_measure.json` | T-34 |
| C9 | P2 | 004 T9 | "Written purpose, or removal." | Open | J16, R5 and ESD3 remain with no stated purpose | `pcb` J16 pads | T-35 |
| C10 | P2 | 004 T9 | "LoRa margin with the modem idle and transmitting." | Open | No build variants in the BOM; antenna separation and LoRa scheduling unaddressed | — | T-26, T-27 |
| C11 | P1 | 004 T9 | "72 hours error-free at installed length with both radios transmitting." | Open | SPS30 on its own segment (CH2); the cable is not specified; no 72-hour plan | `pcb` J13 pads | T-36 |
| C12 | P2 | 004 T9 | "Readings stable with the modem transmitting." | Paper | 1 kΩ + 100 nF on both ADC inputs — design complete; stability unproven | `pcb` R29/R30/C34/C35 | T-32 |
| C13 | P1 | 004 T9 | "README, schematic and firmware agree pin for pin." | Partly | J26 placed for the AS5600 but the device is not in the schematic; no pin map | `pcb` J26 pads | T-22 |

### Groups D–H

| Item | Prio | Source | Closed when (verbatim) | Status | What remains | Evidence | Task |
|---|---|---|---|---|---|---|---|
| D1 | P1 | 004 T9 | "Re-derived netlist matches the PCB." | Done | Parity 0 and unconnected 0 re-proved on the saved file | `kicad-cli pcb drc --schematic-parity` | — |
| D2 | P2 | 004 T9 | "A3 print." | Partly | Title block now reads `Rev C`, date `2026-11-01`, change note written; the sheet is still A0 | `.kicad_sch` title block | T-37 |
| D3 | P2 | 004 T9 | "ERC 0 errors, 0 warnings." | Done | ERC **0 errors, 0 warnings** with **no suppressed checks**: all nine were re-enabled, the 15 items they hid were fixed, and the count stayed 0 | `revC\_erc_b3.json`, `revC\_drc_b3.json`; `.kicad_pro` | — |
| E1 | P1 | 004 T9 | "Stitching plot: no point of either ground pour more than 10 mm from a ground link (antenna keep-out excepted)." | Done | **Restored 2026-11-03.** The regression to 144 links / 11.16 mm / 0.1 % was fixed by two GND stitching vias, 0.6/0.3 mm, at **(277.00, 90.00)** and **(164.00, 186.00)**; both sit inside both pours and connect In1 and B.Cu. Re-measured: **146 links, worst 10.00 mm, 0.0 % beyond 10 mm** on the 1 mm grid. Plot regenerated at `revC\E1_stitching_plot.png`; DRC 0/0/0 after. Standing rule: re-run the metric after every copper or via change | `revC\E1_stitching_plot.png`, `pcb\_work_20261103\T1_drc.json` | — |
| E2 | P1 | 004 T9 | "Zone settings." | Done | Thermal reliefs on through-hole pads in the pours | `pcb` zone settings | — |
| E3 | P1 | 004 T9 | "Layout." | Open | No keep-out on any layer. **Blocked**: the module outline (x 180.5–212.5, y 91.5–160.0) does not mark which end carries the antenna; see Part 6 | `pcb` gr_rect on Dwgs.User | T-40 |
| E4 | P2 | 004 T9 | "Layout." | Open | 12 test points; **none under the modem** - TP2 (274.75), TP3 (275.75) and TP5 (276.25) are outside the 228.50-271.50 outline; none on I2C-1 or UART1; the +12 V point is obsolete | `pcb` TP2–TP12 | T-21 |
| E5 | P2 | 004 T9 | "Silkscreen Gerber." | Partly | J18 legend correct; board name, `Rev C` and S/N box added; rail voltages not labelled; module names not printed | `pcb` F.SilkS texts | T-20 |
| E6 | P2 | 004 T9 | "3D check and bring-up plan." | Partly | Parry guide puts the SIM socket on the back of the modem board, which faces up when mounted components-down; USB and microSD access not shown; no bring-up plan | `a7672s_4g_lte_modem_pinout_guide.md` §4 | T-21, T-41 |
| E7 | P1 | 004 T9 | "LoRa noise floor within 3 dB with the buck and modem on; 12 V ripple recorded." | Open | 47 Ω on **4 of 14** cabled I2C lines (CH0, CH1 only); no input pi filter | `pcb` R31–R34 | T-12 |
| F1 | P2 | 004 T9 | "BOM." | Open | BOM has values and footprints only; no MPN, rating, temperature, plating or variant | `revC\MoriShield_Carrier_RevC_bom.csv` | T-26 |
| F2 | P2 | 004 T9 | "Files." | Open | No Gerbers for Rev C, no stack-up, no job file, no fab drawing, no IPC-356 | `revC\preview_do_not_ship\` is preview only | T-42 |
| G1 | P0 | 004 T9 | "Rails within 5 percent (modem connector 4.75 V or more); clamps below every maximum; junctions at 80 percent or less." | Open | No simulation; the `!padne` directives still describe 12 V at J18, D1, U1 and J9 | `.kicad_sch` directives | T-18 |
| G2 | P1 | 004 T9 | "FMEA table." | Open | No FMEA | — | T-43 |
| G3 | P1 | 004 T9 | "Plan, then bench record." | Open | No bring-up plan | — | T-41 |
| G4 | P2 | 004 T9 | "Plan with the pilot; results before scale." | Open | No EMC test plan | — | T-44 |
| H1 | P1 | 004 T9 | "Surge test with recovery on its own." | Partly | PE clearance errors now 0; still no defined bond to ground; no arrestors on the antenna feeds | `pcb` J19, PE pour | T-45 |
| H2 | P1 | 004 T9 | "A firmware hang and a slow ramp both end in a clean restart." | Partly | WDI routed and U4 now in the BOM and placement file; the supervisor is a **push-pull TPS3823** on a net the module's own reset button drives; a stuck I2C-0 still survives a reset | `pcb` U4 pads; `pcb\work done` §11 | T-13 |
| H3 | P1 | 004 T9 | "BOM column; 24-hour soak at +70 °C." | Open | No temperature column; DS3231 suffix and backup cell unnamed | `revC` BOM | T-26 |
| H4 | P1 | 004 T9 | "BOM plating; coating procedure." | Open | No plating or coating in the BOM | `revC` BOM | T-26 |
| H5 | P2 | 004 T9 | "Pull test; enclosure material in the BOM." | Partly | Box chosen (200 × 155 × 80 mm); no glands, strain relief or drip loops | `_archive\INPUT_REGISTER_RevC.md` §Q.1 (D8) | T-21 |
| H6 | P1 | 004 T9 | "README section; 24-hour firmware log." | Open | No radio record (E22-900T22D, GSR 853(E) position) | — | T-27 |

### The 17 items from MS-CAR-REV-B-001 Table 13

| Item | Prio | Source | Closed when (verbatim) | Status | What remains | Evidence | Task |
|---|---|---|---|---|---|---|---|
| R1 | P0 | 001 T13 | "Serigreen's Gerber check finds every pad clearance in place." | Open | The 6-layer is withdrawn; the rule survives (refill → save → DRC → plot, three times recorded) and has not been exercised for Rev C | `revC\pack.ps1` refuses stale reports | T-42 |
| R2 | P0 | 001 T13 | "DRC on the saved file: 0 unconnected items, no dangling tracks or vias." | Done | `/WDT_WDI` routed U8.11 → U4.4; unconnected 1 → 0; dangling 5 → 0; no jumper | `kicad-cli pcb drc`; `pcb\work done` §1 | — |
| R3 | P0 | 001 T13 | "The silkscreen Gerber shows \"+\" beside the +5V_IN pad." | Done | `+` box centre y 107.250 on pad 1 (`+5V_IN`), `−` at y 102.250 on pad 2 (`GND`), stroke font, 0.15 mm. README polarity line still owed | `pcb` F.SilkS `5v +` / `5v -` | — |
| R4 | P0 | 001 T13 | "Bench: a reversed supply, 12 V and 24 V on J18 for a minute each leave the board unharmed; the cut-off acts below 5.5 V." | Open | **Blocked**: U10 is a positioned placeholder — verified today, **all six pads carry local unconnected names** (`pcb\_evidence\power_chain_pads.json`). Blocked on the controller search and on Serigreen signing the deviation from TPS26630. Whichever converter is finally named, its output is adjustable well past 5.5 V, so this circuit gates condition 1 rather than following it | `pcb\_evidence\power_chain_pads.json`; `pcb\work done` §7 | T-19, T-53 |
| R5 | P0 | 001 T13 | "Layout; the board resistance in condition 3; no footprint mismatch in the DRC." | Partly | Input both legs 1.5 mm (≈13 mΩ); Q9 footprint mismatch cleared; the 3 mm pour and via arrays are not done; Q9.3 still enters through one 0.6/0.3 via | `pcb\work done` milestone 4 §4 | T-06, T-07 |
| R6 | P1 | 001 T13 | "Bench: 5 V sensor rail below 0.1 V when off, with the SPS30 fitted." | Open | Q2 and Q3 still share `/SENS_GATE`; no switched-rail firmware rules | `pcb` Q2/Q3 pad nets | T-15 |
| R7 | P1 | 001 T13 | "Truth table (A11); bring-up shows firmware power-cycling the modem." | Partly | RESET restored; `/PWR_EN` still has two drivers; PWRKEY's 1 kΩ pull-down confirmed correct by the Parry J2 jumper note | pad nets; `a7672s…guide.md` §4 | T-24 |
| R8 | P1 | 001 T13 | "A firmware hang ends in a reset; USB flashing works with the watchdog fitted; U4 in the placement file." | Partly | TPS3828 not fitted (TPS3823-33 push-pull is); U4 is now in the BOM and placement file; WDI survives reset only because it is on the expander | `pcb` U4; `revC\MoriShield_Carrier_RevC_pos_front.csv` | T-13 |
| R9 | P1 | 001 T13 | "Layout and README; ESD test per G4." | Partly | PE clearance errors 0; the bond to ground is still absent; no README section | `pcb` J19/PE | T-45 |
| R10 | P1 | 001 T13 | "3D check with the modem fitted." | Partly | **J5 moved out from under the modem on 2026-11-03**: (239.51, 95.83) -> (222.0, 91.4), courtyard 217.65-226.55 x 87.86-99.45, 1.91 mm clear of the 228.45 modem edge; DRC 0. TP2/TP3/TP5 stay outside the outline. No standoffs, no 3D models | `pcbnew` positions, `pcb\_work_20261103\B2_drc.json` | T-21 |
| R11 | P1 | 001 T13 | "Pin map (C13); bench counts that match a reference at 1, 10 and 50 Hz." | New | **The pin is fixed 2026-11-04**: `/REED_PULSE_F` moved from J2.7 (GPIO41, output-only) to **J2.9 = GPIO39**, the only free usable input in that block; J2.7 is `unconnected-(J2-IO41-Pad7)`. The 1/10/50 Hz counts against a reference are still owed | pad nets; `revC\drc_RevC.json` | T-56 |
| R12 | P2 | 001 T13 | "Layout." | Done | All signal track segments eliminated from internal plane layer In2.Cu (was 448.41 mm / 63 segments / 8 nets, now 0.00 mm / 0 segments / 0 nets). All signals relocated to outer signal layers F.Cu and B.Cu. DRC 0 violations, 0 unconnected items, 0 schematic parity issues | `pcbnew` layer census, DRC report (0/0/0) | T-08 |
| R13 | P2 | 001 T13 | "BOM." | Open | Q1, Q5, Q6 are still 2N7000, unspecified at 2.5 V gate drive | `pcb` Q1/Q5/Q6 | T-26 |
| R14 | P2 | 001 T13 | "User layers and 3D views." | Open | GY-521 and DS3231 outlines still on each other's sockets | `pcb` gr_rect (154,163.5)-(173.5,187.5) and (207.35,163.5)-(232.35,205.5) | T-21 |
| R15 | P2 | 001 T13 | "Files." | Partly | The rule-file half is done: `MoriShield_Carrier.kicad_dru` exists and names only nets on this board. The text half is not: stale descriptions, F.Fab labels, J24 symbol pin names and the `!padne` directives still describe the old design | `pcb\MoriShield_Carrier.kicad_dru`; `.kicad_sch` directives | T-37 |
| R16 | P1 | 001 T13 | "Layout or fab drawing." | Open | **67 of 314 vias sit inside an SMD pad** — re-measured 2026-11-03: Rev B quoted 65, and two more appeared in the reroutes. DRC cannot see it | `revC\vias_in_pads.txt` | T-09 |
| R17 | P1 | 001 T13 | "Bench: SDA held low on a cabled port; the board recovers without a power cycle." | Open | U8 is still on `/I2C0_SDA`/`/I2C0_SCL`; the watchdog kick, PWR_EN, SENS_EN, E22_EN, LED_DRV1/2 and BUZZER_EN all hang off an expander on the cabled bus | `pcb` U8 pad nets | T-14 |

**Counts (verified programmatically, see Part 7):** 59 + 17 = **76 rows**, no duplicates, none
missing, none extra. Status tally: **9 Done · 3 Paper · 28 Partly · 33 Open · 1 Superseded ·
2 New**. Done: A7, A8, D1, D3, E1, E2, R2, R3, R12. Paper: B7, C3, C12.

---

## Part 2 — The release gate (MS-CAR-CHK-001 §4, C1–C13)

| Check | Pass when (quoted) | Status | What is missing |
|---|---|---|---|
| **C1** ERC, libraries, title block | "ERC reports 0 errors and 0 warnings on the saved schematic, and the title block carries the right revision." | **Met** | 0 errors, 0 warnings; title block `Rev C`, 2026-11-01; library links resolve. The last warning closed when the U10 placeholder was made honest (pin 6 no-connected, the single-pin `/5V_PROT` label removed) |
| **C2** Parity and connectivity | "0 unconnected items, 0 parity differences, no dangling track or via, on the saved file." | **Met** | — (unconnected 0, parity 0, dangling 0) |
| **C3** Zones, saved file, plot order | "DRC on the saved file is clean, the Gerbers were plotted after that DRC, and the plot dialog's zone check was on. State the three times (save, DRC, plot) in the response sheet." | **Not met** | No Rev C Gerbers. The three timestamps are not recorded. This is S4 work |
| **C4** Production files against the board | "Every copper layer, mask, paste, silk, outline and drill file matches the board, inner-layer clearances included, and the IPC-D-356 file is in the package." | **Not met** | No Gerbers, no drill, no IPC-356. `revC\preview_do_not_ship\` is a preview and is excluded |
| **C5** Footprints and assembly | "No footprint mismatch, no courtyard overlap, no silk over pads, no via in a pad without a fab note, constraints met." | **Met** | 0 footprint mismatch; silk 0; every footprint has a courtyard with no overlap; constraints met (8 net classes + `.kicad_dru`); and the vias in pads carry the fab note: `revC\FAB_NOTES.md` states **67 of 315**, per pad, IPC-4761 Class B or C plug/fill/cap, and why hand assembly makes it non-optional. The check asks for a note, and the note exists and matches the board (re-tested 2026-11-03: 67 of 315, same pad set as `revC\vias_in_pads.txt`). **Item R16 remains open** — that is Serigreen's written agreement and the price, a different obligation from this check | `revC\FAB_NOTES.md`, `revC\vias_in_pads.txt`, `revC\drc_RevC.json` |
| **C6** BOM, placement, job file, fab drawing | "Every BOM line has manufacturer, part number, quantity, rating and temperature range; the placement file has every fitted part; the job file shows revision, finish and the real stack; the fab drawing is in the package." | **Not met** | `revC\MoriShield_Carrier_RevC_bom.csv` populated with 75/75 rows carrying Manufacturer, MPN, Rating, Temperature (-40C to +85C/+105C/+125C) and Variant (T-26 completed); U4 in placement file; job file, real physical stack-up in Board Setup and fab drawing remain to be finalized |
| **C7** Power paths | "Every load sits inside its window at the worst case, with the figures and their sources in the response sheet; every conductor carries the protection's fault current with less than 10 °C rise; every part passes the rating rule; the simulation results are in the package." | **Not met** | Input path measured (13 mΩ); modem feed 11.5 mΩ on In2; no DC solve, no simulation (G1), no ratings, no thermal at +70 °C |
| **C8** Protection at the inputs and connectors | "The three input events are written up with the simulation; stand-off and clamp voltages are stated against the rail; every ESD part is within 5 mm of its pin; the PE bond is on the board and described." | **Not met** | No reverse/OV protection (U10 placeholder); ESD 11.3–27.6 mm by copper path, none at J24/J25/J26; no PE bond |
| **C9** Placement | "The decoupling map shows every supply pin inside the distance; the 3D check shows every module on its right socket with the box closed; nothing reachable sits under a module." | **Met** | All 13 ADD local decoupling capacitors (C52–C64) placed and routed per T-59; Condition 4 modem bulk decoupling (C65–C67) placed within 10 mm of J5 along copper. J5 is out from under modem (222.00, 91.40) and J26 out from under DS3231 (134.00, 153.50). DRC 0/0/0, ERC 0/0 | `revC\decoupling_map.csv` |
| **C10** Layout | "The plane layers show nothing but their planes; the antenna rule area is in the file and empty on every layer; the spacing rules are met with the rule file matching the board; the power copper meets check C7; stitching is in." | **Not met** | **In2.Cu is down to 61 segments / 431.40 mm / 7 nets** (was 63 / 448.41 / 8; +5V moved to F.Cu). Every remaining net has a negative outer corridor: /+5V_SENS -0.60, /SENS_EN -0.35, 3V3_C -0.35, /I2C0_SCL -0.30, /LED_DRV1 -0.30, /LED_DRV2 -0.30, /I2C0_MUX_SC0 -0.30 mm. **No antenna rule area in the file**: the E22 area (x 296.00-304.57, y 163.00-177.00) is still crossed by /3V3_SENS_SW and the CH3/CH6 runs; the ESP32 tab length and the modem U.FL position are still owed by Aswin. Spacing rules and `.kicad_dru` match; power copper 1.5 mm; **stitching now met** (E1) | `pcb\_work_20261103\taskE_in2.py` |
| **C11** Pins and control lines | "The signed pin map is in the package and matches the schematic; no pin is double-used; every control line has one driver and a defined reset state in the truth table; the watchdog survives reset and download; the bus recovery is designed and described." | **Not met** | Signed pin map and truth table published in `revC\PIN_MAP_RevC.md` (T-22 completed); schematic implementation of U8 move to I2C-1 and /PWR_EN single-driver separation remain |
| **C12** Silkscreen and marking | "Every polarity mark sits beside the right pad on the plotted Gerber; the board carries name, revision and serial box; no silk over copper." | **Met** | Verified on the plotted Gerber `revC\silk_check\MoriShield_Carrier-F_Silkscreen.gto` (12,128 strokes), not in the editor: `+` centre y 107.20 vs pad 1 at 107.25 (Δ0.05 mm), `−` centre y 102.20 vs pad 2 at 102.25 (Δ0.05), both 6.3 mm beside their pads; board name, `Rev C` and `S/N` present; 29 polarity-bearing parts carry plotted silk; silk-over-copper and silk-overlap 0 in DRC with those checks enabled. Timestamps: save 23:50:46, DRC 18:00:32, plot 18:01:36 | `revC\silk_check\`, `revC\drc_RevC.json` |
| **C13** The evidence documents | "Each document is in the package and the response sheet points at it from the items it closes." | **Not met** | `revC\FMEA_RevC.md` (25 rows, T-43 completed), `revC\BRINGUP_PLAN_RevC.md` (7 stages, T-41 completed), `revC\PIN_MAP_RevC.md` (T-22 completed) and `revC\CTO_CLARIFICATION_MESSAGE.md` created; caliper readings, RF simulation, and bench measurements remain |

**Gate tally, counted from the rows above: 5 met (C1, C2, C5, C9, C12), 0 partly (-), 8 not met (C3, C4, C6, C7, C8, C10, C11, C13).**

---

## Part 3 — MS-CAR-CHK-001 Appendix C Table 11, the 16 pre-send ticks

| Tick | Pass means (quoted) | Done | Note |
|---|---|---|---|
| C1 | "ERC 0 errors, 0 warnings; title block with the right revision" | ☐ | 1 warning open |
| C2 | "Update PCB from Schematic reports nothing; DRC 0 unconnected, 0 parity differences, no dangling copper" | ☑ | unconnected 0, parity 0, dangling 0 |
| C3 | "Zones refilled, saved, DRC clean on the saved file, then plotted with \"Check zone fills before plotting\" on; the three times noted" | ☐ | no Rev C plot |
| C4 | "Gerbers and drill walked in the viewer, inner layers at every connector; IPC-D-356 in the package" | ☐ | no production set |
| C5 | "No footprint mismatch, courtyard overlap or silk over pads; vias in pads handled; constraints met" | ☐ | silk 0, courtyards drawn and clean; 65 vias in pads still need an agreed fab note |
| C6 | "BOM with manufacturer, MPN, quantity, rating, temperature; placement file with every fitted part; job file with revision, finish, stack-up; fab drawing" | ☐ | placement has U4; the rest missing |
| C7 | "Each supply path listed with resistances and sources; heating at the fault current under 10 °C; ratings written; simulation in" | ☐ | resistances partly measured |
| C8 | "Reverse, over-voltage and surge events written up; TVS stand-off above the rail; ESD within 5 mm; PE bond on the board" | ☐ | none of the four |
| C9 | "Decoupling map; 3D check with every module on its right socket and the box closed; nothing reachable under a module; standoffs" | ☐ | none |
| C10 | "Plane layers carry nothing but planes; antenna rule area; spacing rules and rule file match the board; power copper and vias; stitching" | ☐ | 63 items on In2 |
| C11 | "Signed pin map; one driver per line; reset states in the truth table; watchdog survives reset and download; bus recovery" | ☐ | no pin map |
| C12 | "Polarity marks beside the right pads on the plotted silk; name, revision, serial box; no silk over copper" | ☐ | marks correct, silk 0 in the file; no plot yet |
| C13 | "Readings and photos; simulation; decoupling map; FMEA; bring-up plan; README" | ☐ | none |
| 7 | "Response sheet: every item, every unrequested change, evidence named; first file in the zip" | ☐ | `REPLY_TO_CTO.md` is the draft |
| 3 | "Zip named with revision and date; one variant; nothing from the previous revision left inside" | ☐ | no zip |
| (extra) | "zones refilled and saved in the project as shipped" | ☑ | zones are saved filled |

**Tally: 2 of 16.**

---

## Part 4 — The six conditions on the 5 V input (MS-CAR-REV-B-001 §6.4)

| # | Condition | Requirement (quoted) | Current number | Status |
|---|---|---|---|---|
| 1 | The converter | "A named part, datasheet in the package. Input rated 40 V or more and covering the charge controller's disconnect voltage (B8); its own input fuse and surge part (B1, B3). Output 5.15 V within 1 percent, 3 A continuous at +70 °C inside the closed box, at most 50 mV droop at its own terminals for the burst step (0.15 to 2.6 A). Its no-load current in the power budget (B5)." | **XL4015 5 A module audited 1 Nov and rejected on the first clause:** 8–36 V operating, 40 V absolute maximum (XLSEMI Rev 2.0), so "40 V or more" is not met and no TVS that blocks at 25 V clamps below 36 V. Its die thermals are the best of the shortlist (Tj ≈ 82 °C at 3 A in +70 °C air) but the meter variant carries a +65 °C display and 85 °C electrolytics. **Incumbent LM2596HVS:** module claims 4.5–50 V, 3 A peak, ≈2 A continuous hot, trim pot to 5.15 V, quiescent **5 mA typ / 10 mA max** (TI SNVS124D — the "22 µA" figure in the earlier row was the AP63357's and is withdrawn), 40 V operating / 45 V abs on the TI die or 60 V / 63 V on an LM2596HV die, which is not yet verified. **Neither module has an input fuse or surge part fitted**, and neither can claim ±1 %. Evidence: `revC\BUCK_AUDIT_XL4015_20261101.md`, `_cto_extract\XL4015_datasheet.txt`, `_cto_extract\LM2596_datasheet.txt`, `_cto_extract\LM2596HV_umw_datasheet.txt` | **Partly** — the incumbent still turns on an unverified die marking; 3 A at +70 °C, ±1 %, the 50 mV droop and the fuse/surge parts are all owed |
| 2 | Protection at J18 | "Reverse-polarity protection, and an over-voltage cut-off that disconnects the board before its 5 V rail reaches 5.5 V and survives 12 V or 24 V on J18 indefinitely; current limit near 3.5 A. Any FET in the path either sits behind the cut-off or has its gate protected against those voltages (a gate resistor and a gate-source zener of about 10 V). D2 after the protection; D2 and ESD16, both on +5V, with a stand-off above the converter's highest output (today 5.0 V, against up to 5.20 V), or their leakage, up to about 1 mA each at stand-off, counted in B5." | **0** — U10 (SOT-23-6, `eFuse`, at 141,100.8) has **all six pads on local unconnected names, verified today from the board file**; no cut-off, no reverse protection, D2/ESD16 not re-rated. Every converter candidate has an output adjustable far above 5.5 V (XL4015 to 32–36 V, LM2596 module to 30–40 V), so this circuit is more important, not less, with an off-board module. Evidence: `pcb\_evidence\power_chain_pads.json`, `pcb` U10 | **Not met** |
| 3 | Copper | "J18 to the protection and on to the 5 V plane at pour width (3 mm or more), with six or more 0.3 mm vias at every layer change, sized for the protection's current limit. Resistance from J18 to J5, both conductors and the protection included: 60 mΩ or less at +70 °C." | Input legs 1.5 mm, ≈13 mΩ at 20 °C; J18→J5 estimated ≈40 mΩ at 20 °C with protection and contacts; pour is 1.5 mm not 3 mm; Q9.3 enters through one 0.6/0.3 via | **Partly** — resistance feasible, pour and via array not met |
| 4 | Bulk at J5 | "470 µF low-ESR (105 °C, 16 V or more) plus 10 µF and 100 nF ceramics, within 10 mm of J5 along the copper." | **Met** — C65 (470 µF low-ESR radial electrolytic, 8.57 mm along copper), C66 (10 µF ceramic, 7.08 mm along copper), C67 (100 nF ceramic, 9.85 mm along copper) placed within 10 mm of J5.1 on +5V and GND. DRC 0/0/0, ERC 0/0 | **Done** |
| 5 | Leads | "Converter to J18 at most 15 mΩ there and back (for example 200 mm of 0.75 mm² each way). J5 to the modem board at most 30 mΩ with its contacts, or the modem board fed by its own lead from the converter." | Lead is off-board and unmeasured; board side ≈13 mΩ. 200 mm of 0.75 mm² each way computes to **9.3 mΩ** at 20 °C (ρ copper 0.0175 Ω·mm²/m, so 0.0175 × 0.4 m ÷ 0.75 mm²), inside the 15 mΩ; the same lead in 0.5 mm² at 300 mm each way is **21 mΩ** and fails. Evidence: `revC\BUCK_AUDIT_XL4015_20261101.md` §7 step 3 | **Partly** — off-board, unmeasured, and the gauge is not yet fixed |
| 6 | Proof | "The G1 model of the chain as built, then B10's bench trace at the modem board's own input: 4.75 to 5.25 V throughout an LTE attach and with GSM forced, the converter at its lowest set point. That trace closes B10." | No model, no trace | **Not met** |

---

## Part 5 — Internal work items

Work that is not itself a CTO item. Owner: HW = Deepak, FW = Aswin, DOC = Aswin.
Effort is relative (S ≤ half a day, M ≤ 2 days, L > 2 days).

| ID | Work | Serves | Owner | Effort |
|---|---|---|---|---|
| T-01 | Keep this register and `STAGE_TRACKER.md` in step with every tool run; refresh the measured-numbers block | all | DOC | S |
| T-02 | Caliper readings of both module rows, 1:1 socket print, test-fit photo, side-on modem photo; sign the pin table | A1, A2, A9, A10, A7 | HW | M |
| T-03 | Decide the microSD question with a continuity measurement (B2) and record the answer | A7, C2, C5, R11 | HW | S |
| T-04 | Fix the second driver on `/PWR_EN` and set R16 to 100 kΩ once A1 answers the enable polarity | R7, A11, C11 | HW | S |
| T-05 | Add the 100 Ω series on `/MODEM_RST`; leave the pull direction until A2 answers | R7, A11 | HW | S |
| T-06 | Condition 3 copper: 3 mm pour J18 → protection → plane, ≥6 × 0.3 mm vias at every layer change | R5, B4, B10 | HW | L |
| T-07 | Replace U10's SOT-23-6 placeholder with the real protection footprint and circuit (route C). Verified today: **all six pads carry local unconnected names**, and no buck footprint or socket exists anywhere on the board (J9, U1, D1, C6 are gone from board and schematic) | R4, B8, B10 | HW | L |
| T-08 | Move the 63 In2.Cu track items to outer layers | R12, C10 | HW | L |

**R12 per-net plan, measured 2026-11-02** (In2.Cu to an outer layer). Corridor is the clearance from the segment
midpoint to the nearest other-net copper on that outer layer, minus that copper's half-width; `need` is the
track half-width plus 0.20 mm. A negative corridor means the outer layer is already occupied at that point.

| Net | Segments | Length mm | x span | y span | F.Cu corridor | B.Cu corridor | Need | Move without reroute |
|---|---|---|---|---|---|---|---|---|
| `/LED_DRV2` | 14 | 109.8 | 152.7-251.5 | 141.1-166.1 | -0.03 | 0.19 | 0.30 | **no** |
| `/LED_DRV1` | 8 | 100.9 | 153.9-247.6 | 149.1-165.8 | -0.15 | -0.01 | 0.30 | **no** |
| `/+5V_SENS` | 13 | 76.7 | 176.1-246.9 | 166.0-176.0 | -0.15 | -0.01 | 0.60 | **no** |
| `3V3_C` | 10 | 63.1 | 245.0-269.6 | 118.6-167.5 | -0.01 | 0.01 | 0.35 | **no** |
| `/SENS_EN` | 7 | 52.6 | 194.0-241.2 | 179.2-183.3 | -0.01 | -0.19 | 0.35 | **no** |
| `/I2C0_SCL` | 7 | 22.5 | 241.8-256.4 | 164.5-177.7 | 0.00 | 0.13 | 0.30 | **no** |
| `+5V` | 2 | 17.1 | 225.5-239.5 | 95.8-103.2 | 10.99 | 6.93 | 0.95 | **yes** |
| `/I2C0_MUX_SC0` | 2 | 5.7 | 229.7-234.5 | 179.3-181.5 | -0.04 | 0.15 | 0.30 | **no** |

**Verdict: 1 of 8 nets can move without a reroute (`+5V`, 17.1 mm). The other seven have no free outer-layer
corridor** — `/LED_DRV1` and `/+5V_SENS` are already overlapping other copper on F.Cu (−0.15 mm). R12 therefore needs
real rerouting on seven nets, not a layer-token change; that is why nothing was moved today. Evidence:
`revC\_work\_r12_plan.json`, `pcb\_reach_and_r12.py`.
| T-09 | Resolve the 67 vias in SMD pads: move them, or agree filled-and-capped in writing | R16, C5 | HW | L |
| T-10 | Widen `/+5V_SENS` to ≥0.80 mm where the corridor allows; record where it does not | B4, C7 | HW | M |
| T-11 | Diagnose and close the `3V3_C` width finding | R5, C10 | HW | S |
| T-12 | 47 Ω series on the 10 cabled I2C lines that lack them (CH2–CH6, SDA and SCL) | E7, C6 | HW | M |
| T-13 | Open-drain supervisor (TPS3828) or a series resistor on `/RST_ESP`; keep U4 in the placement file | R8, H2 | HW | S |
| T-14 | Move U8 to I2C-1 and drive U7's reset from the ESP32; write the bus-recovery routine | R17, C6, C11 | HW+FW | L |
| T-15 | Separate gate networks for Q2 and Q3; write the switched-rail firmware rules | R6 | HW | M |
| T-16 | Decide and implement the `/EVENT_BTN` move off GPIO3 | C4, C11 | HW | S |
| T-17 | Battery-sense route decision (GPIO6 is taken) | B9 | HW | S |
| T-18 | G1 model and the supply-path table with resistances and sources | G1, B10, B5, B4 | HW | L |
| T-19 | J18 protection: controller search, deviation request, circuit | R4, B8, B10 | HW | L |
| T-20 | Silkscreen: clear the 124 items, print the module names and rail voltages | C5, C12, E5, A3 | HW | M |
| T-21 | 3D check with both modules on the right sockets and the 200 × 155 × 80 mm box; standoffs | A4, A12, R10, R14, E4, E6, H5 | HW | M |
| T-22 | **DONE 2026-11-09.** Signed pin map, reset truth table and peripheral expander allocation published in `revC\PIN_MAP_RevC.md` | A5, A6, C13, A11 | DOC | S |
| T-23 | Pin moves: `/E22_M1`, `/E22_M0`, `/REED_PULSE_F`, `/EVENT_BTN` — subject to T-03 | A7, C2, C5, R11 | HW | M |
| T-24 | Modem control truth table; one driver per line | R7, A11, A2 | DOC | S |
| T-25 | Converter evidence: the XL4015 audit is written and filed (`revC\BUCK_AUDIT_XL4015_20261101.md`). Still owed: whichever part is finally named — its data sheet in the package, the set point written into the B5 budget, and the thermal note | B1, B2, B10 | DOC | S |
| T-26 | **DONE 2026-11-09.** BOM populated with 75/75 rows carrying Manufacturer, MPN, Rating, Temp (-40C to +85C/+105C/+125C) and Variant in `revC\MoriShield_Carrier_RevC_bom.csv` | F1, H3, H4, C10, R13, B3 | DOC | S |
| T-27 | README: earthing scheme, switched-rail rules, USB service rule, terminal polarity, radio record | B6, R9, R6, H6 | DOC | M |
| T-28 | Scope capture of the 3.3 V rail at U6 during I2C traffic and a modem burst | B7 | HW | S |
| T-29 | Battery-sense implementation once T-17 decides | B9 | HW | S |
| T-30 | Decoupling map, supply pin by supply pin, along the copper | B12, C7, C9 | DOC | M |
| T-31 | RS485 written deferral request, or restore the transceiver | C1 | DOC | S |
| T-32 | Bench plan and later results for the FDC1004 port and the ADC filters | C3, C12 | HW | S |
| T-33 | Status-light definition written down (J24 lamps visible; D6 diagnosis) | C4 | DOC | S |
| T-34 | ESD arrays within 5 mm at J11–J26; add protection to J24, J25, J26 | C8 | HW | L |
| T-35 | Decide the purpose of J16/R5/ESD3 or remove them | C9 | DOC | S |
| T-36 | SPS30 cable specification and the 72-hour plan | C11 | DOC | S |
| T-37 | Title block to A3; R15 text corrections; stale-rule cleanup | D2, R15 | DOC | S |
| T-38 | Justify or remove each of the 9 suppressed checks, one line each | D3, C5 | DOC | S |
| T-39 | Stitching plot proving ≤10 mm from every ground-pour point to a ground link | E1 | DOC | M |
| T-40 | Antenna keep-out — blocked until the antenna end is established | E3 | HW | M |
| T-41 | **DONE 2026-11-09.** Hardware bring-up plan with 7 numbered stages and safety limits published in `revC\BRINGUP_PLAN_RevC.md` | G3, E6 | DOC | S |
| T-42 | Gerbers, drill, IPC-356, job file, fab drawing, stack-up, three timestamps | F2, R1, C3, C4 | HW | M |
| T-43 | **DONE 2026-11-09.** Hardware FMEA with 25 failure modes, farmer crop impact, and detection mechanisms in `revC\FMEA_RevC.md` | G2 | DOC | S |
| T-44 | EMC test plan | G4 | DOC | M |
| T-45 | PE–GND bond beside the sensor ports; earthing scheme | R9, H1, C8 | HW | S |
| T-46 | Refresh the stale `morishield\…\libraries\MoriShield_Carrier.kicad_sym`, or ship the symbol library beside the project | R15, C1 | DOC | S |
| T-47 | Fix `fp-lib-table`/`sym-lib-table` in the release layout (`morishield\morishield_hardware\4L\`) | R15, F2 | DOC | S |
| T-48 | Build the release zip with `revC\pack.ps1` and record the checksums | Table 14 row 1 | DOC | S |
| T-49 | Draw courtyards for **U4** and **SW1** (none exist), then set `missing_courtyard` back to `warning` or `error` and re-run DRC — expect the two to clear and any real overlap to appear | check C5, D3 | HW | S |
| T-50 | Centre the 13 tracks that end off their via (`track_not_centered_on_via`), then restore that check's severity | check C5 | HW | S |
| T-51 | Make `revC\pack.ps1` stage `MoriShield_Carrier.kicad_dru` and `MoriShield_Carrier.pretty`, and add a staleness gate for the BOM and placement files the way it already has one for ERC/DRC | checks C1, C4, C6, D3 | DOC | S |
| T-52 | Regenerate BOM, placement files, `vias_in_pads.txt` and `FAB_NOTES.md` after the design next settles; all four predate the current board save | checks C6, C12 | DOC | S |
| T-53 | **Converter decision.** The XL4015 5 A module with LED voltmeter is audited and rejected (No-Go). Put question 8a to Serigreen — hold condition 1's "40 V or more" and supply the part, or sign the deviation — and open the LM2596HVS module in hand to read the die marking (`LM2596` vs `LM2596HV`) plus its input capacitor rating and temperature grade. Until that marking is photographed, the incumbent's own 50 V claim is unbacked | B1, B2, B8, B10, condition 1, gate C7 | DOC+HW | S |
| T-54 | Write the **off-board converter chain into the assembly note, not into the board**: the module's own input fuse and the SMBJ/SMCJ24A surge part in the lead (neither is on either module), the lead gauge that keeps condition 5's 15 mΩ, the output set to 5.15 V against a 4½-digit meter, the pot locked, the heatsink and air gap, and the rule that the module's meter display is not evidence of the set point | B1, B3, B5, condition 1, condition 5, gate C8 | DOC | S |
| T-55 | **DONE 2026-11-04.** E22 M0/M1 strapped to GND through 0 ohm R56/R57 (0603) at J6.6/J6.7; `/E22_M0` and `/E22_M1` deleted as nets; J1.16/J1.17 set to `unconnected-(J1-IO10-Pad16)`/`unconnected-(J1-IO11-Pad17)`. ERC 0, DRC 0/0/0 | A7, C2, C5, R11, C11 | DEV | M |
| T-56 | **DONE 2026-11-04.** `/REED_PULSE_F` moved from J2.7 (GPIO41) to J2.9 (GPIO39); no-connect on J2.7 at the pin, not at the old label x. ERC 0, DRC 0/0/0 | R11, C11, C4 | DEV | S |
| T-57 | **Label the ports where a builder will see them**: name every port in the schematic Value field, copy the port names onto F.SilkS at 1.0 mm / 0.15 mm stroke, and mark J6 with its pin functions and its orientation. Do not invent names for J17 and J20 | E5, C12, A3, C11 | DEV | M |
| T-59 | **DONE 2026-11-15.** Place the 13 decoupling capacitors that cannot be moved (Task C, 2026-11-03). All 13 capacitors (C52–C64) placed in schematic and routed in PCB with legal copper widths, net bindings, and clean clearances. DRC 0/0/0, ERC 0/0 | C9, B12 | HW+DOC | M |
| | pin | net | value | footprint | where it should sit | | |
|---|---|---|---|---|---|---|---|
| | J1.1 | 3V3_C | 100 nF | C_0805_2012Metric | (210.50, 157.75) rot 0 | | |
| | J4.3 | 3V3_C | 100 nF | C_0805_2012Metric | (273.50, 117.39) rot 0 | | |
| | J7.2 | 3V3_C | 100 nF | C_0805_2012Metric | (215.65, 163.00) rot 0 | | |
| | J7.8 | 3V3_C | 100 nF | C_0805_2012Metric | (229.14, 169.00) rot 0 | | |
| | J8.5 | 3V3_C | 100 nF | C_0805_2012Metric | (166.06, 157.25) rot 90 | | |
| | J26.1 | 3V3_C | 100 nF | C_0805_2012Metric | (129.75, 152.50) rot 90 | | |
| | J11.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (171.75, 195.00) rot 90 | | |
| | J12.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (187.75, 193.50) rot 90 | | |
| | J15.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (146.13, 193.50) rot 90 | | |
| | J16.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (163.94, 189.50) rot 90 | | |
| | J17.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (266.75, 194.25) rot 90 | | |
| | J24.1 | +5V | 100 nF | C_0805_2012Metric | (138.97, 147.25) rot 0 | | |
| | D7.1 | /+5V_ESP | 100 nF | C_0805_2012Metric | (215.60, 97.50) rot 90 | | |
| | | | | | | | |
| | **Note** | the five rot-90 spots need a rotated 0805; rotating an existing footprint raises `lib_footprint_mismatch`, so these must be added as new parts, not by turning an existing one. Every spot is legal at the moment of measurement and was checked for copper clearance, hole-to-hole, courtyards and module outlines. | | | | | | |
| | **Bulk half** | for every 3V3_C pin the missing part is the **10 uF bulk**, not the 100 nF: the rail has none. For the /3V3_SENS_SW ports the 100 nF site is the blocker and C51 is the only 10 uF on the net. Both are recorded in `revC\decoupling_map.csv` under `verdict_reason` | | | | |
| | **Also open** | 20 further pins have **no legal spot at all** inside the CTO's radius (6 IC pins at 3 mm, 14 others at 5 mm); they are listed in `revC\FAB_NOTES.md` and in the Task C report | | | | | |
| T-58 | **Ask for a keyed or shrouded header at J6** (and J3/J4) as a costed option. Silk makes a reversed insertion obvious; only a key makes it impossible | A3, R16 | DOC | S |

---

## Part 6 — Found, not asked for

These are real findings with no register row. Each is stated with the evidence that proves it.

1. **67 vias inside SMD pads** (65 in Rev B; two appeared in the 2026-11-03 reroutes). The item is
   unaddressed rather than partly done. Invisible to DRC: KiCad does not flag via-in-pad by
   default, which is why it survived a clean DRC run. Positions in `revC\vias_in_pads.txt`;
   re-counted 2026-11-03 at 67 of 315. The recommended fix is one fab note – plug, fill and cap per
   IPC-4761 Class B or C – not 67 routing changes, and it needs Serigreen’s written agreement
   and a price.
2. **The `3V3_C` net-class anomaly, diagnosed.** `3V3_C` is bound to class `3V3` by the
   pattern `3V3_C` → `3V3`. The class's own `track_width` is 0.20 mm, but that is a routing
   default, never a DRC minimum. The floor actually in force is the custom rule
   `"3V3 class floor"` in `MoriShield_Carrier.kicad_dru`, **min 0.30 mm**. That is why the
   count stayed at 13 when the class value was changed from 0.50 to 0.20: the DRC never read
   the class value. The 13 flagged tracks are 10 at 0.200 mm (In2.Cu) and 3 at 0.250 mm
   (F.Cu/B.Cu); the 24 tracks at 0.300 mm pass exactly at the floor. The fix is to widen the
   13 tracks to 0.30 mm, not to lower a number.
3. **`3V3_C` is double-driven.** It connects to J1 pins 1 and 2, which the Edgehax board
   documents as 3.3 V regulated **outputs**, while the carrier's TPS7A2033 also drives the same
   net. Two regulators tied together. Verified in the pad-net dump: `J1.1 = 3V3_C`,
   `J1.2 = 3V3_C`.
4. **`/EVENT_BTN` is on GPIO3**, a strapping pin, loaded by a button and its RC. CHK-001 C11
   says GPIO0, GPIO3, GPIO45 and GPIO46 must not be loaded at reset. Verified: `J1.13 =
   /EVENT_BTN`; J1 pin 13 is IO3 in the header order.
5. **The modem sockets are unkeyed and asymmetric.** J3 and J4 are both 1×12 sockets, the GND
   pins are not in the same positions on the two rows, and nothing prevents a reversed
   insertion. Silk `1` marks at each socket's pin 1 and the note `MODEM THIS WAY UP` were added
   this revision; there is still no mechanical key.
6. **SIM socket side is not proven.** The Parry guide lists J8 (SIM) as "Back of PCB"; the
   module mounts components-down, so the SIM should face up. That is a reading of one vendor
   line and one photo, not a measurement on the unit in hand. It matters because a SIM that
   faces the carrier cannot be changed once the board is installed.
7. **Nine suppressed checks — found and fixed 2026-11-01.** All nine are re-enabled and nothing
   is set to `ignore`. What they hid: `missing_courtyard` 2 (U4 and SW1 had no courtyard at all),
   `track_not_centered_on_via` 13. Both classes were fixed rather than re-suppressed; the other
   seven report zero items on this board.
8. **The release layout's symbol library is stale.** `morishield\morishield_hardware\libraries\
   MoriShield_Carrier.kicad_sym` is 153,623 bytes against the project's 157,936; pointing
   `sym-lib-table` at it re-introduces the library-symbol mismatch class. The release layout
   (`morishield\morishield_hardware\4L\`) uses `../libraries/` for both tables, so shipping that
   structure as it stands would hand Serigreen a schematic whose symbols do not match.
9. **`fp-lib-table` originally pointed at a path that does not exist.**
   `${KIPRJMOD}/../../MORISHIELD/source/MoriShield_Carrier.pretty` was in both `4L\` and
   `pcb\`. It is fixed for `pcb\` (now `../morishield/morishield_hardware/libraries/…`) and for
   the `pcb` symbol table, but **not** for the release layout, which still resolves through
   `../libraries/`.
10. **The 124 silk items involve 48 parts, not 25.** The earlier estimate named U7 (26),
    U8 (25) and C31 (18) as 69 of the 124; today's per-part tally is U7 27, U8 25, **C4 22**,
    C31 22, then a long tail. Fixing U7, U8, C4 and C31 is 96 of the 124.
11. **The `/+5V_SENS` rail is the most significant unreported electrical defect.** It was
    distributed on 0.20 mm inner-layer copper at about 313 mΩ in series, feeding eight sensor
    ports including a heated SPS30. It is now **156.6 mΩ**: every segment meets the 0.80 mm
    class floor except 12 that the corridors cap at 0.60 mm, of which the 55.4 mm In2 run along
    the J7 pad row accounts for 93.2 mΩ. At 0.80 mm that run breaks J7's pad clearance by
    0.05 mm and the band below it is occupied by 3V3_C, U6 and Q4 copper.
12. **The Pin-1 marks and the serial box were added without a register row.** They serve
    C12/E5 but were not asked for item by item; they are declared in `REPLY_TO_CTO.md`.
13. **The `3V3_C` class value in `.kicad_pro` was lowered from 0.50 to 0.20 mm** with a written
    justification (the net carries under 50 mA). It has no DRC effect (see finding 2) and is
    declared as an unrequested change.
14. **`min_text_thickness` is 0.08 mm**, which is our own number, not the fab's. "Text thickness
    passes" therefore means "passes a rule we invented". The silk rule the CTO states is
    0.15 mm stroke and 1.0 mm height; the board's own texts meet that, the check does not.

15. **The ground plane fails its own stitching acceptance, and this was reported as closed.**
    Measured on the filled In1 plane at a 1 mm grid: 87 ground links, but **37.4 % of the plane
    is more than 10 mm from one and the farthest point is 25.9 mm**. E1's acceptance is "no
    point of either ground pour more than 10 mm from a ground link". The previous status,
    "closed on design, plot owed", is withdrawn. This is a layout finding, not a paperwork one.
16. **PE-to-other-net clearance is 0.30 mm, not the 0.5 mm R9 asks for.** The PE net class
    carries `clearance 0.3`; R9 says "PE copper 0.5 mm or more from other nets except at the
    protection parts' pins". The board has 0 PE clearance errors because the rule in force is
    0.3. Raising it to 0.5 is a reroute, not a rule change: the two narrow PE runs are already
    at the physical maximum of their corridors (1.00 mm gap between pad rows minus 2 × 0.30).
17. **`/PWR_EN` carries a dead spur to U8 pin 16 that DRC exposes one segment at a time.**
    Removing the pad from the net leaves a chain of orphaned segments: chasing it consumed 17
    segments over 16 DRC passes without reaching the end, while unconnected stayed 0 — the
    route itself is intact and the spur is a parallel branch. The attempt was reverted from the
    snapshot and the single-driver fix is left for the GUI, where the branch can be seen and
    deleted in one operation. This is why R7's second driver is still present.
    
18. **Two footprints had no courtyard — found and fixed 2026-11-01.** `U4` (SOT-23-5) and `SW1`
    (6 × 6 tact switch) were drawn with no courtyard on either side, so no spacing rule could see
    them. Courtyards were added to the board **and** to the library footprints (`SOT-23-5_HS`,
    `SW_6x6`) at the land extent plus 0.25 mm: U4 x ±2.70, y ±1.50; SW1 x ±4.25, y ±3.25. With
    `missing_courtyard` enabled, both clear and **no courtyard overlaps a neighbour**.
    Evidence: `revC\_work\_drc_b12.json` (13 items) → `revC\drc_RevC.json` (0).
19. **The release layout's symbol library was stale — found and fixed 2026-11-01.** ERC against
    the project's own `pcb\MoriShield_Carrier.kicad_sym` (157,936 B) gave 0 violations; against
    `morishield\morishield_hardware\libraries\MoriShield_Carrier.kicad_sym` (153,623 B) it gave
    **336 `lib_symbol_issues`**. That copy was refreshed to 157,936 B and `pack.ps1` now stages it.
    Measured after the fix: **0 / 0**. Evidence: `revC\_work\scratch\libtest_before|after`.
20. **`fp-lib-table` resolved only inside this folder layout — found and fixed 2026-11-01.** The
    project footprint library was reached through `${KIPRJMOD}/../morishield/...`, so anywhere else
    ERC reported **124 `footprint_link_issues`**. `pack.ps1` now stages the `.pretty` inside
    `project\libraries\` and rewrites both tables to `${KIPRJMOD}/libraries/...` in forward
    slashes. Measured after the fix: **0**. Evidence: `revC\pack.ps1`, `revC\_work\scratch\`.
21. **The package cannot be built today, and four production files describe an older board.**
    `revC\ResponseSheet_RevC.csv` — the file CHK §7 requires to be first in the zip — does not
    exist, so `pack.ps1` throws at its own gate. Separately, the BOM, both placement files,
    `FAB_NOTES.md` and `vias_in_pads.txt` were generated 16:54–17:14 while the board was saved at
    17:49:53, and U10's pad net and 40-odd silkscreen texts changed in that hour. C6 and C12 both
    require these files to match the board, so they must be regenerated after the design settles.
    `pos_back.csv` being empty is correct and not a fault: the board has no footprint and no SMD
    pad on B.Cu.

22. **The XL4015 module's advertised input range is wider than the silicon's specified range, and
    internally impossible.** Robu states 4 V–38 V input and 1.25–36 V output. The XLSEMI data sheet
    (Rev 2.0) gives **8–36 V recommended operating** and −0.3 to **40 V absolute maximum**, with the
    output adjustable to **32 V**, not 36 V. A buck cannot make 5.15 V from 4 V — at 100 % duty and
    0.3 V dropout its ceiling at 4 V input is 3.7 V — so the vendor's floor is not a working figure
    either. The XL4016 (Rev 1.6) has the same 8–36 V operating range and the same 40 V absolute
    maximum, so the "better than 2596" claim is true about current and heat (7 A and 14 A limits,
    40–60 mΩ MOSFET) and false about voltage. **No condition-1 rating may be quoted from the vendor
    page; only from the IC data sheet.** Evidence: `_cto_extract\XL4015_datasheet.txt`,
    `_cto_extract\XL4016_datasheet.txt`, `buck`.

23. **The register contradicted itself about the 40 V clause, and the incumbent's own claim is
    unverified.** B1 said the LM2596HVS does *not* cover the 40 V clause while Part 4 said the
    clause is exceeded (50 V). Both numbers come from different levels of the same product: the
    module's marketing says 4.5–50 V, TI's LM2596 data sheet says **4.5–40 V operating with a 45 V
    absolute maximum**, and the *HV* second-source die (UMW/UTD) says **4.75–60 V with a 63 V
    absolute maximum**. A "HVS" module carrying a plain LM2596 would therefore be sold with a 50 V
    claim above the silicon's rating, and the whole converter argument rests on which die is inside.
    Reading the marking on the module in hand is now a named step (T-53), not a footnote.
    Evidence: `_cto_extract\LM2596_datasheet.txt`, `_cto_extract\LM2596HV_umw_datasheet.txt`.

24. **A 5 A module worsens the fault coordination the review already flagged (R5, B3).** F1 is a
    4 A-hold device needing roughly 8 A to trip, and the input copper is 1.5 mm. The XL4015's switch
    current limit is 7 A typical against the LM2596's 3.6 min / 4.5 typ / 6.9 max A, so with the
    XL4015 a short-circuit can sit between the fuse's hold current and its trip current while the
    converter holds it. Interpolating the review's own Table 6 puts 1.5 mm at about +20 K at 4 A, and
    heating scales near I², so **7 A is about +60 K on that track inside a +70 °C box.** The fix is
    not a lower-current converter: it is condition 2's cut-off with a limit near 3.5 A (T-19) plus
    condition 3's pour (T-06), and an F1 that matches its footprint (B3).

25. **Neither candidate carries the parts condition 1 assigns to it.** Condition 1 asks the
    converter for "its own input fuse and surge part (B1, B3)"; the XL4015 and LM2596 modules as
    sold have neither, and the XL4015-with-voltmeter variant additionally puts a **−10 to +65 °C
    LED display** (a 5–20 mA permanent load, and 0.1 V resolution — three times the ±52 mV window
    the ±1 % clause needs) in a box the design takes to +70 °C. That burden belongs in the assembly
    note beside the board, which does not exist yet (T-54). Evidence:
    `revC\BUCK_AUDIT_XL4015_20261101.md` §2.5, §3, §6.

26. **The E22 antenna keep-out area is crossed by two B.Cu tracks — found 2026-11-02.** The area the brief
    specifies (x 296.00-304.57, y 163.00-177.00) contains no track endpoints, via or pad, but two long
    B.Cu segments pass through it: `/3V3_SENS_SW` (37.05 mm) and `/I2C0_SDA_CH3` (46.00 mm). A rule area
    with tracks, vias, pads and fill excluded therefore reports **2 `items_not_allowed` and 1 unconnected**.
    It was drawn, measured and removed rather than left in the file. E3 cannot close until those two runs
    are moved. Evidence: `revC\_work\_r5_drc5.json`.

27. **SUPERSEDED - J6 is NOT mis-wired.** This finding was first written as "the J6 rewire is a reroute, not a net rename" — measured 2026-11-02.** Applying the correct mapping to
    the pads and labels kept parity at 0, which proves the netlist change is right, but produced **24 DRC
    violations and 3 unconnected items** because every track still ends on the pad it was drawn to. Seven
    nets must swap positions in a vertical row, so they cross unless routed on two layers. Reverted.

28. **Two of the five module outlines were on the wrong sockets, measured 2026-11-01.** The `GY-521` label
    sat on J8 (the RTC socket) and `DS3231 RTC` on J7 (the IMU socket). Corrected, and the envelopes resized
    to the measured 21x16 and 38x22. The E22 outline was 43.5 x 22.5 mm against a 37 x 22 mm module and is
    now 37 x 22; the ESP32 32 x 68 is now 32 x 65; the modem 49 x 60 is now 43 x 60.

29. **The J6 pin-1 confirmation now exists - closed 2026-11-02.** It did not exist when - 2026-11-02.** The run was gated on Aswin confirming that
    the E22 module's physical pin-1 mark matches the datasheet (pin 1 = M0). A search of every document, register and note
    modified in the last 24 hours found no such record. **The J6 correction was therefore not attempted**, and the socket
    remains as designed. **This finding is superseded by finding 32: J6 is NOT mis-wired** - it is numbered for a 180-degree insertion and all seven nets line up that way. What was blocked was the physical pin-1 confirmation, which Aswin gave on 2026-11-02.

30. **The E22 keep-out needs more than one track move - measured 2026-11-02.** The `/3V3_SENS_SW` B.Cu run at x 298.75
    (37.05 mm) was dogtailed to x 293.0 with the via at (298.75, 147.50) kept as the tap. DRC returned **5 items**: three
    `tracks_crossing` and `shorting_items` against `/I2C0_SDA_CH3` and `/I2C0_SDA_CH6`, which occupy that B.Cu corridor.
    Restored. Clearing the area needs those two runs moved as well.

31. **The decoupling map was measuring one requirement, not two.** CHK C9 asks for a 100 nF within 5 mm (3 mm at an IC pin)
    **and** bulk of 10 uF or more within 10 mm. The old map tested only "nearest capacitor of any value", which is why its
    count read 27. Rebuilt with both tests and a class per row: **36 supply pins, 0 meet both, 36 fail local, 31 fail bulk.**

---

32. **The LoRa socket is numbered for a 180-degree insertion, and nothing says so.**
    Found 2026-11-02, and it cost a day. Read against the Ebyte datasheet order
    (1 M0, 2 M1, 3 RXD, 4 TXD, 5 AUX, 6 VCC, 7 GND) with the module inserted the
    obvious way, J6 appeared reversed - VCC on GPIO10, GND on GPIO11, 5 V on M1.
    Inserted the other way round, **all seven nets line up**, including UART
    direction, and it matches Aswin's working bench wiring exactly. The net names
    themselves (`/E22_M0` on pad 7, `/E22_M1` on pad 6) prove the designer intended
    it. The real defect is that **no silk marks the orientation, the footprint pads
    are named only 1 to 7, and the header is unkeyed** - so the wrong way is both
    possible and invisible. Item A3's acceptance is "a reversed module cannot go in
    or is obvious"; today it does neither. Evidence: `pcb\MoriShield_Carrier.kicad_pcb`
    J6 pad nets; Ebyte E22-900T22D manual section 3; Aswin's continuity test on the
    module's GND pin against the SMA shell.

33. **The capacitance sensor is an FDC1004 on J21, which is I2C channel 5 - and J15
    is a separate analog soil input.** The schematic gives J21 the value `FDC1004`;
    J21 carries `/I2C0_SDA_CH5` and `/I2C0_SCL_CH5`. J15 is a 3-pin port carrying
    `/SOIL_ADC_RAW` through R29 and C34 into **GPIO2 = ADC1_CH1**. Both analog inputs
    (J15 on GPIO2, J16 on GPIO1) land on **ADC1**, which is the ADC that keeps working
    with Wi-Fi on - ADC2 (GPIO11-20) does not. That was luck, not a decision, and it is
    worth recording because it constrains any future pin swap. Consequence for the
    keep-out work: **CH5 is not spare**, it is the FDC1004.

34. **Port names are drawn on layers that never print.** Only nine board-level
    silkscreen items exist on F.SilkS: `5v +`, `5v -`, `MoriShield Carrier`, `Rev C`,
    `S/N`, two `1` pin-1 marks, `MODEM THIS WAY UP` and `Q1 buzzer`. Every port name
    (`J15 SOIL`, `J11 SGP41 0x59`, `J12 SHT45 0x44`, `J14 BME688 0x76`, `J13 SPS30 5V`,
    `GY-521`, `DS3231 RTC`, `J5 MODEM 5V`, `J18 +5V IN`) is on **F.Fab**, which is not
    in the Gerber set. A builder therefore sees no port labels at all. In the schematic
    the naming is inconsistent: J21 `FDC1004`, J23 `EXT_BTN`, J24 `PANEL_LED_5V` and
    J25 `BUZZER_5V` are named, while J7, J8, J11, J12, J13, J14, J15, J16, J17, J20,
    J21, J22 and J26 are generic `JST_XH_n` / `Sock_1xnn` values. Items E5 and C12 and
    the CTO's repeated complaint about labels all point here. Evidence: layer-by-layer
    text dump, 2026-11-02.

35. **Part 6 of this register had duplicate finding numbers.** The 2026-11-02 run
    appended its own set without checking the existing numbers, so 22 to 27 each
    appeared twice. Fixed by renumbering every finding in file order. The lesson is
    recorded because a register that cites "finding 23" is ambiguous until it is not.

36. **J17 and J20 have no identified purpose anywhere in the workspace.** Both are
    wired 4-pin I2C channel ports (CH4 and CH6) with ESD arrays, pull-ups and full
    copper. J20 is one of the two runs blocking the LoRa antenna keep-out. Nothing in
    the schematic, the board, the CTO documents or the notes says what sensor goes
    there. Asking Aswin - see `REPLY_TO_CTO.md` question 10.


37. **A rotated 0805 footprint raises `lib_footprint_mismatch`.** Found 2026-11-03 while moving the decoupling
    capacitors: every cap that was turned from rot 0 to rot 90 produced one `lib_footprint_mismatch` warning,
    while the cap already at rot 90 (C43) and the one left at rot 0 (C14) did not. The library copy is the
    reference, so a placed footprint may not be rotated without editing the library too. Consequence: the Task C
    relocations were done at the parts' original rotation, and the five port-row ADD spots that only work at
    rot 90 are handed to Aswin as new parts (T-59).

38. **The decoupling map's bulk test was reading 1 uF as bulk, and "100nF/16V" as 10 uF.** The map's threshold
    was `>= 1 uF`, not the CTO's `10 uF or more`; and the value parser concatenated the voltage digits, so
    `100nF/16V` parsed as 10016 nF = 10.0 uF and counted as bulk. Re-measured with a proper parser and the
    verbatim thresholds the board reads **1 pin meeting both, 3 local, 3 bulk, 33 fail local, 33 fail bulk** -
    not the 31-fail-bulk figure the register carried. The old figure understated the bulk failures.

39. **A 4-pin JST-XH does not fit anywhere on the bottom port row.** Measured 2026-11-03: 347 positions along
    y = 194.5, none legal. The row's courtyards leave 6.6-7.8 mm between ports and the part's courtyard is
    13.49 mm wide; the one 35 mm gap (x 200.4-235.5) is crossed by the /I2C0_SCL_CH0 diagonal at x 218, has two
    GND stitching vias at 207.43 and 219.43, and sits under the GY-521 outline (bottom 192.05). J26 therefore
    went to the left-edge pocket at (134.0, 153.5), 0.36 mm below J24's courtyard and 0.38 mm above R7's.

40. **The +5V 100 nF bank sat in one corner.** C3, C14, C41 and C42 were all inside 16 mm of (282-297, 95),
    while every +5V load pin is 40-160 mm away - the "four 5 V 100 nF still sit together in a corner" finding in
    B12, now measured. Three of the four were relocated onto Q9.3, D2.1 and J24.1; the fourth (C3) has no legal
    spot within 5 mm of any remaining +5V pin.


41. **E1 regressed and nobody noticed, because the metric is not part of DRC.**
    The stitching acceptance is a separate measurement, so a copper change that
    passes DRC 0 can silently break it. Re-measured after the placement work:
    144 links, worst **11.16 mm**, **0.1 %** beyond 10 mm. E1 was recorded as Done
    in all four documents. Standing rule: re-run `pcb\_plot_stitching_final.py`
    after any copper or via change, before any document repeats the old number.
42. **Vias inside SMD pads went 65 to 67.** Two more were introduced by the
    2026-11-03 reroutes. `revC\vias_in_pads.txt` and the fab note in
    `revC\FAB_NOTES.md` were both regenerated from the saved file on 2026-11-03 and
    now read 67 of 315, so check C5's evidence matches the board again. Task 1 added
    two GND stitching vias, which is why the denominator moved from 314 to 315.
    goes anywhere.
43. **The 3.3 V rail has no bulk capacitor at all, which is why no 3V3_C pin can pass C9.** Measured
    2026-11-03: every capacitor on 3V3_C is 100 nF (C4, C7, C8, C9, C10, C30, C36); the nearest 10 uF or
    larger on any other rail is C51 on /3V3_SENS_SW. Ten of the 36 supply pins are on 3V3_C, so ten of them
    can never meet "bulk 10 uF or more within 10 mm" by moving an existing part - a 10 uF has to be added.
    The same is true, one net at a time, for /3V3_SENS_SW: it has exactly one 10 uF (C51 at 186, 173), which
    already serves Q2.3 at 5.83 mm, so moving it to a port would trade one bulk pass for another.

44. **E1 was restored by two vias, not by a reroute.** The two over-10 mm clusters were x 276-279 / y 88-92
    (12 cells, worst 11.16 mm at (277, 90)) and one cell at (169, 180) at 10.07 mm. Both were the footprint
    of the 2026-11-03 work: the four +5V 100 nF capacitors left the top-right corner and took their GND vias
    with them, and the J26 reroute removed a GND link near (169, 180). Two 0.6/0.3 mm GND vias at (277, 90)
    and (164, 186) - both inside both pours - returned the metric to 146 links / 10.00 mm / 0.0 %.

45. **A KiCad local label named X produces the net `/X`, and a board net without the leading slash
    raises `net_conflict` on the label side only.** Found 2026-11-04 while finishing T-55: the board had
    `E22_M1_STRAP`, the schematic's local label produced `/E22_M1_STRAP`, and DRC reported four
    `net_conflict` items - exactly the strap-side pins (J6.6, J6.7, R56.1, R57.1) and none of the GND pins.
    Renaming the board nets to carry the slash cleared all four on the first run. The tell is that only one
    side of a two-pin part conflicts; a pin-order error would conflict on both. Every other label net on this
    board already carries the slash (`/E22_AUX`, `/UART1_LORA_TX`, `/REED_PULSE_F`).

46. **A pcbnew Save re-issues every UUID and merges collinear or corner segments, so a segment count can fall
    with no copper lost.** Found 2026-11-04: the census read 1178 segments before a save and 1166 after, with
    no edit in between, and a UUID diff showed 139 gone / 127 new - i.e. the survivors were renumbered.
    Total copper length proved nothing was lost: 5306.342 mm -> 5306.609 mm (+0.266 mm, the chord shortening
    of merged corners). The guard is now a rule: re-run DRC immediately before text surgery to get current
    UUIDs, and record **total copper length** at every checkpoint alongside the counts.

## Part 7 — Verification of this document

Run after every edit to this file. The verifier parses Part 1 only, so that the C1–C13 ids in
Part 2 are not counted as register rows.

```
python pcb\_verify_tracker.py
```

Expected output:

```
Part 1 rows: 76
A: 12  B: 12  C: 13  D: 3  E: 7  F: 2  G: 4  H: 6  R: 17
duplicates: none
missing: none
extra: none
status tally: {'Open': 35, 'Partly': 25, 'New': 7, 'Done': 5, 'Paper': 3, 'Superseded': 1}
```