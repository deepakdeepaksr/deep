# Work to 2 November — your action list

| | |
|---|---|
| **Document** | WR-CAR-4L-RevC-01 |
| **Date** | 31 October 2026 |
| **Owner** | Aswin (single contact and signatory) |
| **Deadline** | **2 November 2026** — package to Serigreen |
| **Companion** | `INPUT_REGISTER_RevC.md` (the 89 questions) and `TASK_SHEET_RevC_4L.md` (the engineering plan) |

---

## 0. The honest picture first

The board needs about **20 schematic changes** and **18 layout changes**, plus **12 evidence documents**. In three days that is not all possible. Two days of it are.

| What | Possible by 2 Nov? | Why |
|---|---|---|
| Schematic changes (protection, watchdog, I2C, pin moves, gates, filters, bond, battery sense, text) | **Yes**, if the 20 blocking answers arrive today | Each change is local; no routing involved |
| ERC 0/0, title block, pin map, truth table | **Yes** | Paperwork, fast |
| Response sheet (76 rows) + cover message | **Yes** | I draft from the files and your answers |
| Layout (antenna keep-out, In2 plane, ESD at 5 mm, 65 vias, decoupling, J5 move, standoffs) | **No** | This is the bulk of the work and needs the box and the fab rules |
| 3D check, G1 simulation, FMEA, bring-up plan, bench results | **No** | Needs layout, parts and hardware |

**So the 2 November package is the schematic-only one**: schematic PDF, ERC report, response sheet, cover message, the six-condition plan, pin map and truth table. The CTO explicitly welcomes this ("a schematic-only review before you lay out the board is welcome and may save a loop"). Layout follows as a second package.

> **Doubt 1 — the one thing to confirm before anything else:** does "2 November" mean the schematic-only package, or the complete package with Gerbers? If it is the complete one, the date has to move or the scope has to shrink. Everything below assumes schematic-only. Answer as **A9** in the input register.

---

## 1. The three days

| Day | You | Me |
|---|---|---|
| **Fri 31 Oct** | Answer the 20 blocking questions (A8, A9, B1, B2, B4, C1, C3, C4, C6, C10, C19, D1, E1, E3, F1, F2, F11, G2, H3, I6). Send module photos and measurements. Approve the change list. | Back up the project, attempt the WDI route on a copy, start the schematic edits that need no parts |
| **Sat 1 Nov** | Review the schematic PDF. Finish the 1:1 test-fit. Send the module part numbers. Confirm converter and protection parts. | Finish the schematic, ERC 0/0, title block, pin map, truth table, draft the response sheet and cover message |
| **Sun 2 Nov** | Read the response sheet and cover message, correct anything wrong, sign, send. | Final ERC, package contents, checksums, zip named `MoriShield_Carrier_RevC_2026-11-02.zip` |

---

## 2. Your tasks

Each task says exactly what to produce. Times are realistic, not padding.

### W1 — Answer the 20 blocking questions
- **Output:** the answer sheet from `INPUT_REGISTER_RevC.md` §L, filled, or a message with 20 lines.
- **Time:** 60 minutes. **Do today.** **Blocks:** everything.
- **How:** `A9: schematic-only`, `B1: <link>`, `C19: route it`, and so on. "You decide" is acceptable for any of them.
- **Doubt:** none about the format; the answers themselves are yours.

### W2 — Confirm the 2 Nov scope
- **Output:** one line — `A9: schematic-only` or `A9: full package` (with the date you actually want for full).
- **Time:** 2 minutes. **Blocks:** the whole plan.

### W3 — Module photos and measurements
- **Output:** 6 photos + 6 numbers.
  1. ESP32 board label, sharp (the marking decides the pin plan).
  2. ESP32 board side view, pins visible.
  3. Modem label.
  4. Modem side view showing which way the pins point.
  5. Modem supply connector, circled on the photo (J5 must sit next to it).
  6. DS3231 top and bottom (battery underneath).
