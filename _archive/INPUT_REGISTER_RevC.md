# Rev C — All the questions, explained simply

| | |
|---|---|
| **Document** | IR-CAR-4L-RevC-02 (plain-language edition) |
| **Date** | 31 October 2026 |
| **Send date** | **2 November 2026** |
| **Contact and signatory** | **Aswin** |
| **Companion** | `TASK_SHEET_RevC_4L.md` (the engineering plan), `WORK_REGISTER_RevC.md` (your action list) |
| **How many questions** | **99 in the register** — answers in §N, §O and §Q. **Nothing blocks drawing any more**; everything still open takes a default |

**How to answer.** Copy the **answer sheet in §L** into a message and fill the blanks. Or just reply `A2: 5 boards`. "You decide" is a real answer — it means I take the default and log it.

**What each column means:**

- **In plain words** — the question without jargon.
- **Send me exactly this** — a photo, a number with units, a part number, a yes/no. With an example, so there is no guessing.
- **Default** — what I will do if you say "you decide" or don't answer.

**Already answered, recorded, no need to repeat:**

| ID | Answer | Date |
|---|---|---|
| A1 | Package goes to Serigreen on **2 November 2026** | 31 Oct |
| A7 | **Aswin** is the single contact and signs the reply | 31 Oct |
| H2 | Send date **2 November 2026** | 31 Oct |

---

## 0. What I already know — do not answer these

| Fact | Value |
|---|---|
| Board | 178.15 × 118.15 mm, 157 parts, 72 nets, 4 layers |
| Board saved / production files | 27 Oct 19:43 / Gerbers 27 Oct 16:12 — **the Gerbers are older than the board; they must be remade** |
| ERC | 0 errors, 0 warnings (four check types are switched off — I will justify or fix each) |
| DRC on the saved board | 0 errors, 134 warnings: 78 silk-over-copper, 46 silk-overlap, 5 loose vias, 2 loose tracks, 2 thin texts, 1 footprint mismatch (Q9) |
| Unconnected | 1 — the watchdog input, two vias 13.6 mm apart |
| Parity with the schematic | 209 differences |
| Vias inside solder pads | 65 of 224 |
| Track on the 5 V plane layer | 431 mm |
| Keep-out around the Wi-Fi antenna | none |
| Old design (round 1) | 2 layers, 48 parts, 168 × 118 mm, AMS1117 regulator, buck module on board, RS485 |

---

## A. Scope, dates and people

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| A1 | **Answered** — the package goes out on 2 November 2026. | — | — |
| A2 | How many boards will you build first? | One number. Example: `A2: 5` | 5 |
| A3 | Is this revision the one that gets fabricated, or is it another review round? | `fabricate` or `review` | Fabricate |
| A4 | Is there a pilot or field trial this must be ready for, and how many units? | A date and a number, or `none`. Example: `A4: pilot 20 units, 2027-01` | No pilot date |
| A5 | What is the most you want to spend per board? This decides protection style, finish and whether vias get filled. | A number in ₹ or `mid`. Example: `A5: ₹2500/board` | Mid-range: controller + FETs, ENIG, no filled vias |
| A6 | Who solders the boards — you by hand, a local shop, or an SMT service? | `hand`, `local`, or `SMT`. Example: `A6: hand` | Hand |
| A7 | **Answered** — Aswin is the single contact and signs. | — | — |
| A8 | **BLOCK** — Is Deepak available for the hardware side before 2 Nov? Who will solder and rework? | A name and `yes/no`. Example: `A8: Deepak available, he solders` | Deepak available; you solder |
| A9 | **BLOCK** — On 2 Nov, do we send the **schematic-only** package (schematic + ERC + response sheet + decisions), or wait and send everything together? | `schematic-only` or `full`. My recommendation: schematic-only | Schematic-only |

> Why A9 matters: the board has about 20 schematic changes and 18 layout changes to make. Two days is enough for the schematic and the paperwork, not for the layout. The CTO explicitly welcomes a schematic-only review before layout, and it usually removes one full review loop.

## B. Power — the 5 V input

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| B1 | **BLOCK** — Which 12 V→5 V converter will feed J18? I need its name and what it can do. | A link, a photo of the label, or the datasheet. Numbers I need: input voltage range, output voltage, current at 70 °C, how much it sags on a burst, idle current. Example: `B1: Mean Well DDR-15G-5, 9–36 V in, 5 V 3 A, datasheet attached` | I shortlist three and send you a table |
| B2 | **BLOCK** — Where will that converter sit — inside the box, on the cable, on a DIN rail? And who buys it? | One line. Example: `B2: inside the box, we buy it` | Inside the box, we buy it |
| B3 | How long is the cable from the converter to J18, and how thick? | Length in mm and wire size, or `you decide`. Example: `B3: 200 mm, 0.75 mm²` | 200 mm of 0.75 mm² |
| B4 | **BLOCK** — For reverse and over-voltage protection at J18, do we design it ourselves (a controller chip plus two low-resistance FETs), or do you have a part you want? | `design` or a part number. Example: `B4: design it, no preferred part` | We design it: controller + low-Rds FETs |
| B5 | At what current should the input protection cut off? The board's worst case is 2.6 A. | A number in A. Example: `B5: 3.5 A` | 3.5 A |
| B6 | Do you still want a fuse or PTC in series, or is the protection's current limit enough? | `keep fuse` or `no fuse`. Example: `B6: keep a fuse, any type that fits` | Keep one part, chosen to match its footprint |
| B7 | There must be a big capacitor at J5 (470 µF) plus two small ones, all within 10 mm. Is there room? Radial or SMD? | `radial` or `smd`, or `no room`. Example: `B7: radial is fine, room exists` | 10 mm radial + 0805/1206 ceramics |
| B8 | Is the 3.3 V regulator (TPS7A2033) final, or do you want a different one? | `keep` or a part number | Keep TPS7A2033 |
| B9 | Do we keep **two** switchable sensor rails (3.3 V and 5 V), and does the SPS30 stay on the 5 V one? | `both, yes` or corrections | Both rails; SPS30 on 5 V |
| B10 | The board now sees only 5 V, so the battery voltage needs its own wire to be measured. Is such a wire available? What range should it read? | `yes, 0–20 V` or the real range and connector. Example: `B10: yes, 12 V battery, 9–15 V, 2-pin JST` | Divider for 0–20 V on GPIO6, own 2-pin connector |
| B11 | Do you have real current measurements for the modules, or shall I use the datasheets? | Numbers, or `datasheets`. Example: `B11: datasheets` | Datasheets + the CTO's appendix |
| B12 | What is the hottest air inside the box? | A number in °C. Example: `B12: 60 °C` | +70 °C, no vents |

