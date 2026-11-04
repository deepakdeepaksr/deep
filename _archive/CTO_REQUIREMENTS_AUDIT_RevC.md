# CTO Requirements — Full Audit and Traceability, Rev C

| | |
|---|---|
| **Document** | AUD-CAR-4L-RevC-01 |
| **Date** | 1 November 2026 |
| **Audits** | every requirement in the five CTO documents, against `pcb\MoriShield_Carrier.kicad_pcb` and `.kicad_sch` |
| **Method** | each requirement read from the source text, then tested against the files with `kicad-cli`, the pcbnew API, or a direct measurement. Nothing below is marked done because a note claimed it |
| **Baseline** | `VERIFICATION_20261101.md`, `TASK_SHEET_RevC_4L.md` §5, `DELIVERY_STAGES_RevC.md` |

---

## 1. The requirement universe

Nine distinct sets were found across the five documents. All are enumerated so that nothing is missed for being in the wrong place.

| Set | Source | Count | What it binds |
|---|---|---|---|
| **I** | MS-CAR-REV-A-004 §6.2 Table 9 — the 59 items | **59** | the design work, each with its own "closed when" |
| **II** | MS-CAR-REV-B-001 §11 Table 13 — new items | **17** (5 P0, 8 P1, 4 P2) | the current review round |
| **III** | MS-CAR-REV-B-001 §6.4 — the six conditions on the 5 V input | **6** | the accepted architecture |
| **IV** | MS-CAR-REV-B-001 §12 Table 14 — the next package, row for row | **10** | what the package must contain |
| **V** | MS-CAR-CHK-001 §4 — the checks | **13** (C1–C13) | how it is judged |
| **VI** | MS-CAR-CHK-001 §3 Table 2 — contents of a release package | **8** | file formats and their requirements |
| **VII** | MS-CAR-CHK-001 App. C Table 11 — before you send | **16** | the pre-send tick list |
| **VIII** | MS-CAR-CHK-001 §7 — the response sheet | **5 columns + header** | the first file in the zip |
| **IX** | MS-CAR-REV-A-003 §9/§10, MS-CAR-REV-A-001 §7/§8 | *absorbed into I* | superseded by 004's merge |

**Total distinct obligations: 118** (59 + 17 + 6 + 10 + 13 + 8 + 16 − overlaps in sets VI/VII which restate C1–C13). Sets I and II are the design register (76 rows); sets III–VIII are the release gate.

---

## 2. Headline

| | |
|---|---|
| Design register (76 items) | **9 closed · 20 partly · 46 open · 1 superseded** |
| P0 items (19) | **3 closed** (R2, R3, A8, C3, C12 — of which two are paper-only) |
| Release gate C1–C13 | **0 fully met · 1 partly (C12) · 12 not met** |
| Table 14 package rows | **0 of 10 complete** |
| Table 11 pre-send ticks | **2 of 16** |
| Package files that exist | **0 of 8** — no response sheet, no reply, no PDF, no BOM, no evidence documents |
| **Against the 2 Nov commitment (schematic-only pass)** | the bar is *schematic PDF + ERC report + response sheet* (CHK §3 note). **1 of 3 exists, and neither of the two that exist is clean** |

**Verdict: the design has moved a long way and is measurably better than Rev B on every countable axis. The package does not exist. Nothing is deliverable to the CTO today.**

| Measured | Rev B (as reviewed) | Today |
|---|---|---|
| ERC | 328 warnings | **0 errors, 1 warning** |
| DRC errors | not separated | **16, all `track_width`** |
| DRC total | 165 | **145** |
| Unconnected | 1 (watchdog, 13.6 mm gap) | **0** |
| Parity | 211 items | **0** |
| Footprint ↔ library mismatch | 65 vias in pads, Q9 pads turned | **0** |
| Clearance errors | 0 (no rules existed) | **0, now with real rules** |
| Net classes | none defined | **8 defined and binding** |

---

## 3. The release gate — C1–C13, tested

### C1 · ERC, libraries, title block — **NOT MET**
> Pass when: "ERC reports 0 errors and 0 warnings on the saved schematic, and the title block carries the right revision."

