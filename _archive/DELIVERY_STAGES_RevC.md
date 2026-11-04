# Rev C — Staged Delivery Plan

| | |
|---|---|
| **Document** | SD-CAR-4L-RevC-01 |
| **Date** | 1 November 2026 |
| **Board** | MoriShield_Carrier, 4-layer (`pcb\MoriShield_Carrier.kicad_pcb`) |
| **Contact and signatory** | Aswin |
| **First send** | 2 November 2026 — schematic-only review package |
| **Companion** | `TASK_SHEET_RevC_4L.md`, `INPUT_REGISTER_RevC.md`, `WORK_REGISTER_RevC.md`, `VERIFICATION_20261101.md` |

**Rule for every stage:** nothing is claimed as closed unless a tool reports it. Every number below is from a `kicad-cli` run or a measurement, not from recollection.

---

## 0. Where the design stands, verified today

| Check | Result | Tool |
|---|---|---|
| Schematic ↔ PCB parity | **0 items** | `pcb drc --schematic-parity` |
| Unconnected items | **0** | `pcb drc` |
| ERC | **0 errors, 1 warning** (`/5V_PROT` isolated label) | `sch erc` |
| DRC | **145 items, 16 errors** — no shorts, no signal clearance failures | `pcb drc --refill-zones` |
| 5 V input copper | `+5V_IN` and `+5V_F` at 1.5 mm, ≈ 13 mΩ | direct measurement |
| GSM interface | 24 / 24 pads match the vendor guide | cross-checked |
| ESP32 interface | 44 / 44 pins match the Edgehax reference | cross-checked |
| Watchdog (R2, P0) | **closed** — U8 P07 → U4 WDI, no jumper | verified |
| J18 markings (R3, P0) | **closed** — `+` centred on pad 1, `−` on pad 2, stroke font | measured |

---

## 1. Stage summary

| Stage | What ships | My work | Elapsed | Needs from others |
|---|---|---|---|---|
| **S0** | Nothing — design made honest | 2 h | today | nothing |
| **S1** | **Schematic-only review package** | 3 h | tonight → 2 Nov | answers improve it, do not block it |
| **S2** | Power protection and interface close-out | 4 h | 3–5 Nov | A1, A2, B1, B2 + Serigreen on the deviation |
| **S3** | Layout completion package | 8–12 h | 6–9 Nov | A3, A4, B3, B4, C-6 |
| **S4** | **Fabrication release package** | 3 h | 10–11 Nov | Serigreen's written release |
| **S5** | First-article bench evidence | — | boards + 7 days | hardware |

**Total my-work: about 30 hours across ten days.** Elapsed time is dominated by waiting on four people: you, the vendor docs, the bench, and Serigreen.

---

## 2. S0 — Make the design honest *(2 h, today, no inputs needed)*

Everything here is mechanical, reversible, and needs nobody's permission.

| # | Fix | Time | Gate |
|---|---|---|---|
| S0-1 | Title block: `Rev C`, date, drop "Proto-Simple Rev 0.2 (Post-RS485 Stripped)", A3 sheet | 10 min | string absent from the file |
| S0-2 | Delete `3V3_C` from J1.1 and J1.2 — the Edgehax 3V3 pins are **outputs** | 15 min | DRC, parity both 0 regression |
| S0-3 | `3V3` class floor → 0.20 mm with the written justification | 10 min | 13 `track_width` errors → 0 |
| S0-4 | Orientation silk on J3 and J4 — `PIN 1 ▲` plus an arrow, both rows | 15 min | visible on the render |
| S0-5 | `/E22_M1` → J2.8 (GPIO40), `/E22_M0` → J1.8 (GPIO15); delete those two no-connects | 30 min | parity 0, unconnected 0 |
| S0-6 | Add the stackup: 4 layers, 1.6 mm, 1 oz outer / 0.5 oz inner | 15 min | present in project and board |
| S0-7 | Widen the two long `3V3_C` In2 runs (28.4 mm, 21.8 mm) | 20 min | no new clearance errors |
| S0-8 | 100 Ω series on `/MODEM_RST` (pull direction waits on A2) | 15 min | net has 3 members |
| S0-9 | Justify or remove each of the 9 suppressed ERC/DRC checks, one line each | 20 min | list written into the response sheet |
| S0-10 | Clean folder: no `.bak`, `.bak2`, `_geom.json`, `_probe.kicad_prl`, `__pycache__` | 10 min | file list matches §12 Table 14 |

