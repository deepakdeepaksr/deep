# MoriShield Carrier — A7672S Modem Connector Placement Review

**Date:** 2026-10-31
**Scope:** Verify J3 / J4 / J5 placement in `pcb/MoriShield_Carrier.kicad_pcb` against the physical A7672S modem board (`20261031_183310.jpg`, annotated copy `20261031_183310_annotated.jpg`).
**Verdict: placement is correct — 100 % match, mechanically and electrically.**

## 1. Official sources (primary evidence)

| # | Document | Link | Rev / Date | Accessed |
|---|----------|------|-----------|----------|
| 1 | Parry Technology — "4G LTE GSM MODEM" datasheet, **Part PTG4GBOB-SC104V1** (the exact board in the photo), includes official Pin-Out Diagram | https://www.parrytech.net/pdfs/estore/4g-lte-cat-1-modem.pdf | © Parry Technology 2023 | 2026-10-31 |
| 2 | SIMCom — **A7672S Hardware Design V1.00** (UART IO = 1.8 V, VDD_EXT 1.8 V output, module 24 × 24 × 2.4 mm) | https://www.ktron.in/wp-content/uploads/2023/03/A7672S_Hardware_Design_V1.00-1.pdf (mirror of SIMCom document) | V1.00, 2022-11-08 | 2026-10-31 |
| 3 | Project files (local) | `pcb/MoriShield_Carrier.kicad_pcb`, `pcb/MoriShield_Carrier.kicad_sch` | — | 2026-10-31 |

## 2. Mounting direction (confirmed)

- The photo shows the modem's **bottom (solder) side**: no 24 × 24 mm A7672S chip, bare berg pin tails (no plastic bodies), mirrored pin-name order vs. the datasheet's top view, SIM holder with slot visible.
- Carrier `Dwgs.User` note **"A7672S MODEM COMPONENTS-DOWN (SIM UP)"** is therefore correct and consistent with the nets: module is flipped components-down, this solder side (with SIM) faces up.

## 3. Official module pinout (Parry datasheet, top view)

| Pin | Left strip (top → bottom) | Right strip (top → bottom) |
|-----|---------------------------|----------------------------|
| 1 | A7672_PWR_KEY | PWR_EN |
| 2 | GROUND | MIC_N |
| 3 | VDD_IN_UART | MIC_P |
| 4 | A7672_TXD | EAR_N |
| 5 | A7672_RXD | EAR_P |
| 6 | GROUND | GROUND |
| 7 | VDD_1V8 | SDA_1V8 |
| 8 | A7672_RESET | SCL_1V8 |
| 9 | GPIO1_1V8 | GROUND |
| 10 | UART_LOG_RX | GPIO2_1V8 |
| 11 | UART_LOG_TX | ADC |
| 12 | GROUND | GROUND |

## 4. Carrier pin mapping (verified pin-for-pin)

**J3** (left socket, blue dots) ← module PWR_EN/audio strip (right strip above, mirrored by components-down mounting):

| Pin | 1 | 2–5 | 6 | 7–8 | 9 | 10–11 | 12 |
|-----|---|-----|---|-----|---|-------|----|
| Module | PWR_EN | MIC/EAR N,P | GROUND | SDA/SCL 1V8 | GROUND | GPIO2 / ADC | GROUND |
| J3 net | **PWR_EN** | NC | **GND** | NC | **GND** | NC | **GND** |

**J4** (right socket, green dots) ← module PWR_KEY/UART strip (left strip above):

| Pin | 1 | 2 | 3 | 4 | 5 | 6 | 7–11 | 12 |
|-----|---|---|---|---|---|---|------|----|
| Module | A7672_PWR_KEY | GROUND | VDD_IN_UART | A7672_TXD | A7672_RXD | GROUND | VDD_1V8 / RESET / GPIO1 / LOG_RX / LOG_TX | GROUND |
| J4 net | **PWR_KEY** | **GND** | **3V3_C** | **UART2_MOD_RX** | **UART2_MOD_TX** | **GND** | NC | **GND** |

- `3V3_C` on VDD_IN_UART is correct: the datasheet states the module has an **onboard UART level translator supporting 3.3 V–5.0 V** MCU I/O, so this pin is a reference **input**.
- TX/RX crossover (module TXD → host RX net, module RXD → host TX net) is correct.

**J5** (red dots, +/− pads) — module +/− pads are its 5 V input (datasheet: operating voltage 5 V ± 5 %); J5 = +5 V / GND:

- J5 pin 1 maps **0.34 mm** from the module + pad (deliberate alignment), polarity correct.
- Pin pitch 5.0 mm vs module pad spacing 2.74 mm is not an error: the pads face up after mounting, J5 feeds them via short jumper wires.

## 5. Quantitative geometry (photo ↔ carrier)

- 24 pin centres fitted to carrier coordinates: **24/24 inliers, mean residual 0.02 mm, max 0.10 mm**.
- x/y scale anisotropy **1.006** → 2.54 mm pitch and 34.0 mm J3–J4 separation consistent to ≈ ±0.2 mm.
- Module board outline maps to **59.0 mm** vs carrier 60 mm module keep-out; top edge within 1 mm.
- Pin 1 at top on both strips, matching carrier pads (J3/J4 pin 1 at y = 113.56).

## 6. Open items (not placement errors)

1. **Assemble J3/J4 with male pin headers** — the module carries female socket strips (official product photo), the footprint pads (1.7 mm pad / 1.0 mm drill) accept male headers; Value field currently reads "Sock_1x12_L/R".
2. **Check J5 height clearance** — terminal block (~10 mm) sits under the module, whose underside stands ≈ 8.5–9 mm off the carrier on the sockets. Verify in the mechanical stack-up.
3. **Cosmetic:** F.Fab labels "J3 UART" / "J4 PWR" are misleading (J3 carries PWR_EN/audio, J4 carries PWR_KEY + UART). J4 pins 7–11 are NC → no hardware reset / log-UART access; confirm this is intentional.

## 7. Annotated photo reference

`20261031_183310_annotated.jpg` — blue dots = J3 (12 pins), green dots = J4 (12 pins), red dots = J5 (+/− pads).
