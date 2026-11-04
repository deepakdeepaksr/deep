# Reply to Serigreen — MoriShield Carrier, Rev C

| | |
|---|---|
| **Package** | `MoriShield_Carrier_RevC_<date>.zip` (not yet built) |
| **Revision** | Rev C (internal v3, 4-layer board only) |
| **Date** | 2026-11-01 |
| **Author** | Aswin, firmware and software |
| **Single contact and signatory** | Aswin |
| **Answers** | MS-CAR-REV-A-004 v1.0 (the 59 items), MS-CAR-REV-B-001 v1.0 (R1–R17, the six conditions), MS-CAR-CHK-001 v1.0 (the checks) |
| **Board** | `pcb\MoriShield_Carrier.kicad_pcb`, 178.15 × 118.15 mm, 4 copper layers, 159 footprints |

## What this document is

One row per item from 004 Table 9 and 001 Table 13, in the review's order, with what changed,
where, and the evidence. Then the answers we hold, the questions we still need answered, every
change nobody asked for, and the assumptions the design rests on.

**What this package is not.** It is not a release request, and it makes no claim that the board
is fit to fabricate. The release gate is not met: see the status column, which is written from
what the files show. Release is Serigreen's, in writing, naming the exact files by checksum.

**Two namespaces, to avoid confusion.** `A1`–`H6` are items from 004 Table 9. `R1`–`R17` are the
new items from Rev B Table 13. Elsewhere in our documents `C1`–`C13` also names the checks in
MS-CAR-CHK-001 §4, which are a different set; where this file cites a check (for example in §5)
it says "check C5" or "check C12".

---

## 1. Response sheet — the 59 items (004 Table 9)

Status words used here are the response-sheet vocabulary of MS-CAR-CHK-001 §7:
**Done** · **Partly** (what is missing is named) · **Deferred** (only with Serigreen's message
and date, which we do not yet hold) · **Rejected** (reason) · **Agreed before drawing** ·
**Superseded**. One word is added because that vocabulary has no "not started" term:
**Open — answer requested** means nothing has been done and a question is attached.

Our internal register in `TASK_TRACKER.md` uses six words. The mapping is declared here so that
nothing is silently upgraded or downgraded:

| Register word | Meaning in the register | Status written here |
|---|---|---|
| Done | designed in and evidenced | **Done** |
| Paper | design complete, bench or measurement result owed | **Partly** (bench result owed) |
| Partly | some of it is in the files | **Partly** |
| New | regressed or newly understood, nothing in place | **Open — answer requested** |
| Open | not started, or started and reverted | **Open — answer requested** |
| Superseded | the design change removed the item | **Superseded** |

The same table governs §2.