- ERC: 0 errors, **1 warning** — `isolated_pin_label` on `5V_PROT`. Closes when U10 is wired.
- Title block: `rev "Proto-Simple Rev 0.2 (Post-RS485 Stripped)"`, `date 2026-10-22`. **This is the exact failure the CTO cites in "Seen so far"** — *"a title block reading 'Proto-Simple Rev 0.2'"*.
- Library links: 328 `lib_symbol_issues` were cleared by restoring `sym-lib-table` + the current `.kicad_sym`. Two copies of the symbol library now disagree — `4L\` matches, `morishield\…\libraries\` is stale. **A package built from the release layout would re-introduce all 328.**
- **Effort to meet:** 15 min title block + 30 min U10.

### C2 · Parity and connectivity — **NOT MET (one item)**
> Pass when: "0 unconnected items, 0 parity differences, **no dangling track or via**, on the saved file."

- Unconnected **0** ✅ · Parity **0** ✅ · Dangling: **3 vias + 2 tracks** ❌
- Named in C2's own "Seen so far": *"a 13 mm dangling stub and four dangling vias"*. Today: a **13.00 mm `3V3_C` stub on B.Cu**, a 1.05 mm `/EVENT_BTN` stub, and vias on `/PWR_EN`, `/I2C0_SDA`, `/BUZZER_EN`. **The same five items, still there.**
- **Effort:** 20 min.

### C3 · Zones, save order, plot order — **NOT APPLICABLE TODAY, WILL FAIL AT RELEASE**
> Pass when: DRC clean on the saved file, Gerbers plotted after that DRC, zone-check ticked, **and the three times stated in the response sheet**.

- No Gerbers exist for Rev C. The three timestamps (save / DRC / plot) are not recorded anywhere.
- This is the check that caught Rev B's R1. It cannot be satisfied by a schematic-only package, and it must not be forgotten at S4.
- **Effort:** 30 min at S4, plus a standing rule.

### C4 · Production files against the board — **NOT MET**
- No Gerbers, no drill, no IPC-D-356. **Effort:** 45 min at S4.

### C5 · Footprints and assembly — **PARTLY MET**
> "No footprint mismatch, no courtyard overlap, no silk over pads, no via in a pad without a fab note, constraints met."

| Sub-clause | Status |
|---|---|
| Footprint does not match library | ✅ **0** — Q9, U7, U8 all cleared this session |
| Courtyard overlap | ❌ **cannot be assessed — `missing_courtyard` is in the ignored list**, and C5 says *"do not downgrade them to ignored"* |
| Silk over pads / overlaps | ❌ **78 + 46 = 124 items** |
| Vias in SMD pads | ⚠ Rev B had 65. Not re-counted today — **must be measured before release** |
| Constraints 0.15 / 0.3 / 0.2 / 0.2 | ✅ now enforced: 8 net classes, binding, and `annular_width`/`via_diameter` errors went to 0 |
| Hand-solder lands | ✅ library lands restored on the SOT-23 and TSSOP families this session |

**Effort:** 3–4 h for the silk, 30 min to un-ignore courtyards and see the real number, 20 min to count vias-in-pads.

### C6 · BOM, placement, job file, fab drawing — **NOT MET**
> Table 14 row 3 says it plainly: *"placement in mm **with U4 in it**"*.

- **U4 is flagged `board_only` AND `excluded from position files`** — verified by reading the footprint attributes. U4 is the watchdog supervisor. This is the exact defect named in C6's "Seen so far". **Still present.**
- Test points TP2–TP12 and H1–H4 excluded from placement — correct and normal.
- BOM: no Manufacturer, MPN, Rating, Temp or Variant columns. No fab drawing. No job file. No stack-up.
- **Effort:** 2 min to clear U4's flags, 90 min for the BOM fields, 45 min for the drawing.

### C7 · Power paths — **NOT MET**
- Input path now measured: `+5V_IN` 8.4 mΩ + `+5V_F` 4.6 mΩ, both legs at 1.5 mm. **A real improvement and the first honest numbers on this board.**
- Modem feed still 11.5 mΩ on In2 (outer would be 5.8 mΩ, a 4 mm pour 2.2 mΩ).
- No DC solve, no simulation (G1, P0), no supply-path table per load, no part ratings, no thermal at +70 °C.
- **Effort:** 2 h for the solve plus the table; G1 needs tooling.

### C8 · Protection at inputs and connectors — **NOT MET, and badly**
Four sub-clauses, all failing:

| Sub-clause | Rule | Measured today |
|---|---|---|
| Reverse, 12 V, 24 V events | written up + simulated | **no protection exists** — U10 is a footprint with five pads unconnected |
| TVS stand-off above the rail | stated against the rail | D2/ESD16 not re-rated |
| **ESD within 5 mm of every pin that leaves the box** | ≤ 5 mm along the copper | **5.4 to 21.8 mm on 12 connectors.** J24 (lamps) and J25 (buzzer) have **no ESD part at all** — and C8 says *"Panel lamps, buttons and buzzers count as leaving the box."* The new J26 is 35–37 mm from its array |
| PE bond | one defined link, RC alternative, in the README | **still no bond** |

Rev B's "Seen so far" said *"ESD parts 5 to 22 mm from their pins"*. **We are at the same numbers.**
**Effort:** 2 h for the U10 block, 3 h to move or add ESD arrays at 14 connectors, 30 min for the PE bond.

### C9 · Placement — **NOT MET**
- No decoupling map exists. B7 is closed (U6's 1 µF at 2.1 and 2.4 mm) but B12 is not: four 5 V 100 nF still sit together in a corner, nothing within 41 mm of J5, E22 at 28.4 mm.
- No 3D with the modules or the enclosure. Module outlines live on F.Fab, which C9 notes *"are not printed"*.
- R14: two module outlines still on each other's sockets.
- Standoffs: none (A12).
- **Effort:** 2 h for the map, 2 h for the 3D, 30 min for the outlines.

### C10 · Layout — **NOT MET**

| Sub-clause | Measured |
|---|---|
| *"Plane layers carry nothing but planes"* | ❌ **63 track items on In2.Cu** — `/LED_DRV2` 14, `/+5V_SENS` 13, `3V3_C` 10, `/LED_DRV1` 8, `/I2C0_SCL` 7, `/SENS_EN` 7, `+5V` 2, `/I2C0_MUX_SC0` 2. This is R12, and Table 14 row 7 names it |
| Antenna keep-out | ❌ none in the file (E3) |
| Spacing rules and a rule file matching the board | ⚠ 8 net classes now binding; **no `.kicad_dru` exists**, and R15's stale-rule point is unaddressed |
| Power copper: **pour ≥3 mm, six or more 0.3 mm vias per layer change** | ❌ the input is a 1.5 mm track — condition 3 is not met |
| Stitching: no pour point >10 mm from a ground link | ⚠ 233 vias, **plot not produced** (E1) |

**Effort:** 3–4 h. This is the largest single block of remaining layout work.

### C11 · Pins and control lines — **NOT MET. All five named defects are still present.**

This is the most important finding of the audit. C11 lists what it has "Seen so far" — five specific faults. Every one of them is still in the file:

| C11 "Seen so far" | Rule | Verified today |
|---|---|---|
| *"the radio's mode lines on the microSD pins"* | C11: **"GPIO10 to 14 are the board's own microSD"** | ❌ `/E22_M1` = GPIO10 (J1.16), `/E22_M0` = GPIO11 (J1.17). **J1.18/19/20 (GPIO12/13/14) sit unconnected — the remaining SD signals.** Table 14 row 5 requires *"nothing on J1 pins 16 to 20 (A7)"* |
| *"a reed input on an LED pin"* | C11: **"GPIO40 to 42 carry the board's LEDs and are outputs only, never inputs"** | ❌ `/REED_PULSE_F` = GPIO41 (J2.7) — an input on an output-only LED pin |
| *"two drivers on the modem's power enable"* | *"A line that two devices can drive has one of them removed"* | ❌ `/PWR_EN` = J1.7 (GPIO7) **and** U8.16 (expander) **and** R16 4.7 kΩ to GND |
| *"the watchdog kick on an expander that sits on the cabled bus"* | *"Nothing the board needs to recover sits on that bus"* | ❌ `/WDT_WDI` = **U8.11**, and U8's pads carry `/I2C0_SDA` and `/I2C0_SCL` — the expander is still on the cabled I2C-0 bus. **R17 is not done** |
| *"a push-pull supervisor output on the ESP32 board's enable pin, which its own reset button also drives"* | *"the supervisor's output is open-drain if anything else drives the same line"* | ❌ U4 pad 1 (`RESET`, push-pull on a TPS3823) drives `/RST_ESP`, which is also J1.3 — the Edgehax board's RST pin, which carries **its own RESET button and an internal pull-up** |

Two further C11 failures:
- **`/EVENT_BTN` is on GPIO3.** C11: *"GPIO0, GPIO3, GPIO45 and GPIO46 are strapping pins and must not be loaded at reset."* A button is a load. ❌
- **No signed pin map exists.** ❌
- One genuine success: the watchdog **chain is correct** — U4 pin 1 `RESET` → `/RST_ESP` → J1.3, pin 3 `MR` pulled up by R13, pin 4 `WDI` from U8.11, pin 5 `VDD`, pin 2 `GND`. The symbol's pin map was checked and the routing is electrically sound. **R2 is closed.**

**Effort:** 2 h for the pin moves and single-driver fixes, 1 h for the pin map, and R17's expander move is 3 h.

### C12 · Silkscreen and marking — **PARTLY MET**
- ✅ **Polarity on J18 is now correct and measured**: `+` box centre y 107.250 on pad 1 (`+5V_IN`), `−` box centre y 102.250 on pad 2 (`GND`), stroke font, 0.15 mm. **R3 closed.**
- ❌ No board name, no revision, no serial box on the silkscreen (E5).
- ❌ 124 silk-over-copper and silk-overlap items — C12 says *"clear them"*.
- ⚠ Marks needed by a person sit on F.Fab (module outlines, `J18 +5V IN`, `J5 MODEM 5V`, `J13 SPS30 5V`) — **F.Fab is not printed.**
- **Effort:** 30 min for the name/rev/serial, 3–4 h for the 124.

### C13 · The evidence documents — **NOT MET, none exist**

| Document | Status |
|---|---|
| Root readings with calipers, 1:1 test-fit print, side-on module photos | ❌ none (A1, A9, A10) |
| DC solve or simulation | ❌ none (G1) |
| Decoupling map | ❌ none (B7, B12, C7) |
| FMEA, 20–30 rows | ❌ none (G2) |
| Bring-up plan | ❌ none (G3) |
| Pin map and truth table | ❌ none (C13, A11) |
| README — earthing, switched-rail rules, USB service rule, terminal polarity | ❌ none (B6, R9, R6) |

**Effort:** 5–6 h total. These are the documents that close the most rows — C13 alone is the evidence for 11 items.

---

## 4. Table 14 — the next package, row for row

| Row | Requirement | Status | What is missing |
|---|---|---|---|
| 1 | Response sheet, all 59 + R1–R17, every P0 designed in and evidenced | ❌ 0 % | the file does not exist |
| 2 | 4-layer project + schematic PDF, ERC 0/0, DRC 0/0/0, parity clean | ⚠ 60 % | PDF not plotted; 1 ERC warning; 16 DRC errors; 129 warnings |
| 3 | Gerbers X2 + drill + IPC-356 + placement **with U4** + fab drawing | ❌ 0 % | and U4 is flagged out of the placement file |
| 4 | BOM with MPN, quantity, rating, temperature, plating, two variants | ❌ 0 % | no fields exist on any symbol |
| 5 | Module fit: readings, side-on photo, 1:1 test-fit, **signed pin map**, AS5600 port, A6 decision, **nothing on J1.16–20** | ❌ 10 % | A6 is now answerable; J1.16/17 violate the rule |
| 6 | Power: six conditions with the converter named, G1 results, supply resistances, decoupling map, B10 trace | ⚠ 20 % | converter named (LM2596HVS, 4.5–50 V); resistances partly measured; nothing else |
| 7 | EMC: antenna keep-out, ESD ≤5 mm incl. J24/J25, PE bond, E22 filter + **47 Ω on every cabled I2C line**, In2 as a plane | ❌ 10 % | 47 Ω on **4 of 14** lines; In2 has 63 items; no keep-out |
| 8 | Interfaces: RS485 decision, microSD archive, FDC1004, button and status light, **I2C recovery path** | ⚠ 25 % | RS485 deferral unagreed; microSD unusable; no recovery |
| 9 | 3D with modules on their right sockets + enclosure, standoffs, nothing under the modem | ❌ 5 % | outlines still swapped (R14); no standoffs |
| 10 | Bring-up plan and FMEA | ❌ 0 % | neither exists |

---

## 5. Table 11 — before you send

| Tick | Pass means | Today |
|---|---|---|
| C1 ERC 0/0 + title block | | ❌ 1 warning, wrong revision |
| C2 Update-PCB nothing; 0 unconnected, 0 parity, **no dangling** | | ❌ 5 dangling |
| C3 refill, save, DRC, plot with zone check, three times | | ❌ no plot |
| C4 Gerbers walked, IPC-356 in package | | ❌ |
| C5 no mismatch, no courtyard, no silk over pads, vias in pads handled | | ❌ 124 silk, courtyards ignored |
| C6 BOM fields, placement with every fitted part, job revision/finish/stack, fab drawing | | ❌ |
| C7 resistances with sources, heating <10 °C, ratings, simulation | | ⚠ partly measured |
| C8 events written, TVS stand-off, ESD ≤5 mm, PE bond | | ❌ |
| C9 decoupling map, 3D, nothing reachable under a module, standoffs | | ❌ |
| C10 planes only on plane layers, antenna area, rules match, power copper, stitching | | ❌ |
| C11 signed pin map, one driver per line, reset states, watchdog survives download, bus recovery | | ❌ |
| C12 polarity on the plotted silk, name, revision, serial box, no silk over copper | | ⚠ polarity only |
| C13 readings, simulation, decoupling map, FMEA, bring-up, README | | ❌ |
| 7 response sheet, every item, every unrequested change, evidence named, first in zip | | ❌ |
| 3 zip named with revision and date, one variant, nothing from the previous revision | | ❌ |
| *(one more)* zones refilled and saved in the project as shipped | | ✅ |

**2 of 16.**

---

## 6. The six conditions on the 5 V input

| # | Condition | Status |
|---|---|---|
| 1 | Converter set to **5.15 V ±1 %**, and that set point stated | ⚠ named (LM2596HVS, trim pot) — set point not yet written into the budget |
| 2 | Reverse + over-voltage cut-off that **disconnects below 5.5 V**, survives 12 V and 24 V indefinitely, limit ≈3.5 A | ❌ **not designed.** U10 is a placeholder |
| 3 | **Pour ≥3 mm** from J18 through the protection to the plane, **≥6 × 0.3 mm vias** at every layer change | ❌ today's input is a 1.5 mm track |
| 4 | Bulk and 100 nF at the pins, decoupling map | ⚠ B7 closed, B12 and C7 open |
| 5 | Converter→J18 lead **≤15 mΩ** (≈200 mm of 0.75 mm²) | ⚠ the lead is off-board and unmeasured; the board side is now 13 mΩ |
| 6 | The allocation: **15 mΩ lead + 60 mΩ board + 30 mΩ modem lead**, modem sees 4.75–5.25 V in a burst | ⚠ board budget now feasible (13 + 11.5 + contacts + FET ≈ 40 mΩ) — **not yet written up or signed** |

**Route C (discrete controller + low-Rds FET) is the only architecture that fits condition 6** — a 31 mΩ integrated switch makes the total 66 mΩ against a 60 mΩ allocation. That argument is written; the circuit is not.

---

## 7. The design register — all 76 items, re-statused today

Status words: **Done** · **Paper** (closed on paper, bench result owed) · **Partly** · **Open** · **New** (regressed or newly understood).

### 7.1 The 59 items (MS-CAR-REV-A-004 Table 9)

| Item | P | Now | What is left, in one line |
|---|---|---|---|
| A1 | P0 | Open | row spacing still unmeasured with calipers; E22 M1/M0 on the microSD pins, reed on an LED pin |
| A2 | P0 | Partly | truth table missing; spacing 34.00 mm unmeasured; supply per B10 |
| A3 | P1 | Partly | J5 is a screw terminal unlike the sensor ports; outlines on F.Fab, which is not printed; sockets unkeyed |
| A4 | P0 | Partly | two outlines on the wrong sockets; no heights; no enclosure in the 3D |
| A5 | P1 | Open | no GPIO map in the package |
| A6 | P0 | **Done-ready** | module identified from the shield marking: **ESP32-S3-WROOM-1 N16R8**, octal PSRAM, GPIO35–37 taken. Needs the decision written down |
| A7 | P0 | **New** | *"nothing on J1 pins 16 to 20"* — **violated**: J1.16 = `/E22_M1` (GPIO10), J1.17 = `/E22_M0` (GPIO11) |
| A8 | P0 | **Done** | J1/J2 at y 154.00, J3/J4 at y 113.56 — re-verified unchanged today |
| A9 | P0 | Partly | components-down drawn and pins mapped; the side-on photo is missing |
| A10 | P0 | Open | no readings, no 1:1 test-fit; 26.00 vs ≈26.2 and 34.00 vs ≈33.8 |
| A11 | P1 | Partly | RESET now wired (`/MODEM_RST` J1.6→J4.8 ✅); still two drivers on PWR_EN; no truth table |
| A12 | P1 | Partly | J5 is outside the modem footprint ✅; no standoffs; ESP32 unclamped; test points under the modem unverified |
| B1 | P1 | Done-ready | moves into the converter spec; **LM2596HVS 4.5–50 V** covers it |
| B2 | P1 | Done-ready | converter named, ≥40 V, 3 A, adjustable to 5.15 V |
| B3 | P1 | Open | F1 a 4 A PTC on glass-fuse clips; C13 a ceramic code on an electrolytic footprint; no BOM ratings |
| B4 | P1 | Partly | both input legs now 1.5 mm, 13 mΩ measured ✅; condition 3's 3 mm pour not met |
| B5 | P1 | Open | no per-mode budget written |
| B6 | P2 | Open | no README, no USB service rule |
| B7 | P1 | **Done** | C26/C27 now 2.1 and 2.4 mm from U6's pins |
| B8 | P1 | Done-ready | sits with the converter input; 50 V covers the 22–25 V disconnect |
| B9 | P1 | **New** | the planned sense pin **GPIO6 is now `/MODEM_RST`**. No ADC1 pin remains — see §8.5 |
| B10 | P0 | Open | six conditions partly met on numbers, none signed; no G1 results |
| B11 | P2 | Superseded | no buck on the board; record the reason |
| B12 | P1 | Open | four 100 nF still together; nothing within 41 mm of J5; E22 at 28.4 mm |
| C1 | P0 | Open | RS485 removal never agreed in writing — the deferral must be signed or the transceiver restored |
| C2 | P0 | **New** | CHK C11 states **GPIO10–14 are the microSD** → the slot is unusable while M1/M0 sit there. See §8.1 |
| C3 | P0 | Paper | FDC1004 port on CH5 with pull-ups and ESD; bench read owed |
| C4 | P0 | Partly | GPIO42 drives D6 on the carrier, not an outside lamp; J24 carries the visible lamps |
| C5 | P1 | Open | M0/M1 on separate pins but on the microSD pins |
| C6 | P1 | Open | expander still shares I2C-0 (verified); U7 reset is a power-on RC only |
| C7 | P1 | Open | 10 µF 5.3 mm from J13; 100 µF 28.5 mm; nearest 100 nF 22 mm |
| C8 | P1 | Open | ESD 5.4–21.8 mm from the pins; **none at all on J24/J25** |
| C9 | P2 | Open | J16, R5 and ESD3 still present with no stated purpose |
| C10 | P2 | Open | no build variants; antenna separation and LoRa scheduling unaddressed |
| C11 | P1 | Open | SPS30 on CH2; cable not specified; 72-hour run not planned |
| C12 | P2 | Paper | 1 kΩ + 100 nF on both ADC inputs; stability with the modem transmitting unproven |
| C13 | P1 | Partly | **J26 placed for the AS5600** ✅ but the device is not in the schematic and there is no pin map |
| D1 | P1 | **Done** | parity 0 and netlist re-proved today |
| D2 | P2 | Open | sheet still A0; revision still "Proto-Simple Rev 0.2" |
| D3 | P2 | Partly | ERC 0/1; **9 checks suppressed** (4 ERC + 5 DRC) with no justification |
| E1 | P1 | Paper | continuous plane with stitching; the stitching plot is not produced |
| E2 | P1 | **Done** | thermal reliefs; zone settings are the evidence |
| E3 | P1 | Open | no antenna keep-out on any layer |
| E4 | P2 | Open | 12 test points; three under the modem; none on I2C-1 or UART1; obsolete +12 V point |
| E5 | P2 | Partly | **J18 legend fixed** ✅; no board name, revision or serial box; rails unlabelled |
| E6 | P2 | Open | SIM, USB and microSD access not shown; **SIM side is now an open question — see §8.7** |
| E7 | P1 | Open | **47 Ω on 4 of 14 cabled I2C lines** — CH0/CH1 only; no input filter |
| F1 | P2 | Open | BOM has values and footprints only |
| F2 | P2 | Open | no Gerbers, no stack-up, no job file, no fab drawing, no IPC-356 |
| G1 | P0 | Open | no simulation; `!padne` directives still describe 12 V, D1, U1 and J9 |
| G2 | P1 | Open | no FMEA |
| G3 | P1 | Open | no bring-up plan |
| G4 | P2 | Open | no EMC test plan |
| H1 | P1 | Partly | PE clearance errors now 0 ✅; still no defined bond to ground, no arrestors on the antenna feeds |
| H2 | P1 | **New** | WDI routed ✅, but **U4 is `board_only` + excluded from the placement file**, push-pull supervisor on a buttoned net, and a stuck I2C-0 still survives a reset |
| H3 | P1 | Open | no temperature column; DS3231 suffix and backup cell unnamed |
| H4 | P1 | Open | no plating or coating in the BOM |
| H5 | P2 | Partly | enclosure chosen (200 × 155 × 80 mm); no glands, strain relief or drip loops |
| H6 | P1 | Open | no radio record (E22-900T22D, India band plan) |

### 7.2 The 17 items from Rev B (MS-CAR-REV-B-001 Table 13)

| Item | P | Now | Note |
|---|---|---|---|
| R1 | P0 | Open | 6-layer withdrawn; **the rule survives** — every future Gerber set must be refill → save → DRC → plot, with the three times recorded. Not yet exercised for Rev C |
| **R2** | P0 | **Done** | `/WDT_WDI` routed U8.11 → U4.4, unconnected 1 → 0, no jumper. Full chain verified against the symbol's pin map |
| **R3** | P0 | **Done** | `+` at y 107.250 on the `+5V_IN` pad, `−` at y 102.250 on GND, stroke 0.15 mm. README polarity line still owed |
| R4 | P0 | Open | U10 is a positioned placeholder, five pads unconnected. Blocked on the controller and on Serigreen's deviation sign-off |
| R5 | P0 | Partly | input now 1.5 mm both legs; **Q9 footprint mismatch cleared** ✅; the 3 mm pour and via arrays are not done |
| R6 | P1 | Open | Q2/Q3 gate networks still shared; no switched-rail firmware rules |
| R7 | P1 | Partly | RESET restored ✅; PWR_EN still has two drivers; PWRKEY held by 1 kΩ (now **confirmed correct** by the Parry guide's J2 jumper note) |
| R8 | P1 | Partly | TPS3828 not fitted; the supervisor is still a push-pull TPS3823-33 driving a net with the module's own button; U4 still out of the placement file |
| R9 | P1 | Partly | PE clearance errors 0 ✅; the bond to ground is still absent |
| R10 | P1 | Partly | J5 outside the modem outline ✅ (y 95.83 vs socket row at 113.56); test points under the modem unverified; standoffs none |
| R11 | P1 | **New** | the reed is still on GPIO41 — and C11 states plainly that **GPIO40–42 are output-only LED pins**. This is a named violation, not a judgement call |
| R12 | P2 | Open | 63 items still on In2 |
| R13 | P2 | Open | Q1/Q5/Q6 still 2N7000, unspecified at 2.5 V gate drive |
| R14 | P2 | Open | GY-521 and DS3231 outlines still swapped |
| R15 | P2 | Open | stale descriptions, F.Fab labels, J24 pin names, `!padne` directives, and **no `.kicad_dru` at all** |
| R16 | P1 | Open | vias-in-pads not re-counted since the library lands were rebuilt — **must be measured** |
| R17 | P1 | Open | **U8 is still on `/I2C0_SDA`/`/I2C0_SCL`** — verified today. The watchdog kick, PWR_EN, SENS_EN, E22_EN, LED_DRV1/2 and BUZZER_EN all hang off an expander on the cabled bus |

### 7.3 Counts

| | Done | Paper | Partly | Open | New | Superseded |
|---|---|---|---|---|---|---|
| 59 items | 5 | 3 | 15 | 35 | 1 | 1 |
| R1–R17 | 2 | 0 | 6 | 9 | 1 | 0 |
| **76 total** | **7** | **3** | **21** | **44** | **2** | **1** |

**P0 view (19 rows):** closed 4 (R2, R3, A8, D1-adjacent) · paper 2 (C3, C12) · open or new 13.
**Thirteen P0 items still block a fabrication release.**

---

## 8. Found by this audit — not in any register

### 8.1 The microSD question is settled, by the CTO's own document

Three sources disagreed. The tie-breaker is MS-CAR-CHK-001 §4 C11, which states it as a rule rather than as a claim:

> "ESP32-S3 pins that are not free on the EdgeHax board: … **GPIO10 to 14 are the board's own microSD**; **GPIO40 to 42 carry the board's LEDs and are outputs only, never inputs**."

Corroborated by the Edgehax diagram's own alternate-function labels — GPIO10 `FSPI-CS0`, GPIO11 `FSPID`, GPIO12 `FSPICLK`, GPIO13 `FSPIQ`, GPIO14 `FSPIWP` — a textbook 1-bit SPI card. And Espressif's WROOM-1 datasheet makes the Keyestudio page's alternative (io35/36/37/39) **physically impossible**, because on an N16R8 those three pins are the octal PSRAM.

**Conclusion: `/E22_M1` on GPIO10 and `/E22_M0` on GPIO11 collide with the microSD slot.** The 31 October plan to move them was right; last round's reversal was wrong, and it was based on a vendor page that cannot be true of the module in the photo.

### 8.2 The pin budget is short by two, and this is the real constraint

Of the 36 GPIOs on J1/J2, C11 reserves 19: GPIO0/3/45/46 strapping, 19/20 USB, 43/44 console, 35/36/37 PSRAM, 10–14 microSD, 40/41/42 LED-and-output-only. That leaves **17 input-capable pins, 19 of which are already allocated.**

Four signals must move and one clean free pin remains:

| Signal | Today | Why it must move | Candidate |
|---|---|---|---|
| `/E22_M1` | GPIO10 | microSD CS | GPIO40 (output-only rule satisfied — but the orange LED hangs there) |
| `/E22_M0` | GPIO11 | microSD MOSI | **GPIO15** — the only unreserved pin left |
| `/REED_PULSE_F` | GPIO41 | input on an output-only LED pin | GPIO39 (MTCK — JTAG already forfeit on 41/42) |
| `/EVENT_BTN` | GPIO3 | **strapping pin loaded at reset** — a C11 violation nobody had listed | needs a fifth pin |

**There is no fifth pin.** Either `/EVENT_BTN` moves onto the I/O expander (which is on the cabled bus — the thing R17 exists to stop), or GPIO38 is used against its "avoid repurposing" note, or a function is dropped. **This must be put to Serigreen as a proposal, which is exactly what their Appendix B invites.**

### 8.3 DRC passing is not evidence the copper is adequate — and it nearly fooled me twice

The project shipped with **one net class, `Default`, at 0.2 mm, and no net assigned to any class**. A 0.3 mm inner-layer track carrying the modem's 2 A was therefore invisible to every DRC run, including mine. Restoring Rev A's eight classes made 16 width errors appear instantly.

Two consequences: **the fab capability sheet (question F1/SQ) is still a guess**, and `min_text_thickness 0.08 mm` is our number, not the fab's — so "text_thickness 0" means "passes a rule we invented". Both belong in the response sheet as assumptions.

### 8.4 The release layout would re-break the schematic on the CTO's machine

`fp-lib-table` in both `4L\` and `pcb\` pointed at `${KIPRJMOD}/../../MORISHIELD/source/MoriShield_Carrier.pretty` — **a path that does not exist here**, producing 328 `lib_symbol_issues` and 113 `footprint_link_issues`. Repointing it cleared DRC from 164 to 132 and ERC from 441 to 0.

But the release layout (`morishield\morishield_hardware\`) uses `../libraries/` for both tables, and **its copy of `MoriShield_Carrier.kicad_sym` is stale** — pointing at it produces 328 mismatches again. **Shipping the release structure as it stands hands Serigreen a broken schematic.** The library must be refreshed or shipped beside the project.

### 8.5 B9's battery sense lost its pin

The plan put the 0–20 V battery divider on **GPIO6. GPIO6 is now `/MODEM_RST`.** Worse, every remaining ADC1 channel on the headers is allocated (1, 2, 4, 5, 7, 8, 9), and ADC2 is unreliable with Wi-Fi active — which the E3 answer says we will use.

Three options: the modem board's own `ADC` pin (0–1.8 V, documented, currently unconnected at J3.11); reclaim GPIO10/11 and accept no microSD; or move the FSR or soil ADC to the modem's ADC and free a channel. **This needs a decision, not a workaround.**

### 8.6 Nine suppressed checks, none justified

`missing_courtyard`, `track_not_centered_on_via`, `tuning_profile_track_geometries`, `footprint_filters_mismatch`, `footprint_type_mismatch` (DRC) and `single_global_label`, `four_way_junction`, `simulation_model_issue`, `footprint_filter` (ERC).

C5 says of courtyards: *"do not downgrade them to ignored."* `single_global_label` is what lets `/5V_PROT` pass today. `footprint_type_mismatch` ignored is likely hiding the SMD/thru-hole mismatch on the sockets. **D3 asks for one line per suppression; we have none, and two of the nine are hiding real classes of fault.**

### 8.7 A new mechanical question on the modem

The Parry guide lists **J8 (SIM socket) as "Back of PCB"**. The modem mounts **pins-down** on J3/J4. If the SIM socket is on the pad side, it faces the carrier and **the SIM cannot be changed once the board is installed** — which is a field-service requirement. Needs an answer before the enclosure is cut.

---

## 9. Blocking dependencies

| # | Dependency | Blocks | Owner | Ask |
|---|---|---|---|---|
| D-1 | **PWR_EN enable polarity** (which level turns the regulator on) | R7, A11, the truth table, the safe default state | Parry docs | A1 |
| D-2 | **RESET polarity and pulse width** | R7 pull direction | Parry docs | A2 |
| D-3 | **Route-C deviation sign-off** (TPS26630 is named in the review) | R4, B10, condition 2 — **a P0** | Serigreen | deviation request |
| D-4 | **E22 module part number and header pinout** — J6's pads are named `1…7` with no signal names | C11, E22 bring-up; possible 5 V on a mode pin | you, bench | B1 |
| D-5 | **microSD / PSRAM contradiction** on a board Serigreen supplies | A7, C2, C5, the pin budget, local logging | Serigreen | §8.1 write-up |
| D-6 | **RS485 deferral in writing** | C1 (P0) | Serigreen | response-sheet row |
| D-7 | **Fab capability sheet** — annular, track/gap, via fill and cap | R16, C5, the stack-up, every resistance figure | Serigreen / fab | F1 |
| D-8 | **SIM socket side** | A3, A4, E6, the enclosure cut | Parry docs or a photo | A3 |
| D-9 | **Pin budget — the fifth pin** | A7, C2, C5, R11, B9, C13 | Serigreen, with our proposal | §8.2 |
| D-10 | **Battery sense route** | B9 | you decide | §8.5 |

**Six of the ten need one message to Serigreen. Two need a multimeter. Two need a datasheet page.** None need a decision from us to start.

---

## 10. Prioritised action list

Order is by *what unblocks the most*, not by what is easiest.

### Now — no input needed (me)

| # | Action | Closes | Effort |
|---|---|---|---|
| 1 | Clear U4's `board_only` and `excl_POS` flags | C6, Table 14 row 3, H2 | **2 min** |
| 2 | Title block: Rev C, date, A3, one-line change note | C1, D2 | 15 min |
| 3 | Delete the 5 dangling tracks and vias | C2 | 20 min |
| 4 | Un-ignore `missing_courtyard` and `footprint_type_mismatch`, measure the real number | C5, D3 | 20 min |
| 5 | Count vias inside SMD pads | R16, C5 | 20 min |
| 6 | Move `/E22_M0` → GPIO15, `/REED_PULSE_F` → GPIO39, `/E22_M1` → GPIO40 | A7, C2, C5, R11 | 45 min |
| 7 | Remove U8.16 from `/PWR_EN`; R16 4.7 k → 100 k | R7, A11, C11 | 20 min |
| 8 | Refresh the stale `.kicad_sym` in the release libraries | §8.4 | 10 min |
| 9 | Add the stack-up; write the copper-weight assumption into the notes | C6, F2, §8.3 | 15 min |
| 10 | 47 Ω series on the 10 cabled I2C lines that lack them | E7, Table 14 row 7 | 60 min |
| 11 | Board name, revision and serial box on F.Silkscreen | C12, E5 | 20 min |
| | **Subtotal** | | **≈ 5 h** |

### Next — needs one input each

| # | Action | Needs | Effort |
|---|---|---|---|
| 12 | Route-C controller search (5 V gate drive **and** ≈5.4 V trip) | — | 45 min |
| 13 | Draw U10: controller, N-FET, gate resistor, zener, bulk | 12, D-3 | 60 min |
| 14 | Re-rate D2 and ESD16 above the converter's highest output | 12 | 20 min |
| 15 | 3 mm pour J18 → protection → plane, ≥6 vias per layer change | 13 | 2–3 h |
| 16 | Move `/EVENT_BTN` off GPIO3 | D-9 | 30 min |
| 17 | Battery sense decision | D-10, §8.5 | 30 min |
| 18 | Open-drain supervisor (TPS3828) or a series resistor on `/RST_ESP` | D-2 | 30 min |
| 19 | Move U8 to I2C-1; drive U7 reset from the ESP32 | R17, C6 | 3 h |
| 20 | ESD arrays within 5 mm at J11–J17, J20–J26; add them to J24/J25 | C8, Table 14 row 7 | 3 h |
| 21 | PE bond link beside the sensor ports + README scheme | H1, R9, C8 | 45 min |
| 22 | Antenna keep-out rule area on all copper layers | E3 | 45 min |
| 23 | Move the 63 In2 items to outer layers | R12, C10 | 2–3 h |
| 24 | 124 silk items | C5, C12 | 3–4 h |
| 25 | Module outlines on the right sockets, with heights | A4, R14 | 1 h |
| 26 | 3D with both modules and the 200 × 155 × 80 box | A4, C9 | 1.5 h |
| 27 | Decoupling map, supply pin by pin | B12, C7, C9 | 1 h |
| 28 | BOM with Manufacturer, MPN, Rating, Temp, Variant | F1, H3, H4 | 90 min |
| 29 | Signed pin map + truth table | A5, C13, A11 | 60 min |
| 30 | README, FMEA, bring-up plan, EMC plan | G2, G3, G4, B6 | 4 h |
| 31 | DC solve / simulation for all six G1 cases | G1, B10 | 3 h |
| 32 | Caliper readings, 1:1 test-fit, side-on photos | A1, A9, A10 | 2 h |
| 33 | Response sheet (76 rows), reply, ERC/DRC reports, PDF, checksums, zip | Table 14 rows 1–2 | 3 h |
| 34 | Gerbers, drill, IPC-356, job file, fab drawing | C3, C4, F2 | 60 min |
| | **Subtotal** | | **≈ 36 h** |

**Total to full compliance: ≈ 41 hours of design and document work, plus the bench items that can only be done on built boards.**

---

## 11. Roadmap to full compliance

| Stage | Date | Gate to pass | Ships |
|---|---|---|---|
| **S1 — schematic-only pass** | **2 Nov** | CHK §3 note: schematic PDF + ERC report + response sheet. Actions 1–5, 8–9, 11 done; the 13 open P0s declared with their questions attached | 10 files |
| **S2 — protection and pins** | 5 Nov | Actions 6–7, 10, 12–18. ERC 0/0. R4 designed, A7/C2/C5/R11 closed | revised project + updated sheet |
| **S3 — layout completion** | 9 Nov | Actions 19–27. **DRC 0 errors, 0 warnings**, no dangling, courtyards honest | board + renders + maps |
| **S4 — fabrication release** | 12 Nov | Actions 28–34. **All 16 Table 11 ticks pass.** Gerbers plotted after a clean DRC on the saved file, three times recorded | full release zip |
| **S5 — first-article evidence** | boards + 7 d | C3, C12, A2, B10, C11, R7, R17 bench results; G4 EMC | evidence pack |

**S1 is a review pass, not a release.** It is explicitly invited by CHK-001 §3 — *"A schematic-only pass is quick and usually saves a layout loop"* — and it should say so in its own header so nobody mistakes it for a release request.

---

## 12. Where we actually stand

**Better than Rev B on every measurable axis:** ERC 328 warnings → 1. Unconnected 1 → 0. Parity 211 → 0. Footprint mismatches 3 → 0. Net classes 1 → 8, binding. Clearance errors 0 → 0 *with real rules behind them now*. The two P0s the review led with — R2 and R3 — are closed and independently verified.

**Not closer to release on the thing that matters most:** the release gate is a package, and **there is no package.** Zero of the eight files in CHK Table 2 exist. Thirteen P0 design items are open, and four of them (R4, B10, G1, C1) are the ones the review leads with.

**And three things this audit found that no register row covered:** the CTO's own release check settles the microSD conflict against us (C11 states GPIO10–14 are the SD); the pin budget is short by one pin after four signals move; and the release layout's stale symbol library would hand Serigreen a schematic with 328 warnings.

**The single most useful thing to do today is not a design change.** It is the one message to Serigreen carrying D-3, D-5, D-6, D-7 and D-9 — five of the ten blocking dependencies sit with them, and three of the thirteen open P0s cannot move until one of those five comes back.
