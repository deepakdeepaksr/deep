# MoriShield Carrier — Rev C (4-layer) Task Sheet and TODO Register

| | |
|---|---|
| **Document** | TS-CAR-4L-RevC-01 |
| **Date** | 30 October 2026 |
| **Board** | MoriShield_Carrier, 4-layer only (`4L\MoriShield_Carrier.kicad_pcb`) |
| **Round** | This sheet prepares package **3**: our internal **v3**, the CTO's **Rev C**. The submitted 4L package is our **v2** (CTO: Rev B); the pre-4L board is our **v1** (CTO: Rev A). See §0.6. |
| **Driven by** | MS-CAR-REV-A-004 v1.0 (16 Oct 2026 — the 59 items), MS-CAR-REV-B-001 v1.0 (29 Oct 2026 — status, R1–R17, the six conditions), MS-CAR-CHK-001 v1.0 (30 Oct 2026 — the procedure) |
| **Team** | Deepak (hardware and electronics), Aswin (firmware and software) |
| **Contact and signatory** | **Aswin** — single point of contact with Serigreen, signs the reply |
| **Delivery** | **2 November 2026: schematic-only package** (G1b): schematic PDF, ERC, response sheet, cover message, six-condition plan, pin map and truth table. Layout and production files follow as a second package; date to be set. |
| **Status** | Working plan. Rev B is **not released for fabrication**. Nothing is ordered before Serigreen's written release, which names the files by checksum. |

**Scope decisions already taken by Serigreen (do not revisit):**

1. The **4-layer board goes forward**; the **6-layer is withdrawn** (review §9, R1). The 6L folder is frozen — archive it, do not carry anything from it into the next package except the capacitor-spread lesson (B12).
2. The **5 V input at J18 is accepted on the six conditions** of review §6.4. B10 closes on a bench trace at the modem board's own input.

**What this sheet is:** the complete, item-by-item work plan for the next package — 59 carried items (A1–H6) plus 17 new items (R1–R17), the decisions that must be settled before drawing, the evidence each item needs, and the checks to run before sending. It is also the seed of the response sheet that must be the **first file in the next zip** (CHK §7).

---

## Read this first

1. **The item text is authoritative, not this sheet.** Where this sheet compresses an item, the document wins. 004's Table 9 carries the 59 items with their own "closed when" column; 003 carries the module pin map and §9; both are in `cto remarks\old remarks\`, and both are quoted in §5 here.
2. **Every change answers an item.** A change nobody asked for is agreed by message **before** it is drawn (CHK Rule 3). Log it in the response sheet with status "Agreed before drawing".
3. **Check the file you ship.** Refill → save → DRC on the saved file → plot, in that order, every time, however small the edit (CHK C3). The 6L Gerber short is exactly this failure.
4. **The files are the evidence.** "Fixed" and "checked" are not evidence; layer, area, reference designator, page and measurement are.
5. **Send the schematic-only package early.** It is cheap, and Serigreen says it may save a layout loop (review §12 step 5, CHK §3).

---

## 0. Ground rules

### 0.1 Status vocabulary (use these words everywhere, including the response sheet)

| Status | Meaning |
|---|---|
| `TODO` | not started |
| `WIP` | in progress |
| `DONE` | designed in **and** evidenced in the files being shipped |
| `DEFERRED` | agreed in writing by Serigreen, with the agreement named (date, message reference) |
| `REJECTED` | with the reason, agreed by Serigreen |
| `SUPERSEDED` | the design change removed the item (only B11 today) |

### 0.2 Owners, sizes, gates

* Owners: **HW** = Deepak, **HW+FW** = both. Firmware-owned items are marked **FW**.
* Size: **S** ≤ half a day, **M** ≤ 2 days, **L** > 2 days (relative, not a commitment).
* Gates: **G0** decisions → **G1** schematic freeze → **G2** layout → **G3** evidence → **G4** final check → **G5** send. Nothing advances a gate with an open P0 in its own scope.

### 0.3 Evidence convention

```
4L\_qa\revC\
    ResponseSheet_RevC.csv          <- first file in the zip
    G1\  G2\  ...  R17\             <- one folder per item, evidence inside
    maps\   decoupling_map.csv, pin_map.csv, truth_table.csv
    reports\ erc.json, drc.json, parity.txt, board_stats.txt
    fab\    gerber\, drill\, ipc356\, fab_drawing.pdf
    pkg\    (staging copy of exactly what ships)
```

Evidence must be readable by someone who has never seen the board: **file + layer/area + refdes + value**. Screenshots are acceptable only when they show the value (a highlighted net, a measured distance in the Measure tool, a register readout).

### 0.4 Repository guardrails (project conventions, already agreed)

1. **Backup before any modification:** timestamped copy of `.kicad_pcb` / `.kicad_sch` (e.g. `_backup\RevC_step1_20261102_1015.kicad_pcb`).
2. **Copper census guard:** before and after every scripted edit, count tracks, vias and per-net copper; a silent loss must fail the run.
3. **Routing:** 0° / 45° / 90° only. Net classes: PE 1.0 mm, Power_5V 1.0 mm, Power_5V_IN 2.0 mm (input path raised to **3 mm pour** by condition 3 — the wider figure wins), 3V3 0.6 mm, Signal/GND 0.3 mm unless a rule says otherwise.
4. **No hand-edited footprints.** Any mismatch is fixed by updating from the library (CHK C5). Q9 is the standing example.
5. **Refill → save → DRC → plot**, with "Check zone fills before plotting" on (CHK C3).
6. **Nothing stale travels:** no files from Rev B, no scratch scripts, no `.history`, no 6L content. `_release\pack.ps1` already refuses scratch files and scans for tooling references — keep it that way.
7. **Deliverable documents** are written as neutral engineering prose: results and measured facts only, no tooling provenance.

### 0.5 Source documents — all four are now in the repo

| Document | File | Use in this sheet |
|---|---|---|
| **MS-CAR-REV-A-004 v1.0** — fabrication readiness, §6.2 Table 9 = **the 59 items**, each with its own "closed when" | `cto remarks\old remarks\MoriShield-Carrier-FabReadiness-v1.0.pdf` | authoritative acceptance wording for A1–H6 (quoted in §5) |
| **MS-CAR-REV-A-003 v1.1** — module fit, §9 pin map, module dimensions | `cto remarks\old remarks\MoriShield-Carrier-ModuleFit-Review-v1.1.pdf` | pin-map baseline; A1–A12 |
| **MS-CAR-REV-A-001 v1.2** — Rev A design review | `cto remarks\old remarks\MoriShield-Carrier-RevA-Review-v1.2.pdf` | background for the v1.2 items |
| **The old design files** reviewed by 001/003/004 — 2-layer board, 48 parts, 168 × 118 mm, U1 (AMS1117), J9 (buck socket), D1, JST J5, no watchdog/expander/mux | `cto remarks\old remarks\design\MoriShield_Carrier.kicad_pcb` / `.kicad_sch` (schematic is A3 with an empty title block) | reference only — read it to understand an item, never copy from it |
| **MS-CAR-REV-B-001 v1.0** — Rev B package review, §1–§12 + R1–R17 | `cto remarks\MoriShield-Carrier-RevB-Review-v1.0.pdf` | current status, the six conditions, the new items |
| **MS-CAR-CHK-001 v1.0** — release check | `cto remarks\MoriShield-Carrier-ReleaseCheck-v1.0.pdf` | procedure, response sheet, C1–C13 |