## C. Pins, modules and connectors

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| C1 | **BLOCK** — Which exact ESP32 board do you have? The marking matters: some versions have PSRAM that steals pins, some have a 32 kHz crystal. | A sharp photo of the label, plus `crystal yes/no` if you know. Example: `C1: ESP32-S3-DevKitC-1 N16R8, photo attached` | N16R8 (octal), no crystal |
| C2 | Do you have a spare ESP32 board to measure, and can one be used for photos (not destroyed)? | `yes/no`. Example: `C2: one spare, can photograph` | One spare to measure |
| C3 | **BLOCK** — Which exact modem board is it, and do its pins point **down** toward the carrier? | Model name + a side-on photo. Example: `C3: A7672S board, pins point down, photo attached` | A7672S, pins down |
| C4 | **BLOCK** — Where is the modem's own 5 V connector on that board? J5 must sit next to it, or the cable cannot reach. | A photo with the connector circled, or `near the SIM edge`. Example: `C4: short edge opposite the antenna, circled in photo` | Place J5 at the nearest edge |
| C5 | On the modem board, does pulling PWRKEY low mean "press the button"? And do we need a reset line to it? | `low = press`, plus `reset needed yes/no`. Example: `C5: low = press, no reset needed` | Low = press; no reset line |
| C6 | **BLOCK** — RS485: do we put it back on this board, or do you want to drop it and ask Serigreen to agree in writing? If we put it back, what powers it now that 12 V is gone? | `restore, powered from 5 V` or `defer`. Example: `C6: defer to next revision` | Restore, powered from 5 V through a PTC |
| C7 | Which port does the wind-direction chip (AS5600) use, and is it on this board? | A port name, or `not yet`. Example: `C7: I2C-1, on this board` | I2C-1, on this board |
| C8 | Is the wind-speed reed switch on this board? Which pin do you want it on? | `yes, GPIO39` etc. Example: `C8: yes, GPIO39` | GPIO39 |
| C9 | Do you need the microSD card slot to work on this board? Which card? | `yes/no` + card name. Example: `C9: yes, SanDisk Industrial 8 GB` | Yes; card model to be named |
| C10 | **BLOCK** — Which light tells a person at the box that the unit is alive: the small LED on the carrier, or a lamp on the panel? | `D6` or `panel lamp`. Example: `C10: panel lamp on J24` | D6, seen through a light pipe |
| C11 | What lamps connect to J24? Voltage, current, connector. | Numbers. Example: `C11: two 5 V LEDs, 20 mA each, JST XH` | 5 V LEDs, 20 mA, JST XH |
| C12 | What buzzer connects to J25? Type and current. | `magnetic` or `piezo`, plus current. Example: `C12: magnetic 5 V, 30 mA` | Magnetic, ~30 mA |
| C13 | How long is the cable to the FDC1004 electrode, and what connector? | Length + connector. Example: `C13: 1 m shielded, JST XH` | 1 m shielded, JST XH |
| C14 | How long is the SPS30 cable? Is it I2C or UART? | Length + `I2C`/`UART`. Example: `C14: 1 m shielded, I2C` | 1 m shielded, I2C |
| C15 | Which GY-521 and DS3231 modules do you have? Sizes and pin order matter, and the DS3231 has a battery under it. | Photos + sizes in mm. Example: `C15: GY-521 21×16, DS3231 38×22 with battery underneath` | GY-521 8-pin; DS3231 6-pin, battery underneath |
| C16 | Are J15/J16 (FSR and soil) actually used? If not, we remove them and their parts. | `used for …` or `remove`. Example: `C16: remove` | Remove J16, R5, ESD3 |
| C17 | Which nets do you want as test points? I propose: converter output, modem 5 V, 3V3_C, GND, EN, WDI, PE, I2C-0, I2C-1, UART1. | `take proposal` or a list. Example: `C17: take proposal, add SENS_EN` | Take the proposal |
| C18 | Do you already have a firmware pin map that must be kept? | Attach it, or `none`. Example: `C18: none, make it` | We issue the map for you to sign |
| C19 | **BLOCK** — The watchdog input: do we **route the wire** (my recommendation), or do you still want a physical jumper? If you think it cannot be routed, send me the top and bottom copper pictures around x 240–260, y 163–176 and I will try on a copy. | `route it` or `jumper`. Example: `C19: route it` | Route it; no jumper |
| C20 | Who writes the firmware-facing papers — README, pin map, truth table? You or me? | `you` or `me`. Example: `C20: you draft, I check` | I draft, you sign |

## D. Mechanical

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| D1 | **BLOCK** — Which box will the board live in? If you have not chosen, may I choose? | A drawing/STEP, a box name, or `you choose`. Example: `D1: you choose, IP65` | We choose a UV-stable IP65 box |
| D2 | May the board outline change — for example a notch so the Wi-Fi antenna hangs over the edge? Today it is 178 × 118 mm. | `keep` or `may change`. Example: `D2: keep the outline` | Keep the outline; keep-out area only |
| D3 | What standoffs hold the modem board — M2.5 or M3 — and how tall? | Numbers. Example: `D3: M3, 8 mm` | M3 × 8 mm; ESP32 clamp accepted |
| D4 | Where do the three antennas sit, and how do their cables run? | A simple sketch or `on the modules`. Example: `D4: on the modules` | On the modules, no coax |
| D5 | Which cables leave the box, and through what glands? | A list. Example: `D5: 6 sensor cables + 5 V in + earth` | Sensors ×6, supply, earth |
| D6 | Is there a panel with lamps, buzzer and a button? Where? | `yes, on the lid` or `no panel`. Example: `D6: no panel` | No panel |
| D7 | How is the box mounted — wall, pole, DIN rail? Any drop or water requirement? | One line. Example: `D7: wall plate, IP65` | Wall plate, IP65 |

## E. Earthing and EMC

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| E1 | **BLOCK** — At the site, is there an earth rod? Who connects the earth terminal to it, and is the installer expected to bond earth to ground at the box? | One or two lines. Example: `E1: earth rod at the pole, installer bonds PE to GND` | Earth rod; single PE–GND bond at the board |
| E2 | Do the antennas connect by cable from this board, or are they mounted on the modules? | `module` or `coax`. Example: `E2: module-mounted` | Module-mounted, no arrestors |
| E3 | **BLOCK** — Will anyone use Wi-Fi or Bluetooth at the box (for setup or service)? | `yes` or `no`. Example: `E3: yes, setup only` | Yes — build the full keep-out |
| E4 | Who will run the EMC and ESD tests — you, a lab — and on which units? | A name + `pilot`/`first boards`. Example: `E4: lab, pilot units` | Plan now, test on pilot units |
| E5 | Does the board get conformal coating? Which type, and what must stay uncoated? | `yes, acrylic, contacts masked` or `no`. Example: `E5: yes` | Acrylic, contacts masked |
| E6 | What cable lengths should we use for the ESD and surge tests? | Numbers. Example: `E6: 1 m sensors, 2 m supply` | 1 m sensors, 2 m supply |