**Exit:** DRC **145 → ≈ 125, 0 errors**. ERC 0/1. Parity 0. Unconnected 0.

---

## 3. S1 — Schematic-only review package, send 2 November *(3 h)*

**Contents — the ten row-groups the review asks for:**

| File | What it is | Time |
|---|---|---|
| `ResponseSheet_RevC.csv` | **file 1.** All 76 rows: item, priority, what changed and where, evidence, status | 75 min |
| `Reply_to_CTO.pdf` / `.md` | The document Serigreen asked for — architecture, the six conditions with numbers, the two self-declared changes, the open list | 45 min |
| `MoriShield_Carrier_RevC.pdf` | Schematic, A3, correct title block | 10 min |
| `erc_RevC.json` + `.md` | Report plus the ignore justifications | 10 min |
| `drc_RevC.json` + `.md` | Report plus every remaining item classified | 15 min |
| `cond6_budget.md` | Six-condition allocation with measured mΩ, droop and worst-case modem voltage | 25 min |
| `pinmap_RevC.md` + `truth_table.md` | 44 ESP32 pins, 24 modem pins, 7 E22 pins, LED/buzzer truth table — closes C13 | 30 min |
| `deviation_request.md` | Route C vs the named TPS26630, with the 40-vs-66 mΩ table. *Agreed before drawing* | 15 min |
| `renders\` | The `_shots_revC\` evidence, renamed and captioned | 10 min |
| `SHA256SUMS.txt` + zip | Every file named by checksum | 5 min |

**What S1 honestly declares open:**

| Item | Status word used | Why that word |
|---|---|---|
| **R4** reverse / over-voltage protection | `Agreed before drawing` | U10 is a positioned placeholder; route C is chosen on resistance but unsigned |
| `/PWR_EN` two drivers | `Open — vendor question A1 attached` | cannot nominate an owner without the enable polarity |
| `/MODEM_RST` pull | `Partly — series fitted, pull waits on A2` | direction unknown |
| J6 E22 header order | `Open — needs the module datasheet (B1)` | pads are named 1…7, no signal names |
| microSD vs PSRAM | `Open — Serigreen's component, question attached` | vendor docs contradict the module datasheet |
| Layout items | `Deferred — second package, date named` | S1 is schematic-only by agreement |

**Gate:** CHK-001 criteria that S1 *can* meet — response sheet first, files named by checksum, ERC clean, parity clean, netlist re-derived, title block filled. Criteria it cannot meet are listed, not skipped silently.

---

## 4. S2 — Power protection and interface close-out *(4 h, 3–5 Nov)*

**Blocked until these arrive:**

| Input | From | Unblocks |
|---|---|---|
| **A1** — PWR_EN: which level enables | Parry docs or vendor | the `/PWR_EN` owner decision and R16's value |
| **A2** — RESET polarity and pulse width | Parry docs or vendor | the pull direction on `/MODEM_RST` |
| **B1** — E22 module part number and header pinout | you, bench | J6 correctness; may be a live fault |
| **B2** — microSD continuity: GPIO9–14 or GPIO35–39 | you, bench | whether S0-5 was insurance or a necessary fix |
| **Serigreen reply** to `deviation_request.md` | Serigreen | route C vs route A |
| **Route-C controller search** | me, unblocked now | the actual U10 circuit |

**Work once they land:**

