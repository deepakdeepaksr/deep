# MoriShield Carrier Rev C — Complete Project Context and Handoff Package

| | |
|---|---|
| **Document** | CTX-CAR-4L-RevC-01 |
| **Date** | 2026-11-02 |
| **Purpose** | Single onboarding file for a new machine. Read this first, then `TASK_TRACKER.md` |
| **Audiences** | **Devin Desktop** (implementation) and **Qoder** (planning, status, documentation, prompt generation) |
| **Design files** | `pcb\MoriShield_Carrier.kicad_pcb` · `.kicad_sch` · `.kicad_pro` · `.kicad_sym` · `.kicad_dru` |
| **Status of the board** | **Not released for fabrication.** Release is Serigreen's, in writing, naming files by checksum |
| **Verification note** | **Read §9 first, then §8.** Both supersede parts of §3, §4 and §7. Last verified 2026-11-03 by an independent tool run |

---

## 1. Project overview

**What the hardware is.** The MoriShield Carrier is a 4-layer agricultural sensing board, **178.15 × 118.15 mm**, **159 footprints**, fitting a **200 × 155 × 80 mm** enclosure on an acrylic base. It carries two socketed modules — an **ESP32-S3 (Keyestudio/Edgehax S3-PRO, WROOM-1 N16R8, octal PSRAM)** on J1/J2 and a **Parry A7672S 4G LTE modem** on J3/J4 — plus an E22 LoRa radio (J6), and sensor ports for FDC1004 soil moisture, SPS30 particulate, MPU-6050, DS3231 RTC, an AS5600 magnetic wind vane (J26) and a reed-switch wind-speed input. Status LEDs (J24) and a buzzer (J25) are panel-facing.

**Power architecture.** The board is fed **5 V at J18** from an **external buck converter mounted inside the enclosure and supplied by Serigreen**. The 12 V rail is gone from the board entirely; the previous 12→5 V buck was removed from the carrier. Serigreen accepted the 5 V input **on six written conditions** (MS-CAR-REV-B-001 §6.4) — named converter, reverse/over-voltage protection at J18, 3 mm-class input copper, bulk capacitance at J5, lead-resistance budget, and a bench proof (B10). Those six conditions are tracked in `TASK_TRACKER.md` Part 4 and are the spine of the remaining power work.

**RS485.** Removed from this revision. The wind sensor became a reed switch + AS5600, and the soil probe is read on demand by a laptop through a USB-RS485 adapter rather than continuously. Item **C1 (P0)** therefore stands as a **deferral request** to Serigreen, not a completed change.

**People.** Aswin — firmware/software, **single point of contact with Serigreen and sole signatory** of the reply. Deepak — hardware and layout, works nights. Serigreen Technologies — the CTO office that reviews and releases.

**Where the project is.** Revision round 3: our **v3**, the CTO's **Rev C**. Rev A (2-layer, withdrawn) → Rev B (the 4L+6L package, reviewed 29 Oct) → **Rev C** (4-layer only; the 6-layer is withdrawn). Phase: **design hardening**. Stage gates S1–S5 are defined in `STAGE_TRACKER.md` (S1 schematic review, S2 power and interfaces, S3 layout completion, S4 fabrication release package, S5 bench evidence). The project sits between **S1** and **S3**, with **S4** and **S5** still ahead.

**The requirement universe — 118 obligations, 76 of them items.**

| Set | Source | Count |
|---|---|---|
| Items A1–H6 | MS-CAR-REV-A-004 §6.2 Table 9 ("the 59 items"), each with a priority and a *closed when* | 59 |
| Items R1–R17 | MS-CAR-REV-B-001 §11 Table 13 (new at Rev B) | 17 |
| Conditions 1–6 | MS-CAR-REV-B-001 §6.4 (the accepted 5 V architecture) | 6 |
| Checks C1–C13 | MS-CAR-CHK-001 §4 — the release gate | 13 |
| Package rows, pre-send ticks | CHK-001 Table 2 / Table 11 | 8 + 16 |
| Response-sheet columns | CHK-001 §7 | 5 |

**Naming caution.** `C1…C13` means **two different things** in this project: items C1–C13 of 004 Table 9, and checks C1–C13 of the release gate. `REPLY_TO_CTO.md` labels checks as "check C5", "check C12". Keep that convention.

---

## 2. Document purpose guide

### 2.1 The three live documents

| Document | What it is | Who edits it | Authority rule |
|---|---|---|---|
| **`TASK_TRACKER.md`** | The single authoritative register. Part 0 measured numbers · Part 1 the 76 items · Part 2 release gate C1–C13 · Part 3 the 16 pre-send ticks · Part 4 the six conditions · Part 5 internal tasks T-01…T-52 · Part 6 findings nobody asked for · Part 7 self-verification | Both. Devin updates rows from tool runs; Qoder owns structure and cross-document consistency | **Status authority lives here.** Other files copy from it, never the reverse |
| **`REPLY_TO_CTO.md`** | The **only outbound document**. §1 the 59 items · §2 the 17 new items · §3 answers we hold · §4 questions Serigreen must answer · §5 changes nobody asked for · §6 declared assumptions · §7 release statement | Qoder drafts and reconciles; Devin corrects rows from evidence | Never states anything a tool has not proved. Never says "ready". Never describes this board as a non-production build. |
| **`STAGE_TRACKER.md`** | Stage gate S1→S5 with verbatim acceptance wording from CHK §4 and 004 §7, plus the current measured-numbers block | Both | Gate wording is **quoted**, not paraphrased. Numbers refresh after every run |

### 2.2 Deliverable and evidence files