## F. Making the board — fab, assembly, parts

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| F1 | **BLOCK** — Which factory makes the board? Their rules decide whether our 0.2 mm tracks, 0.3 mm vias and vias-in-pads are allowed. | The fab name plus its capability page/PDF, or `usual 4-layer pool`. Example: `F1: JLCPCB 4-layer, capability PDF attached` | Standard 4-layer pool: 0.15 mm ring, 0.2/0.2 mm, 0.3 mm via, no fill |
| F2 | **BLOCK** — Hand soldering or machine (SMT)? If machine, we add fiducials and panelise. | `hand` or `SMT`. Example: `F2: hand` | Hand, individual boards |
| F3 | Surface finish: ENIG (flat, better for fine parts) or HASL (cheaper)? | `ENIG` or `HASL` | ENIG |
| F4 | Confirm four basics: IPC class 2, Tg 150 °C laminate, 1.6 mm thick, 1 oz copper. | `all yes` or corrections. Example: `F4: all yes` | All four confirmed |
| F5 | Solder-mask and silkscreen colours? | Two words. Example: `F5: green, white` | Green mask, white silk |
| F6 | How many boards, and do you want them in one panel or separate? | Number + `panel`/`separate`. Example: `F6: 5, separate` | 5, separate |
| F7 | The CTO asks for two build variants. What are they, and what differs? | Two names + the difference. Example: `F7: with/without SPS30` | One build until you name the second |
| F8 | Where do you buy parts, and what is already in stock? | `Mouser`/`DigiKey`/`local` + a short stock list. Example: `F8: Mouser, 0805 passives in stock` | Mouser/DigiKey, stock checked per line |
| F9 | Any part that must **not** change because you already bought it? | A list or `none`. Example: `F9: none` | None |
| F10 | Send the exact part numbers/links for the plug-in modules: ESP32 board, modem, E22, SPS30, GY-521, DS3231, FDC1004 breakout. | One link per line. Example: `F10: E22 → ebyte link; SPS30 → sensirion link` | We source and list links |
| F11 | **BLOCK** — For the new parts (protection chip, FETs, TVS, ESD arrays for J24/J25, logic-level FETs, PE bond link, bulk capacitors, RS485 chip if restored): do I choose and you approve, or do you have preferred parts? | `you choose` or a list. Example: `F11: you choose, I approve` | I choose, you approve |

## G. Instruments and bench

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| G1 | What test gear do you have? Scope (model and bandwidth), multimeter, electronic load, bench supply with current limit. | A list. Example: `G1: 100 MHz scope, Fluke DMM, 5 A supply, no e-load` | 100 MHz scope, DMM, 5 A supply, no load |
| G2 | **BLOCK** — Do you have the modem, a SIM, and working LTE/GSM coverage where you test? If not, who can run that test? | `yes` or a name. Example: `G2: yes, SIM and coverage at office` | No bench — the reply asks for Serigreen's written allowance (which 004 already offers for A2, B10, C1–C4) |
| G3 | Do you have the SPS30, E22, GY-521 and DS3231 to test with? | `yes` or a list. Example: `G3: all four` | All available |
| G4 | Do you have calipers and a printer that prints exactly 1:1? | `both` or which is missing. Example: `G4: both` | Both |
| G5 | Can you take sharp photos with a phone? (label, side view, top view) | `yes` | Yes |
| G6 | Do you have 3D models (STEP) for the modules, or do we use dimensions only? | `STEP` or `dimensions`. Example: `G6: dimensions only` | Dimensions only |
| G7 | Have you measured anything already — 5 V rail, currents, temperatures? | Numbers or `none`. Example: `G7: none` | None |
| G8 | Who will measure the first boards when they arrive? | A name. Example: `G8: Deepak` | We do, on delivery |

## H. Names, process, sending

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| H1 | Who checks the package before it leaves? | A name. Example: `H1: Deepak checks hardware, Aswin signs` | You review, Deepak checks hardware |
| H2 | **Answered** — send date 2 November 2026. | — | — |
| H3 | **BLOCK** — How should the reply be formatted for the CTO? | `XLSX`, `CSV`, or `PDF table`. Example: `H3: XLSX + PDF` | XLSX plus a PDF export |
| H4 | Should the 2 Nov package be the schematic-only one (the CTO recommends this)? | `yes` or `full`. Example: `H4: yes` | Yes |
| H5 | How does the CTO want to receive it — email, WhatsApp, a shared folder? | One line. Example: `H5: email, PDF + XLSX` | Email with PDF and XLSX |
| H6 | Confirm the label everyone will see is **"Rev C"** (our internal numbering says v3). | `Rev C` or another name. Example: `H6: Rev C` | Rev C |
| H7 | The 6-layer version: keep it in the repo marked withdrawn, or delete it? | `archive` or `delete`. Example: `H7: archive` | Archive, marked withdrawn |
| H8 | Do you want a one-page status after each stage (decisions, schematic, layout, send)? | `yes/no`. Example: `H8: yes` | One page per stage |

## I. The reply itself

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| I1 | Two changes were made without asking Serigreen first: the buck moved off the board, and the watchdog input was left open. Do we say so plainly and ask for their agreement after the fact? | `yes` or `no`. Example: `I1: yes, own both` | Yes, one short paragraph each |
| I2 | Do we show the six power conditions with real numbers (resistance table, converter datasheet, capacitor positions)? | `yes/no`. Example: `I2: yes` | Yes |
| I3 | Do we include a small table comparing the old board and this one (2 layers → 4, buck removed, watchdog/mux added)? | `yes/no`. Example: `I3: yes` | Yes |
| I4 | Any words we must avoid? The old QA note said "manufacturing ready" while a P0 was open — that hurt. | `avoid …` or `none`. Example: `I4: never say ready` | Avoid "manufacturing ready", "release candidate", "production ready" |
| I5 | A one-page summary in front of the response sheet? | `yes/no`. Example: `I5: yes` | Yes |
| I6 | **BLOCK** — Do you approve this schematic change list? (J18 protection; Q9 fixed or removed; F1/C13 corrected; big capacitor at J5; separate gate drives for Q2/Q3; TPS3828 watchdog with a WDI that floats in download; expander moved to I2C-1 and switch reset from the ESP32; one PWR_EN driver; pin moves M1→GPIO40, M0→GPIO15/39, reed→GPIO39; battery divider; PE–GND bond; 47 Ω on every cabled I2C line and input filter; logic-level FETs; status light; truth table; text corrections; title block) | `approve all` or `change these: …`. Example: `I6: approve all except RS485` | Approve all |

## J. Open floor