| Item | What changed and where | Evidence | Status |
|---|---|---|---|
| A1 | No change to the sockets this round. Row spacing still unmeasured with calipers; `/E22_M1` and `/E22_M0` sit on J1 pins 16 and 17 (GPIO10/11) and are the subject of question 3 | `TASK_TRACKER.md` A1; pad-net dump | Open — answer requested |
| A2 | Modem rows level at y 113.56 and drawn components-down; the 35.56 mm note is gone. Truth table and supply proof not done | `MODEM_CONNECTOR_PLACEMENT_REVIEW.md` §2–§5 | Partly — needs the readings, the truth table and the B10 proof |
| A3 | `1` marks at J3 pin 1 and J4 pin 1 and the note `MODEM THIS WAY UP` added on F.SilkS; module names still on F.Fab and Dwgs.User, which are not printed; sockets unkeyed | F.SilkS texts at (232.2,113.56), (272.4,113.56), (240,108.6) | Partly — needs printed module names and a mechanical key |
| A4 | Five module outlines drawn on Dwgs.User and F.Fab; no heights; no enclosure in the 3D; two outlines are on the wrong sockets (R14) | `revC\render_top.png`, `revC\render_iso.png` | Partly — needs heights, the right sockets, and the box in the 3D |
| A5 | No GPIO map in the package | — | Open — answer requested |
| A6 | Module identified from the shield marking as ESP32-S3-WROOM-1 **N16R8**, octal PSRAM, GPIO35–37 unavailable on the header. No net uses those pins. The written ECC decision is owed | `INPUT_REGISTER` (archived) §Q.1 C24; pad nets | Partly — needs the decision recorded in writing |
| A7 | **Closed 2026-11-04.** `/E22_M0` and `/E22_M1` are gone as nets; J1.16 and J1.17 are `unconnected-(J1-IO10-Pad16)` and `unconnected-(J1-IO11-Pad17)`; M0/M1 are strapped to GND through 0 ohm R56/R57 at J6.6/J6.7, so GPIO10 and GPIO11 are free for the microSD | pad nets read back from the saved file; `revC\drc_RevC.json` | Done |
| A8 | J1/J2 both at y 154.00; J3/J4 both at y 113.56. Re-verified this round | `pcbnew` footprint positions | Done |
| A9 | Components-down and pin-mapped against the Parry datasheet, 24/24 pads; the side-on photo is still missing | `MODEM_CONNECTOR_PLACEMENT_REVIEW.md` §3–§4 | Partly — needs the photo |
| A10 | No readings, no 1:1 test-fit. 26.00 mm against an estimate of 26.2; 34.00 against 33.8 | — | Open — answer requested |
| A11 | `/MODEM_RST` wired from J1 pin 6 (GPIO6) to J4 pin 8; PWR_EN still has two drivers; no truth table | pad nets; `pcb\work done` milestone 4 §6 | Partly — needs one driver and the truth table |
| A12 | J5 moved outside the modem outline; no standoffs; the ESP32 board is not clamped | `pcbnew` positions | Partly |
| B1 | The 12 V input is off-board, so the TVS requirement moves into the converter input specification. **We audited the XL4015 5 A module you pointed us at (XLSEMI Rev 2.0) and rejected it: 8–36 V operating input, 40 V absolute maximum, so "input rated 40 V or more" is not met.** B1's own worked example decides it — an SMBJ/SMCJ24A stands off 24 V, breaks down at 26.7 V minimum and clamps at 38.9 V, which is above the XL4015's 36 V ceiling; and no 600 W/1500 W TVS that stays off at the 22–25 V disconnect clamps under 36 V, because clamp/standoff is 1.5–1.6 for this family. The incumbent LM2596HVS passes the same arithmetic (module 4.5–50 V; the TI die is 40 V operating/45 V absolute, an LM2596HV die is 60 V/63 V) | `revC\BUCK_AUDIT_XL4015_20261101.md` §2, `_cto_extract\XL4015_datasheet.txt`, `_cto_extract\SMBJ_series.txt` | Partly — clamp table now written; the die marking in the module we hold is unverified, and the named part still needs your signature (question 8a) |
| B2 | Input floor and range: 9 V is inside both candidates (XL4015 8 V, LM2596 4.5 V) up to the B8 maximum. Thermal at 3 A: the XL4015's MOSFET switch is the better die (≈0.4 W, RθJA 30 °C/W → **Tj ≈ 82 °C in +70 °C air**) against the LM2596's bipolar switch at VSAT 1.16 V typ (**≈130 °C — over its 125 °C operating limit, which is why we quote ≈2 A for it**). But the XL4015 module as sold fails the clause around its die: its LED voltmeter is rated −10 to **+65 °C**, its electrolytics are 85 °C stock where B3 asks for 105 °C long-life, and 3 W of module loss in an unventilated 2.5 L box is worth roughly 25 K. Neither module can claim the 5.15 V ±1 % as a rating (XL4015 reference ±2 %, module regulation ±2.5 %; LM2596 reference ±3–4 %), and neither can claim the 50 mV droop without the bench step test | `revC\BUCK_AUDIT_XL4015_20261101.md` §2.3, §3 | Partly — XL4015 rejected; the 3 A at +70 °C deviation on the incumbent still needs your agreement (question 8) |
| B3 | F1 is a 4 A PTC on glass-fuse clips; C13 carries a ceramic value on an electrolytic footprint; the BOM has no ratings | `revC\MoriShield_Carrier_RevC_bom.csv` | Open — answer requested |
| B4 | Both input legs widened to 1.5 mm (≈13 mΩ). The 3 mm pour of condition 3 is not met. `/+5V_SENS` now meets the 0.80 mm class floor except 12 segments capped at 0.60 mm, taking it from 313 mΩ to **156.6 mΩ** | `revC\EVIDENCE_RevC.md` §7 | Partly |
| B5 | No per-mode power budget | — | Open — answer requested |
| B6 | No USB service rule and no README section | `README.MD` is a product description only | Open — answer requested |
| B7 | C26 and C27 moved to 2.1 and 2.4 mm from U6 pins 1 and 5. The scope capture is owed | C26/C27 positions | Partly — bench result owed |
| B8 | Both candidates survive 22–25 V at the input in steady state. The XL4015's problem is the surge case: its 40 V absolute maximum sits under the only clamp level that can hold off at 25 V, so a surge event destroys rather than survives it. The board's own over-voltage cut-off is still not designed — **all six U10 pads carry local unconnected names, re-verified from the board file today** (`pcb\_evidence\power_chain_pads.json`) | `revC\BUCK_AUDIT_XL4015_20261101.md` §2.2, §4; `pcb` U10 | Partly |
| B9 | **Regressed.** The planned sense pin GPIO6 is now `/MODEM_RST`. Every ADC1 channel on the headers is allocated | pad nets | Open — answer requested (question 6) |
| B10 | Six conditions partly met on numbers; the board budget is feasible at ≈40 mΩ; no model, no trace | `TASK_TRACKER.md` Part 4 | Open — answer requested |
| B11 | Superseded: there is no buck on the board | — | Superseded |
| B12 | Four 5 V 100 nF still sit together in a corner; nothing within 41 mm of J5; the E22 supply at 28.4 mm | — | Open — answer requested |
| C1 | RS485 removed without your written agreement. We request a deferral: the wind sensor is a reed plus an AS5600, and the soil probe is read occasionally by laptop through an RS485–USB adapter | `INPUT_REGISTER` (archived) §N.1 C6 | Open — answer requested (question 1) |
| C2 | **The conflict is closed 2026-11-04** - GPIO10/11 no longer carry the mode pins, so the slot is usable. The 24-hour run and the 20 power cuts are still owed and need a plan | pad nets | Partly |
| C3 | FDC1004 port J21 on CH5 with pull-ups and ESD — design complete; bench read owed | J21 pad nets | Partly — bench result owed |
| C4 | Button on GPIO3, which is a strapping pin; buzzer on the expander; D6 on the carrier, J24 is the visible lamp pair | pad nets | Partly — needs the button moved and the status light defined in writing |
| C5 | M0 and M1 are now hard-strapped to GND through 0 ohm R56/R57 at J6.6/J6.7. Configuration mode is reached by lifting one strap with the module out of its socket; AUX and both UART lines are unaffected, so the read-back stays possible | `revC\FAB_NOTES.md` | Partly |
| C6 | One segment per cabled port with 4.7 kΩ pull-ups; the expander still shares I2C-0; U7's reset is a power-on RC | U7/U8 pad nets | Partly |
| C7 | 10 µF at 5.3 mm from J13; the 100 µF at 28.5 mm; nearest 100 nF about 22 mm | `TASK_TRACKER.md` C7 | Open — answer requested |
| C8 | Copper-path distance from each field connector pad to its array is 11.3–27.6 mm on J11–J23; **no array at all on J24, J25, J26** | `revC\_esd_measure.json` | Open — answer requested |
| C9 | J16, R5 and ESD3 remain with no stated purpose | J16 pad nets | Open — answer requested |
| C10 | No build variants in the BOM; antenna separation and LoRa scheduling unaddressed | — | Open — answer requested |
| C11 | SPS30 on its own segment (CH2); the cable is not specified; no 72-hour plan | J13 pad nets | Open — answer requested |
| C12 | 1 kΩ + 100 nF on both ADC inputs — design complete; stability unproven | R29/R30/C34/C35 | Partly — bench result owed |
| C13 | J26 placed for the AS5600; the device is not in the schematic; no pin map | J26 pad nets | Partly |
| D1 | Parity 0 and unconnected 0 re-proved on the saved file | `kicad-cli pcb drc --schematic-parity` | Done |
| D2 | Title block now `Rev C`, `2026-11-01`, change note written; the sheet is still A0 | `.kicad_sch` title block | Partly |
| D3 | ERC **0 errors, 0 warnings** and **no suppressed checks at all**: all nine re-enabled. What they hid is fixed, not re-suppressed: courtyards drawn for U4 and SW1 (board and library), 13 track ends centred on their vias. DRC stayed 0 with every check live | `revC\erc_RevC.json`, `revC\drc_RevC.json`; `.kicad_pro` `rule_severities` (no `ignore` entries) | Done |
| E1 | **Restored on 2026-11-03, and the way it broke is recorded.** A GND pour was added on B.Cu with 85 stitching vias, which took the worst distance to 10.00 mm and 0.0 % beyond. The placement and reroute work then moved copper again and re-measurement gave **144 links, worst 11.16 mm, 0.1 % beyond 10 mm** - outside your 10 mm acceptance. The stitching metric is not a DRC check, so a clean DRC gave no warning. Two GND stitching vias (0.6/0.3 mm) at **(277.00, 90.00)** and **(164.00, 186.00)** returned it to **146 links, worst 10.00 mm, 0.0 % beyond 10 mm**, plot regenerated. The measurement is now re-run after every copper or via change | `revC\E1_stitching_plot.png` | Done |
| E2 | Thermal reliefs on through-hole pads in the pours | zone settings | Done |
| E3 | **Blocked, and deliberately not drawn.** The module outline (x 180.5–212.5, y 91.5–160.0) does not mark which end carries the antenna; a keep-out over the wrong end is worse than none | `pcb` gr_rect on Dwgs.User | Open — answer requested (question 4) |
| E4 | 12 test points; none under the modem; none on I2C-1 or UART1; the +12 V point is obsolete | TP2–TP12 | Open — answer requested |
| E5 | J18 legend correct and verified on the plotted Gerber (0.05 mm from pad centres); board name, `Rev C` and S/N box printed. **Unchanged finding:** every port name is on F.Fab, which is not in the Gerber set, so the physical board still carries no port labels. Ten labels were attempted on 2026-11-03 at 1.0 mm / 0.15 mm and produced 15 silk violations; two repositioning passes did not clear them, so the attempt was reverted. The blocker is that the bottom silk band is already occupied by reference fields, which must move first | F.SilkS and F.Fab text dump; `pcb\_snap\T57_silk_20261103_181704\` | Partly - labels still not printed |
| E6 | The Parry guide puts the SIM socket on the back of the modem board, which faces up when mounted components-down; USB and microSD access not shown; no bring-up plan | `a7672s_4g_lte_modem_pinout_guide.md` §4 | Partly |
| E7 | 47 Ω on 4 of 14 cabled I2C lines (CH0, CH1 only); no input pi filter | R31–R34 | Open — answer requested |
| F1 | BOM has values and footprints only | `revC\MoriShield_Carrier_RevC_bom.csv` | Open — answer requested |
| F2 | No Rev C Gerbers, no stack-up, no job file, no fab drawing, no IPC-356 | `revC\preview_do_not_ship\` is preview only | Open — answer requested |
| G1 | No simulation; the `!padne` directives still describe 12 V at J18, D1, U1 and J9 | `.kicad_sch` directives | Open — answer requested |
| G2 | No FMEA | — | Open — answer requested |
| G3 | No bring-up plan | — | Open — answer requested |
| G4 | No EMC test plan | — | Open — answer requested |
| H1 | PE clearance errors now 0; no defined bond to ground; no arrestors on the antenna feeds | J19, PE pour | Partly |
| H2 | **Regressed in one respect.** WDI routed and U4 now in the BOM and placement file, but the supervisor is a push-pull TPS3823 on a net the module's own reset button drives, and a stuck I2C-0 survives a reset | U4 pad nets; `pcb\work done` §11 | Partly |
| H3 | No temperature column; DS3231 suffix and backup cell unnamed | BOM | Open — answer requested |
| H4 | No plating or coating in the BOM | BOM | Open — answer requested |
| H5 | Box chosen (200 × 155 × 80 mm); no glands, strain relief or drip loops | `INPUT_REGISTER` (archived) §Q.1 D8 | Partly |
| H6 | No radio record | — | Open — answer requested |

## 2. Response sheet — the 17 new items (001 Table 13)

| Item | What changed and where | Evidence | Status |
|---|---|---|---|
| R1 | 6-layer withdrawn. The rule survives: refill → save → DRC on the saved file → plot, with the three times recorded. Not yet exercised for Rev C | `revC\pack.ps1` refuses stale reports | Open — answer requested |
| R2 | `/WDT_WDI` routed U8 pad 11 → U4 pad 4 on F.Cu/B.Cu, 0.2 mm, 0.6/0.3 via; unconnected 1 → 0; dangling 5 → 0; no jumper | `kicad-cli pcb drc`; `pcb\work done` §1 | Done |
| R3 | `+` box centre y 107.250 on pad 1 (`+5V_IN`); `−` at y 102.250 on pad 2 (`GND`); stroke font, 0.15 mm | F.SilkS `5v +` and `5v -` | Done |
| R4 | **Blocked.** U10 is a positioned placeholder — verified today from the board file, **all six pads carry local unconnected names**. Blocked on the controller search (5 V gate drive and a 5.4 V trip) and on your signature for the deviation from TPS26630. Note this interacts with the converter choice: every module candidate has an output adjustable far above 5.5 V (XL4015 to 32 V, LM2596 module to 30–40 V), and the XL4015's 7 A typical current limit sits between F1's 4 A hold and its 8 A trip, so the missing cut-off and the un-upgraded 1.5 mm input copper are a pair | `pcb\_evidence\power_chain_pads.json`; `pcb\work done` §7; `revC\BUCK_AUDIT_XL4015_20261101.md` §4 | Open — answer requested (question 2) |
| R5 | Input both legs 1.5 mm (≈13 mΩ); Q9's footprint mismatch cleared; the 3 mm pour and the via arrays are not done; Q9.3 still enters through one 0.6/0.3 via | `pcb\work done` milestone 4 §4 | Partly |
| R6 | Q2 and Q3 still share `/SENS_GATE`; no switched-rail firmware rules | Q2/Q3 pad nets | Open — answer requested |
| R7 | RESET restored; `/PWR_EN` still has two drivers; PWRKEY's 1 kΩ pull-down confirmed correct by the Parry J2 jumper note | pad nets; Parry guide §4 | Partly |
| R8 | TPS3823-33 push-pull fitted, not the TPS3828; U4 is now in the BOM and placement file; WDI survives reset only because it sits on the expander | U4; `revC\MoriShield_Carrier_RevC_pos_front.csv` | Partly |
| R9 | PE clearance errors 0; the bond to ground is still absent; no README section | J19/PE | Partly |
| R10 | **J5 moved out from under the modem 2026-11-03** to (222.0, 91.4), 1.91 mm clear of the modem outline, DRC 0; TP2/TP3/TP5 unchanged; no standoffs, no 3D models | `pcbnew` positions | Partly |
| R11 | **The pin is fixed 2026-11-04**: `/REED_PULSE_F` moved from J2.7 (GPIO41, output-only) to **J2.9 = GPIO39**; J2.7 is `unconnected-(J2-IO41-Pad7)`. The 1/10/50 Hz bench counts are still owed | pad nets | New |
| R12 | 63 track items, 448.41 mm, on In2.Cu across 8 nets | `pcbnew` layer census | Open — answer requested |
| R13 | Q1, Q5, Q6 still 2N7000, unspecified at 2.5 V gate drive | Q1/Q5/Q6 | Open — answer requested |
| R14 | GY-521 and DS3231 outlines still on each other's sockets | gr_rect (154,163.5)-(173.5,187.5) and (207.35,163.5)-(232.35,205.5) | Open — answer requested |
| R15 | `.kicad_dru` now exists and names only nets on this board; stale descriptions, F.Fab labels, J24 symbol pin names and `!padne` directives remain | `pcb\MoriShield_Carrier.kicad_dru` | Partly |
| R16 | **67 of 319 vias sit inside an SMD pad** - re-measured 2026-11-04 from the saved board; the four strap vias were moved clear, so the count did not rise. DRC cannot see it. Serigreen's written agreement to plug/fill/cap per IPC-4761 and a price are still owed | `revC\vias_in_pads.txt` | Open |
| R17 | U8 is still on `/I2C0_SDA`/`/I2C0_SCL`. The watchdog kick, PWR_EN, SENS_EN, E22_EN, LED_DRV1/2 and BUZZER_EN all hang off an expander on the cabled bus | U8 pad nets | Open — answer requested |

---

## 3. Answers received to the input register

Every question in `INPUT_REGISTER_RevC.md` that carries a recorded answer is repeated here with
that answer, so that the register can be archived without losing anything.

| Question | Answer received | Date | What it changed |
|---|---|---|---|
| A1 | The package goes to Serigreen on 2 November 2026 | 31 Oct | Delivery date |
| A6 | All components come from Serigreen; Aswin buys only what he damages on the bench | 31 Oct | Purchase split, written into this reply |
| A7 | **Closed 2026-11-04.** `/E22_M0` and `/E22_M1` are gone as nets; J1.16 and J1.17 are `unconnected-(J1-IO10-Pad16)` and `unconnected-(J1-IO11-Pad17)`; M0/M1 are strapped to GND through 0 ohm R56/R57 at J6.6/J6.7, so GPIO10 and GPIO11 are free for the microSD | pad nets read back from the saved file; `revC\drc_RevC.json` | Done |
| A8 | Deepak available 31 Oct 20:00–1 Nov 05:00 and 1 Nov 20:00–2 Nov 05:00 | 31 Oct | Routing windows |
| A9 | Schematic-only package, worked on 1 November | 31 Oct | Package contents |
| B1 | SmartElex module with AP63357 (later superseded by B13a) | 31 Oct | Converter shortlist |
| B2 | Converter inside the enclosure; Serigreen buys it | 31 Oct | Condition 5 lead length |
| B4 | Keep it simple: one SMD part, diodes if possible | 31 Oct | Protection architecture |
| B13a | LM2596HVS, Robu, in stock, under ₹300 — **revisited 1 Nov:** the XL4015 5 A module with LED voltmeter was audited against 001 §6.4 condition 1 and rejected on its 36 V input ceiling; the audit is in `revC\BUCK_AUDIT_XL4015_20261101.md` and the question back to you is 8a | 31 Oct, revisited 1 Nov | The converter |
| C1 | Edgehax S3-PRO with on-board microSD, no 32 kHz crystal | 31 Oct | Pin plan |
| C3 | A7672S, pins facing the carrier | 31 Oct | Socket direction |
| C4 | Modem 5 V is the JST at the top-right when flipped | 31 Oct | J5 placement |
| C6 | RS485 removed; wind sensor is reed + AS5600; soil probe read occasionally by laptop | 31 Oct | C1 becomes a deferral request |
| C7 | Reed is in; the wind vane is not on the board | 31 Oct | New J26 header |
| C8 | Reed is in; check which GPIO | 31 Oct | Reed stays on GPIO41 |
| C9 | 8 GB SanDisk or Hikvision card | 31 Oct | Purchase line only |
| C10 | J24 = two 5 V lamps; J25 = buzzer; D3/D4/D6 diagnosis | 31 Oct | Status-light definition |
| C19 | Could not route; Deepak tried many reroutes; decided on a jumper | 31 Oct | Superseded by the P07 route (R2) |
| C23 | No 32.768 kHz crystal; X11 is a B5819WS Schottky diode | 31 Oct | GPIO15/16 free |
| C24 | ESP32-S3-WROOM-1 MCN16R8 (photo) | 31 Oct | A6 |
| C25 | GPIO map is not fixed; written once the PCB freezes | 31 Oct | Closes C18 |
| C26 | Keep the permanent 1 kΩ on PWRKEY | 31 Oct | R7 |
| C27 | Yes — wire A7672_RESET to whichever pin is easiest | 31 Oct | `/MODEM_RST` on GPIO6 |
| C28 | "Explain this more clearly" — explained; the 1.8 V/0 V measurement is still owed | 31 Oct | VDD_UART stays on 3V3_C by default |
| C29 | Closed — no photo needed; J5 stays at (239.51, 95.83) with a 100 mm lead | 31 Oct | R10 |
| D1 | Box already chosen; acrylic base plate; holes cut for antennas and cables | 31 Oct | A4 |
| D8 | 200 × 155 × 80 mm | 31 Oct | 3D check |
| E1 | **Restored on 2026-11-03, and the way it broke is recorded.** A GND pour was added on B.Cu with 85 stitching vias, which took the worst distance to 10.00 mm and 0.0 % beyond. The placement and reroute work then moved copper again and re-measurement gave **144 links, worst 11.16 mm, 0.1 % beyond 10 mm** - outside your 10 mm acceptance. The stitching metric is not a DRC check, so a clean DRC gave no warning. Two GND stitching vias (0.6/0.3 mm) at **(277.00, 90.00)** and **(164.00, 186.00)** returned it to **146 links, worst 10.00 mm, 0.0 % beyond 10 mm**, plot regenerated. The measurement is now re-run after every copper or via change | `revC\E1_stitching_plot.png` | Done |
| E3 | No Bluetooth; GSM primary; Wi-Fi only when GSM is unavailable or the field has Wi-Fi | 31 Oct | The full antenna keep-out stays (E3 remains P1) |
| F1 | Standard 4-layer pool: 0.15 mm annular, 0.2/0.2, 0.3 mm via | 31 Oct | No via fill — R16 must be moved or agreed |
| F2 | Hand assembly | 31 Oct | No fiducials; 0805/1206 passives |
| F11 | Aswin selects the parts | 31 Oct | Part selection |
| G2 | Bench coverage exists; field may vary | 31 Oct | B10 trace can be taken in-house |
| H2 | Send date 2 November 2026 | 31 Oct | Delivery date |
| H3 | XLSX | 31 Oct | Response sheet format |
| I6 | Approved, with the reasoning: the buck ran hot, no 12 V is needed anywhere, keeping the board at 5 V is safer, RS485 has no consumer, and the layout went from 40+ unconnected to 1 | 31 Oct | The change list |

## 4. Questions we need answered

Numbered, one line each. Questions 1–8a are for Serigreen and are the ones that stop work.
Questions 9–79 are the still-open entries of the input register, each with who holds it; they
are listed so that no question is lost when the register is archived.

**For Serigreen — these stop work**

1. **RS485 (C1, P0).** Do you accept a written deferral for this revision, on the grounds that the wind sensor is now a reed plus an AS5600 and the soil probe is read occasionally by laptop? If not, what supplies the transceiver now that 12 V is off-board?
2. **J18 protection (R4, P0).** Do you accept a discrete over-voltage/reverse controller driving low-Rds FETs in place of the named TPS26630? The arithmetic is 40 mΩ against 66 mΩ, and 66 mΩ cannot meet condition 3.
3. **microSD versus GPIO10/11 (A7, C2, C5, R11) - ANSWERED BY US 2026-11-02, kept for the record; see 8b for the correction we are asking you to make.** CHK-001 C11 states GPIO10–14 are the EdgeHax board's microSD; the Keyestudio pin table puts it on io35–39. Which is right for the board you supply? A continuity measurement is in hand to settle it, but we need your statement for the record.
4. **Antenna position (E3).** Which end of the Edgehax module carries the antenna? We will not draw a keep-out over a guess. A photo of the module's top face or the board drawing is enough.
5. **The reed on GPIO41 (R11) - CLOSED BY US 2026-11-02, we are moving it to GPIO39.** C11 says GPIO40–42 are output-only LED pins; the vendor reference calls GPIO41 a plain GPIO. Do we move the reed, and to which pin? The pin budget is short by one after the four moves you already asked for.
6. **Battery sense (B9).** GPIO6 is now `/MODEM_RST` and every ADC1 channel on the headers is allocated. Do we use the modem board's own ADC pin (0–1.8 V, currently unconnected at J3.11), reclaim GPIO10/11 and accept no microSD, or move an existing analog input?
7. **Vias in SMD pads (R16), now 67 of 315.** Do you agree to specify plug, fill and cap per IPC-4761 Class B or C, and will you price it? The alternative is moving 65 vias on the densest part of the board.
8. **Converter (condition 1) — one decision, and our audit says No-Go on the proposed part.** Condition 1 asks for a converter rated **40 V input or more**. We audited the **XL4015 5 A module with an LED voltmeter** proposed on 2026-11-01 and rejected it: **8–36 V operating, 40 V absolute maximum**, which is below the ~39 V surge clamp, and its 7 A limit sits between F1's hold and trip (≈+60 K on 1.5 mm input copper); its display is rated +65 °C and its electrolytics 85 °C inside a +70 °C box. The incumbent **LM2596HVS** (4.5–50 V in, 3 A peak / about 2 A continuous on its heatsink, trim to 5.15 V) meets the voltage clause and is what we have costed. **Please either name a converter that meets condition 1 by its numbers, or sign the deviation** for the LM2596HVS including the ~2 A continuous at +70 °C figure. We will not substitute a part on our own authority. Audit: `revC\BUCK_AUDIT_XL4015_20261101.md`.
8a. **Converter choice (B1, B2, condition 1 — this one stops S2).** You pointed us at the XL4015 5 A module as the better part. Its die is genuinely cooler than the incumbent's — 0.4 W against 1.2 W at 3 A, because it switches a 60 mΩ MOSFET where the LM2596 drops 1.16 V — and it carries 5 A. But XLSEMI's own data sheet puts its **operating input at 8–36 V with a 40 V absolute maximum**, and condition 1 asks for "input rated 40 V or more". Worse, B1's clamp test has no solution at that ceiling: any TVS that stays off through the 22–25 V battery-disconnect event clamps at 38.9 V or higher, and any TVS that clamps under 36 V breaks down at 24.4 V or lower and conducts during the event B1 exists to survive. We therefore **reject the XL4015 (and the XL4016, which has the same 36 V/40 V window) for this input chain**, and we also reject the meter variant on thermal grounds: its display is a +65 °C part in a box we are told reaches +70 °C, and it draws 5–20 mA permanently, which lands in B5. Two answers are needed, and either is acceptable to us: **(a)** hold your own B1 text — "pair it with a buck rated 60 V" — and supply the converter, since A6 already makes Serigreen the supplier of every component and the ₹300 ceiling was our constraint, not yours; or **(b)** sign a written deviation from "input rated 40 V or more" and accept a re-coordinated surge plan that puts a series element between the TVS and the converter, because the TVS alone cannot do it. If instead you want the 3 A hot capability, the honest route is the incumbent plus the die check we have asked for in the same row of §6.

8b. **A correction to CHK-001 C11, with the measurement behind it.** C11 states "GPIO10 to 14 are the
board's own microSD". Our continuity test on the board you supply gives **GPIO10, 11, 12 and 13** - the
card's CS, MOSI, CLK and MISO - and **GPIO14 is not connected to the slot**, nor is GPIO9. That matters
because `/I2C0_SCL` sits on GPIO9 and is safe, and because a rule that bans GPIO14 costs us a pin we do
not need to ban. Please confirm or correct.

8c. **E22 mode pins - one decision we would like from you before we place parts.** We intend to strap M0
and M1 to ground through 0 ohm resistors, which is what the module's manual permits and what we ran over
the air. The trade is that hardware mode control is then only available by lifting a strap with the module
removed from its socket. If you want mode control from firmware instead, we will move M0 and M1 to two
spare pins on the I/O expander - say so now, because it changes the parts we order.

8d. **E22 supply rail.** The board feeds the LoRa module from 5 V. Its TXD and AUX outputs are TTL and
follow the supply, and the ESP32-S3 is not 5 V tolerant, so we propose moving the module to the 3.3 V
rail - which is also how we tested it. Confirm you have no objection, or tell us to keep 5 V and add the
manual's 4-10 k pull-ups instead.

8e. **Two ports we cannot identify.** J17 (channel 4) and J20 (channel 6) are fully wired 4-pin I2C ports
with ESD arrays and pull-ups, and nothing in 003, 004, the schematic or our notes says which sensor goes
in them. J20 is one of the two runs blocking the LoRa antenna keep-out, so if it is spare we can free the
corridor; if it is not, we reroute. Which is it?

8f. **Keyed headers.** J6, J3 and J4 are unkeyed, so a module can be inserted rotated 180 degrees. We are
adding silkscreen so it is obvious, but only a key makes it impossible. Do you want a shrouded or keyed
header specified, and at what cost limit?
**Still open in the input register — held by us or the bench, not by you**

9. A2 — how many boards in the first build. Default 5.
10. A3 — is Rev C the fabrication release or another review round. Default: another review round, then fabricate.
11. A4 — pilot date and units. Default: none stated.
12. A5 — budget per board. Default: no cap stated.
13. B3 — converter-to-J18 lead length and gauge. Default 200 mm of 0.75 mm².
14. B5 — input current limit. Default 3.5 A.
15. B6 — keep a fuse or not. Default: keep one part matching its footprint.
16. B7 — room for 470 µF plus ceramics at J5. Default: radial plus 0805/1206.
17. B8 — is TPS7A2033 final. Default: keep.
18. B9 — see question 6.
19. B10 — battery wire and range. Default 0–20 V on a dedicated lead.
20. B11 — real currents or datasheets. Default: datasheets.
21. B12 — hottest air in the box. Default +70 °C, no vents.
22. B13 — 40 V route, adjustability and rated current at +70 °C. Answered in substance by B13a (LM2596HVS) and B13b below.
23. B13b — is the converter adjustable to 5.15 V and is the pot lockable. Default: yes, trim pot.
24. C2 — spare board to measure. Default: one spare.
25. C5 — PWRKEY behaviour and reset line. Answered in substance by C26/C27.
26. C11 — panel lamps. Default: two 5 V LEDs, 20 mA, JST XH.
27. C12 — buzzer type and current. Default: magnetic, about 30 mA.
28. C13 — FDC1004 cable. Default: 1 m shielded, JST XH.
29. C14 — SPS30 cable and bus. Default: 1 m shielded, I2C.
30. C15 — GY-521 and DS3231 modules. Default: GY-521 8-pin, DS3231 6-pin with under-cell.
31. C16 — are J15/J16 used. Default: remove J16, R5, ESD3.
32. C17 — test points. Default: take the proposal.
33. C18 — existing firmware GPIO map. Replaced by C25: the map is written once the PCB freezes.
34. C20 — who writes README, pin map, truth table. Default: we draft, you sign.
35. C21 — module shield marking and X1 close-up. Partly answered by C24/C23.
36. C22 — modem test-fit photo. Closed by C29.
37. D2 — may the outline change. Default: keep.
38. D3 — standoffs. Default M3 × 8 mm.
39. D4 — antenna placement and cable route. Default: on the modules.
40. D5 — cables and glands. Default: six sensor cables, supply, earth.
41. D6 — panel. Default: no panel.
42. D7 — mounting. Default: wall plate, IP65.
43. E2 — antennas module-mounted or coax. Default: module-mounted.
44. E4 — who runs EMC/ESD. Default: plan now, test on pilot units.
45. E5 — conformal coating. Default: acrylic, contacts masked.
46. E6 — cable lengths for tests. Default: 1 m sensors, 2 m supply.
47. F3 — ENIG or HASL. Default ENIG.
48. F4 — IPC class 2, Tg 150 °C, 1.6 mm, 1 oz. Default: all four confirmed.
49. F5 — mask and silk colours. Default green/white.
50. F6 — quantity and panel. Default 5, separate.
51. F7 — the two build variants. Default: one build until named.
52. F8 — distributors and stock. Default Mouser/DigiKey.
53. F9 — parts that must not change. Default none.
54. F10 — module part numbers and links. Default: we source and list.
55. F12 — who approves the parts list. Default: the CTO approves in this reply.
56. G1 — instruments. Default: 100 MHz scope, DMM, 5 A supply.
57. G3 — SPS30/E22/GY-521/DS3231 available. Default: all four.
58. G4 — calipers and 1:1 printer. Default: both.
59. G5 — camera. Default: phone.
60. G6 — STEP models. Default: dimensions only.
61. G7 — existing measurements. Default: none.
62. G8 — who measures first boards. Default: we do.
63. H1 — who checks the package. Default: you review, Deepak checks hardware.
64. H4 — schematic-only first. Answered by A9.
65. H5 — how the CTO receives the package. Default: same channel as before.
66. H6 — label "Rev C". Default: Rev C.
67. H7 — 6L archive or delete. Default: archive, marked withdrawn.
68. H8 — status reports. Default: one page per stage.
69. I1 — own the two unagreed changes. Default: yes.
70. I2 — six conditions with numbers. Default: yes.
71. I3 — old-board comparison. Default: yes.
72. I4 — words to avoid. Default: never "ready".
73. I5 — one-page summary. Default: yes.
74. J1 — anything else we should know. Default: nothing.
75. J2 — anything to leave out. Default: nothing.
76. C28 — the VDD_UART 1.8 V/0 V measurement. Default: treat as an input, keep J4.3 on 3V3_C.
77. B13b — the 5.15 V set point on the bench. Default: set and lock the pot.
78. C21 — the X1 close-up. Closed by C23.
79. C24 — the module marking photo. Answered.
80. C26 — PWR_KEY held low. Answered.
81. A10 — Deepak's second window end. Scheduling only.

---

## 5. Changes nobody asked for

Every change in this package that no CTO item requested, with the reason. None is a silent
substitution.

| Change | Where | Why | Status |
|---|---|---|---|
| Board name, `Rev C` and a blank S/N box added on F.SilkS | (139.5,202.6), (139.5,200.2), (150,200.2) | C12 and E5 ask for them, but no single item names the serial box | Done |
| `1` marks at J3 pin 1 and J4 pin 1, and `MODEM THIS WAY UP` between the rows | (232.2,113.56), (272.4,113.56), (240,108.6) | A3 asks for a pin-1 mark; the extra orientation note is ours | Done |
| J26, a 4-pin JST-XH on I2C-1 in parallel with J8, for the AS5600 | (162.45,181.35) | The wind vane had no connector at all; C13 names the AS5600's port | Done |
| `/MODEM_RST` wired J1.6 → J4.8 | 67 mm route, 0.25 mm, 4 vias | A11 asks for a recovery path; the specific pin choice is ours | Done |
| Net classes increased to eight, with a `.kicad_dru` of width floors | `.kicad_pro`, `.kicad_dru` | C10 asks for spacing rules and a rule file matching the board | Done |
| The `3V3` class routing default lowered from 0.50 to 0.20 mm | `.kicad_pro` | The net carries under 50 mA; the class value is a routing default and has no DRC effect (see §6) | Done |
| `/+5V_SENS` widened from 0.20 mm to 0.5–0.8 mm | In2.Cu chain, x ≈176–247 | B4 and C7 imply it; no item names the sensor rail's width | Done |
| `/3V3_SENS_SW` widened from 0.3 to 0.5 mm | all 28 segments | Same reasoning | Done |
| The PE back-edge 153 mm wire deleted, the B.Cu pour carrying it | (143,203.5)-(296,203.5) | Redundant copper; the pour already fills that strip | Done |
| Q9, U7 and U8 footprints restored from the library, with the library corrected where it was wrong | `.pretty` library and board | R5 and C5 ask for no mismatch; correcting the library file itself was ours | Done |
| Title block changed to `Rev C`, `2026-11-01`, with a change note | `.kicad_sch` | C1 and D2 ask for the revision; the note text is ours | Done |
| U4's `board_only` and `exclude_from_pos_files` flags cleared | board | C6 and Table 14 row 3 ask for U4 in the placement file | Done |
| The eight dead copper objects removed | `3V3_C`, `/EVENT_BTN`, `/PWR_EN`, `/I2C0_SDA`, `/BUZZER_EN` | R2 names the dangling branch | Done |
| `MoriShield_Carrier.kicad_dru` created | `pcb\` | C10 asks for a rule file; the specific floors are ours | Done |
| Silkscreen cleanup: 124 violations to 0 | U7/U8 body outlines inset 0.3 mm; their pin-1 dots moved inward; Q9's two corner marks removed; 40 reference fields raised to 1.0 mm / 0.15 mm; 30 more moved off pads and other silk | C5 and C12 ask for no silk over copper and 1.0 mm / 0.15 mm text; how it was done is ours | Done |
| The 13 `3V3_C` tracks widened from 0.200/0.250 mm to 0.300 mm | F.Cu, B.Cu, In2.Cu | The floor in force is the custom rule "3V3 class floor" at 0.30 mm, not the 0.20 mm class default. Widening closes the finding without lowering a rule | Done |
| The PE width floor lowered from 0.60 mm to 0.35 mm in the rule file, with the reason written in the file | `pcb\MoriShield_Carrier.kicad_dru` | Three PE runs are at the physical maximum of their corridors; deleting them was proved to break connectivity (unconnected 0 to 2) | Done |
| U10 pin 6 no-connected and the single-pin `/5V_PROT` label removed | Schematic, U10 area; board pad 6 | The placeholder had one net with one pin, which was the last ERC warning. Making the placeholder honest removes the warning without pretending the circuit exists | Done |
| One "Q1 buzzer" label moved | F.SilkS, from (132.5, 188.5) to (130.0, 191.8) | It sat over R14 pad 1 once its text was raised to the 1.0 mm minimum | Done |
| Courtyards drawn for U4 and SW1, on the board and in the library footprints | `SOT-23-5_HS`, `SW_6x6`; land extent + 0.25 mm | Neither part had one, so no spacing rule could see them. Found by re-enabling the suppressed check | Done |
| Thirteen track ends snapped onto their via centres | 3V3_C, PE, /3V3_SENS_SW, /LED_DRV1/2, /+5V_SENS, /I2C0_MUX_SC0, /I2C0_SDA_CH4 | The suppressed `track_not_centered_on_via` check named them; largest move 0.283 mm | Done |
| `min_text_thickness` raised from 0.08 to 0.15 mm | `.kicad_pro` | 0.08 was our own number, not the fab's; DRC still 0, so every text already met 0.15 | Done |
| GND pour added on B.Cu, PE zone priority raised to 1, thermal gap 0.25 / bridge 0.4 | B.Cu, whole board | E1 cannot be met without outer-layer ground copper. PE was given priority so the earth pour cannot be starved; the tighter thermal features clear 7 starved thermals that the default settings produced | Done |
| 85 stitching vias added, 0.6/0.3 mm, GND | B.Cu pour to In1 plane | They are the links that make E1's 10 mm rule hold; each was placed clear of other-net copper and holes | Done |
| `min_text_height` raised from 0.8 to 1.0 mm | `.kicad_pro` | The CTO's silk rule is 1.0 mm; every text already met it, so DRC stayed 0 | Done |

---

## 6. Declared assumptions

These are not measurements. Each is used somewhere in the design or in a number quoted above,
and each must be confirmed before release.

| Assumption | Value used | Where it is used | What confirms it |
|---|---|---|---|
| Copper weight, outer layers | 1 oz (35 µm) | every resistance figure | The fab's capability sheet (D-7) |
| Copper weight, inner layers | ½ oz (17.5 µm), half-etched | In2 resistances, including the 11.5 mΩ modem feed | same |
| Sheet resistance | **0.505 mΩ per square outer, 1.01 mΩ per square inner**, at 20 °C, rising 0.39 % per °C | the condition-3 budget and the route-C comparison | follows from the two copper weights above, so it is only as good as they are |
| Board thickness and stack | 4 layers, 1.6 mm, no stack-up in the project file | job file, impedance (none specified) | The fab's stack-up |
| Minimum features | 0.20 mm track and gap, 0.6/0.3 mm via, 0.15 mm annular, 0.5 mm copper-to-edge | the constraint set | The fab's capability sheet |
| Silkscreen minimum | 0.15 mm stroke, 1.0 mm height | the silk cleanup | The fab's capability sheet; the project's own `min_text_thickness` is 0.08 mm, which is our number, not the fab's |
| Surface finish | ENIG | fab drawing | F3 |
| Hand assembly | no fiducials, 0805/1206 passives | placement, via-in-pad decision | F2 |
| Via treatment | none specified today | R16 is open | Your agreement and the fab's price |
| Converter | **Two candidates, one decision owed (question 8a).** XL4015 5 A module with LED voltmeter: audited 1 Nov, **rejected** — XLSEMI Rev 2.0 gives 8–36 V operating / 40 V absolute, ±2 % reference, 7 A switch limit, RθJA 30 °C/W. Incumbent LM2596HVS: module page says 4.5–50 V, set to 5.15 V, pot locked, heatsink fitted, 5 mm air, ≤200 mm of 0.75 mm² to J18 (that lead computes to 9.3 mΩ there and back, inside condition 5's 15 mΩ) | condition 1 and 5 | `revC\BUCK_AUDIT_XL4015_20261101.md`; your signature (8a) and the die check below |
| **Which die is in the LM2596HVS module** | we assume LM2596HV (60 V operating, 63 V absolute per the UMW/UTD sheet) | B1, condition 1, the whole 40 V argument | **Not verified.** TI's plain LM2596 is 40 V operating / 45 V absolute, so the module's 50 V claim only holds if the die is the HV variant. Opening the module and photographing the marking is a 15-minute bench step (T-53) |
| **The converter's own input fuse and surge part** | a fuse sized to the converter's limit plus an SMBJ/SMCJ24A at the module input, in the lead — **neither part exists on either module** | condition 1, B1, B3, check C8 | The assembly note, which is not written yet (T-54), and the bench clamp measurement |
| Module display as set-point evidence | not usable: 0.1 V resolution, roughly ±1 % + 1 digit | condition 1's ±1 % | A 4½-digit meter at the module terminals, and the pot locked |
| Modem supply allocation | 15 mΩ lead + 60 mΩ board + 30 mΩ modem lead | condition 6 | The G1 model and the bench trace |
| Modem input capacitance | 220 µF with 0.20 Ω ESR plus 10 µF ceramic | the B10 model | The modem board's datasheet, which we do not have |
| Earth scheme | PE bonded to GND at one point beside the sensor ports; box bonded to an earth rod by the installer | R9, H1 | Your earthing intent (SQ17) |
| **Libraries used to produce the reported ERC and DRC numbers** | the project's own `pcb\MoriShield_Carrier.kicad_sym` (157,936 B) and the footprint library resolved through `fp-lib-table` | every ERC figure quoted above, and check C1 | **If you open the schematic against the release layout's copy of the symbol library (153,623 B) you will see 336 `lib_symbol_issues`**, and if the footprint library does not travel with the package you will see 124 `footprint_link_issues`. Both were measured here. The package must carry the current library and the `.kicad_dru`; until it does, our DRC and ERC numbers are not reproducible on your machine |
| **Suppressed checks behind the reported numbers** | 9 checks set to `ignore` (5 DRC, 4 ERC) | the DRC 0 and ERC 0/0 above | Lifting them adds 15 DRC items. We have not yet justified them individually, which is item D3 |

---

## 7. Release

Release is Serigreen's, in writing, naming the exact file set by checksum. Nothing in this
package is an order, and no date in it authorises fabrication.