| # | Task | Time |
|---|---|---|
| S2-1 | Controller search: 5 V-capable gate drive **and** ≈5.4 V trip, 4.5–60 V tolerant. Two named parts with citations, or an honest "none — take route A" | 45 min |
| S2-2 | Draw U10: controller, low-Rds N-FET, gate resistor, zener, bulk and bypass. Wire `/5V_PROT` end to end | 60 min |
| S2-3 | Re-rate D2 and ESD16: stand-off above the converter's highest output | 15 min |
| S2-4 | Settle `/PWR_EN` to one owner; retire the second driver | 20 min |
| S2-5 | Fit the `/MODEM_RST` pull in the correct direction | 10 min |
| S2-6 | Fix J6 if B1 says the order is wrong | 20 min |
| S2-7 | Re-run ERC/DRC, update the response sheet rows R4, R5, B10, C-13 | 30 min |

**Exit:** ERC 0/0 — the `/5V_PROT` warning disappears when U10 is wired. **R4 moves from placeholder to designed.** Response sheet updated and re-issued.

---

## 5. S3 — Layout completion package *(8–12 h, 6–9 Nov)*

This is the stage that needs hands on the board, and it is where the real time goes.

| # | Task | Time | Input needed |
|---|---|---|---|
| S3-1 | Condition 3: **≥3 mm pour** from J18 through the protection to the plane, ≥6 × 0.3 mm vias at each layer change. Today's 1.5 mm track does not meet it | 2–3 h | — |
| S3-2 | Move the modem 5 V feed from In2 to an outer layer or pour (11.5 → 5.8 mΩ, 2.2 mΩ as a 4 mm pour) | 1 h | — |
| S3-3 | Finish the Q9 rework and the F1 / C13 / bulk-at-J5 changes | 1 h | — |
| S3-4 | **78 `silk_over_copper` + 46 `silk_overlap`** — the largest single item count left | 3–4 h | — |
| S3-5 | Clear the 3 `via_dangling` and 2 `track_dangling` | 30 min | — |
| S3-6 | Q9 `lib_footprint_mismatch` | 20 min | — |
| S3-7 | Stitching plot for E1: no point of either ground pour more than 10 mm from a ground link, antenna keep-out excepted | 1 h | — |
| S3-8 | Antenna keep-out and clearance check against the Edgehax and Parry board outlines | 1 h | **A4** — is there a drawing of both modules? |
| S3-9 | 3D with the enclosure: 200 × 155 × 80 mm box, acrylic plate, converter on the plate with 5 mm air, gland holes | 1.5 h | **A3** — SIM access; **B4** — which regulator is warm |
| S3-10 | Decoupling map: every IC, its capacitor, its value and its distance | 1 h | — |
| S3-11 | Test points, logic-level FET gate drives, battery divider 0–20 V on GPIO6 | 1 h | **C-6** — confirm the divider ratio |

**Exit:** DRC 0 errors and a stated, justified warning count. Every R-item that is a layout item closed with a render.

---

## 6. S4 — Fabrication release package *(3 h, 10–11 Nov)*

| # | Deliverable | Time |
|---|---|---|
| S4-1 | Gerbers, 4 layers + drill, **regenerated from the saved board** — the Rev B package failed on stale files (R1), this is the check that catches it | 20 min |
| S4-2 | BOM and CPL/POS consistent with the board and the job file | 30 min |
| S4-3 | Fab drawing: stackup, copper weights, tolerances, impedance note, edge clearance, via-fill ask | 30 min |
| S4-4 | Assembly drawing and the orientation notes born out of S0-4 and B1 | 20 min |
| S4-5 | FMEA, bring-up sequence, first-article test plan | 45 min |
| S4-6 | Response sheet final, all 76 rows re-statused with evidence | 30 min |
| S4-7 | CHK-001 C1–C13 walked on the files actually in the zip; three timestamps recorded | 20 min |
| S4-8 | Zip + checksums, response sheet as file 1 | 10 min |

**Gate — nothing ships unless all of these are true:**