| ID | In plain words | Send me exactly this | Default |
|---|---|---|---|
| J1 | Anything I should know that is not in a question — earlier failures, things promised to the CTO, parts on order, dates already quoted? | Free text or `nothing`. | Nothing |
| J2 | Anything you do **not** want in the reply? | Free text or `nothing`. | Nothing excluded |

---

## K. The 20 that block drawing

Everything else can wait; these cannot.

| Group | IDs | What they decide |
|---|---|---|
| People and scope | **A8 A9** | Who does the hardware; schematic-only or full package on 2 Nov |
| Power | **B1 B2 B4** | Which converter, where it lives, how J18 is protected |
| Modules and pins | **C1 C3 C4 C6 C10 C19** | ESP32 board, modem and its connector, RS485, status light, watchdog route |
| Mechanical | **D1** | Which box, and whether the outline may change |
| Earthing and radio | **E1 E3** | Earth scheme; whether Wi-Fi/BT is used |
| Making the board | **F1 F2 F11** | Fab rules, hand or SMT, who selects the new parts |
| Bench and admin | **G2 H3 I6** | Modem/bench access, reply format, approval of the schematic change list |

---

## L. Answer sheet — fill this and send it back

Copy from here down. One line each. "You decide" is fine.

### People and scope

| ID | What it is | Your answer |
|---|---|---|
| A1 | Send date | **2 Nov 2026** (recorded) |
| A2 | Boards to build | |
| A3 | Fabricate, or another review round | |
| A4 | Pilot date and units | |
| A5 | Budget per board | |
| A6 | Who assembles | |
| A7 | Who signs / single contact | **Aswin** (recorded) |
| A8 | Deepak available? Who solders? | |
| A9 | 2 Nov: schematic-only or full | |

### Power

| ID | What it is | Your answer |
|---|---|---|
| B1 | Converter part and ratings | |
| B2 | Where it lives, who buys it | |
| B3 | Lead length and gauge | |
| B4 | Protection: design it or a part | |
| B5 | Current limit (A) | |
| B6 | Keep a fuse or not | |
| B7 | Room for 470 µF + 10 µF + 100 nF | |
| B8 | Keep TPS7A2033 or change | |
| B9 | Two switched sensor rails? | |
| B10 | Battery wire and range | |
| B11 | Real currents or datasheets | |
| B12 | Hottest air in the box | |

### Pins and modules

| ID | What it is | Your answer |
|---|---|---|
| C1 | ESP32 board variant + crystal | |
| C2 | Spare board to measure | |
| C3 | Modem model + pins down | |
| C4 | Modem supply connector position | |
| C5 | PWRKEY behaviour + reset line | |
| C6 | RS485 restore or defer | |
| C7 | AS5600 port | |
| C8 | Reed switch and pin | |
| C9 | microSD needed + card | |
| C10 | Status light | |
| C11 | Panel lamps | |
| C12 | Buzzer | |
| C13 | FDC1004 cable | |
| C14 | SPS30 cable and bus | |
| C15 | GY-521 / DS3231 modules | |
| C16 | J15/J16 used or removed | |
| C17 | Test points | |
| C18 | Existing GPIO map | |
| C19 | WDI: route or jumper | |
| C20 | Who writes README/pin map/truth table | |

### Mechanical

| ID | What it is | Your answer |
|---|---|---|
| D1 | Enclosure | |
| D2 | May the outline change | |
| D3 | Standoffs | |
| D4 | Antennas and cable route | |
| D5 | Cables and glands | |
| D6 | Panel | |
| D7 | Mounting | |

### Earthing and EMC

| ID | What it is | Your answer |
|---|---|---|
| E1 | Earthing scheme | |
| E2 | Antennas: module or coax | |
| E3 | Wi-Fi/BT used | |
| E4 | Who runs EMC/ESD tests | |
| E5 | Conformal coating | |
| E6 | Cable lengths for tests | |

### Making the board

| ID | What it is | Your answer |
|---|---|---|
| F1 | Fab + capability sheet | |
| F2 | Hand or SMT | |
| F3 | ENIG or HASL | |
| F4 | IPC 2, Tg 150, 1.6 mm, 1 oz | |
| F5 | Mask and silk colours | |
| F6 | Quantity and panel | |
| F7 | Two build variants | |
| F8 | Distributors and stock | |
| F9 | Parts that must not change | |
| F10 | Module part numbers/links | |
| F11 | Who selects the new parts | |

### Bench and process

| ID | What it is | Your answer |
|---|---|---|
| G1 | Instruments | |
| G2 | Modem, SIM, LTE coverage | |
| G3 | SPS30/E22/GY-521/DS3231 | |
| G4 | Calipers and 1:1 printer | |
| G5 | Camera | |
| G6 | STEP models | |
| G7 | Existing measurements | |
| G8 | Who measures first boards | |
| H1 | Who checks the package | |
| H2 | Send date | **2 Nov 2026** (recorded) |
| H3 | Reply format | |
| H4 | Schematic-only first | |
| H5 | How to send to the CTO | |
| H6 | Label "Rev C" | |
| H7 | 6L archive or delete | |
| H8 | Status reports | |

### The reply

| ID | What it is | Your answer |
|---|---|---|
| I1 | Own the two unagreed changes | |
| I2 | Six conditions with numbers | |
| I3 | Old-board comparison | |
| I4 | Words to avoid | |
| I5 | One-page summary | |
| I6 | Approve the schematic change list | |
| J1 | Anything else I should know | |
| J2 | Anything to leave out | |

All three recorded answers are in the table with their values. Everything else is blank for you to fill.

---

## M. What happens with your answers

| Stage | When | What I do | What you do |
|---|---|---|---|
| 1 | Today, 31 Oct | Log the 20 answers in `TASK_SHEET_RevC_4L.md`, start the WDI route attempt on a copy, begin the schematic edits | Answer the 20; send module photos and measurements |
| 2 | 31 Oct evening | Schematic: J18 protection, watchdog, I2C, pin moves, gates, filters, bond, battery sense, text fixes | Approve the change list (I6); confirm converter and protection parts |
| 3 | 1 Nov | ERC clean, title block, pin map + truth table, draft response sheet and cover message | Review the schematic PDF; measure and 1:1 test-fit; send photos |
| 4 | 2 Nov | Final ERC, response sheet with statuses, package assembled and checksummed | Sign and send |
| 5 | After 2 Nov | Layout: keep-outs, In2 plane, ESD placement, vias, decoupling, standoffs, 3D | Set the layout package date; provide the box |

**Tracker:** 89 questions — 3 answered, 20 blocking, 66 can follow. Progress is recorded in §L and in the decision log of `WORK_REGISTER_RevC.md`.

---

## N. Answers received 31 October — logged, with what each changes

### N.1 The answers