- **Numbers, in mm with calipers:** row spacing on each module (pin 1 to pin 1 across the two rows), row length (pin 1 to last pin), pin-1 offset from the board edge, module height, module width.
- **Time:** 90 minutes. **Deadline:** 1 Nov noon. **Blocks:** A1, A2, A7, A9, A10, C4, R14.
- **Doubt:** are both modules physically with you today? If one is in the field, say so and we use the datasheet dimensions and mark the item "measure on arrival".

### W4 — 1:1 print and test-fit
- **Output:** one photo of the printed socket layer with both modules pressed into place.
- **Time:** 60 minutes. **Deadline:** 1 Nov. **Blocks:** A10 (row spacing is the single most expensive thing to get wrong twice).
- **How:** print at exactly 1:1 (check a 10 mm ruler on the sheet with calipers first), tape it to a table, press the modules in.

### W5 — Converter decision
- **Output:** one part, with link or datasheet — or `you choose` and I shortlist three.
- **Time:** 30 minutes. **Deadline:** 31 Oct. **Blocks:** B1, B10, G1, J18 protection sizing.
- **Doubt:** do you already own a converter? If yes, its ratings are the hard constraint and everything else follows from it.

### W6 — Protection approach and parts
- **Output:** `design it` (recommended) or a preferred part; plus approval of the parts list I send.
- **Time:** 20 minutes. **Blocks:** R4, R5.
- **Doubt:** is there any reason to keep the P-channel FET (Q9) at all? Removing it removes its footprint problem and half the resistance.

### W7 — Enclosure
- **Output:** box name/drawing, or `you choose`. Also: may the outline change?
- **Time:** 30 minutes. **Blocks:** D1, A4, E3, the 3D check later.
- **Doubt:** do you already have the box on the shelf, or is it bought fresh? The board's 178 × 118 mm is tight for most IP65 boxes with glands.

### W8 — Fab and its capability sheet
- **Output:** fab name + PDF (annular ring, track/gap, via drill, via fill/cap, copper-to-edge).
- **Time:** 15 minutes to ask; the reply may take a day. **Blocks:** F1, R16, DRC constraint set.
- **Doubt:** is there an account/relationship with a fab already, or do we use a pool service?

### W9 — Bench inventory
- **Output:** one line per instrument — scope (model + bandwidth), DMM, electronic load, bench supply (current limit), and whether the modem + SIM + LTE coverage exist.
- **Time:** 15 minutes. **Blocks:** G1, G2, B10 bench plan.
- **Doubt:** without LTE coverage, the modem burst trace cannot be taken in-house; the reply must then name who takes it and when.

### W10 — Approve the schematic change list
- **Output:** `I6: approve all` or the items you want changed.
- **Time:** 20 minutes. **Blocks:** every schematic edit.
- **Doubt:** RS485 is the one item I cannot decide for you — restoring it costs pins, board area and a transceiver, and it is a P0.

### W11 — Module part numbers for the BOM
- **Output:** one link per module: ESP32 board, modem, E22, SPS30, GY-521, DS3231, FDC1004 breakout.
- **Time:** 30 minutes. **Blocks:** F1, F10, release gate row 4.
- **Doubt:** are any of these already purchased in a specific variant that the BOM must match exactly?

### W12 — Review the schematic (1 Nov)
- **Output:** comments, or `approved`.
- **Time:** 60 minutes. **How:** open the PDF I send; check the pin map against the module photos; check the truth table; check the title block says Rev C.
- **Blocks:** sending.
- **Doubt:** will you review it in KiCad itself, or only the PDF? Reviewing the PDF is enough for the CTO; reviewing the project catches more.

### W13 — Review the response sheet and cover message (2 Nov)
- **Output:** corrections or `approved`.
- **Time:** 60 minutes. **Blocks:** sending.
- **What to check:** every "Done" row actually has evidence; nothing claims more than the files show; the two unagreed changes are owned openly.

### W14 — Sign and send (2 Nov)
- **Output:** the email to the CTO with the zip attached; the send date and message reference recorded in the register.
- **Time:** 30 minutes.
- **Doubt:** do you have the CTO's current email, and does he expect the reply on the same thread as the review?