| File | Role |
|---|---|
| `revC\ResponseSheet_RevC.csv` | The response sheet CHK §7 requires as **file 1 in the zip**. 76 rows, 5 columns. **Generated** by `pcb\_make_response_sheet.py` from `REPLY_TO_CTO.md` §1/§2 — **never hand-edit it** |
| `revC\FAB_NOTES.md` | Fabrication and assembly instructions for the vendor: min features, via-fill requirement for the 65 vias in SMD pads, copper weights stated as assumptions, silkscreen rules |
| `revC\BUCK_AUDIT_XL4015_20261101.md` | 297-line component-selection analysis of the XL4015 candidate against condition 1 and items B1/B2/B8. **Verdict: No-Go** for the voltmeter variant. Recommendation: let Serigreen name the converter by condition-1 numbers, not by a ₹300 shelf part. §4 raises a **new protection-coordination risk** |
| `revC\erc_RevC.json`, `revC\drc_RevC.json` | Machine-verified ERC/DRC for the current files. `pack.ps1` Gate 1 refuses if either is older than the design |
| `revC\EVIDENCE_RevC.md` | Written evidence: §3 stitching, §7 the `/+5V_SENS` resistance arithmetic, the In2 inventory |
| `revC\E1_stitching_plot.png` | The E1 acceptance plot. Reproducible: run `pcb\_plot_stitching_final.py` |
| `revC\MoriShield_Carrier_RevC_bom.csv`, `..._pos_front.csv`, `..._pos_back.csv` | Sourcing and placement. Gate 4 refuses if older than the board. `pos_back` is header-only **by design** — no part sits on B.Cu |
| `revC\vias_in_pads.txt` | The 65 vias inside SMD pads, one row each. Invisible to DRC, so this file is the only evidence |
| `revC\decoupling_map.csv`, `_esd_measure.json`, `_evidence_maps.json` | C9 decoupling, C8 ESD distances, the plane/stitching datasets |
| `revC\pack.ps1` | The **only** sanctioned way to build a zip. Five gates, described in §6.4 |
| `revC\_work\` | Scratch DRC/ERC from intermediate steps, and `_e1_trial_plan.json` (the 85 via positions). **Note:** `REPLY_TO_CTO.md` cites `_e1_trial_plan.json` as `revC\` — it is at `revC\_work\` |
| `pcb\_snap\<purpose>_<stamp>\` | Snapshots before every board edit, with `census.json`. Restore point. **Do not delete or overwrite** |
| `pcb\*.py`, `pcb\*.ps1` | Working scripts (`_census.ps1`, `_plot_stitching_final.py`, `_make_response_sheet.py`, `_sexp.py`, `_verify_docs.py`). Many are single-use, but they are the audit trail |
| `_cto_extract\*.txt` | Plain-text extracts of all five CTO PDFs, page-marked — searchable source for requirement wording |
| `_cto_extract\*.py` | Qoder's independent verification scripts: `drcprobe\` (suppression audit), `erc_x.py` (library resolution), `trace_audit.py` / `trace2.py` (76-id reconciliation), `pos_check.py`, `e1_state.py`, `r4_verify.py` |
| `work done` (root) | Current session report. `pcb\work done` — earlier milestone log, sections 1–10 |
| Vendor references (root) | `ESP32_S3_WROOM_N16R8_Pinout_Reference.md`, `a7672s_4g_lte_modem_pinout_guide.md`. **Read-only. Never merge into project docs** |
| `_archive\` | The seven superseded planning documents. Read for wording, not for status |

### 2.3 Design library dependency — not optional

`pcb\fp-lib-table` resolves `${KIPRJMOD}/../morishield/morishield_hardware/libraries/MoriShield_Carrier.pretty`. The **whole folder tree must move together**, `morishield\` included. Separation is not theoretical: measured consequences are **336 `lib_symbol_issues`** if the symbol library is stale and **124 `footprint_link_issues`** if the `.pretty` does not travel. Both were produced deliberately as experiments; `pack.ps1` now stages both inside `project\libraries\`.

---

## 3. Completion status — verified

Re-verified on 2026-11-02 by independent tool runs. `ignored_checks` being `[]` in every report is what makes these zeros trustworthy.

| Item / check | Result | Evidence | Independently reproduced |
|---|---|---|---|
| **ERC** | **0 errors, 0 warnings**, no suppressed checks | `revC\erc_RevC.json` | ✅ own run → 0 items, `ignored []` |
| **DRC** | **0 violations, 0 unconnected, 0 parity**, no suppressed checks | `revC\drc_RevC.json` | ✅ own run with `--refill-zones --schematic-parity --severity-all --all-track-errors` |
| **Nine former suppressions** | All re-enabled; the **15 items they hid** (13 `track_not_centered_on_via`, 2 `missing_courtyard`) were **fixed, not re-hidden** | `.kicad_pro` severities, Part 6 findings 7/18 | ✅ `rule_severities` contains **no** `ignore` |
| **Courtyards** | Every one of 159 footprints has a courtyard (U4 and SW1 added; board **and** library) | `missing_courtyard` enabled, 0 items | ✅ text scan: 0 footprints without `CrtYd` |
| **Silkscreen** | `silk_over_copper` 78 → **0**, `silk_overlap` 46 → **0**, stroke font, all text ≥1.0 mm | `revC\drc_RevC.json` | ✅ `min_text_height 1.0`, `min_text_thickness 0.15` in `.kicad_pro` |
| **E1 ground stitching** | **Done.** 143 links inside both GND pours, worst distance **10.00 mm**, **0.0 %** beyond 10 mm (was 58 links / 35.36 mm / 55.6 %) | `revC\E1_stitching_plot.png` | ✅ ran `pcb\_plot_stitching_final.py` → `links=143 cells=15189 max=10.00 mm over10=0.0 %` |
| **How E1 was closed** | A **GND pour added on B.Cu** plus **85 stitching vias** (0.6/0.3 mm). An F.Cu pour was rejected on measurement: 1575 F.SilkS items vs **0** B.SilkS items at `min_silk_clearance` 0.0 | `pcb\_e1_stitch_trial.py`, `_work\_e1_trial_*.json` | ✅ zones now 6, incl. `GND B.Cu filled`; 143 GND vias counted directly |
| **Thermal relief** | 7 `starved_thermal` warnings on connector pads appeared with default zone settings and were cleared by thermal gap 0.25 / bridge 0.40 mm; PE zone priority raised to 1 so the earth pour is not starved | trial DRC series | ✅ PE still holds 2,015 mm² on B.Cu; B.Cu GND 15,174 mm² |
| **Census** | 159 footprints · 1171 segments · **314 vias** · **6 zones** · 134 net names. No removals; +85 vias and +1 zone are named | `pcb\_snap\E1_apply_20261101_234936` | ✅ own count matches exactly |
| **Pack.ps1 Gate 4** | **Passes** — BOM 23:51:39, POS 23:51:40, board saved 23:50:46 | running `pack.ps1` | ✅ it now stops at **GATE 5 PRODUCTION** (no release Gerbers), which is correct at this stage |
| **Library packaging** | `pack.ps1` stages `.kicad_sym`, `.kicad_dru` and the whole `.pretty` into `project\libraries\` with forward-slash `${KIPRJMOD}/libraries/` tables | `revC\pack.ps1` | ✅ stale-lib 336 → refreshed 0; missing-pretty 124 → staged 0 |
| **Traceability** | 76 ids in register, reply and CSV; **0 status disagreements** under the declared mapping; **0 priority mismatches** | `_cto_extract\trace2.py` | ✅ own audit |
| **Outbound truth (Block 0)** | `REPLY_TO_CTO.md` D3 corrected from the false "suppressions remain" to **Done**; gate row C5 corrected; R15 reconciled to Partly; status mapping declared in §1 | `REPLY_TO_CTO.md` | ✅ present in the file |
| **`/+5V_SENS` rail** | 313 → 177.4 → **156.6 mΩ**. 25 segments at 0.80 mm, 12 capped at 0.60 mm | `revC\EVIDENCE_RevC.md` §7 | ✅ width histogram confirms 0.8×25 / 0.6×12 |
| **R2 watchdog** | Closed since the previous round: `/WDT_WDI` routed, no jumper | DRC 0 unconnected | ✅ holds |
| **R3 J18 polarity** | `+` centred on pad 1 (`+5V_IN`), `−` on pad 2 (GND), stroke font | board text geometry | ✅ holds |

**Register tally (76 items):** Done 7 · Paper 3 · New 4 · Partly 27 · Open 34 · Superseded 1.
**Release gate:** **2 of 13 met** (C1, C2), 2 partly (C5, C12), 9 not met.

---

## 4. Pending work

### 4.1 Ready to execute — no external input needed

| # | Work | Item(s) | Why it is open | Effort |
|---|---|---|---|---|
| P1 | Move the 63 track items (448 mm, 8 nets) off In2.Cu so plane layers carry only planes: `/LED_DRV2` 14, `/+5V_SENS` 13, `3V3_C` 10, `/LED_DRV1` 8, `/I2C0_SCL` 7, `/SENS_EN` 7, `+5V` 2, `/I2C0_MUX_SC0` 2 | **R12**, check C10 | Needs real rerouting; a layer-token change alone creates clearance failures. Deliberately not half-done | L |
| P2 | 47 Ω series resistors on the 10 cabled I2C lines that lack them (CH2–CH6; only CH0/CH1 have R31–R34) | **E7**, check C10 | Needs new symbols, wires and labels in a 735 KB schematic whose topology is not safely visible to a script; parity 0 must survive | M |
| P3 | ESD protection within 5 mm along the copper: now 11.3–27.6 mm at J11–J23, **none at all** on J24, J25, J26 | **C8**, check C8 | Moving arrays is placement + reroute; new arrays need part numbers that must not be invented | L |
| P4 | Last 12 segments of `/+5V_SENS` at 0.60 mm | **B4**, condition 6 | 0.70 mm was **tested and rejected**: 11 clearance items on F.Cu, 2 on In2, colliding with J7, a `+5V` via at (184.86, 168.95) and a `3V3_C` via at (209.25, 168.00) | M |
| P5 | Plot release Gerbers, drill, **IPC-D-356 netlist**, job file, fab drawing, then run `pack.ps1` | checks C3, C4 | `pack.ps1` Gate 5 blocks on purpose. **No IPC-356 file exists anywhere in `revC\`** | S |
| P6 | Record the three timestamps (save → DRC → plot) in the response sheet | check C3, item D1 | Required wording; cannot be back-filled honestly | S |
| P7 | Bench plan + evidence shells: G1 transient model, FMEA, bring-up, readings, 3D with both modules and the box | **G1–G4**, checks C9, C13 | Documents do not exist yet | M |
| P8 | Reconcile placement exclusions: H1–H4 and TP2–TP12 carry `excl_pos=True` but **TP1 is placed** — 144 of 159 in the file | check C6 | Asymmetry is unexplained; confirm intentional or align | S |

### 4.2 Blocked on Serigreen — these stop work

| Q | Question | Items | Effect |
|---|---|---|---|
| 1 | Accept a written **RS485 deferral**? | **C1 (P0)** | Cannot close C1 or gate the package |
| 2 | Accept **route C** (discrete OVP/reverse controller + low-Rds FETs) in place of the named TPS26630? Arithmetic: 40 mΩ vs 66 mΩ against a 60 mΩ budget | **R4 (P0)**, condition 2, U10 | U10 stays a placeholder; ERC-clean but the board has **no protection at J18** |
| 3 | **Converter choice** — see `BUCK_AUDIT_XL4015_20261101.md`. Our audit says **No-Go** on the XL4015 voltmeter module (8–36 V operating, 40 V absolute max, condition 1 asks ≥40 V) and asks Serigreen to name the part **by condition-1 numbers**. Also raises a new coordination risk: the XL4015's 7 A limit sits between F1's hold and trip, ≈+60 K on 1.5 mm input copper | conditions 1, 5; **B1, B2, B10** | Stops S2 power work. **Note:** `REPLY_TO_CTO.md` carries both Q8a and Q9 on this decision — merge before sending |
| 4 | Which end of the ESP32 module carries the **antenna**? | **E3**, check C10 | No keep-out drawn; we refuse to guess |
| 5 | microSD vs GPIO10/11 — CHK-001 C11 says GPIO10–14 are the board's SD; the Keyestudio table says io35–39 | **A7, C2, C5, R11** | Pin map cannot be signed |
| 6 | Reed switch on GPIO41, which C11 calls output-only | **R11** | Pin budget short by one |
| 7 | Battery sense: GPIO6 is now `/MODEM_RST`; every ADC1 header channel is used | **B9** | No supply monitoring |
| 8 | Agree **plug/fill/cap per IPC-4761 Class B or C** for the **65 vias in SMD pads**, and price it | **R16**, check C5 | Alternative is 65 routing changes |
| 9 | Accept the ~2 A continuous at +70 °C deviation on the incumbent converter | **B2** | Condition-1 compliance |

### 4.3 Blocked on the bench (a person with an instrument)

`B1` E22 LoRa header pinout — **highest risk**: J6's pads are unnamed and the carrier order does not match the Ebyte convention; 5 V on a mode pin would stop the radio booting. `B2` microSD continuity. `B3` GPIO41 LED presence. `B4` which 3.3 V regulator is warm — **`3V3_C` is double-driven** by J1.1/J1.2 and the carrier's TPS7A2033. `A1` PWR_EN polarity, `A2` RESET polarity. Plus the B10 burst trace and the six-condition proof.

### 4.4 Deliberately not attempted by script

Four schematic surgeries — `/PWR_EN` second driver, `3V3_C` off J1.1/J1.2, `/MODEM_RST` series resistor, U8 to I2C-1. A previous attempt at the first exposed a dead spur that DRC revealed one segment at a time across 17 segments; it was reverted from a snapshot. **These need the KiCad GUI.**

### 4.5 Known inaccuracies still in the files (fix before sending)

1. **`STAGE_TRACKER.md` measured-numbers block has four stale rows** that contradict its own top rows: "Package build **blocked** — ResponseSheet missing / gate 3" (the CSV exists and it stops at Gate 5); "`pack.ps1` does not stage `.kicad_dru`/`.pretty`" (it now does); "Derived files older than the design … 16:54–17:14" (regenerated 23:51); "`/+5V_SENS` 177.4 mΩ" (now 156.6 mΩ).
2. Gate tally not re-counted after E1 and the courtyard/text work.
3. `REPLY_TO_CTO.md` cites `revC\_e1_trial_plan.json`; the file is at `revC\_work\_e1_trial_plan.json`.
4. Q8a and Q9 both ask the converter question — one should carry the audit's No-Go.
5. `min_text_thickness` 0.15 mm and `min_text_height` 1.0 mm are **the CTO's stated rule, not a fab capability sheet** — declared, but F1 is still open.

---

## 5. Workflow instructions — which tool does what

### 5.1 Environment (both tools)

```
Workspace   C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb   (OneDrive-synced)
KiCad       10.0  ->  C:\Program Files\KiCad\10.0\bin\kicad-cli.exe
KiCad Py    C:\Program Files\KiCad\10.0\bin\python.exe   (NOT plain "python" — no pcbnew there)
Shell       PowerShell 7
```

> **⚠ Migration hazard — check this first on the new machine.** **95 files embed the absolute path** `C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb` (126 occurrences), including **`revC\pack.ps1`** (`$root = 'C:\Users\...'`) and every working script in `pcb\`. If the new laptop uses a different username or path, `pack.ps1` throws "missing design file" and the analysis scripts read nothing. Either keep the identical path, or run one pass replacing `$root`/`P`/`base` literals with the new path in `revC\*.ps1` and `pcb\*.py`, then re-verify §3. Also confirm KiCad **10.0** is installed at the same location and that `morishield\morishield_hardware\libraries\` came with the tree.

### 5.2 Devin Desktop — implementation

Owns: KiCad CLI runs, Python board surgery, Gerber/plot/export, script creation, applying design changes.

Standing rules (each exists because of a mistake already made here):

1. **Snapshot then census** before every board edit: copy to `pcb\_snap\<purpose>_<stamp>\`; record footprints/segments/vias/zones/net names. If a count drops and you cannot name what you removed, restore.
2. **Always** pass `--refill-zones --schematic-parity --severity-all --all-track-errors`. Without `--schematic-parity` the parity section is silently empty and reports a misleading 0. This produced false "clean" results twice.
3. **Never** `board.Remove()` on copper — it invalidates the track container. Edit the `.kicad_pcb` as text and delete the balanced `(segment …)` / `(via …)` block whose UUID the DRC report gives. Then reload and re-run DRC. Deleting one dangling segment orphans a via, which orphans the next track: chase the whole dead branch.
4. **Zones:** fill via `ZONE_FILLER.Fill(b.Zones())` in memory; adding or editing zones through the API has crashed saves. Trial zone work goes on a **copy** first, and the trial is only real once `--refill-zones` DRC on the saved file is clean.
5. **Library paths use forward slashes.** Backslashes are eaten as escapes, resolution fails silently, and ERC then reports hundreds of phantom `lib_symbol_issues`. Whenever you change a path, run the unmodified control in the same pass and report both numbers.
6. **Text tokens:** layer token is `F.SilkS`; in `(justify a b)` the vertical token comes second (`right center` makes the board refuse to load); DRC `pos` values are already millimetres; `PCB_TEXT` has no `GetOrient`/`GetStrokeWidth`/`GetFontSize` — read the file.
7. **In2 is a plane layer.** Items placed there are visible to the fab as copper; `starved_thermal` appears the moment an outer pour exists — set thermal gap 0.25 / bridge 0.40 and keep PE at priority 1.
8. **Never invent** MPNs, ratings, temperatures, fab capabilities, dielectric constants or measurements. Write `TBC` and add a question.
9. **Never** describe this board as a non-production or throwaway build — that wording is banned from every document in this project, including denial sentences. **Never** claim fabrication readiness. Do not mark an item Done unless a tool or measurement proves it.
10. After every change: update `TASK_TRACKER.md` Part 0/1/2 and `STAGE_TRACKER.md` **from the tool output**, then regenerate the CSV with `pcb\_make_response_sheet.py` — never by hand.
11. Session report goes to the root file `work done`, in the nine-part format: numbers before/after · census · status changes with evidence · not finished and why · newly found errors · files touched.

### 5.3 Qoder IDE — planning, status, documentation, prompts

Owns: requirement tracing and reconciliation, document structure and cross-document consistency, status honesty, question drafting, prompt generation for Devin, independent verification of Devin's claims.

Standing rules:

1. **Re-run, don't trust.** Verify any claimed number with `kicad-cli` or a board script before it enters a document. Every figure in §3 was reproduced this way; two of Devin's earlier claims and one of Qoder's own hypotheses were disproved by doing this.
2. **Run the control.** When an experiment produces a surprising number, first prove your harness is not the cause. A phantom "460 ERC items" and a "328/113 from the wrong project" were both harness artefacts.
3. Register is authoritative. CSV and reply follow it. Report drift as a count.
4. Quote requirement wording from `_cto_extract\*.txt` rather than paraphrasing.
5. Prompts for Devin: block-structured, safety rules first, explicit **DO NOT ATTEMPT** list, and a numbered **REPORT BACK** contract.
6. Update memory for durable project facts; never record credentials.

### 5.4 Handoff protocol between the two tools

```
Qoder -> Devin : prompt in chat, block-structured, with a REPORT BACK contract
Devin -> repo  : design edits + snapshots + script evidence, then trackers updated
Devin -> root  : "work done" session report (nine-part format)
Qoder -> repo  : re-runs ERC/DRC/census/traceability, corrects stale rows,
                 regenerates REPLY_TO_CTO.md + CSV, then writes the next prompt