| ID | Your answer | What it changes |
|---|---|---|
| A8 | Deepak available 31 Oct 20:00–1 Nov 05:00, and 1 Nov 20:00–2 Nov 05:00 (nights) | Routing and any rework go to his two windows; follow-up A10 on the second window |
| A9 | **Schematic only**, worked on 1 November | Package = schematic + ERC + response sheet + plans. Layout follows separately |
| B1 | SmartElex module with **AP63357** (Robu link) | AP63357: 3.8–32 V in, 3.5 A, 0.8 V ±1 % reference, 22 µA quiescent, 450 kHz. **Two gaps to close — see B13** |
| B4 | Keep it simple: one SMD part, diodes if possible | Proposal: **one integrated-FET eFuse** (TPS26630/31, 4.5–60 V, 31 mΩ typ, OV cut-off + current limit + reverse). One IC + passives; no extra track complexity |
| C1 | Edgehax **S3-PRO** with on-board microSD, **no 32 kHz crystal** | Pin plan assumes GPIO15/16 free → M0 on GPIO15, reed on GPIO39. Two things to confirm — see C21 |
| C3 | **A7672S**, pins facing the carrier | Confirms components-down; J3/J4 mapping stays |
| C4 | Modem 5 V is the JST at the top-right when flipped | J5 must sit at that corner; confirm with a test-fit photo — see C22 |
| C6 | **RS485 removed**: wind sensor is now reed + AS5600; soil sensor (XBS-3001-TR-RS) read occasionally by laptop through an RS485–USB adapter | C1 becomes a **written deferral request** with a strong reason: no continuous RS485 need on the board |
| C10 | D3/D4/D6 = diagnosis, pesticide-detection and consumer-alert LEDs; J24 = two 5 V LEDs; J25 = 5 V buzzer | The externally visible status is the **J24 lamp pair**; D6 stays a diagnosis LED. Confirm the wording in the reply |
| C19 | Could not route; Deepak tried many reroutes; decided on a jumper | A better option exists — see N.3. A jumper is now a last resort, not the plan |
| D1 | Box already chosen (link), acrylic base plate inside, holes cut for antennas and cables | Need internal L×W×H to check the board fits with glands — see D8 |
| E1 | Ground stand on the ground; earth wire from the PCB at assembly | README scheme: PE → stand → earth. The board-side PE–GND bond (R9) still goes in |
| E3 | No Bluetooth. GSM primary on master; **Wi-Fi only when GSM is unavailable or the field has Wi-Fi** | Wi-Fi **is** used ⇒ the full antenna keep-out stays (E3 remains P1) |
| F1 | Standard 4-layer pool: 0.15 mm annular, 0.2/0.2, 0.3 mm via | No via fill/cap ⇒ the **65 vias in pads must be moved**, not filled (R16) |
| F2 | Hand assembly | No fiducials needed; keep 0805/1206 passives |
| F11 | Aswin selects the parts | Recorded as: Aswin selects, I shortlist with rationale, Serigreen sees the list in the reply. See F12 |
| G2 | Bench coverage exists; field may vary; evidence sheet to follow | The B10 burst trace can be taken in-house — schedule it after the first board |
| H3 | XLSX | Response sheet exported to XLSX (and PDF for the cover) |
| I6 | Approved, with the reasoning: the buck ran hot, no 12 V is needed anywhere, keeping the board at 5 V is safer, RS485 has no consumer, and the layout went from 40+ unconnected to 1 | Recorded. The reasoning goes into the cover message, in engineering terms |

### N.2 Follow-ups — 5 blocking, 2 admin

| ID | Question | Why it blocks |
|---|---|---|
| **B2** | Where does the converter physically sit — inside the box, on a bracket, on the cable — and who supplies it? Your B2 answer was the datasheet link, which answered B1 | Lead length and who owns it decide condition 5 |
| **B13** | Two things about the AP63357. (1) It is **32 V maximum input**; condition 1 asks for **40 V or more**. It does cover the 22–25 V disconnect with margin, so we can ask Serigreen to accept the deviation — but say so. (2) The module must be set to **5.15 V**, not 5.00 V: at 5.00 V the modem sees 4.70 V in a burst, below its 4.75 V minimum. Does the board have a trim pot, or is the divider fixed? | This decides whether B10 can ever pass, and whether the converter needs replacing |
| **C21** | Two photos: (a) the module shield marking (N16R8 or N8R2), (b) a close-up of **X1** near the BATT connector. The front photo shows an X1 crystal; if it is the 32.768 kHz one on GPIO15/16, then M0 and E22 AUX both have to move | It decides the whole pin plan (A1, A7, C2, C5, R11) |
| **C22** | One photo of the **modem sitting on J3/J4** (test-fit), so I can place J5 at the right corner | R10 and J5 placement |
| **D8** | Internal dimensions of the chosen box: L × W × H in mm | A4 and the 3D check; also whether the 178 × 118 mm board fits with glands |
| A10 | Confirm Deepak's second window ends **2 Nov 05:00** (you wrote 1 Nov) | Scheduling only |
| F12 | You wrote "you (Shanmugam) approve". I am the assistant, not Dr. Murugesan — take this as: Aswin selects, the CTO sees and approves the list in the reply. Confirm | Avoids a wrong signature line |

### N.3 The WDI finding — probably no jumper at all

I checked the corridor between the two islands. It is genuinely crowded: within 0.5 mm of the straight line there are **six nets on F.Cu** (PWR_EN, I2C0_SDA ×5, BUZZER_EN ×2), **two on B.Cu** (SENS_EN, E22_AUX) and **two on In2** (I2C0_SCL, +5V_SENS). Deepak's conclusion that the direct line is blocked is correct.

But the expander has **ten unused I/O pins**, and two of them sit on the side facing U4:

| Free pad | Port | Position (mm) | Distance to the WDI via (244.5, 173.5) |
|---|---|---|---|
| U8.10 | P06 | 249.00, 169.28 | 6.5 mm |
| **U8.11** | **P07** | **249.00, 169.93** | **5.8 mm** |
| U8.9 | P05 | 249.00, 168.62 | 6.8 mm |

Free ports on U8 today: P00, P03, P04, P05, P06, P07, P10, P11, P12, P17.

**Proposal instead of a jumper:** move WDI from P14 to **P07**, and re-aim its via toward the expander's left side. The link drops from 13.6 mm to about 5.8 mm and no longer crosses the I2C0_SDA wall. If one obstacle remains, bridge it with a **0 Ω 0603** — a real part in the schematic and BOM, fitted by default, so the DRC reads zero unconnected.

This is worth one attempt in Deepak's window tonight. If it fails, the reply states the blockage with these coordinates and asks for the fitted-link exception. Either way, "won't go to production" should not appear in the reply — it reads as "this design is not the real one".

---