Plain-text extracts of all five PDFs are in `_cto_extract\` (one `.txt` per document, page-marked) so the tables can be searched and quoted without opening the PDFs.

Still to request from Serigreen:

| # | Item | Why |
|---|---|---|
| T0-01 | Converter datasheet (the part chosen under condition 1) | Conditions 1–2 and G1 cannot close without it |
| T0-02 | The two build-variant definitions (C10) | F1's Variant column needs them |
| T0-03 | RS485 supply intent, if DEC-1 restores RS485 | 004's C1 assumed a switched **12 V** through a PTC; the 12 V rail is now off-board, so the transceiver's supply must be stated |
| T0-04 | The enclosure choice (H5) or the three candidate boxes | A4's 3D check needs a box |
| T0-05 | Fab capability sheet (annular 0.15, track/gap 0.2, via fill/cap) | Decides R16 and the constraint set (SQ21) |
| T0-06 | Modem board schematic, or a note on its PWRKEY/RESET translator | A11, R7 (SQ11) |
| T0-07 | Module marking photo for the ESP32 board | A6 (SQ5) |
| T0-08 | Earthing intent — earth rod, box bonding, installer's bond | R9 README (SQ17) |

### 0.6 Revision and document map — read before naming anything

| Round | Our name | CTO's name | What was submitted | Files | CTO's response |
|---|---|---|---|---|---|
| 1 | v1 | **Rev A** (package "v3", 12 Oct) | 2-layer board; 12 V input with an on-board buck; RS485; 48 parts; 168 × 118 mm; no watchdog, expander or I2C switch | `cto remarks\old remarks\design\` | `old remarks\`: A-001 v1.2, A-003 v1.1, **A-004 v1.0 — the 59 items** |
| 2 | **v2** | **Rev B** (27 Oct) | the 4L + 6L package; the 4L is 4-layer, 157 parts, 178 × 118 mm | `4L\` (the board we work on), `6L\` (withdrawn) | `cto remarks\`: **B-001 v1.0** + CHK-001 v1.0 |
| 3 | **v3** | **Rev C** (to be submitted) | 4L only | this repo, after the work in §4 | — (this sheet prepares it) |

Rules that follow:

1. **Use the CTO's label first in everything we send**: "Rev C", with our internal number in brackets only if it helps — "Rev C (internal v3)". Never call the 4L package "v2" in a document Serigreen will read; to them it is Rev B.
2. **One string everywhere**: title block, job file, folder and zip all read `Rev C`; the zip is `MoriShield_Carrier_RevC_<date>.zip` (SQ27 confirms the label).
3. **The old design is reference only.** Its stack-up, parts and rules are the ones the 59 items criticised; read it to understand an item, never copy from it.
4. **Round 1 items are not reopened.** Items already closed (A8, C3, C12, D1, E1, E2) stay closed; the response sheet records them as done, with the evidence from this round.

---

## 1. Baseline verified on 30 October 2026

Everything below was read from the folder today. The ERC/DRC figures were produced by a **read-only** re-run (`kicad-cli` with `--refill-zones`, no `--save-board`); no project file was modified.

### 1.1 Files and reports

| Fact | Value today | How verified |
|---|---|---|
| Board | 178.15 × 118.15 mm, 157 footprints, 72 nets | `pcbnew` load of `4L\MoriShield_Carrier.kicad_pcb` |
| Board saved | 27 Oct 2026 19:43:48 | file timestamp |
| Production set (Gerbers, drill, job file) | 27 Oct 2026 **16:12:05** | file timestamps |
| → consequence | **The shipped production set is older than the board it claims to represent.** Stale by definition (CHK C3). | — |
| Job file | `Revision: "rev?"`, `Finish: "None"`, no stack-up | `MoriShield_Carrier-job.gbrjob` |
| BOM (current export) | 153 rows, columns `Refs, Value, Footprint, Qty, DNP`; no manufacturer, MPN, rating, temperature or variant | `_qa\fab\MoriShield_Carrier-bom.csv` |
| Placement | 141 parts; **U4 absent** | `_qa\fab\MoriShield_Carrier-pos.csv` |
| Title block | paper **A0**; title "MoriShield Carrier Board"; date 2026-10-22; rev **"Proto-Simple Rev 0.2 (Post-RS485 Stripped)"** | `MoriShield_Carrier.kicad_sch` |
| README | none | folder listing |
| Custom rules file | none (`*.kicad_dru` absent); net classes = one **Default** class only (0.2 mm clearance/width, via 0.6/0.3) | project file |
| 004 / 003 / 001 review documents | **present** under `cto remarks\old remarks\` (FabReadiness, ModuleFit, RevA) | folder listing |

### 1.2 Re-run results today (saved files)

| Check | Result | Detail |
|---|---|---|
| ERC | **0 errors, 0 warnings** | with four check classes ignored project-wide: `single_global_label`, `four_way_junction`, `simulation_model_issue`, `footprint_filter` |
| DRC (refilled in memory) | **0 errors, 134 warnings** | 78 silk-over-copper, 46 silk-overlap, 5 dangling vias, 2 dangling tracks, 2 silk text thickness, 1 library footprint mismatch (Q9) |
| Unconnected | **1** | `/WDT_WDI`: U8 pad 17 track ends at via (257.0, 168.1); the other island ends at via (244.5, 173.5) — 13.6 mm apart (R2) |
| Schematic parity | **209 differences** | 133 `footprint_symbol_mismatch`, 58 `net_conflict`, 14 `footprint_symbol_field_mismatch`, 4 `extra_footprint` |

> The Rev B package shipped an *older* ERC (522 warnings: 328 library-symbol, 194 off-grid) and DRC than the current files. Both are now cleaner, but **no report in the folder matches the files that will be shipped** — regenerate everything at G4 (T9-02).

### 1.3 Board facts confirmed by direct measurement

| Fact | Value | How verified |
|---|---|---|
| Vias inside SMD pads | **65** of 224 vias | geometric hit test, all SMD pads |
| Copper on In2 | 448.4 mm on 8 nets; **431.3 mm on the seven nets named in R12** (LED_DRV1 100.8, LED_DRV2 109.8, +5V_SENS 76.8, 3V3_C 63.0, SENS_EN 52.6, I2C0_SCL 22.5, I2C0_MUX_SC0 5.7); plus a 17.1 mm +5V stub | track lengths by net and layer |
| Copper on In1 | **0 mm of track** — ground plane is clean (E1 stands) | track lengths by layer |
| Zones | 5 filled: GND (In1, 19 741 mm²), +5V (In2, 16 074 mm²), 3V3_SENS_SW ×2 (In2), PE (B.Cu, 2 043 mm²) | zone list |
| Rule areas / keep-outs | **0** (E3 stands) | zone list, `rule_area` absent |
| U4 attributes | 28 = board-only + exclude-from-BOM + exclude-from-position | footprint attributes |
| J18 | pad 1 `+5V_IN` at y 107.25; pad 2 `GND` at y 102.25; silk `"5v +"` at y 100.50, `"5v -"` at y 107.00 | pad nets + silk items (R3 confirmed) |
| Q9 | SOT-23, the single `lib_footprint_mismatch` in DRC | DRC violations (R5 confirmed) |
| Sockets | J1–J2 26.00 mm, J3–J4 34.00 mm; J1/J2 at y 154.00, J3/J4 at y 113.56 | footprint positions (A8 stands) |
| I2C topology | U7 pads 22/23 and **U8 pads 22/23 both on `/I2C0_SCL` and `/I2C0_SDA`** | pad nets (R17 confirmed) |
| Sensor-rail gates | Q2 and Q3 share `/SENS_GATE` only | pad nets (R6 confirmed) |
| Panel ports | J24 `+5V, LED1_K, LED2_K, GND`; J25 `+5V, BZ_NEG`; no ESD fitted | pad nets (C8 confirmed) |
| Test points under the modem | TP2 (274.75, 138.50), TP3 (275.75, 132.75), TP5 (276.25, 126.50) | footprint positions (R10 confirmed) |
| Watchdog part | TPS3823-33 fitted; TPS3828 not present | schematic symbol values (R8 confirmed) |
| DC-solve directives | still `VOLTAGE v=12V p=J18.1 n=J18.2`, `REGULATOR p=U1.2 …`, `J9` — Rev A | schematic directive text (G1/R15 confirmed) |

### 1.4 What the baseline implies — do these, not just edits

1. **Regenerate, do not incrementally patch, the production set.** Gerbers, drill, job file, IPC-356, placement, BOM, fab drawing must all be produced from the Rev C board at G4.
2. **The 6L staleness lesson applies to the 4L too**, merely by timestamps: any plot made before the last save is suspect. Record the three times (save, DRC, plot) in the response sheet.
3. **Parity must actually be clean** (0, not 209 "benign"). Serigreen counts parity differences; the gate says clean parity.
4. **The ERC ignore list is itself evidence.** Keep only ignores that are justified in one line each (four today); ideally fix the underlying conditions so the list shrinks.
5. **The 65 vias-in-pads must be resolved as a layout task**, not as a fab note by reflex — a hand-assembled board with unfilled vias in pads starves joints (CHK C5).
6. **One net class is not enough** for the spacing rules the CTO states (Power, PE 0.5 mm, >15 V 0.3 mm). Add them and a `.kicad_dru` that names only nets on this board.
7. **64 of the 65 board facts above are unchanged since the review** — the reviewed package is the current package. No work has started.

---

## 2. Decisions to close before drawing (G0)

These are **not** drawing tasks. Each one changes the schematic; drawing before deciding is the documented cause of lost loops (CHK §5).

| ID | Decision | Needed from | Blocks | Default if unanswered |
|---|---|---|---|---|
| DEC-1 | **RS485: restore or defer in writing** (C1, P0) — either the fault-protected 3.3 V transceiver with termination jumper, fail-safe bias, TVS to earth and pins on GPIO38/39 as 003 planned, or a written deferral. If it returns, say what supplies the transceiver now that the 12 V rail is off-board (004 assumed a switched 12 V through a PTC) | Serigreen | Pin map, A6, C13, layout | Cannot proceed; C1 is P0 |
| DEC-2 | **ESP32 module variant** (A6, P0) — non-octal EdgeHax preferred: it frees GPIO35–37 and settles reed + AUX | Serigreen + module marking photo | A1, A7, C2, C5, R11 | Keep N16R8 octal → reed needs GPIO39 and AUX must move |
| DEC-3 | **Converter part** (condition 1) — named part, ≥40 V input, 5.15 V ±1 %, 3 A at +70 °C, ≤50 mV droop, fuse + surge | Serigreen/hardware | J18 protection sizing, copper, B5, G1 | Cannot size the 5 V path |
| DEC-4 | **J18 protection architecture** (condition 2) — eFuse (TPS26630/31) vs OV/reverse controller + low-Rds FETs; D2/ESD16 re-rating | Hardware | R4, R5, copper, silk legend | eFuse meets 60 mΩ only at typical values — prefer controller + FETs |
| DEC-5 | **Status light definition** (C4, P0) — is the status light D6 on the carrier (GPIO42) or a panel lamp on J24? | Serigreen | C4, E5 labels | State D6 in writing |
| DEC-6 | **PWRKEY behaviour** (A11) — does the modem board's translator make a 1 kΩ pull-down "pressed", i.e. automatic power-on? | Modem board documentation / bench | R7, A11 truth table | Keep pull-down if A11 confirms automatic power-on |
| DEC-7 | **Battery sense** (B9) — divider on GPIO6 fed by its own lead from the battery, since the board now sees 5 V only | Serigreen/hardware | B9, C13 | Add divider; state divider ratio and full-scale |

**Exit G0:** all seven written down (message + date) and copied into the response sheet's "Agreed before drawing" rows.

> These seven are asked as **SQ2, SQ3, SQ4, SQ5, SQ10, SQ11 and SQ16** in the single message of §10, so the team sends one list, not three.

---

## 3. Gate plan

| Gate | Exit criteria | Evidence produced | Owner |
|---|---|---|---|
| **G0** Decisions | DEC-1…DEC-7 answered in writing | Message log, `revC\decisions.md` | HW+FW |
| **G1** Schematic freeze | All schematic-scope items done (WP1–WP4 schematic parts); ERC 0/0; title block Rev C; pin map + truth table signed; response sheet drafted | `revC\G1\`, `erc.json`, `pin_map.csv`, `truth_table.csv` | HW+FW |
| **G1b** Schematic-only review — **2 Nov 2026** | Schematic PDF + ERC 0/0 + draft response sheet + cover message + six-condition plan + pin map/truth table sent to Serigreen | `revC\G1\` | Aswin |
| **G2** Layout | Layout-scope items done (WP5–WP6); zones refilled and saved; DRC 0/0/0 with parity on the saved file | `drc.json`, `parity.txt`, screenshots | HW |
| **G3** Evidence | WP8 documents complete: G1 model, decoupling map, 3D, FMEA, bring-up, readings, budget | `revC\G1…G4\`, maps | HW+FW |
| **G4** Final check | CHK C1–C13 all pass on the files in the zip; three timestamps recorded; BOM/POS/job/fab drawing consistent | `revC\reports\final_checklist.md` | HW |
| **G5** Send | Zip `MoriShield_Carrier_RevC_YYYY-MM-DD.zip`, response sheet first, checksums recorded | `_release\` | HW |

---

## 4. Work packages

Work is grouped so that each package can be started and finished without waiting on another, except where a dependency is stated. Item IDs in **bold** are closed by the task.

### WP1 — 5 V input, protection and copper (the accepted-on-conditions block)

**Goal:** J18 survives a reversed supply, 12 V and 24 V; the modem board holds 4.75–5.25 V in a burst; the input copper is sized for the protection's fault current.

| Task | Items | What to do | Owner | Size |
|---|---|---|---|---|
| T1-01 | B10, cond 1–2 | Close DEC-3 and DEC-4 on paper: named converter, protection part, allocation table (converter 5.15 V ±1 %, 50 mV droop, 15 mΩ lead, 60 mΩ board, 30 mΩ modem lead). Write the allocation into `revC\cond6_budget.md`. | HW | M |
| T1-02 | R4, B10 | Redraw the J18 block: reverse protection + over-voltage cut-off that disconnects **before the rail reaches 5.5 V**, survives 12 V/24 V indefinitely, current limit ≈3.5 A; gate resistor + ~10 V gate-source zener if any FET stays in the path; re-rate **D2 and ESD16** (stand-off above the converter's highest output, leakage counted in the budget). | HW | M |
| T1-03 | R5, B3 | Q9: either reverse it properly (drain to J18, source to load, gate to ground + zener) or delete it in favour of the protection part; **restore the library footprint** either way (today's DRC still reports the mismatch). | HW | S |
| T1-04 | B3, R5 | F1: replace the 4 A PTC on a 5×20 mm glass-fuse clip footprint with a part and footprint that match; put the rating in the BOM; verify C13's footprint matches its value. | HW | S |
| T1-05 | R5, B4, cond 3 | Layout: J18 → protection → In2 at **≥3 mm pour**, **≥6 × 0.3 mm vias** at every layer change, sized for the protection's limit (not hold) current; measure J18→J5 both conductors at +70 °C and fill the resistance table (review Table 5 replacement). | HW | M |
| T1-06 | R3, B10 | Swap the J18 silkscreen so "+" is beside pad 1 (`+5V_IN`, y 107.25) and "−" beside pad 2 (`GND`, y 102.25); check on the **plotted** silk Gerber, not the canvas; add the polarity to the README. | HW | S |
| T1-07 | cond 4 | Bulk at J5: **470 µF low-ESR (105 °C, ≥16 V) + 10 µF + 100 nF within 10 mm along the copper** (today: 100 nF at 41.5 mm, 10 µF at 75 mm). | HW | S |
| T1-08 | cond 6, B10, A2, C3, C12 | Write the **first-board bench plan** that closes the items that need hardware: the B10 trace (converter at its lowest set point, modem board's own input, LTE attach with GSM forced), modem registering on the network (A2), reverse / 12 V / 24 V one minute each with the cut-off below 5.5 V (R4), FDC1004 read at installed length with the modem transmitting (C3), ADC readings stable during bursts (C12). One page, instrument + node + pass value per line. Confirm bench access first (SQ26). | HW+FW | S |

**Done when:** DRC shows no footprint mismatch; the resistance table shows ≤60 mΩ at +70 °C; the silk Gerber shows "+" at pad 1; the bench plan names the instrument, the node and the pass window.

### WP2 — Power distribution, switched rails and decoupling

**Goal:** every load sees its capacitor where the load is; the sensor rails actually turn off; the power budget exists.

| Task | Items | What to do | Owner | Size |
|---|---|---|---|---|
| T2-01 | R6 | Separate gate networks for Q2 and Q3: each PFET pulled up to **its own source**, both gates pulled down by **one** enable (a second N-FET, or two diodes from Q4's drain). Target: 5 V sensor rail < 0.1 V when off with the SPS30 fitted. | HW | M |
| T2-02 | R6, B6, C10 | README and firmware rules: never enable a switch channel while its rail is off; hold UART1, M0 and M1 low while Q7 has the E22 switched off; USB service rule; **LoRa traffic scheduled away from modem bursts** (C10). | FW | S |
| T2-03 | B7 | Move C26/C27 to ≤3 mm from U6's pins **along the copper** (today 11.6 and 9.3 mm straight line). | HW | S |
| T2-04 | B12 | Break up the four 5 V 100 nF capacitors that sit together in the top-right corner (C3, C14, C41, C42): one at each load (J5, E22 J6 pin 2, modem UART reference J4 pin 3, ESP32 5 V pin J1 pin 21). E22 10 µF ≤10 mm; UART reference 100 nF ≤5 mm. | HW | M |
| T2-05 | C7 | SPS30 (J13): 100 µF within 10 mm, 100 nF within 5 mm (today 28.5 mm and ~22 mm); if 10 mm proves impossible, record the stated reason (SQ24). | HW | S |
| T2-06 | B5 | Power budget per operating mode (idle, sensors, LoRa TX, Wi-Fi TX, modem burst, all-peak), including D3/D4 always-on, TVS/ESD leakage, converter no-load. Table + one-line assumption per row. | HW+FW | M |
| T2-07 | G1 | Feed the budget into the G1 model (T8-01) so the two agree. | HW | S |

**Done when:** the decoupling map (T8-02) shows every supply pin inside its limit; the budget covers every load in Appendix A of the review; the 5 V sensor rail off-state is a bench line, not a claim.

### WP3 — Watchdog, reset, control lines and I2C robustness

**Goal:** a firmware hang resets the board, flashing still works, and no single stuck cable can lock the board.

| Task | Items | What to do | Owner | Size |
|---|---|---|---|---|
| T3-01 | R8, H2 | Replace **TPS3823 (push-pull) with TPS3828 (open-drain)** so the ESP32 reset button and USB auto-reset are not fought. Clear U4's three flags (board-only, exclude-from-BOM, exclude-from-position) — today attributes = 28. | HW | S |
| T3-02 | R8 | WDI source: a pin high-impedance through reset **and** USB download (TPS382x treats floating WDI as watchdog-off), or the expander with a **series jumper** for flashing plus firmware that kicks within 0.9 s. Decide, draw, and state the choice in the pin map. | HW+FW | M |
| T3-03 | R2 | Route `/WDT_WDI`: the two islands end at vias (244.5, 173.5) and (257.0, 168.1), 13.6 mm apart. Delete the dangling copper the same DRC lists: 13 mm 3V3_C stub on B.Cu, 1 mm EVENT_BTN track, dangling vias on PWR_EN, I2C0_SDA, BUZZER_EN (5 dangling vias + 2 dangling tracks today). | HW | S |
| T3-04 | R17, C6 | Move **U8 to I2C-1** (today U7 pads 22/23 and U8 pads 22/23 are both on `/I2C0_SCL`/`/I2C0_SDA`), and reset **U7 from the ESP32** (supervisor reset line or a GPIO) instead of the power-on RC only. Firmware: bus-recovery routine (nine clocks, re-init). | HW+FW | M |
| T3-05 | R7 | One driver per modem line: delete the expander driver on PWR_EN (keep GPIO7); R16 keeps it low in reset; PWRKEY per DEC-6 (keep 1 kΩ to ground only if A11 confirms automatic power-on, else a GPIO). | HW | S |
| T3-06 | A11 | Truth table: every control line, its reset state, who drives it, and what that state means for the module (off/on/pressed). Include PWR_EN, PWRKEY, SENS_EN, E22_GATE, LED_DRV, BUZZER_EN, I2C_SW_RST, WDI. | FW | S |
| T3-07 | R8, R17, H2 | Bench plan: firmware hang ends in a reset; USB flashing works with the watchdog fitted; SDA held low on a cabled port recovers without a power cycle. | FW | S |

**Done when:** DRC unconnected = 0 with no dangling items; the truth table matches the schematic line for line; the recovery bench steps exist with pass conditions.

### WP4 — Pin plan, module fit and interfaces

**Goal:** the sockets are placed once, from measurements; no carrier net sits on a pin the ESP32 board already uses; every cabled port is named.

| Task | Items | What to do | Owner | Size |
|---|---|---|---|---|
| T4-01 | A10, A1, A2 | Caliper readings of both modules (row pitch, row spacing, pin-1 offsets, heights) and a **1:1 print of the socket layer with both boards pressed in**. ESP32 rows 26.00 mm (estimate ~26.2); modem rows 34.00 mm (estimate ~33.8). Record before moving anything. | HW | M |
| T4-02 | A9, E6 | Side-on photo of each module on its socket confirming components-down and pin direction; note SIM-up, USB and microSD access direction. | HW | S |
| T4-03 | A1, A5, A7, C2, C5, C13, B9, R11 | Signed **pin map v1**: every ESP32 and modem pin, module function, carrier net, direction, reset state, driver; the Table 10 moves; **nothing on J1 pins 16–20**; the AS5600's port named; battery-sense divider on GPIO6 with its own lead. | HW+FW | M |
| T4-04 | A1, A7, C2, C5, R11 | Schematic pin moves per Table 10: E22 M1 → GPIO40 (J2 pin 8); M0 → GPIO15 (J1 pin 8) if no 32 kHz crystal, else GPIO39 with AUX moved; wind reed → GPIO39 (J2 pin 9). | HW | M |
| T4-05 | C4 | Status light per DEC-5: state in writing whether D6 (GPIO42, carrier) or a J24 panel lamp is the status light; label accordingly. | HW+FW | S |
| T4-06 | R11 | Reed bench: counts match a reference at 1, 10 and 50 Hz. | FW | S |
| T4-07 | C1, B9, C13 | Close DEC-1 and DEC-2 in the pin map, then re-issue the signed sheet (the schematic follows the sheet, never the reverse). | HW+FW | S |

**Done when:** readings + 1:1 photo + side-on photos are in `revC\A10\` and `revC\A9\`; the pin map is signed and matches the schematic; J1 pins 16–20 are free in the board file as well as on paper.

### WP5 — Layout integrity: planes, antenna, PE, ESD, vias

**Goal:** In2 is a plane under every B.Cu signal, the antenna sees no copper, PE is bonded, protection sits at the pins, and no via is open inside a solder pad.

| Task | Items | What to do | Owner | Size |
|---|---|---|---|---|
| T5-01 | E3 | Add a **rule area over x 182–211, y 152–170 on every copper layer** (tracks, vias, pads, fill kept out). Clear the area: today the antenna footprint (x 187.5–205.5, y 154–162) is 100 % covered by both planes, and 46 track segments of 13 nets, 7 vias and J7, Q2, Q4, U6 sit in the wider area. If Wi-Fi/BT is not used at the box, obtain a **written** statement — the item then returns to P2 (SQ20). An antenna overhang past the board edge is the alternative if the outline may change (SQ19). | HW | L |
| T5-02 | R12 | Move the seven nets off In2 (431.3 mm today: LED_DRV1 100.8, LED_DRV2 109.8, +5V_SENS 76.8, 3V3_C 63.0, SENS_EN 52.6, I2C0_SCL 22.5, I2C0_MUX_SC0 5.7) and remove or justify the 17.1 mm +5V stub, so that **no B.Cu signal crosses a cut** in the 5 V plane (54 crossings today). | HW | L |
| T5-03 | R9, H1 | Bond PE to GND at **one point beside the sensor ports** (link, with an RC footprint as the alternative); keep PE copper ≥0.5 mm from other nets except at protection pins (today 0.225 mm at J11/J17 and 0.25 mm along ~110 mm of BUZZER_EN and J20's pads); README earthing scheme. Decide the antenna-feed arrestors (H1). | HW | M |
| T5-04 | C8 | Move every ESD array to **≤5 mm along the copper** from the pin it protects (today 5.4–21.8 mm; J20 pin 1 is 46 mm), before any other part; add arrays to **J24 and J25** (panel lamps and buzzer leave the box). Produce the measured distance table. | HW | M |
| T5-05 | E7 | 47 Ω series on **every** cabled I2C line (today CH0/CH1 only) and an input filter on the E22 supply. | HW | S |
| T5-06 | R16 | Resolve the **65 vias inside SMD pads** (224 vias total): move them off the pads, or specify filled and capped vias on the fab drawing and say so in the package. Prefer moving them — this board is hand assembled. | HW | L |
| T5-07 | R13 | Replace Q1, Q5, Q6 (2N7000) with parts specified at **2.5 V gate drive**; check footprint pinout on the new part. | HW | S |
| T5-08 | R14 | Swap the GY-521 and DS3231 outlines and labels (J7 has the GY-521 pinout, J8 the DS3231); verify the expected DS3231 overhang (~38 × 22 mm with coin cell) over J16/J15 and the parts around them (ESD7, R5, C35, C43, Q3 with R20, R25, R26, C26) has no collision; redo the 3D check. | HW | M |
| T5-09 | C10 | Net classes and rules that match this board: Default 0.2/0.2; Power class (5 V 1.0 mm, input path pour); **PE 0.5 mm clearance**; >15 V 0.3 mm; ground stitching ≤10 mm; a `.kicad_dru` naming only nets on this board (none exists today); delete any rule that names a net or area that is not here. | HW | M |
| T5-10 | E4 | Move TP2, TP3, TP5 out from under the modem; add test points on I2C-1 and UART1; replace the obsolete +12 V point with the converter output at J18, plus WDI and PE (SQ29); keep the remaining points meaningful. | HW | S |

**Done when:** In1/In2 show nothing but planes (a Net Inspector export proves it); the rule area exists and is empty on every layer; the PE spacing rule passes; the ESD distance table is ≤5 mm on every line leaving the box; DRC reports no via-in-pad without a fab note.

### WP6 — Mechanical, placement and the 3D check

| Task | Items | What to do | Owner | Size |
|---|---|---|---|---|
| T6-01 | R10, A3 | Move **J5 outside the modem board's outline**, at the edge nearest its supply connector, with a short lead; move the three test points out. Standardise the terminal family or document the exception (A3). | HW | M |
| T6-02 | A12 | Add **four standoff holes for the modem board** and a clamp for the ESP32 board; nothing a person must reach sits under a module. | HW | M |
| T6-03 | H5, E6, C9 | Choose the enclosure (H5); check mounting holes 5 mm from the edges against the box; show USB/microSD/SIM access; state the purpose of J16, R5 and ESD3 or remove them (C9). | HW | M |
| T6-04 | A4, R14, A12, R10 | 3D check with **every module on its right socket at its real height** — attach a 3D model to each socket footprint — and the lid on; both sides; the DS3231 overhang visible. This is the evidence that closes A4, R14 (with T5-08), A12 and R10. | HW | M |

**Done when:** the 3D renders show modules + enclosure; a person can reach J5, the test points, the USB and the microSD with the modem fitted; four standoffs are in the board file.

### WP7 — Files, BOM, stack-up, fab drawing and marking

| Task | Items | What to do | Owner | Size |
|---|---|---|---|---|
| T7-01 | F1, H3, H4, C10 | Symbol fields on every part: **Manufacturer, MPN, Rating (V/A/W), Temp range, Variant**; BOM grouped by value and footprint with real quantities; temperature column (H3); plating/coating (H4); the two build variants (C10). | HW | L |
| T7-02 | F1, R8 | Footprint attributes: every fitted part clear of "exclude from position", "exclude from BOM", "not in schematic" — **U4 is the known offender** (attributes = 28). | HW | S |
| T7-03 | F2 | Board Setup → Physical Stackup: real 4-layer build (1.6 mm, 1 oz), dielectric thicknesses, **finish** (e.g. ENIG). The job file is generated from it and carries the title-block revision. | HW | S |
| T7-04 | F2, R16 | Fab drawing PDF on Dwgs.User: outline and dimensions, stack-up table, finish, mask/silk colours, **via treatment (tented / filled / capped)**, minimum track and gap, drill type (PTH/NPTH), and ≥3 fiducials if SMT assembly is used (SQ21). | HW | M |
| T7-05 | F2 | IPC-D-356 netlist export; drill map PDF. | HW | S |
| T7-06 | F1, F2 | Component placement in mm, both sides, same origin as the Gerbers; count lines against the BOM (today 141 parts, U4 missing). | HW | S |
| T7-07 | D2, E5 | Title block: real revision (Rev C), date, names, one-line change note; sheet size that prints (A3 or A2, not A0); board name, revision and a blank **serial box** on the silkscreen. | HW | S |
| T7-08 | E5, C12, A3 | All human-facing labels on F.SilkS (not F.Fab/Dwgs.User): connector names, pin 1, polarity, rail voltage beside each connector, LED/buzzer functions. Key the sockets so a reversed module cannot be fitted. Check the plotted silk. | HW | M |
| T7-09 | R15 | Text and description corrections: "U8 decoupling" descriptions, C13's value, F1's value (4 A vs 5 A in the description), F.Fab labels (ESP32 "DevKitC"; J13/J14 labels beside J20/J17; "J3 UART"/"J4 PWR" swapped by the remap), the "REVERSE-POLARITY PROTECTION" title over Q9, **J24's symbol pin names** (pin 2 "GND" carries LED1_K, pin 3 "SCL" carries LED2_K, pin 4 "SDA" is ground — a harness built from the names would be miswired), and the DC-solve directives that still describe 12 V at J18, D1, U1 and J9. | HW+FW | M |
| T7-10 | R15 | Regenerate the QA note **from the files in the zip** (the current `PCB_QA_Report.md` calls the board "manufacturing-ready" and calls the open watchdog "an intended jumper gap") — or leave a QA note out. It must not contradict the response sheet. | HW | S |
| T7-11 | C11 | Specify the SPS30 cable (connector, length, shielding) in the BOM/README. | HW | S |

**Done when:** job file shows revision + finish + real stack; BOM has MPN, quantity, rating and temperature on every line; placement has every fitted part; the fab drawing answers via treatment; no document in the package contradicts a file in the package.

### WP8 — Evidence documents

| Task | Items | What to do | Owner | Size |
|---|---|---|---|---|
| T8-01 | G1, B10 | Update the `!padne` directives (they still say `VOLTAGE 12V` at J18, `U1`, `J9`) and run the chain in the KiCad simulator or the DC solve: modem rail under bursts, SPS30 start, LoRa transmit, reversed input, 12 V and 24 V on J18, thermal at +70 °C. Plots + the setup in one page. | HW | L |
| T8-02 | B7, B12, C7, E1, cond 4 | **Maps and plots**: the decoupling map (one row per supply pin — pin, nearest 100 nF, nearest bulk, distance **along the copper**, pass/fail against 5 mm, 3 mm for IC pins, 10 mm for bulk); and the **ground-stitching plot** the release gate asks for (no point of either ground pour more than 10 mm from a ground link, antenna keep-out excepted). | HW | M |
| T8-03 | G2 | **FMEA**, 20–30 rows for this board: each fuse, FET, regulator, the protection, each connector and cable, the watchdog, the I2C switch. Failure, effect on the board, effect on the farmer, detection, safe state. | HW+FW | M |
| T8-04 | G3 | **Bring-up plan**: numbered steps — input stage alone, then regulators, then one module at a time; expected value and stop condition at each step. | HW+FW | M |
| T8-05 | G4 | **EMC/ESD test plan**: IEC 61000-4-2 on every port that leaves the box, 4-5 on the antenna feed and the 5 V input; pass criteria. | HW | S |
| T8-06 | H6 | **Radio record**: E22 module certification/antenna note, power settings, duty cycle. | HW+FW | S |
| T8-07 | A1, A2, A9, A10 | Readings, 1:1 test-fit photo, side-on photos — assembled into one short fit report. | HW | S |
| T8-08 | A4, A12, R10, R14, H5 | 3D pack: module renders both sides, enclosure, nothing reachable under a module. | HW | M |
| T8-09 | all | **Response sheet** compiled, one row per item, evidence column pointing at a file + layer/area + refdes + value (section 6). | HW+FW | M |

**Done when:** every P0 has a document or a bench plan behind it, and each document is named from at least one response-sheet row.

### WP9 — Packaging and submission

| Task | Items | What to do | Owner | Size |
|---|---|---|---|---|
| T9-01 | R1 | **Freeze the 6L:** add a withdrawal note, remove `6L\` from `_release\morishield_hardware\` and from the packaging list so it cannot be zipped again (the packaging tree currently holds 6L, 4L and libraries). | HW | S |
| T9-02 | C3, F2 | Regenerate, in this order and from the **saved** board: refill → save → DRC (parity on) → ERC → plot Gerbers → drill → job file → IPC-356 → placement → BOM → schematic PDF. Record the save, DRC and plot times. | HW | M |
| T9-03 | all | Walk the CHK C1–C13 checklist (section 8) on the files **in the zip**, not on screen. | HW | M |
| T9-04 | — | Zip named `MoriShield_Carrier_RevC_YYYY-MM-DD.zip`, one variant, response sheet **first**, nothing from Rev B or 6L inside, checksums recorded. Reuse `_release\pack.ps1` (it refuses scratch files and scans for tooling references) and `verify_stage.ps1`. | HW | S |
| T9-05 | — | Send, and log the send date/message reference in the response sheet header. | HW | S |
| T9-06 | D3, C2, gate row 2 | Close the **209 schematic-parity differences** (133 footprint-symbol mismatch, 58 net conflict, 14 field mismatch, 4 extra footprint) and justify or remove each ERC ignore. If Serigreen accepts documented exceptions instead of literal zero, record them with the acceptance (SQ25). | HW | M |

**Done when:** the zip contains exactly the ten row-groups of review §12 Table 14, with the response sheet as file 1 and its checksum list beside it.

---

## 5. The item register

### 5.0 What the 59 items are

The 59 items are **§6.2 Table 9 of MS-CAR-REV-A-004 v1.0** (16 October 2026). That table merges every open change from three documents into one list: MS-CAR-REV-A-001 v1.2, MS-CAR-REV-A-003 v1.1, and the six requests 004 added itself (B7, B10, B11, B12, E7, G4). Each item has a **priority** and a **"closed when"** line — the acceptance test. Aim at that line, not at the wording of the finding.

| Group | Covers | Items | Count |
|---|---|---|---|
| **A** | Modules and fit (ESP32 board, modem board, sockets, pin map, 3D) | A1–A12 | 12 |
| **B** | Power (input chain, rails, bursts, decoupling, budget) | B1–B12 | 12 |
| **C** | Interfaces (RS485, microSD, FDC1004, button/LED/buzzer, I2C, SPS30, ESD, pin map) | C1–C13 | 13 |
| **D** | Schematic quality (netlist, title block, ERC) | D1–D3 | 3 |
| **E** | Layout and EMC (stitching, reliefs, antenna, test points, silk, access, filters) | E1–E7 | 7 |
| **F** | Files (BOM, fab data) | F1–F2 | 2 |
| **G** | Process (simulation, FMEA, bring-up, EMC plan) | G1–G4 | 4 |
| **H** | Field and environment (earth/surge, watchdog, temperature, plating, enclosure, radio) | H1–H6 | 6 |
| | | **Total** | **59** |

**Priorities when 004 was issued:** 14 P0, 30 P1, 15 P2. The Rev B review raised **E3 to P1**, so the carried set is now **14 P0 / 31 P1 / 14 P2**.

**Status in the Rev B package** (judged on the 4-layer files, review §10): **6 closed** (A8, C3, C12, D1, E1, E2), **24 partly done**, **28 open**, **1 superseded** (B11). Adding the 17 new items (5 P0, 8 P1, 4 P2) gives **76 items to answer: 19 P0, 39 P1, 18 P2** — the response sheet has one row for each, plus one row per unrequested change.

**P0 means:** designed in **and evidenced** in the package before fabrication. A P0 cannot be deferred. The P0 set is: A1, A2, A4, A6, A7, A8, A9, A10, B10, C1, C2, C3, C4, G1 carried, plus R1, R2, R3, R4, R5 new. Of these, A8 and C3 are already closed on design; the other twelve carried P0s are open or partly done.

**How to read 004's wording (round 1) against this board (round 2).** 004 was written on the pre-4L design — the 2-layer board now kept in `cto remarks\old remarks\design\`. Some of its text therefore names parts and rails that no longer exist on the 4L: **U1** (AMS1117), **J9** (buck socket), **D1**, **C6**, the **12 V input**, **RS485**, and the old 0.45 mm vias. The "What remains" column below is written against the 4L; where the two disagree, the review's Rev B column (MS-CAR-REV-B-001 §10) and the six conditions of §6.4 are the authority.

### 5.1 Group A — modules and fit

| Item | P | Rev B | What remains (Rev C action) | Closed when (004 Table 9) | Task |
|---|---|---|---|---|---|
| A1 | P0 | Open | Rows level but spacing unmeasured; E22 M1/M0 sit on the microSD pins, the reed on the LED pin. Take readings, sign the pin table, move those lines. | Photos, measured drawing, signed pin table, test-fit. | T4-01, T4-03, T4-04 |
| A2 | P0 | Partly | Rows level, drawn components-down, stale 35.56 mm note gone. Missing: measurements, truth table, 5 V supply proof. | Bench capture of the supply inside 4.75–5.25 V in a burst; modem registers on the network. | T4-01, T3-06, T1-01, T1-08 |
| A3 | P1 | Partly | Outlines and labels live on F.Fab/Dwgs.User (not printed); sockets not keyed. J5 is a screw terminal, unlike the sensor ports. | Silkscreen Gerber; a reversed module cannot go in or is obvious. | T7-08, T6-01 |
| A4 | P0 | Partly | Five outlines, two on the wrong sockets; no heights; 3D shows only carrier parts; no enclosure. | 3D views; enclosure and shield drawing. | T6-03, T6-04, T8-08 |
| A5 | P1 | Open | No GPIO map in the package. | README table matching schematic labels, signed. | T4-03 |
| A6 | P0 | Open | No decision on the ESP32 module variant (octal PSRAM takes GPIO35–37). | Module marking photo and rating, or ECC confirmed in the build. | DEC-2, T4-07 |
| A7 | P0 | Open | Modem lines are off GPIO10–14, but E22 M1/M0 now sit on GPIO10/11 (J1 pins 16/17). | Nothing but pads on J1 pins 16 to 20; firmware map agrees. | T4-04 |
| A8 | P0 | Closed | J1/J2 at y 154.00, J3/J4 at y 113.56 — keep. Re-verify after any placement move. | Pin 1 y coordinates equal, or a measured offset documented. | T4-01 |
| A9 | P0 | Partly | Components-down drawn and pins mapped; the side-on photo is missing. | Side-on photo; footprint and test-fit match. | T4-02 |
| A10 | P0 | Open | No readings, no test-fit; 26.00 mm (6L 25.75) against ~26.2; 34.00 against ~33.8. | Readings table and test-fit photo. | T4-01 |
| A11 | P1 | Partly | R16 holds PWR_EN low in reset; no truth table; two drivers on PWR_EN; PWRKEY held by 1 kΩ only; RESET dropped. | README table; bring-up shows firmware power-cycling the modem. | T3-05, T3-06 |
| A12 | P1 | Partly | Modem moved 15 mm down; no standoffs; ESP32 not clamped; J5 + 3 test points under the modem. | 3D check; test-fit shows the holes line up. | T6-02, T6-01, T6-04 |

### 5.2 Group B — power

| Item | P | Rev B | What remains (Rev C action) | Closed when (004 Table 9) | Task |
|---|---|---|---|---|---|
| B1 | P1 | Open | 12 V input is off-board: the TVS requirement moves into the converter's input specification (≥40 V, clamp below the converter's maximum). | Clamp simulation; no TVS current at the highest charge voltage. | T1-01, T8-01 |
| B2 | P1 | Open | No buck on the board: the converter must be 40 V in minimum, 5 V/3 A at +70 °C, low no-load. | 5 V within 5 percent from 9 V to the B8 maximum at full load; rise measured in the closed box. | T1-01, T8-01 |
| B3 | P1 | Partly | F1 is a 4 A PTC on glass-fuse clips; C13 has a ceramic code on an electrolytic footprint; no ratings in the BOM. | Part numbers and ratings in the BOM. | T1-04, T7-01 |
| B4 | P1 | Partly | 5 V plane on In2 stands; the input path narrows to 0.5 mm and one 0.3 mm via. | G1 transient; bench capture. | T1-05, T8-01 |
| B5 | P1 | Partly | LDO and switched rails fitted, default off; D3/D4 always on; no budget. | Budget table; measured sleep and active current. | T2-06, T8-01 |
| B6 | P2 | Partly | D7 feeds J1 pin 21; no USB service rule and no README. | Schematic and service note. | T2-02 |
| B7 | P1 | Open | U6 (TPS7A2033) is now the 3.3 V regulator; C26/C27 are 11.6 and 9.3 mm from its pins in a straight line. | Layout; no sustained oscillation on the 3.3 V rail, ripple and transients under 50 mV peak to peak. | T2-03, T8-02 |
| B8 | P1 | Open | Moves into the converter input (cover the battery-disconnect voltage) and into the J18 over-voltage cut-off. | Bench test with 22 V on the input; restart when the battery returns. | T1-01, T1-02 |
| B9 | P1 | Open | GPIO6 unused; no divider. With 5 V at J18 the battery needs its own sense lead. | Within 2 percent of a meter from 9 to 15 V. | T4-03, DEC-7 |
| B10 | P0 | Open | Restated as the six conditions of review §6.4; the board resistance still exceeds the 60 mΩ allocation and the copper is below its protection. | Model, then bench trace at the modem connector: 4.75 to 5.25 V through LTE attach and forced GSM at minimum input. | T1-01…T1-08, T8-01 |
| B11 | P2 | Superseded | No buck on the board — no action; record the reason in the response sheet. | Layout. | — |
| B12 | P1 | Partly | ESP32 5 V pin decoupled (10 µF at 6.9 mm); nothing within 41 mm of J5; E22 at 28.4 mm; UART reference at 51 mm; the four 100 nF sit together in a corner. | Decoupling map: every supply point within 10 mm of its capacitor along the copper, or a stated reason. | T2-04, T8-02 |

### 5.3 Group C — interfaces

| Item | P | Rev B | What remains (Rev C action) | Closed when (004 Table 9) | Task |
|---|---|---|---|---|---|
| C1 | P0 | Open | RS485 removed in the title block "for off-board USB testing", never agreed. Restore (transceiver, termination jumper, fail-safe bias, TVS to earth, pins per 003 §9) or obtain a written deferral. | Sensors read over Modbus at installed length; survives a 12 V miswire. | DEC-1, T4-07 |
| C2 | P0 | Open | microSD slot unusable while E22 M1/M0 sit on GPIO10/11. | 24-hour run; no corruption after 20 power cuts. | T4-04, T4-03 |
| C3 | P0 | Closed | FDC1004 port J21 on CH5 with pull-ups and ESD — keep; bench read still owed on first boards. | Bench read at installed length with the modem transmitting. | T1-08 (bench plan) |
| C4 | P0 | Partly | Button on GPIO3 with RC and ESD; buzzer on the expander; GPIO42 drives D6 **on the carrier**, not a light seen from outside. | Press logged with RTC time; status visible from outside the box. | DEC-5, T4-05 |
| C5 | P1 | Partly | M0/M1 on separate pins but on the microSD pins. | Firmware reads back channel, address, power and key. | T4-04, T3-06 |
| C6 | P1 | Partly | One segment per cabled port with 4.7 kΩ pull-ups; GY-521/DS3231 on I2C-1; but the expander shares I2C-0 and U7's reset is a power-on RC. | Rise under 1 µs and low level under 0.4 V at installed lengths; one shorted cable leaves the rest working. | T3-04 |
| C7 | P1 | Partly | 10 µF at 5.3 mm from J13; the 100 µF is 28.5 mm away; nearest 100 nF about 22 mm. | Layout; scope capture at fan start. | T2-05 |
| C8 | P1 | Partly | Every sensor port has ESD returned to PE, but 5.4–21.8 mm from the pins (J20 pin 1: 46 mm) and none on J24/J25. | IEC 61000-4-2, ±4 kV contact and ±8 kV air, on each port. | T5-04 |
| C9 | P2 | Open | J16, R5 and ESD3 remain with no stated purpose. | Written purpose, or removal. | T6-03 |
| C10 | P2 | Open | No build variants in the BOM; antenna separation and LoRa scheduling unaddressed. | LoRa margin with the modem idle and transmitting. | T7-01, T2-02 |
| C11 | P1 | Partly | SPS30 on its own segment (CH2); the cable is not specified. | 72 hours error-free at installed length with both radios transmitting. | T7-11 |
| C12 | P2 | Closed | 1 kΩ + 100 nF on both ADC inputs — keep; readings still to be shown stable with the modem transmitting. | Readings stable with the modem transmitting. | T1-08 (bench plan) |
| C13 | P1 | Open | No pin map; the AS5600's port is unnamed. | README, schematic and firmware agree pin for pin. | T4-03 |

### 5.4 Groups D–H

| Item | P | Rev B | What remains (Rev C action) | Closed when (004 Table 9) | Task |
|---|---|---|---|---|---|
| D1 | P1 | Closed | The +5 V/GND overlap near J9 is redrawn — keep. Re-prove netlist parity in the Rev C package. | Re-derived netlist matches the PCB. | T9-02 |
| D2 | P2 | Partly | Title block filled, but the sheet is A0 and the revision reads "Proto-Simple Rev 0.2". | A3 print. | T7-07 |
| D3 | P2 | Open | ERC is now 0/0, from 522 warnings, with four check classes ignored. Justify each ignore in one line or remove it. | ERC 0 errors, 0 warnings. | T9-02, T9-06 |
| E1 | P1 | Closed | Continuous ground plane with stitching — keep. The release gate still asks for the **stitching plot**. | Stitching plot: no point of either ground pour more than 10 mm from a ground link (antenna keep-out excepted). | T8-02 |
| E2 | P1 | Closed | Thermal reliefs on plane connections — keep; zone settings are the evidence. | Zone settings. | T9-02 |
| E3 | P1 | Open | No keep-out; both planes cover the antenna footprint 100 %; 46 segments, 7 vias and 4 parts in 003's area. | Layout. | T5-01 |
| E4 | P2 | Partly | Eleven test points; three under the modem; none on I2C-1 or UART1; the +12 V point is obsolete (no 12 V on the board). | Layout. | T5-10 |
| E5 | P2 | Open | J18 legend reversed; no board name, revision or serial box; rail voltages not shown. | Silkscreen Gerber. | T1-06, T7-07, T7-08 |
| E6 | P2 | Partly | SIM side noted ("SIM up"); USB and microSD access not shown. | 3D check and bring-up plan. | T6-03, T8-04 |
| E7 | P1 | Partly | Ferrite and capacitors on the E22 supply; 47 Ω on CH0/CH1 only; no input filter. | LoRa noise floor within 3 dB with the buck and modem on; 12 V ripple recorded. | T5-05, T1-05 |
| F1 | P2 | Open | BOM has values and footprints only: no MPN, module SKUs, housings, crimps, ratings, plating or variants. | BOM. | T7-01 |
| F2 | P2 | Partly | X2 Gerbers, drill and placement in mm; but revision "rev?", no stack-up, finish, fab drawing, IPC-356 or README; passives already 0805/1206 where it matters. | Files. | T7-03…T7-10 |
| G1 | P0 | Open | No simulation results; the `!padne` directives still describe 12 V at J18, D1, U1 and J9. | Rails within 5 percent (modem connector 4.75 V or more); clamps below every maximum; junctions at 80 percent or less. | T8-01 |
| G2 | P1 | Open | No FMEA. | FMEA table. | T8-03 |
| G3 | P1 | Open | No bring-up plan. | Plan, then bench record. | T8-04 |
| G4 | P2 | Open | No EMC test plan. | Plan with the pilot; results before scale. | T8-05 |
| H1 | P1 | Partly | Earth terminal J19 and ESD returned to PE; no defined bond to ground; no arrestors on the antenna feeds; the 12 V surge parts move to the converter. | Surge test with recovery on its own. | T5-03, T1-01, T8-05 |
| H2 | P1 | Partly | Supervisor, expander and E22 switch fitted; WDI open; push-pull output on EN; U4 out of the placement file; a stuck I2C-0 survives a reset. | A firmware hang and a slow ramp both end in a clean restart. | T3-01…T3-07 |
| H3 | P1 | Open | No temperature column; DS3231 suffix and backup cell not named. | BOM column; 24-hour soak at +70 °C. | T7-01 |
| H4 | P1 | Open | No plating or coating in the BOM. | BOM plating; coating procedure. | T7-01, T6-03 |
| H5 | P2 | Open | Enclosure not chosen; no strain relief, glands or drip loops. | Pull test; enclosure material in the BOM. | T6-03 |
| H6 | P1 | Open | No radio record. | README section; 24-hour firmware log. | T8-06 |

### 5.5 New items from the Rev B review (R1–R17)

| Item | P | What to do | Closed when (review Table 13) | Task |
|---|---|---|---|---|
| R1 | P0 | 6-layer Gerbers short the ESP32 header; the variant is withdrawn. For **every** Gerber set from now on: refill, save, DRC on the saved file, then plot. | Serigreen's Gerber check finds every pad clearance in place. | T9-01, T9-02 |
| R2 | P0 | Route `/WDT_WDI` to U4 pin 4 (islands at vias 244.5,173.5 and 257.0,168.1), together with R8; delete the dangling 3V3_C stub, EVENT_BTN track and the PWR_EN / I2C0_SDA / BUZZER_EN vias. | DRC on the saved file: 0 unconnected items, no dangling tracks or vias. | T3-03 |
| R3 | P0 | Swap the J18 legend: "+" beside pad 1 (`+5V_IN`), "−" beside pad 2 (`GND`); state polarity in the README. | The silkscreen Gerber shows "+" beside the +5V_IN pad. | T1-06 |
| R4 | P0 | Reverse and over-voltage protection per condition 2; if a P-channel FET is kept, drain to J18, source to load, gate resistor + ~10 V gate-source zener, or sit it behind the cut-off; re-rate D2 and ESD16. | Bench: reversed supply, 12 V and 24 V on J18 for a minute each leave the board unharmed; the cut-off acts below 5.5 V. | T1-01, T1-02, T1-08 |
| R5 | P0 | Pour-width copper and via arrays from J18 to the 5 V plane, sized for the protection's trip/limit current; a footprint that matches the protection part; the library footprint restored for Q9. | Layout; the board resistance in condition 3; no footprint mismatch in the DRC. | T1-03, T1-04, T1-05 |
| R6 | P1 | Separate gate networks for Q2 and Q3, each pulled up to its own source, both pulled down by one enable; switched-rail firmware rules into the README. | Bench: 5 V sensor rail below 0.1 V when off, with the SPS30 fitted. | T2-01, T2-02 |
| R7 | P1 | One driver per modem control line (PWR_EN on GPIO7); PWRKEY decided with A11. | Truth table (A11); bring-up shows firmware power-cycling the modem. | T3-05, T3-06 |
| R8 | P1 | TPS3828 (open-drain) on EN; WDI from a pin that floats through reset and download, or through a jumper; U4 in the BOM and placement file. | A firmware hang ends in a reset; USB flashing works with the watchdog fitted; U4 in the placement file. | T3-01, T3-02, T3-07 |
| R9 | P1 | Bond PE to ground at one point beside the sensor ports (link, RC alternative); PE copper ≥0.5 mm from other nets except at protection pins; earthing scheme in the README. | Layout and README; ESD test per G4. | T5-03 |
| R10 | P1 | Nothing under the modem board: J5 outside its outline at the edge nearest its supply connector, with a short lead; test points outside. | 3D check with the modem fitted. | T6-01, T6-04 |
| R11 | P1 | Move the wind reed input off the LED pin, per the Table 10 pin plan. | Pin map (C13); bench counts that match a reference at 1, 10 and 50 Hz. | T4-04, T4-06 |
| R12 | P2 | Move the seven nets routed on In2 to the outer layers so no B.Cu signal crosses a cut in the 5 V plane. | Layout. | T5-02 |
| R13 | P2 | Replace Q1, Q5, Q6 (2N7000) with parts specified at 2.5 V gate drive. | BOM. | T5-07 |
| R14 | P2 | Swap the GY-521 and DS3231 outlines and labels; redo the 3D check. | User layers and 3D views. | T5-08, T6-04 |
| R15 | P2 | Correct the descriptions, values, F.Fab labels, J24 symbol pin names and stale DC-solve directives; delete or rewrite stale rules; regenerate the QA note from the shipped files. | Files. | T7-09, T7-10 |
| R16 | P1 | Move the 65 vias off SMD pads, or specify filled and capped vias in the fab notes. | Layout or fab drawing. | T5-06, T7-04 |
| R17 | P1 | Move U8 to I2C-1 and reset U7 with the ESP32 (supervisor reset line or a GPIO); firmware bus recovery. | Bench: SDA held low on a cabled port; the board recovers without a power cycle. | T3-04 |

**Counts:** 59 carried (14 P0 / 31 P1 / 14 P2) + 17 new (5 P0 / 8 P1 / 4 P2) = **76 rows**, **19 P0 / 39 P1 / 18 P2**.

---

## 6. The response sheet — the first file in the zip

One row per item, in the review's order (A1…H6, then R1…R17), plus one row for every change nobody asked for. Spreadsheet or CSV; `4L\_qa\revC\ResponseSheet_RevC.csv`.

**Columns** (CHK §7):

| Column | Content |
|---|---|
| `Item` | A1, B10, R3 … or `(new)` for an unrequested change |
| `Prio` | P0 / P1 / P2 as it stands today (E3 = P1) |
| `What changed, and where` | the change in one sentence + schematic sheet / board area / refdes |
| `Evidence (file, page, measurement)` | file name + layer/area + refdes + value, e.g. "F.Silkscreen Gerber, J18 area; pad 1 net +5V_IN, silk '+' at y 107.0" |
| `Status` | `Done` / `Partly (say what is missing)` / `Deferred (name Serigreen's message and date)` / `Rejected (reason)` / `Agreed before drawing` / `Superseded` |

**Header block above the rows** (so the sheet is self-contained):

```
Package     MoriShield_Carrier_RevC_<date>.zip
Sent        <date> by <name>; message reference <ref>
Board save  <timestamp>      DRC  <timestamp>      Plot <timestamp>
ERC         <errors> errors / <warnings> warnings   (ignored checks: <list>)
DRC         <errors> / <warnings> / <unconnected> / parity <n>
Files       <name>  <sha256>   (one line per file in the zip)
```

**Example rows** (form only — not a record of work done):

| Item | Prio | What changed, and where | Evidence | Status |
|---|---|---|---|---|
| R3 | P0 | Silk: "+" moved beside pad 1 (`+5V_IN`), "−" beside pad 2 (`GND`); polarity added to README §2 | F.Silkscreen Gerber, J18 area; screenshot with pad nets highlighted | Done |
| B7 | P1 | C26/C27 (1 µF) moved to 2.1 and 2.4 mm from U6 pins 1 and 5 along the copper | Decoupling map row U6; scope capture 3V3_C, 38 mV pp | Done |
| C1 | P0 | RS485 deferred to Rev C | Serigreen's message of `<date>` | Deferred, agreed |
| (new) | — | J5 changed from JST XH to a screw terminal | Schematic sheet 2; Serigreen's message of `<date>` | Agreed before drawing |

**Rule:** the status column is written from what the **files** show, not from what was intended. If a row says Done, the evidence cell must let a stranger find it in a minute.

---

## 7. The package against the release gate (review §12, Table 14)

The next package is the **4-layer board only**, with every item in §5 answered, carrying these ten row-groups:

| # | What the row asks for | What we attach | Produced by |
|---|---|---|---|
| 1 | Response sheet against the 59 items and R1–R17: what changed, evidence; every P0 designed in and evidenced; P1 closed or deferred in writing; P2 closed or listed for Rev C; rejections with reasons | `ResponseSheet_RevC.csv` (first file) | T8-09 |
| 2 | 4-layer KiCad project + schematic PDF; ERC 0/0; DRC 0/0/0 on the saved file with zones refilled; clean parity | project zip, `sch.pdf`, `erc.json`, `drc.json`, parity log | T9-02 |
| 3 | Gerbers with revision and X2, drill, **IPC-356**, placement in mm **with U4**, fab drawing with stack-up, finish and via treatment | `fab\gerber\`, `drill\`, `ipc356\`, `pos.csv`, `fab_drawing.pdf` | T7-03…T7-06 |
| 4 | BOM with MPN, quantities, ratings, temperature range, plating and the two build variants | `bom.csv` | T7-01 |
| 5 | Module fit: root readings, side-on modem photo, 1:1 test-fit photo, signed pin map with Table 10 changes and the AS5600 port; A6 decision with module marking; nothing on J1 pins 16–20 | `A10\`, `A9\`, `pin_map.csv`, `A6\` | T4-01…T4-04 |
| 6 | Power: six conditions met with the converter named; G1 results (modem rail, SPS30 start, LoRa transmit, reverse/12 V/24 V, thermal at +70 °C); supply-path resistances or DC solve; decoupling map with copper distances; B10 trace or the agreed plan | `cond6_budget.md`, `G1\`, `decoupling_map.csv`, `bench_plan.md` | T1-01…T1-08, T8-01, T8-02 |
| 7 | EMC layout: antenna keep-out, protection within 5 mm of every pin that leaves the box (J24/J25 included), PE bond, E22 filter and 47 Ω on every cabled I2C line, In2 as a plane | `E3\`, `C8\`, `R9\`, `R12\`, **stitching plot** | T5-01…T5-05, T8-02 |
| 8 | Interfaces: RS485 decision, microSD archive, FDC1004 port, button and status light, with bench plans; I2C recovery path | `C1\`…`C4\`, `R17\` | T3-04, T4-05, T8-04 |
| 9 | 3D check with every module on its right socket and the enclosure; enclosure and shield drawing; modem standoffs; nothing under the modem | `A4\`, `3D\` | T6-02…T6-04, T8-08 |
| 10 | Bring-up plan and FMEA | `G3\`, `G2\` | T8-03, T8-04 |

---

## 8. Pre-send checks (CHK C1–C13) with our commands

Run in this order, on the files that go into the zip. Record the result in `revC\reports\final_checklist.md`.

| Check | How we run it here | Pass means | Today's baseline |
|---|---|---|---|
| **C1** ERC + libraries + title block | `kicad-cli sch erc --severity-all --format json -o revC\reports\erc.json 4L\MoriShield_Carrier.kicad_sch`; review the ignored-checks list; read the title block | 0 errors, 0 warnings, revision in title block | 0/0, with 4 ignored check classes; rev reads "Proto-Simple Rev 0.2" |
| **C2** Board vs schematic | `kicad-cli pcb drc --refill-zones --schematic-parity --severity-all --all-track-errors --format json -o revC\reports\drc.json 4L\MoriShield_Carrier.kicad_pcb`; also Tools → Update PCB from Schematic must report nothing | 0 unconnected, 0 parity differences, no dangling track/via | 1 unconnected, 209 parity, 5 dangling vias + 2 dangling tracks |
| **C3** Zones, saved file, plot order | Refill (B) → Save → DRC on the saved file → fix → refill → save → DRC → **then** Plot with "Check zone fills before plotting" on | DRC clean on the saved file; Gerbers plotted **after** that DRC; record save/DRC/plot times | Gerbers 16:12:05 vs board saved 19:43:48 — **fails today** |
| **C4** Production files vs board | gerbview: walk every layer, inner layers at every through-hole connector and via field; hover with X2 net attributes; drill map count vs Inspect → Board Statistics; export IPC-D-356 | every layer matches the board; IPC-D-356 in the package | IPC-356 absent |
| **C5** Footprints and assembly | Board Setup → Violation Severity: "Footprint does not match library" = error; DRC; Compare Footprint with Library on F1, Q9, J18, TVS; vias in pads; constraints 0.2/0.2, via 0.6/0.3, annular 0.15, copper-edge 0.5 | no mismatch, no courtyard overlap, no silk over pads, vias handled | 1 mismatch (Q9), 65 vias in pads; project limits looser (via 0.5, annular 0.1) |
| **C6** BOM, placement, job file, fab drawing | symbol fields → BOM; footprint attributes; Physical Stackup + Finish; placement both sides mm; line count vs BOM | every line has MPN/qty/rating/temp; placement has every fitted part; job file has rev + finish + stack; fab drawing present | 153 BOM rows with no MPN; 141 placement lines; "rev?" / "None"; no fab drawing |
| **C7** Power paths | resistance table (`R = ρL/(wt)`, ρ = 1.72e-8, t = 35 µm, +0.39 %/°C); IPC-2221 rise at the **fault** current; DC budget; ratings 2× V / 1.5× I / ≤80 % junction at +70 °C | every load inside its window; conductors < 10 °C rise at fault current; ratings written; simulation in | J18→J5 122 mΩ cold / 171 mΩ hot vs 60 mΩ target |
| **C8** Protection | write up three events (reverse, 12 V/24 V, surge): what conducts, what limits, what each load sees; TVS stand-off vs rail; ESD distance table; PE bond | events written with simulation; stand-off above highest rail; ESD ≤5 mm; PE bonded | no reverse/OV protection; ESD 5.4–21.8 mm; no PE bond; J24/J25 unprotected |
| **C9** Placement | decoupling map (5 mm / 3 mm IC / 10 mm bulk, along copper); module outlines + heights; nothing reachable under a module; enclosure | map inside limits; 3D with modules and box; nothing reachable under a module | nothing within 41 mm of J5; J5 + 3 TPs under modem; no standoffs |
| **C10** Layout | plane layers show nothing but planes (Net Inspector export); antenna rule area; net classes + `.kicad_dru`; power copper and via arrays; stitching ≤10 mm | planes only, rule area empty on all layers, rules match board, stitching in | 431.3 mm on In2, 0 keep-outs, one net class, no `.kicad_dru` |
| **C11** Pins and control | signed pin map; one driver per line; reset states; watchdog survives reset and download; bus recovery | pin map matches schematic; no double-use; one driver each; watchdog safe; recovery designed | M1/M0 on microSD pins; reed on LED pin; 2 drivers on PWR_EN; WDI on expander |
| **C12** Silkscreen and marking | read the pad net, then check the **plotted** silk; labels on F.SilkS; name/rev/serial box; DRC silk checks | polarity correct on the Gerber; name/rev/serial; no silk over copper | J18 legend reversed; 78 silk-over-copper + 46 overlaps; no name/rev/serial |
| **C13** Evidence documents | readings, simulation, decoupling map, FMEA, bring-up, README, pin map + truth table | each document in the package and named from a response-sheet row | none of them exist yet |
| **§7** Response sheet | every item, every unrequested change, evidence named | response sheet first in the zip | not started |
| **§3** Zip | named with revision and date, one variant, nothing from the previous revision | `MoriShield_Carrier_RevC_<date>.zip` | Rev B zip contains both variants |

---

## 9. Sequence, dependencies and sign-off

### 9.1 Start here (first working sessions)

0. **Answer the input register** (`INPUT_REGISTER_RevC.md`, the 20 blocking questions). Nothing starts until A9 confirms that 2 Nov is the schematic-only package. `WORK_REGISTER_RevC.md` holds the day-by-day plan.
1. Send one message with §10's questions plus T0-01…T0-08. Everything downstream waits on SQ2, SQ3, SQ4, SQ5, SQ6 and SQ17.
2. Take the readings and the 1:1 test-fit (T4-01). Physical parts, half a day, and it settles A1, A2, A10 and the socket placement for good.
3. Freeze the 6L (T9-01) so it cannot be picked up by the packaging script again.
4. Close the 209 parity differences and justify the four ERC ignores (T9-06), and add the net classes + `.kicad_dru` (T5-09). Both are cheap now and expensive at G4.
5. Make one small, complete change set to prove the pipeline end to end — R3 (silk legend), R2 (route the watchdog input), R5 (Q9 footprint) — then refill → save → DRC → plot and keep the three timestamps. This is the habit the rest of the work depends on.
6. Only then start the schematic redraw for R4, R6, R8 and R17.

### 9.2 Dependencies that will bite if ignored

| This | Waits on | Why |
|---|---|---|
| T3-03 (route WDI) | T3-01/T3-02 (watchdog part and WDI source) | Routing follows the net, and the net follows the decision |
| T1-05 (input copper) | DEC-3, DEC-4 | Copper is sized for the protection's limit current |
| T4-04 (pin moves) | DEC-1, DEC-2 | RS485 and the module variant decide which pins exist |
| T5-02 (In2 as a plane) | T5-01, T5-04 | Moving the antenna area and the ESD parts changes the routing that must leave In2 |
| T7-04 (fab drawing) | T5-06 (vias in pads) | The via treatment is either a layout fix or a fab note |
| T7-01 (BOM) | T0-01, T0-02 | MPNs and variants need the part decisions |
| T8-01 (G1) | DEC-3, DEC-4 | The model needs the real parts |
| T9-02 (outputs) | everything else | Plot last, always |

### 9.3 Sign-off

| Gate | Hardware (Deepak) | Firmware (Aswin) | Date | Note |
|---|---|---|---|---|
| G0 decisions | | | | all seven in writing |
| G1 schematic freeze | | | | ERC 0/0, pin map + truth table signed |
| G1b schematic-only send | | | | optional |
| G2 layout | | | | DRC 0/0/0 on saved file |
| G3 evidence | | | | G1 model, maps, 3D, FMEA, bring-up |
| G4 final check | | | | C1–C13 ticked on the zip |
| G5 send | | | | zip + checksums |

---

## 10. Questions to Serigreen — send as one message

Answer each with one line; the SQ numbers are for our tracking. Questions marked **BLOCKS** stop drawing; the rest can be answered while we work. Where a question maps to a decision in §2, the DEC number is shown. The documents and parts to send with the answers are listed in §0.5 (T0-01…T0-08).

### 10.1 Decisions that block drawing

| # | Question | Maps to / why | Default if no answer |
|---|---|---|---|
| SQ1 | Is **5 V at J18 final** for this revision, with the converter off-board? Will the carrier ever see 12 V or battery voltage again? | Confirms the scope decision; changes protection, TVS ratings, clearance class and H1 | 5 V only, converter external |
| SQ2 | **BLOCKS** — Do you nominate the **converter**, or shall we propose one for approval? Confirm: input covering the 22–25 V disconnect, 5.15 V ±1 %, 3 A at +70 °C, ≤50 mV droop, own fuse and surge part, no-load current stated | DEC-3; conditions 1–2, G1 | We propose four candidates in a comparison table |
| SQ3 | **BLOCKS** — **Protection architecture** at J18: eFuse (TPS26630/31) or over-voltage/reverse controller with low-Rds FETs? The review notes the eFuse meets 60 mΩ only at typical values | DEC-4; R4, R5, copper | Controller + low-Rds FETs |
| SQ4 | **BLOCKS** — **RS485**: restore or written deferral? If restored, what supplies the transceiver now that 12 V is off-board, and must Modbus work on this revision? | DEC-1; C1, pin map | We request a written deferral |
| SQ5 | **BLOCKS** — **ESP32 module**: can you confirm or supply a non-octal EdgeHax variant? If N16R8 stays, is PSRAM ECC with the setting recorded acceptable? Does the board carry a **32 kHz crystal on GPIO15/16**? | DEC-2; A6, A1, A7, C2, C5, R11 | N16R8 + ECC recorded; no crystal assumed → M0 on GPIO15 |
| SQ6 | Who **signs the pin map** with us, and will you accept a PDF of the table plus a one-line approval? | A5, C13, gate row 5 | We send a PDF and ask for "pin map approved" |
| SQ7 | Is the **60 mΩ board allocation** fixed, or may we divide it differently between lead and board as long as the model and trace hold? | Condition 3/5 | Keep 60 mΩ |
| SQ8 | What is the **converter's highest output** at tolerance (5.20 V?) and is up to 1 mA stand-off leakage per clamp acceptable in the budget? | R4, B5, condition 2 | 5.20 V; 1 mA each |

### 10.2 Pins, interfaces and firmware contracts

| # | Question | Maps to / why | Default |
|---|---|---|---|
| SQ9 | Is a **~3.5 A input current limit** acceptable against a 2.6 A all-peak load, or do you want 4 A to match today's PTC? | Copper is sized for the trip current | 3.5 A |
| SQ10 | Which is the **status light** — D6 on the carrier (GPIO42) or a panel lamp on J24? Must it be visible with the box closed? | DEC-5; C4, E5 | D6, visible through a light pipe |
| SQ11 | Does a 1 kΩ pull-down on **PWRKEY** mean "pressed" on the modem board (auto power-on)? Is auto power-on acceptable so PWR_EN cycling is the only recovery? Is a modem RESET line needed — it was dropped | DEC-6; R7, A11 | Auto power-on; PWR_EN only |
| SQ12 | Watchdog WDI: do you accept the **float-through-reset-and-download** approach, or prefer the expander with a series jumper for flashing? Any preferred timeout (1.6 s typical)? | R8 | Floating pin, TPS3828 |
| SQ13 | With U8 moved to I2C-1, do the GY-521 and DS3231 stay on that segment, or should U8 have its own? Should U7 also be resettable from a GPIO, and which pin? | R17, C6 | Same segment; U7 reset from the supervisor line |
| SQ14 | **AS5600**: which port does it use? Is the reed the anemometer and the AS5600 the wind vane — and is the reed on this revision at all? | C13, R11 | Reed on GPIO39; AS5600 on I2C-1 |
| SQ15 | microSD archive: confirm it uses the ESP32 board's own slot (GPIO10–14) and must work on this revision. Which industrial card goes in the BOM? | C2 | Confirm; card model to us |
| SQ16 | **Battery sense**: with 5 V only at J18, is a battery lead available at the carrier? What range should the divider cover (004 said 9–15 V at 2 %) and where is its ground taken? | DEC-7; B9 | Divider for 0–20 V on GPIO6, own lead |
| SQ17 | **Earthing**: is the box bonded to an earth rod? Do you accept a single PE–GND bond beside the sensor ports (link, RC alternative), and what wording do you want in the README? | R9, H1 | Single bond + README section |
| SQ18 | **Antennas**: are the LTE and LoRa antennas coax-fed from the carrier (needing arrestors) or mounted on the modules? What gains for the radio record? | H1, H6 | Module-mounted, no arrestors; gains from datasheets |

### 10.3 Mechanical and EMC

| # | Question | Maps to / why | Default |
|---|---|---|---|
| SQ19 | **Enclosure**: which box, material, glands, antenna exits? May the board outline change (e.g. an antenna overhang notch), or must it stay 178 × 118 mm? Standoffs M2.5 or M3, what height? Must the SIM be reachable with the box closed? | A4, A12, H5, E3 | Keep the outline; rule area only |
| SQ20 | Is **Wi-Fi/Bluetooth used at the box** for setup or service? If not, will you put in writing that E3 can return to P2? | E3 | Assume used → full keep-out |
| SQ21 | **Fab and assembly**: which fab, and can we have its capability sheet (annular 0.15, track/gap 0.2, via fill/cap)? Is SMT assembly used (fiducials) or hand assembly only? | R16, C5, T7-04 | Hand assembly; vias moved, not filled |
| SQ22 | **Finish and coating**: ENIG or HASL? Conformal coating spec and contact masking for H4? IPC class 2, Tg 150 °C, 1.6 mm, 1 oz confirmed? | F2, H4 | ENIG; IPC-2; 1.6 mm; 1 oz |
| SQ23 | **Build variants** (C10): what are the two builds and what differs in the BOM? | F1, C10 | Two variants named by you |
| SQ24 | SPS30 decoupling: 100 µF + 10 µF + 100 nF within 10 mm is tight at J13. Is a **stated reason** acceptable if we cannot reach 10 mm? | C7, B12 | Aim 10 mm, document otherwise |

### 10.4 Evidence, bench and process

| # | Question | Maps to / why | Default |
|---|---|---|---|
| SQ25 | **ERC ignores and parity**: will you accept a documented ignore list (four checks today) and documented parity exceptions, or must both read literally zero? All 209 parity differences are closable, but it costs layout churn | D3, T9-06, gate row 2 | Literal zero — we close them |
| SQ26 | **Bench access**: do we have in-house the A7672 modem + SIM + LTE/GSM coverage, SPS30, E22, GY-521 and DS3231 to run B10, A2, C3, C12, R6, R8, R11 and R17? If not, can you confirm **in writing now** that these close on the first boards (004 allows it for A2, B10, C1–C4)? | B10, A2, C3, C12, R6, R8, R11, R17 | Plans in the package, results on first boards |
| SQ27 | **Response sheet**: CSV acceptable, or a spreadsheet in your column order? Is **"Rev C"** the official label for the next package (ours is internal v3), and is the 6L to be archived rather than shipped? | Gate row 1, F2 | CSV, "Rev C", 6L archived |
| SQ28 | **Schematic-only review**: do you want one before layout (recommended)? Can you send 003 §9 as an editable table so we can sign and return it? | G1b; saves a layout loop | Yes; we send at G1b |
| SQ29 | **Test points**: the +12 V point is obsolete. Replace it with the converter output at J18 and the modem 5 V? Any other points you want (EN, WDI, PE)? | E4 | Converter output, modem 5 V, WDI, PE |
| SQ30 | **Logic-level switches** (R13): a preferred part (BSS138, DMG2302, …) or shall we select and list it? | R13 | We select and list in the BOM |

### 10.5 Documents and parts to send with the answers

Converter datasheet (SQ2) · fab capability sheet (SQ21) · enclosure drawing (SQ19) · modem board schematic or the PWRKEY/RESET translator note (SQ11) · module markings for the ESP32 board (SQ5) · the two build definitions (SQ23) · the intended earthing scheme (SQ17). Tracked as T0-01…T0-08 in §0.5.

---

## Appendix A — the six conditions as acceptance tests (review §6.4)

| # | Condition | Test we must pass |
|---|---|---|
| 1 | **Converter** | Named part, datasheet in the package; input ≥40 V covering the battery-disconnect voltage; its own input fuse and surge part; output 5.15 V ±1 %, 3 A continuous at +70 °C in the closed box, ≤50 mV droop for the 0.15→2.6 A step; no-load current in the budget |
| 2 | **Protection at J18** | Reverse protection + over-voltage cut-off that disconnects before the 5 V rail reaches 5.5 V and survives 12 V/24 V indefinitely; current limit near 3.5 A; any FET behind the cut-off or gate-protected (resistor + ~10 V zener); D2 re-rated above the converter's highest output; D2/ESD16 leakage (up to ~1 mA each) in the budget |
| 3 | **Copper** | ≥3 mm pour from J18 to the protection and on to the 5 V plane; ≥6 × 0.3 mm vias at every layer change, sized for the limit current; **J18→J5 both conductors ≤60 mΩ at +70 °C** |
| 4 | **Bulk at J5** | 470 µF low-ESR (105 °C, ≥16 V) + 10 µF + 100 nF within 10 mm along the copper |
| 5 | **Leads** | Converter→J18 ≤15 mΩ there and back (e.g. 200 mm of 0.75 mm² each way); J5→modem ≤30 mΩ with contacts, or the modem fed by its own lead |
| 6 | **Proof** | G1 model of the chain as built, then a bench trace at the modem board's own input through an LTE attach with GSM forced, converter at its lowest set point: 4.75–5.25 V throughout |

## Appendix B — numbers to reproduce on the Rev C board

Use these to check our own measurements before Serigreen does; they come from the Rev B files and the review.

| Quantity | Rev B | Rev C target |
|---|---|---|
| J18→J5 both conductors | 122 mΩ at 25 °C, 171 mΩ at +70 °C | ≤60 mΩ at +70 °C |
| Modem board at burst, J18 at 5.10 V | 4.73 V at 25 °C, 4.60 V at +70 °C | ≥4.75 V at the modem connector |
| Copper on In2 (seven nets) | 431.3 mm | 0 mm (all to outer layers) |
| B.Cu slot crossings | 54 | 0 |
| Antenna footprint plane coverage | 100 % both planes | 0 % (rule area) |
| Vias inside SMD pads | 65 of 224 | 0 (or filled/capped + fab note) |
| ESD part to protected pin | 5.4–21.8 mm (J20 pin 1: 46 mm) | ≤5 mm |
| PE to other nets | 0.225 mm | ≥0.5 mm |
| Nearest cap to J5 | 100 nF at 41.5 mm | 470 µF + 10 µF + 100 nF ≤10 mm |
| Nearest cap to U6 pins | 11.6 mm and 9.3 mm | ≤3 mm along copper |
| 100 nF at SPS30 (J13) | ~22 mm | ≤5 mm |
| DRC unconnected | 1 | 0 |
| Schematic parity | 209 | 0 |
| ERC | 0/0 with 4 ignored classes | 0/0, ignores justified |
| Placement file | 141 parts, no U4 | every fitted part, U4 in |
| BOM | 153 rows, no MPN/qty | MPN, qty, rating, temp, plating, variants |
| Job file | rev "rev?", finish "None" | revision, real stack-up, finish |

## Appendix C — the not-to-repeat list (CHK §6, with our own cases)

| What happened | Where it happened | Rule from now on |
|---|---|---|
| Gerbers plotted before zones were refilled and saved | 6 Oct files; Rev B 6-layer; **and the current 4L set (Gerbers 3.5 h older than the board)** | Refill → save → DRC → plot, always; record the three times |
| A hand-edited footprint on a power part | Q9's pads turned, 0.425 mm gate-to-source | Update from library; treat "does not match library" as an error |
| Polarity legend beside the wrong pad | J18, the only power input, with no reverse protection behind it | Read the pad net, then check the plotted silk |
| A part flagged out of placement and BOM | U4 (attributes 28) | Every fitted part clear of all three flags |
| BOM without MPN or quantity | Rev A, Rev B, and today's export | Fields filled before the BOM is exported |
| Files left from the previous revision | Stale design rules; a QA note describing a part not on the board; a QA note calling the board "manufacturing-ready" | Every report regenerated from the shipped files; no document may contradict a file |
| Two drivers on one line; an input floating at reset | PWR_EN; WDI on the expander | One driver per line; reset state in the truth table |
| Changes made without agreement first | 12 V→5 V input, RS485 removal, a second layer count | Ask first, one message; log "Agreed before drawing" |
| No item-by-item response | Rev B carried no change log | Response sheet first in the zip |
| Module dimensions estimated, never measured | Socket spacing wrong twice | Calipers and a 1:1 test-fit before the sockets are placed |
| A 6-layer variant built in parallel to a 4-layer one | Two packages, two sets of files, one shorted | One variant per package, one revision per package |