```

No file is edited by both tools in the same pass. Board files belong to Devin; document integrity and the outbound reply belong to Qoder.

---

## 6. Evidence verification protocol

### 6.1 The three commands that decide everything

```powershell
$kc = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
$root = 'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'   # fix on a new machine

& $kc sch erc --severity-all --format json -o "$root\_cto_extract\erc_now.json" `
       "$root\pcb\MoriShield_Carrier.kicad_sch"

& $kc pcb drc --refill-zones --schematic-parity --severity-all --all-track-errors `
       --format json -o "$root\_cto_extract\drc_now.json" "$root\pcb\MoriShield_Carrier.kicad_pcb"

& 'C:\Program Files\KiCad\10.0\bin\python.exe' "$root\pcb\_plot_stitching_final.py"   # E1
```

### 6.2 How to parse a report — four numbers, not one

| Extract | Must read |
|---|---|
| ERC | `[v for s in d['sheets'] for v in s['violations']]` by severity |
| DRC | `len(d['violations'])` **and** `len(d['unconnected_items'])` **and** `len(d['schematic_parity'])` |
| **Both** | `[i['key'] for i in d['ignored_checks']]` → must be **`[]`**. A 0 with suppressions in it is not a clean board |

### 6.3 Hidden-defect probes — the checks that DRC cannot see

| Probe | Command | Current value |
|---|---|---|
| Vias inside SMD pads | `pcb\` via-vs-pad `HitTest`, or `revC\vias_in_pads.txt` | **65** of 314 |
| Suppressed-check impact | re-enable every `ignore` on a scratch copy and re-run (`_cto_extract\undercite.py`, which writes `_cto_extract\drcprobe\drc_undenied.json`) | was 15 hidden → now **0**, and nothing re-suppressed |
| Library resolution | point tables at each candidate library, forward slashes only (`_cto_extract\erc_x.py`) | own **0** · stale **336** · no `.pretty` **124** |
| Census guard | `pcb\_census.ps1` or `_cto_extract\r4_verify.py` | 159/1171/314/6/134 |
| Placement completeness | `_cto_extract\pos_check.py` | 144 of 159; 15 excluded, TP1 asymmetry open |
| Timestamp integrity | compare `revC\` artefact times against the board save | all fresh (23:51) |

### 6.4 The five `pack.ps1` gates — what each protects

| Gate | Rule | State |
|---|---|---|
| 1 REPORTS | ERC/DRC must not be older than the schematic/board (finding **R1** — the Rev B failure) | pass |
| 2 INPUTS | design files **and** the `.pretty` must exist | pass |
| 4 DERIVED | BOM and both placement files must post-date the board (C6) | **pass** since 23:51 |
| 3 SHEET | `ResponseSheet_RevC.csv` must exist and be file 1 (CHK §7) | pass |
| 5 PRODUCTION | release Gerbers + drill must exist and post-date the DRC (C3: refill → save → DRC → plot) | **blocks here — correct for this stage** |

### 6.5 Traceability reconciliation

`_cto_extract\trace2.py` compares TASK_TRACKER Part 1 ↔ REPLY_TO_CTO §1/§2 ↔ CSV for all 76 ids: presence, priority, and status under the declared mapping `New→Open`, `Paper→Partly`. **Current result: 0 disagreements, 0 priority mismatches.** Re-run after any status edit; a non-zero count means the outbound reply no longer describes the board.

---

## 7. Next immediate actions, in order

### 7.1 Machine setup (30 min, blocking)

- [ ] Replicate the path `C:\Users\<user>\OneDrive\Desktop\PCB\SERIGREEN\new pcb` **exactly**, or run one replacement pass over `revC\pack.ps1` and `pcb\*.py` (95 files hold absolute literals)
- [ ] Install KiCad **10.0** at `C:\Program Files\KiCad\10.0`; confirm `kicad-cli.exe` and `bin\python.exe` both exist
- [ ] Copy the tree **with** `morishield\morishield_hardware\libraries\` and `pcb\_snap\`
- [ ] Run §6.1 ERC + DRC → expect **0/0 and 0/0/0 with `ignored_checks []`**
- [ ] Run `_cto_extract\trace2.py` → expect **0 disagreements**
- [ ] Run `revC\pack.ps1` → expect a stop at **GATE 5 PRODUCTION**

### 7.2 Then, in this order

| # | Action | Tool | Effort | Gate unlocked |
|---|---|---|---|---|
| 1 | Fix the five stale rows in §4.5 and re-count the gate tally; regenerate the CSV | Qoder | S | outbound accuracy |
| 2 | Merge REPLY Q8a/Q9 into one converter question carrying the audit's No-Go | Qoder | S | Q3 to Serigreen |
| 3 | **Send the question set to Serigreen now** — Q1, Q2, Q3, Q9 are on the critical path and cost nothing to ask | Aswin | S | unblocks S2 |
| 4 | Bench item `B1` E22 header pinout before any further radio work | Aswin/Deepak | S | A11, C4 |
| 5 | Placement-exclusion reconciliation (TP1 vs TP2–TP12), then a note in `FAB_NOTES.md` | Devin | S | check C6 |
| 6 | P4 — the 12 capped `/+5V_SENS` segments: pour inset or route change, then re-measure mΩ | Devin | M | condition 6, B4 |
| 7 | P2 — 47 Ω on the 10 I2C lines, schematic + board, parity must stay 0 | Devin | M | E7, C10 |
| 8 | P1 — clear 63 items off In2.Cu, one net at a time, DRC after each | Devin | L | R12, C10 |
| 9 | P3 — ESD arrays to ≤5 mm at J11–J23, J24/J25/J26 | Devin | L | C8 |
| 10 | P7 — evidence documents (G1 model, decoupling map, 3D with box, FMEA, bring-up) | Both | M | C9, C13 |
| 11 | P5/P6 — plot release Gerbers + drill + **IPC-D-356**, record the three timestamps, build the zip | Devin | S | C3, C4 |

### 7.3 What "done for this round" means

Not fabrication release. The honest end-state for Rev C's next outbound package: ERC/DRC 0 with **no suppressions** (✅ today), every gate row justified in writing, the six conditions answered with numbers or an explicit deviation request, C1/C8/E7/E3/R4 moved from Open, and the release held by Serigreen's written approval naming the zip's checksums.


---

## 8. Deltas from 2026-11-02, late session - read this before §3, §4 and §7

Everything below was measured or read out of the files on 2026-11-02 and is current as of
23:55. Where it contradicts an earlier section, **this section wins**.

### 8.1 Verified state at the end of 2026-11-02

| Measure | Value | How it was checked |
|---|---|---|
| ERC | **0 violations, `ignored_checks []`** | own `kicad-cli` run |
| DRC | **0 violations, 0 unconnected, 0 parity, `ignored_checks []`** | own run with all four flags |
| Census | **159 footprints · 1171 segments · 314 vias · 6 zones · 134 net names** | own `pcbnew` count |
| Zones | PE on B.Cu · **GND on In1.Cu** · **GND on B.Cu** · /3V3_SENS_SW ×2 and +5V on In2.Cu | own run |
| E1 ground stitching | **Met.** 143 links inside both pours, worst distance 10.00 mm, 0.0 % beyond 10 mm | own re-run of `pcb\_plot_stitching_final.py` |
| Vias inside SMD pads | **65** of 314, unchanged; IPC-4761 plug/fill/cap note present in `FAB_NOTES.md` | own geometric test |
| Release gate | **4 of 13 met** (C1, C2, C5, C12), 1 partly (C9), 8 not met | `STAGE_TRACKER.md` |
| Traceability | 76 ids in register, reply and CSV; **0 status disagreements, 0 priority mismatches** | `_cto_extract\trace2.py` |
| `pack.ps1` | stops at **GATE 5 PRODUCTION** (no release Gerbers). Gates 1-4 pass | own run |
| Timestamps | board save 22:31:44 → DRC 22:45:13 → plot 22:45:15, the order C3 requires | `STAGE_TRACKER.md` |

### 8.2 The finding that reversed a day of work

**J6 is not mis-wired.** Read against the Ebyte E22-900T22D datasheet order
(1 M0, 2 M1, 3 RXD, 4 TXD, 5 AUX, 6 VCC, 7 GND) with the module inserted the obvious way, the
socket looked mirror-imaged - VCC on GPIO10, GND on GPIO11, 5 V on M1. **Inserted 180 degrees
the other way, all seven nets line up**, UART direction included, matching Aswin's working bench
wiring exactly. The net names themselves (`/E22_M0` on pad 7, `/E22_M1` on pad 6) prove the
designer intended it. Aswin then confirmed on the physical module: labels read M0, M1, RXD, TXD,
AUX, VCC, GND, and the GND pin is continuous with the SMA shell and the three mounting holes.

**What is actually wrong is that nothing marks or keys the orientation.** No silkscreen, footprint
pads named only 1 to 7, header unkeyed. Item A3's acceptance is "a reversed module cannot go in or
is obvious" - today it does neither. Devin also recorded the method lesson: a net rename kept
parity at 0 while breaking the copper, so **parity alone is not evidence**.

### 8.3 Measured pin facts (Aswin's multimeter, 2026-11-02)

| Fact | Result | Consequence |
|---|---|---|
| microSD slot | pin 2→**GPIO10**, 3→**GPIO11**, 5→**GPIO12**, 7→**GPIO13**, 4→3V3, 6→GND | CHK-001 C11 is **right about 10-13, wrong to include 14**. The card's CS and MOSI are being driven by `/E22_M1` and `/E22_M0` |
| GPIO9 | **not on the slot** | `/I2C0_SCL` on GPIO9 is **safe** - the whole I2C-0 bus (mux, expander, MPU, RTC) stands |
| GPIO35-38 | octal-PSRAM group on the N16R8 | unusable. **GPIO39 (J2.9) is the only free usable input** in that block - the reed's destination |
| Reed switch | `/REED_PULSE_F` → J2.7 = **GPIO41**, which C11 calls output-only | moves to J2.9 = GPIO39 (T-56) |
| Analog inputs | J15 soil → GPIO2 = **ADC1_CH1**; J16 → GPIO1 = **ADC1_CH0** | both on ADC1, which keeps working with Wi-Fi on. Luck, not a decision - recorded because it constrains future swaps |
| Capacitance sensor | **FDC1004 on J21 = I2C channel 5**, not on J15 | CH5 is not spare |
| J17 (CH4) and J20 (CH6) | fully wired ports, **no identified sensor anywhere** | J20 blocks the LoRa keep-out - question 8e |

### 8.4 Decisions taken, and the one still open

**Taken:** E22 M0 and M1 will be strapped to ground through **0 ohm 0603 resistors** (not dead
wire) so configuration mode stays reachable by lifting a strap with the module out of its socket.
This frees GPIO10/11 for the microSD. It was chosen over driving them from expander U8 because a
hard strap is deterministic at every power-up and does not put radio mode behind a muxed, cabled
I2C bus that item R17 already says is unreliable.

**Still open, and it changes parts:** whether Serigreen would rather have mode control from
firmware (expander pins) than a lift-a-strap service action - question 8c. Also the **E22 supply
rail**: the board feeds it 5 V, its TXD and AUX follow VCC, and the ESP32-S3 is not 5 V tolerant,
so we propose 3V3 (how it was bench-tested) - question 8d.

### 8.5 What is queued and not yet in the board

| Task | Change | Items |
|---|---|---|
| **T-55** | Strap E22 M0/M1 to GND through 0 ohm; delete `/E22_M0` and `/E22_M1`; J1.16/J1.17 become unconnected | A7, C2, C5, R11, C11 |
| **T-56** | Move `/REED_PULSE_F` from J2.7 (GPIO41) to J2.9 (GPIO39) | R11, C11 |
| **T-57** | Name every port in the schematic Value field **and print the names on F.SilkS**; mark J6 with pin functions and orientation | E5, C12, A3, C11 |
| **T-58** | Ask Serigreen to price a keyed or shrouded header at J6/J3/J4 | A3 |

**T-55 and T-56 are the highest-value remaining edits on the board** - they close the microSD
conflict, which is a P0 (A7, C2) and blocks the signed pin map (C11).

### 8.6 S3 status, corrected

| Check | State | Reason |
|---|---|---|
| C2 | **Met** | 0 unconnected, 0 parity, no dangling |
| C5 | **Met** on its own wording | mismatch 0, courtyard 0, silk 0, constraints met, 65 vias carry a fab note. Item R16 (agreement + price) stays open |
| C12 | **Met** | verified on the plotted Gerber, J18 marks 0.05 mm off pad centres, timestamps in order |
| C9 | **Partly - and harder than it looked** | **36 supply pins, 0 meeting the CTO's two-part rule** (21 connector, 6 MOSFET, 6 IC, 3 diode; 36 fail local 100 nF, 31 fail bulk). J5 sits under the modem outline; **J26, the AS5600 port added this revision, sits under the DS3231 outline** |
| C10 | **Not met** | 63 items on In2.Cu; no antenna rule area - the E22 zone is blocked by `/3V3_SENS_SW` and `/I2C0_SDA_CH3/CH6` in the same corridor; power copper 1.5 mm not the 3 mm pour of condition 3 |

**S3 is not reachable today.** C9 became a real layout problem (36 capacitor moves), and C10 needs
routing hours plus two answers. Deliverable now: **4 of 13 checks met, S3 partial with named
reasons.**

### 8.7 What is still owed by people, not by tools

| Who | Item |
|---|---|
| **Aswin** | ESP32 **antenna tip to nearest header pin**, in mm (fixes the outline and lets the keep-out be drawn) · what J17 and J20 are for · whether the ESP32 and modem antenna whips exit the lid (92 mm whip will not stand in an 80 mm box - two sealed SMA bulkheads proposed) · E22 physical pin-1 photo for the record |
| **Serigreen** | questions 1, 2, 4, 6, 7, 8/8a, 8b-8f in `REPLY_TO_CTO.md` |
| **Bench** | B1-B4, A1, A2, the B10 burst trace, the 24-hour run (C2), reed counts at 1/10/50 Hz (R11) |

### 8.8 Document state at handoff

| Document | Last written | Notes |
|---|---|---|
| `TASK_TRACKER.md` | 2026-11-02 23:55 | Part 6 renumbered **1-36 in file order, no duplicates**; rows A7, C2, C5, R11 rewritten with the measurements; T-55 to T-58 added |
| `REPLY_TO_CTO.md` | 2026-11-02 23:55 | questions 3 and 5 marked answered-by-us; **8b-8f added**; rows A7, C2, C5, E5, R11 rewritten |
| `STAGE_TRACKER.md` | 2026-11-02 23:55 | five new measured rows; E1 removed as an S3 blocker |
| `revC\ResponseSheet_RevC.csv` | regenerated | 76 rows, generator reports 0 mismatches |
| `_cto_extract\` | - | every verification script used here, plus timestamped `.bak-` copies of the three documents before this pass |

**Rollback:** `_cto_extract\TASK_TRACKER.bak-*` and `_cto_extract\REPLY_TO_CTO.bak-*` hold the
pre-edit versions of this pass. Board rollback: `pcb\_snap\T2_keepout_20261102_224411\` and
`pcb\_snap\T4_geom_20261102_223102\`.


---

## 9. Session 2026-11-03 - what landed, and the two regressions it caused

### 9.1 Board work completed (all verified by re-running the tools)

| Change | Result |
|---|---|
| **J26** (the AS5600 wind-vane port) moved out from under the RTC | 347 bottom-row positions measured, **0 legal** - courtyards leave 6.6-7.8 mm for a 13.49 mm part. Left-edge rot-90: 0 legal. Left-edge rot-0: **20 legal**. Placed at **(134.00, 153.50)**, 61.4 mm reroute, 1.175 mm margin |
| **J5** (modem 5 V terminal) moved out from under the modem | 904 legal positions; placed at **(222.00, 91.40)**, 1.91 mm outside the outline. Rotation rejected - it raises `lib_footprint_mismatch` |
| **Decoupling**: three capacitors relocated | C41 to Q9.3, C14 to D2.1, C33 to J13.1 |
| **Silkscreen**: 14 reference fields moved, 12 port labels + 8 J6 pin/orientation marks added | all at 1.0 mm / 0.15 mm stroke font, **DRC 0**, every one confirmed present in the plotted Gerber by stroke count |
| **Schematic Value fields** for 10 ports | parity stayed 0 - a property edit, not netlist surgery |
| **In2.Cu**: +5V moved to F.Cu | 63 to **61 segments**, 448.41 to **431.40 mm**, 8 to **7 nets**. Only +5V had a free corridor (+0.24 mm) |

### 9.2 Two regressions - found by re-measuring, not reported by the run

**These are the important part of this section.**

1. **E1 ground stitching has regressed and is no longer met.** Re-running
   `pcb\_plot_stitching_final.py` gives **144 links, worst 11.16 mm, 0.1 % beyond 10 mm** -
   against the 143 / 10.00 mm / 0.0 % that every document still carried. The copper moves
   above broke it. **E1 is now recorded as `New` (regressed) in `TASK_TRACKER.md`, and
   `REPLY_TO_CTO.md` says so openly.** The cause is structural: the stitching metric is not
   a DRC check, so DRC 0 gives no warning. **Standing rule: re-run the stitching measurement
   after every copper or via change, before any document repeats a number.**
2. **Vias inside SMD pads went 65 to 67.** Two were introduced by the reroutes.
   `revC\vias_in_pads.txt` and the fab note in `revC\FAB_NOTES.md` still say 65 of 314, so
   **check C5's evidence quotes a number the board no longer matches.** Both files need
   regenerating. C5's *wording* is still satisfied (a fab note exists), but the count in it
   is wrong.

### 9.3 Verified state at the end of 2026-11-03

| Measure | Value |
|---|---|
| ERC | 0 violations, `ignored_checks []` |
| DRC | 0 violations, 0 unconnected, 0 parity, `ignored_checks []` |
| Census | 159 footprints / **1178** segments / **313** vias / 6 zones / 134 nets |
| Vias in SMD pads | **67** of 314 |
| E1 stitching | **11.16 mm worst, 0.1 % beyond 10 mm - FAILING** |
| Decoupling | 36 supply pins: **1 meets both, 3 meet local, 33 fail** |
| Under-module | modem: J3, J4 only. DS3231: 7 parts, J26 gone. GY-521: R31, R32. ESP32: J1, J2. E22: J6 |
| In2.Cu | 61 segments, 431.40 mm, 7 nets |
| Gate | **4 met** (C1, C2, C5, C12), **1 partly** (C9), **8 not met** — counted from the Part 2 rows. **C9 and C10 are the two S3 checks still open** |
| Traceability | 76 / 76 / 76 ids, 0 disagreements, 0 priority mismatches |
| pack.ps1 | stops at GATE 5 PRODUCTION, no zip |

### 9.4 A methodology bug worth knowing about

The old decoupling map **counted 1 uF as "bulk" and parsed the string "100nF/16V" as
10 uF**. So the earlier published numbers (36 fail local, 31 fail bulk, worst 173.11 mm)
were partly wrong. The current map uses the CTO's verbatim thresholds and every row carries
a verdict. **Do not quote the pre-2026-11-03 decoupling figures anywhere.**

### 9.5 What is owed by whom, right now

**Aswin, in the KiCad GUI - nothing else can move these:**
- **T-55** the E22 M0/M1 0 ohm straps to GND (closes the microSD conflict, a P0)
- **T-56** the reed from GPIO41 to **GPIO39** at J2 pin 9
- **T-59** 13 decoupling pins that have a legal capacitor site but no movable donor -
  they need new parts added in the schematic; coordinates are in `TASK_TRACKER.md`
- ESP32 antenna **tab tip to nearest header pin**, in mm
- What **J17 and J20** are for (J20 blocks the LoRa keep-out)
- GY-521 and DS3231 **heights**

**Devin, board-only:**
- Fix E1: add stitching vias where the plane exceeds 10 mm, then re-measure
- Regenerate `revC\vias_in_pads.txt` and the count in `revC\FAB_NOTES.md` to 67
- The remaining 20 connector-class decoupling pins, board-only moves

**Serigreen:** questions 1, 2, 4, 6, 7 (now 67 vias), 8/8a, 8b to 8f in `REPLY_TO_CTO.md`.

### 9.6 Rollback for this session

`pcb\_snap\T_A_J26_*`, `T_B_J5_*`, `T_C_caps_*`, `T_D_silk_*`, `T_E_in2_*`.
Document backups before the 2026-11-03 corrections:
`_cto_extract\TT.bak3`, `_cto_extract\RT.bak3`.

### 9.7 Gate tally correction, and one more standing rule

`TASK_TRACKER.md` Part 2's own summary line said "2 partly (C9, C10), 7 not met" while its
rows say **C9 Partly and C10 Not met** - 4 met, 1 partly, 8 not met. Corrected in place.
The same wrong tally had propagated into `PROJECT_CONTEXT_RevC.md` and the 2026-11-03
session report.

**Standing rule added: a summary count must be derived from the rows, never typed.**
`python _cto_extract\gate_truth.py` now recomputes it from Part 2 and prints the three
numbers; run it with every wrap-up and copy its output into the tally line.