## O. Photo review, 31 October — what the images change

### O.1 What the images show

**ESP32 board (Edgehax S3-PRO):**
1. microSD slot on board, two USB-C ports, BATT connector, RESET and BOOT buttons.
2. **Corrected 31 Oct — no crystal.** The part at **X11** is a **B5819WS / 1N5819 Schottky diode** (SOD-323, factory marking "X11") in the BATT / 5 V power path, not a crystal. There is **no 32.768 kHz crystal** on the board: GPIO15/16 go straight to the header with no crystal and no load capacitors. The USB-UART is a **CH340C** with an internal oscillator. Accurate time already comes from the **DS3231** module on I2C-1, so nothing is missing.
3. The module shield marking is not legible in the photo. Edgehax's own listing for the S3 board is **N16R8** (8 MB octal PSRAM), which makes GPIO35–37 unusable.
4. Header order read from the silkscreen: one row is `G, TX, RX, 1, 2, 42, 41, 40, 39, 38, 37, 36, 35, 0, 45, 48, 47, 21, 20, 19…`; the other `3V3, 3V3, RST, 4, 5, 6, 7, 15, 16, 17, 18, 3, 46, 9, 10, 11, 12, 13, 14, 8`.

**Modem board (Parry PTG4GB0B-SC104V1, module A7672S / S2-10F6D-Z32CD):**
5. Exposed signals, read from the back silkscreen: **PWR_KEY**, GND, **VDD_UART**, A7672_TXD, A7672_RXD, GND, **VDD_1V8**, **A7672_RESET**, UART1_LOG_RX, UART1_LOG_TX, GND, **PWR_EN**, MIC, EAR_P/N, SDA, SCL, ADC0.
6. The 5 V input is the white JST on the module edge plus the `+/−` solder pads beside it.
7. The SIM socket is on the **back** of the modem board, so it faces up when the board is mounted components-down. E6 (SIM access) is satisfied by the mounting direction.

**Carrier, from the board file (the socket map that must now match the GPIO map):**

| Connector | Pins in use |
|---|---|
| J1 | 1–2 3V3_C · 3 RST_ESP · 4 I2C1_SDA · 5 I2C1_SCL · 7 PWR_EN · 9 E22_AUX · 10/11 UART1_LORA_TX/RX · 12 I2C0_SDA · 13 EVENT_BTN · 15 I2C0_SCL · 16 E22_M1 · 17 E22_M0 · 21 +5V_ESP · 22 GND |
| J2 | 4 FSR_ADC_F · 5 SOIL_ADC_F · 6 STATUS_LED · 7 REED_PULSE_F · 16/17 UART2_MOD_RX/TX · 18 MPU_INT · 1, 21, 22 GND |
| J3 | 1 PWR_EN · 6/9/12 GND · **pins 2, 3, 4, 5, 7, 8, 10, 11 free** |
| J4 | 1 PWR_KEY · 2 GND · 3 3V3_C (feeds VDD_UART) · 4/5 UART2_MOD_RX/TX · 6 GND · **pins 7–11 free** |

### O.2 Why this matters

- **GPIO15/16 are free**, so the pin plan stands as written: **E22 M1 → GPIO40 (J2 pin 8), M0 → GPIO15 (J1 pin 8), reed → GPIO39 (J2 pin 9), AUX stays on GPIO16 (J1 pin 9)**. No pin reshuffle is needed, and GPIO39 is not contested. The only pin-related question left is the module variant (N16R8 vs N8R2), which affects A6's wording, not the map.
- The carrier **holds `PWR_KEY` low through R15 (1 kΩ)**. A7672's PWRKEY is pulse-operated: low for ~0.5 s powers on, low for >3.5 s powers off. A permanent low is a functional risk, not just a missing truth-table line.
- **`A7672_RESET` is available** on the modem and unused on the carrier, while J3/J4 have eight free pins. A recovery reset is one wire away.

### O.3 New questions (answer with §L's format)

| ID | Question | Why | Default |
|---|---|---|---|
| **C23** | **Answered 31 Oct** — no 32.768 kHz crystal; X11 is a B5819WS Schottky diode in the BATT/5 V power path; GPIO15/16 are free | Nothing to test; the pin plan stands: M0 on GPIO15, AUX on GPIO16, reed on GPIO39 | — |
| **C24** | A bright, close photo of the module shield marking, or the exact product variant from the Edgehax page (`N16R8`, `N8R2`…) | Decides whether GPIO35–37 exist for us, and whether A6 needs PSRAM ECC | N16R8 octal, ECC recorded |
| **C25** | Send the firmware's current GPIO map, or say "none, define it" | The carrier sockets are fixed; the GPIO numbers come from the header order, and nothing matches until this exists | We define it and you sign |
| **C26** | Is `PWR_KEY` held low on purpose? Do you want it driven by a GPIO (pulsed 0.5 s on, 3.5 s off) instead? | A permanent low can power the modem off after boot | Drive it from a GPIO |
| **C27** | Do we wire **`A7672_RESET`** to a free J4/J3 pin (a GPIO), for recovery? | Gives a hard recovery path the CTO asked about (A11) | Yes — wire it, one GPIO |
| **C28** | `VDD_UART` is fed from J4 pin 3 (3V3_C). Is that deliberate, so the modem's UART is 3.3 V? | If the modem's UART is 1.8 V, every line needs level shifting | Yes — 3.3 V reference, no shifter |
| **C29** | Photo of the modem sitting on J3/J4, its 5 V JST visible | Places J5 at the right corner (R10) | J5 at the corner nearest the JST |

---

## P. Current open list — 31 October, after the crystal correction

**Status: 99 questions in the register, 23 answered, 76 open.** Of the open ones, 4 block, 9 are needed for the schematic tonight, 14 are for the paperwork, and 49 take a default unless you say otherwise.

### P.1 Blocking (4)

| ID | Question |
|---|---|
| B2 | Where the converter physically sits — inside the box, on the acrylic plate, on the cable — and who supplies it |
| B13 | 40 V route A or B; is the module adjustable to 5.15 V; what is its rated current at +70 °C |
| C29 | Photo of the modem on J3/J4 with its 5 V JST visible |
| D8 | Box internal L × W × H in mm |

### P.2 Needed for the schematic tonight (9)

| ID | Question |
|---|---|
| C24 | Module shield marking (`N16R8` / `N8R2`), so A6 can say "ECC recorded" correctly |
| C25 | Existing firmware GPIO map, or `define it` (replaces C18) |
| C26 | PWR_KEY: GPIO pulse or keep the permanent 1 kΩ to ground (replaces C5) |
| C27 | Wire A7672_RESET to a free J3/J4 pin? which one? |
| C28 | VDD_UART on 3V3_C — deliberate 3.3 V UART reference? |
| C10 | Confirm: J24 lamps are the visible status, D6 is diagnosis only |
| C7 | AS5600 port — I2C-1? |
| C8 | Reed on GPIO39 — confirm |
| C9 | microSD from the ESP32 board's own slot — which card? |