- ERC 0 errors / 0 warnings, every ignore justified in writing
- DRC 0 errors; warnings listed with a reason each
- Parity 0, unconnected 0
- Gerber timestamps newer than the board save
- BOM, POS, job file and fab drawing agree with the board
- Response sheet complete, first file in the zip, checksums beside it
- Serigreen's **written** release naming the files by checksum

---

## 7. S5 — Bench evidence *(boards arrive + 7 days)*

These items **cannot be closed on paper**, whatever the schedule says. They are listed so nobody mistakes silence for completion.

| Item | What has to be shown |
|---|---|
| **B10 / condition 6** | Modem input stays 4.75–5.25 V through an LTE burst, measured at the modem board |
| **R4** | Reverse supply, 12 V and 24 V for one minute each; cut-off fires below 5.5 V |
| **A2** | Modem registers on the network through the carrier socket |
| **C11** | SPS30 runs 72 hours error-free at installed cable length with both radios transmitting |
| **C12** | FDC1004 and soil readings stable with the modem transmitting |
| **G4** | ESD and surge per the test plan, on pilot units |
| **A11 / R7** | PWRKEY and RESET behaviour on real hardware |
| microSD | whether the slot works at all on the N16R8 module |

---

## 8. Critical path and what slips

| If this is late | Then | Recovery |
|---|---|---|
| A1 / A2 (vendor polarity) | S2-4 and S2-5 cannot be finished; `/PWR_EN` ships with two drivers | Send the question today; if no answer by 5 Nov, pick the safe state (pull so the modem is **off** by default) and say so |
| Serigreen deviation reply | R4 stays a placeholder into S4 | **Do not fabricate.** A P0 power-protection gap is a respin; a delayed order is not |
| B1 (E22 pinout) | J6 may be wrong in the released file | Highest-consequence unverified item on the board — 5 V on an M0 pin. Do it first |
| B2 (microSD) | S0-5 remains insurance | Harmless either way; already done in S0 |
| A3 (SIM access) | Enclosure may need a window or the sockets raised | Cheapest to fix in the model, not after drilling glands |
| Silk cleanup (S3-4) | S3 slips 3–4 h | It is cosmetic and can ship as a declared residual if the date is hard |

---

## 9. Inputs still outstanding, in one list

**From the vendor documents or Parry:**
A1 PWR_EN enable polarity · A2 RESET polarity and pulse width · A3 which side the SIM socket is on · A4 module outline drawings · A5 part number — `PTG4GB0B` or `PTG4GBOB`

**From the bench (you):**
B1 E22 module part number and header pinout · B2 microSD continuity GPIO9–14 vs GPIO35–39 · B3 does GPIO41 drive an LED · B4 which 3.3 V regulator is warm when both are powered

**From Serigreen:**
Route-C deviation approval · the microSD / octal-PSRAM contradiction on a board they supply · converter acceptance at 50 V input · fab capability sheet

**Decisions from you, all recommended yes and all reversible:**
C-1 `/PWR_EN` owner = GPIO7 · C-2 series + pull on `/MODEM_RST` · C-3 orientation silk · C-4 E22 move to GPIO15/GPIO40 · C-5 split `3V3_C` and set the 0.20 mm floor · C-6 battery divider ratio

---

## 10. Effort, honestly

| Stage | My hours | Your hours | Calendar |
|---|---|---|---|
| S0 | 2 | 0 | today |
| S1 | 3 | 1 review | tonight → 2 Nov |
| S2 | 4 | 1 | 3–5 Nov |
| S3 | 8–12 | 2 | 6–9 Nov |
| S4 | 3 | 1 | 10–11 Nov |
| S5 | — | 8+ on hardware | boards + 7 days |
| **Total to fabrication release** | **≈ 30** | **≈ 5** | **10 working days** |

S0 and S1 need nothing from anyone and are the whole of tomorrow's commitment. **Everything from S2 onward is gated on the twelve inputs in §9** — send those questions today and the ten days hold; send them next week and they do not.