### W15 — Hardware hands
- **Output:** who does the hardware work and who solders/reworks — and are they available before 2 Nov.
- **Time:** 10 minutes. **Blocks:** A8, and realistically the layout stage.
- **Doubt:** if Deepak is unavailable, the schematic can still be finished, but layout and bench work need someone with hands on the board.

### W16 — Set the layout package date
- **Output:** a date for the second package (layout + Gerbers + evidence).
- **Time:** 10 minutes.
- **Doubt:** do you want one package after layout, or a schematic-only now plus a layout-only later plus the full package? Two is the sensible number.

---

## 3. What I do in parallel

| # | Work | Depends on | Output |
|---|---|---|---|
| 1 | Back up `4L\` (board + schematic) before any edit | — | timestamped copies |
| 2 | WDI route attempt on a **copy**, F.Cu/B.Cu, 0/45/90° | C19 | routed or a documented blockage with coordinates |
| 3 | J18 protection block, Q9, F1/C13 | B1, B4, F11 | schematic edits |
| 4 | Watchdog (TPS3828, WDI), one PWR_EN driver | C19, I6 | schematic edits |
| 5 | U8 → I2C-1, U7 reset | I6 | schematic edits |
| 6 | Pin moves M1/M0/reed, battery divider | C1, C6, C13 | schematic edits |
| 7 | Gate networks, filters, PE bond, logic-level FETs | I6, F11 | schematic edits |
| 8 | Status light, truth table, pin map | C10, C20 | `pin_map.csv`, `truth_table.csv` |
| 9 | Text corrections + title block Rev C | — | schematic |
| 10 | ERC clean, ignores justified | 1–9 | `erc.json` 0/0 |
| 11 | Response sheet 76 rows | 1–10 | `ResponseSheet_RevC.csv` |
| 12 | Cover message, evidence index, "not claimed" list | 11 | PDF |
| 13 | Package + checksums | 12, W14 | zip |

---

## 4. Doubts I hold — answer these and I stop guessing

| # | Doubt | Why it matters | Where it is asked |
|---|---|---|---|
| 1 | 2 Nov = schematic-only, or the full package? | The whole plan changes; full package is not possible in two days | A9 / H4 |
| 2 | Is Deepak in this at all before 2 Nov? | Layout and bench work need hands | A8 / W15 |
| 3 | Are the ESP32 board and modem physically with you today? | No photos → pin plan is guesswork, and twice it has been wrong | C1, C2, C3 |
| 4 | Do you own a 12 V→5 V converter already? | Its ratings constrain protection and copper | B1 / W5 |
| 5 | Is there a modem + SIM + LTE coverage in-house? | Without it, B10 cannot be measured before boards exist | G2 / W9 |
| 6 | Is there a box on the shelf? | A4 needs it; it also decides whether the outline may change | D1 / W7 |
| 7 | Which fab, and does it fill vias? | 65 vias sit in pads; fill/cap changes cost and the fab note | F1, F2 |
| 8 | Who approves the new parts? | I can shortlist in hours, but someone must own the choice | F11 |
| 9 | Does the CTO expect only the response sheet on 2 Nov, or the package with it? | If only the sheet, we have room; if the package, the date is at risk | J1 |
| 10 | RS485 — restore or defer? | P0, and it changes pins, area and power | C6 |

---

## 5. What slips if a piece is late

| If this is late | This slips | Recovery |
|---|---|---|
| The 20 answers | Schematic start | I proceed on defaults and mark them `ASSUMED` in the reply |
| Module photos | Pin plan, A1/A2/A7 | Use datasheet dimensions; mark "measure on arrival" — the CTO has flagged this twice already |
| Converter choice | J18 protection, B10 | Reply carries a shortlist and a plan, not a design |
| Fab sheet | Constraint set, R16 | Use the standard pool assumptions and say so |
| Box | A4, 3D, E3 | Reply says the box is chosen after the schematic pass |
| Bench/modem | B10 proof | Reply asks for the written allowance that 004 itself offers |
| Review and sign | The send date | Nothing ships without Aswin's signature |

---

## 6. The 2 November checklist

- [ ] 20 blocking answers logged in the register's decision log
- [ ] Backup of `4L\` taken before any edit
- [ ] WDI routed, or the blockage documented with coordinates
- [ ] Schematic changes applied; ERC 0 errors, 0 warnings; ignores justified
- [ ] Title block: "Rev C", date, names, change note
- [ ] Pin map and truth table signed by Aswin
- [ ] Response sheet: 76 rows, status from the files, evidence named
- [ ] Cover message: what changed, the two unagreed changes owned, what is asked
- [ ] Six-condition plan + converter comparison table
- [ ] Evidence index + "not claimed" list
- [ ] Zip `MoriShield_Carrier_RevC_2026-11-02.zip`, checksums recorded
- [ ] Sent by Aswin; date and message reference written back into the register

---

## 7. Decision log

| Date | Who | Decision | Where recorded |
|---|---|---|---|
| 31 Oct | Aswin | Send date 2 November 2026 | `INPUT_REGISTER_RevC.md` §Header |
| 31 Oct | Aswin | Aswin is single contact and signs | same |
| | | | |
| | | | |
| | | | |

---

## 8. Update, 31 October — 19 answers in, new work

**W1 status:** 19 of the 20 blocking questions answered and logged in `INPUT_REGISTER_RevC.md` §N. **B2 is still open** (where the converter physically sits, and who supplies it) — the reply to B2 was the datasheet link, which answered B1.

**A9 reading:** "1 nov schematic only" is taken as *the schematic-only package, prepared on 1 November, sent 2 November* (A1). If you meant the send moves to 1 November, say so — the plan compresses but holds.

### New tasks

| ID | Task | Output | Time | Deadline |
|---|---|---|---|---|
| **W17** | Deepak, in the first night window: re-try the watchdog link **from expander P07 (U8 pad 11, at 249.00, 169.93)** instead of P14, and re-aim its via toward the expander. If one obstacle remains, bridge it with a **0 Ω 0603** (a real part, not wire). Report: success, or the blocking item with coordinates | Screenshot + one line | 30 min | 1 Nov 05:00 |
| **W18** | One photo: the ESP32 module shield marking (`N16R8` or `N8R2`). The crystal question is closed — no 32.768 kHz crystal, GPIO15/16 are free | 1 photo | 5 min | 31 Oct |
| **W19** | Photo of the modem **sitting on J3/J4**, so J5 can be placed at the right corner | 1 photo | 10 min | 31 Oct |
| **W20** | Internal dimensions of the chosen box: **L × W × H** in mm (the Amazon page may not list them) | 3 numbers | 10 min | 31 Oct |
| **W21** | Converter: does the module have a **trim pot**, and can it be set to **5.15 V**? What is its rated output at **+70 °C**? Do you accept asking Serigreen to agree the **32 V vs 40 V** input clause? | 3 answers | 20 min | 31 Oct |
| **W22** | Two one-liners: (a) Deepak's second window ends **2 Nov 05:00**, not 1 Nov? (b) the "approve" in F11 means the CTO approves in the reply, not the assistant | 2 confirmations | 2 min | 31 Oct |

### What the answers changed in the plan

| Answer | Change |
|---|---|
| A9 schematic-only | The 2 Nov zip carries no Gerbers. The layout package becomes a second delivery |
| C6 RS485 removed | C1 turns from "restore" into a **written deferral request** — the reply must ask Serigreen to agree it, with your reasoning (no continuous RS485 need; soil sensor read occasionally by laptop) |
| F1 no via fill | R16 cannot be solved by a fab note: the **65 vias must move out of the pads** during layout. That is now a named layout task, not an option |
| E3 Wi-Fi used | The antenna keep-out is mandatory; the acrylic mounting plate must not put copper or metal under the antenna |
| C10 panel lamps | The externally visible status is J24; D6 stays a diagnosis LED. The silk should say which is which |
| C19 jumper | Replaced by the P07 attempt (W17). A 0 Ω 0603 is acceptable only if one obstacle remains |

### Still blocking the schematic

| ID | What | Who |
|---|---|---|
| B2 | Where the converter sits, who supplies it | Aswin |
| B13 | 5.15 V set point; 32 V vs 40 V acceptance | Aswin + converter page |
| C24 | Module shield marking photo — not blocking the pin map, only the A6 wording | Aswin |
| C22 | Modem test-fit photo | Aswin |
| D8 | Box internal dimensions | Aswin |

Everything else in the schematic can be drafted now: J18 protection, Q9 removal, F1/C13, bulk at J5, Q2/Q3 gates, TPS3828, U8→I2C-1, one PWR_EN, battery divider, PE bond, filters, logic-level FETs, text fixes, title block.

---

## 9. Update, 31 October evening — nothing blocks the schematic

**All four blocking items are closed.** B2 (converter inside the box, Serigreen buys it), B13 (LM2596HVS), D8 (200 × 155 × 80 mm) and C29 (no photo needed). The schematic can be drawn tonight without waiting for anything.

Answers are logged in `INPUT_REGISTER_RevC.md` §Q. This section records only what **changes the work**.

### 9.1 Three changes to the change list

| Change | Was | Now | Why |
|---|---|---|---|
| **Add J26** — 4-pin JST-XH on I2C-1, in parallel with J8 | — | **New task W19** | The AS5600 wind vane has no connector at all today. I checked the netlist: I2C-1 reaches only J7 (MPU-6050) and J8 (DS3231), both full |
| **Wire modem RESET** | Modem `RESET` left open | **New task W20** — `/MODEM_RST` = J1 pin 6 (GPIO6) → J4 pin 8 | Recovery path, now that PWR_KEY is held low permanently and cannot power-cycle the modem |
| **Move the reed to GPIO39** | On the change list | **Withdrawn** | GPIO41 is a plain GPIO. The move was based on my mistake; §Q.3 in the register has the correction |

### 9.2 New tasks

| ID | Task | Output | Time | Owner |
|---|---|---|---|---|
| **W19** | Draw **J26**: 4-pin JST-XH beside J8 at (157.65, 161.50), pads on `3V3_C`, `GND`, `I2C1_SDA`, `I2C1_SCL`. Label it `WIND VANE AS5600 (I2C-1, 0x36)` | Schematic + label | 20 min | Aswin |
| **W20** | Draw `/MODEM_RST` from **J1 pin 6** to **J4 pin 8**, with a 100 Ω series resistor at the modem side and a 100 kΩ pull-down so the modem is not reset while the ESP32 boots | Schematic | 20 min | Aswin |
| **W21** | Record the converter decision in `cond6_budget.md`: **LM2596HVS**, 4.5–50 V in, set to **5.15 V** on the bench, pot locked, heatsink fitted, mounted on the acrylic plate with 5 mm air, ≤200 mm of 0.75 mm² to J18 | One page | 15 min | Aswin |
| **W22** | Write the **purchase-split sentence** into the cover message: all components supplied by Serigreen; Aswin replaces only what he damages on the bench | One sentence | 5 min | Aswin |
| **W23** | Put the box into the A4 evidence: **200 × 155 × 80 mm** against a 178.15 × 118.15 mm board — 21.8 mm length, 36.9 mm width, 80 mm height of clearance | Line in the A4 row | 10 min | Aswin |

### 9.3 Tonight, in this order

1. **W19 and W20** — the two new nets. Small, local, no routing.
2. The existing schematic list: J18 protection, Q9 removal, F1/C13, bulk at J5, Q2/Q3 gate resistors, TPS3828, U8 → I2C-1, one PWR_EN, battery divider, PE bond, filters, logic-level FETs, text fixes, title block.
3. ERC to 0/0 with each ignored check justified in one line.
4. Then Deepak's window (20:00–05:00) takes the watchdog link from U8 pad 11 and any routing the new nets need.

### 9.4 One question left, and it is a measurement not a decision

**C28** — power the modem from its own 5 V JST and measure the `VDD_UART` pad with a DMM:

- **≈1.8 V** → the modem board generates it, so J4 pin 3 must be cut and the UART needs a level shifter.
- **0 V or floating** → we feed it, 3.3 V is correct, nothing changes. This is the default if not measured.

Everything else is either answered or on a default, and a default never stops the drawing.