### P.3 For the paperwork (14)

| ID | Question |
|---|---|
| A2 | Boards to build |
| A3 | Fabrication release, or another review round |
| A4 | Pilot date and units, or `none` |
| A5 | Budget per board |
| F3 | ENIG or HASL |
| F4 | IPC class 2, Tg 150 °C, 1.6 mm, 1 oz — confirm |
| F7 | The two build variants, or `one build` |
| H1 | Who checks the package before it is sent |
| H4 | Schematic-only package first — confirm |
| H5 | How the CTO receives it |
| H6 | Label "Rev C" — confirm |
| H7 | 6L: archive or delete |
| C20 | Who writes README, pin map, truth table — you or me |
| E5 | Conformal coating — type, masked areas |

### P.4 Defaults unless you say otherwise (49)

`A6` hand assembly (derived from F2) · `B3` 200 mm of 0.75 mm² · `B5` 3.5 A limit · `B6` keep one fuse · `B7` radial 470 µF + ceramics · `B8` keep TPS7A2033 · `B9` both sensor rails, SPS30 on 5 V · `B10` divider for 0–20 V on GPIO6 · `B11` datasheets · `B12` +70 °C, no vents · `C2` one spare board · `C11` two 5 V LEDs, 20 mA, JST XH · `C12` magnetic buzzer, ~30 mA · `C13` 1 m shielded, JST XH · `C14` 1 m shielded, I2C · `C15` GY-521 8-pin / DS3231 6-pin with under-cell · `C16` remove J16, R5, ESD3 · `C17` take the test-point proposal · `D2` keep the outline · `D3` M3 × 8 mm · `D4` antennas on the modules · `D5` six sensor cables, supply, earth · `D6` no panel · `D7` wall plate, IP65 · `E2` module-mounted antennas · `E4` test on pilot units · `E6` 1 m sensors, 2 m supply · `F5` green mask, white silk · `F6` 5 boards, no panel · `F8` Mouser/DigiKey · `F9` no frozen parts · `F10` we source and list · `F12` CTO approves the parts list in the reply · `G1` 100 MHz scope, DMM, 5 A supply · `G3` all four modules available · `G4` calipers + 1:1 printer · `G5` phone camera · `G6` dimensions only · `G7` no prior measurements · `G8` we measure first boards · `H8` one page per stage · `I1` own the two changes · `I2` six conditions with numbers · `I3` old-board comparison · `I4` avoid "ready" claims · `I5` one-page summary · `J1` nothing further · `J2` nothing excluded.

---

## Q. Answers received 31 October, second batch — 14 logged

### Q.1 The answers, and what each one changes

| ID | Your answer | What it changes | Checked against the board? |
|---|---|---|---|
| **A6** | All components come from Serigreen; Aswin buys only the replacements he damages on the bench | Goes into the cover message as one explicit sentence, so the cost split is written down rather than remembered | — |
| **B2** | Converter **inside the enclosure**; **Serigreen buys it** | Closes the last blocking item. Condition 5's ≤15 mΩ is the converter→J18 lead: ~200 mm of 0.75 mm² inside the box | — |
| **B13a** | I pick the module: Robu, in stock, under ₹300 | **LM2596HVS** — reasoning in §Q.6 | — |
| **C24** | ESP32-S3-WROOM-1, **MCN16R8** (photo) | 16 MB flash + 8 MB **octal** PSRAM. GPIO35/36/37 belong to the PSRAM and are dead on the header (J2 pads 11, 12, 13). **No net uses them**, so nothing has to move | ✅ |
| **C25** | GPIO map is not fixed; it is written once the PCB freezes | Closes the old C18. The sockets are fixed; firmware follows the board, not the other way round | — |
| **C26** | **Keep** the permanent 1 kΩ | R15 = 1 kΩ from `/PWR_KEY` to GND, verified. The modem self-starts; power-off is by AT command; recovery is by RESET, which is why C27 matters | ✅ |
| **C27** | Yes — whichever pin is easiest to route | **J1 pin 6 = GPIO6 → J4 pin 8 = RESET** — see §Q.5 | ✅ |
| **C28** | "Explain this more clearly" | Explained in §Q.4. It needs one 30-second measurement, not a decision | ✅ |
| **C7** | Reed is in; the wind vane is not — go and check | **Confirmed: there is no AS5600 anywhere in the schematic or the netlist.** I2C-1 reaches only J7 (MPU-6050) and J8 (DS3231), both fully used. A new 4-pin header is needed — §Q.2 | ✅ |
| **C8** | Reed is in; check which GPIO | **J2 pin 7 = GPIO41**, through R50 = 100 Ω, C40 = filter, ESD17, R49 = 10 kΩ pull-up, and J22 = the reed's own 2-pin JST. Complete and correct. **Nothing has to move** — §Q.3 | ✅ |
| **C9** | 8 GB SanDisk or Hikvision | The card lives in the ESP32 board's own slot. Nothing on the carrier changes; it is a purchase line, not a PCB line | ✅ |
| **C10** | Yes | J24 = two 5 V lamps, J25 = buzzer, D3/D4/D6 = diagnosis. Unchanged | ✅ |
| **D8** | **200 × 155 × 80 mm** | Board is 178.15 × 118.15 mm, so the box leaves 21.8 mm length, 36.9 mm width and 80 mm height. A4's 3D check can run | ✅ |

**Result: no question blocks the schematic any more.** The four that did — B2, B13, C29, D8 — are all closed.

### Q.2 C7 — the wind vane has no connector. This is a real gap, not a doubt

I checked the netlist rather than trusting the comment in the title block. `AS5600` appears in exactly one place: the schematic's comment field, "Added DIY Wind Sensor (AS5600 + Reed)". There is no AS5600 symbol, no net, and no connector for it.

I2C-1 reaches only two headers, and both are occupied:

| Header | At | What is on it |
|---|---|---|
| **J7**, 8 pins | 212.11, 166.00 | MPU-6050: `MPU_INT, 3V3, XCL, XDA, SDA, SCL, GND, 3V3` |
| **J8**, 6 pins | 157.65, 161.50 | DS3231 RTC: `32K, SQW, SCL, SDA, 3V3, GND` |

**Proposal — one new part, nothing else changes:** add **J26**, a 4-pin JST-XH, wired in parallel with J8's I2C-1 pins (`3V3_C`, `GND`, `I2C1_SDA`, `I2C1_SCL`). I2C is a bus, so two devices share it. The AS5600 answers at address **0x36** and the DS3231 at **0x68** — no clash, no jumper, no firmware trick. Place J26 beside J8 so the routing is under 20 mm.

That is the smallest possible fix and it makes C7 closable. If you would rather the vane share a connector with something else, say which.

### Q.3 C8 — the reed is already correct; my earlier plan to move it was wrong

The chain that is actually on the board:

```
J22 (2-pin JST, the reed)  →  /REED_PULSE  →  R49 10k pull-up to 3V3_C
                                           →  C40 to GND   (filter)
                                           →  ESD17        (protection)
                                           →  R50 100R     (series)
                                           →  /REED_PULSE_F  →  J2 pin 7
```

J2 pin 7 is **GPIO41**. On the ESP32-S3-WROOM-1 that is a plain GPIO — not a strapping pin, not a PSRAM pin, not USB. The only cost of using it is that **JTAG debugging is lost on that pin**; we flash and debug over the CH340C UART anyway, so the cost is zero.

**Therefore: the reed stays on GPIO41 and the earlier idea of moving it to GPIO39 is withdrawn.** It was based on my mistaken reading of that pin's role.

### Q.4 C28 — what VDD_UART is, in plain words

The modem board has a pin called `VDD_UART`. On the carrier, that pin is wired straight to `3V3_C` at **J4 pin 3** (verified in the netlist).

What the pin means: the modem's UART lines (`A7672_TXD`, `A7672_RXD`) do not swing to 3.3 V by themselves. The board has a small level translator in front of them, and `VDD_UART` sets the voltage that the *modem side* of that translator swings to. You feed it a voltage, and the UART talks at that voltage.

There are only two possibilities, and they need opposite handling:

| If `VDD_UART` is… | What it means | What we do |
|---|---|---|
| **an input** (we feed it) | 3.3 V in → the UART talks at 3.3 V → it matches the ESP32 directly. This is the good case | Nothing. Keep J4.3 as it is |
| **an output** (the modem board makes it) | The board is generating its own 1.8 V there and we have tied that to our 3.3 V rail. The two regulators fight each other | Cut the J4.3 connection, leave the modem pin open, and then the modem UART is 1.8 V, so a level shifter is needed on RX/TX |

**How to tell in 30 seconds, no carrier needed:** power the modem from its own 5 V JST on the bench, and measure the `VDD_UART` pad with a multimeter.

- reads **≈1.8 V** → it is an output. Say so and I redesign that pin.
- reads **0 V** or floats → it is an input. 3.3 V is correct and C28 is closed.

Answer like: `C28: 1.8 V measured → output` or `C28: 0 V → input, keep`.

### Q.5 C27 — the RESET pin, and why GPIO6

J4 pin 8 is `RESET` and is unconnected today. Free, safe pins on J1: **GPIO6** (J1.6), GPIO12/13/14 (J1.18/19/20), and on J2: GPIO38, GPIO39, GPIO40.

| Candidate | Why yes / why no |
|---|---|
| **GPIO6 — J1 pin 6** ✅ | Free; not strapping; not PSRAM; not USB. Sits at (209.50, 141.30), and J4.8 is at (269.50, 131.34) — a 60 mm run that crosses under the modem, where In1 and In2 are empty |
| GPIO46 — J1.14 | **No.** Strapping pin; must be high at boot |
| GPIO0, GPIO45 — J2.14, J2.15 | **No.** Strapping pins |
| GPIO19, GPIO20 — J2.19, J2.20 | **No.** Native USB D−/D+ |
| GPIO35/36/37 — J2.11/12/13 | **No.** PSRAM on this module |

The voltage domain is right too: the modem's IO on J4 is referenced to `VDD_UART` = `3V3_C`, so a 3.3 V GPIO drives RESET directly, no shifter.

**Answer recorded: `/MODEM_RST` = J1 pin 6 (GPIO6) → J4 pin 8.** Say if Deepak wants a different one tonight.

### Q.6 B13a — the converter: LM2596HVS

**Robu part:** `LM2596HVS DC-DC Buck Converter 4.5–50 V to 3–40 V Adjustable Step Down Power Module`
`robu.in/product/lm2596hvs-dc-dc-buck-converter-4-5-50v-to-3-40v-adjustable-step-down-power-module/`

| Requirement | This module | Verdict |
|---|---|---|
| Input survives the 22–25 V disconnect event | 4.5–50 V | ✅ 25 V is mid-range |
| Input survives a fast transient clamped by the TVS (~39 V) | 4.5–50 V | ✅ 11 V of margin — this is why it wins |
| Output settable to **5.15 V** | 3–40 V, multi-turn trim pot | ✅ set it on the bench, then lock the pot |
| 3 A at +70 °C | 3 A peak; about 2 A continuous on its own heatsink | ⚠ average load is under 1 A (modem bursts are short), so it passes — but see the note below |
| Under ₹300, in stock | ₹100–150 band at Indian sellers | ✅ |

**Why not the others:**

| Module | Input max | Why rejected |
|---|---|---|
| AP63357 (your first pick) | 32 V | Too close to the 25 V event, and no room for a 24 V TVS clamp above it |
| XL4015 5 A | 38 V | Better thermally, but the TVS clamp lands right on its ceiling |
| XL4016 8 A | 40 V | Best thermally, but again the clamp is at the limit |

**Honest caveat.** The LM2596 is a 150 kHz part with about 75 % efficiency at 25 V → 5 V. At 1 A average that is roughly 1.7 W in the box. So the purchase note must say: **fit the heatsink that comes with it, mount it on the acrylic plate with 5 mm of air around it, and keep it away from the modem.** If Serigreen will stretch the price to about ₹400, an XL4016 module is cooler-running but only rated 40 V — then the input TVS has to be dropped, and that has to be said in the condition-5 answer.

**What I could not check:** Robu blocks automated page reads, so I could not see the live stock badge. Confirm it in the cart when ordering. The same module is listed at zbotic.in for ₹100 if Robu is out.

### Q.7 What is still open, and all of it has a default

| ID | Still open | Default if you say nothing |
|---|---|---|
| C28 | The 1.8 V / 0 V measurement above | Treated as an input → keep J4.3 on 3V3_C |
| C7 | Approval of the new J26 wind-vane header | Added at J8 with a 4-pin JST-XH |
| C29 | **Closed — no photo needed.** J5 stays at (239.51, 95.83) and the modem is fed by a 100 mm 2-wire lead to its own JST | Closed |
| A2 | How many boards in the first build | 5 |
| A3 | Is Rev C the fabrication release, or another review round? | Another review round, then fabricate |
| A5 | Budget per board | No cap stated |
| F3 / F4 | ENIG or HASL; IPC class 2, Tg 150 °C, 1.6 mm, 1 oz | ENIG; all four confirmed |
| H5 | How the CTO receives the package | Same channel as before |
| E5 | Conformal coating | Acrylic, contacts masked |
