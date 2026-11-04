# Session report - MoriShield Carrier Rev C - 2026-11-03 (third pass: Tasks A-E, board only)

Board: `pcb\MoriShield_Carrier.kicad_pcb`, saved 2026-11-03 19:49:36.
Schematic touched only through Value properties (D.5); no netlist surgery.

## 1. Verification numbers after every task

| Point | ERC | DRC viol | Unconnected | Parity | Census (fp/seg/via/zone/net) |
|---|---|---|---|---|---|
| Baseline on entry | 0 | 0 | 0 | 0 | 159 / 1171 / 314 / 6 / 134 |
| After Task A (J26) | 0 | 0 | 0 | 0 | 159 / 1180 / 314 / 6 / 134 |
| After Task B (J5) | 0 | 0 | 0 | 0 | 159 / 1180 / 314 / 6 / 134 |
| After Task C (caps) | 0 | 0 | 0 | 0 | 159 / 1178 / 313 / 6 / 134 |
| After Task D (silk + Values) | 0 | 0 | 0 | 0 | 159 / 1178 / 313 / 6 / 134 |
| After Task E (+5V to F.Cu) | 0 | 0 | 0 | 0 | 159 / 1178 / 313 / 6 / 134 |

`revC\drc_RevC.json` and `revC\erc_RevC.json` are the final runs; both report 0 with `ignored_checks []`.
Connectivity read-back from the saved file: J26.1 200 items, J26.2 308, J26.3 48, J26.4 40; J5.1 58, J5.2 308.

## 2. Census, with every difference named

- 1171 -> 1180 segments: -4 old J26 stubs, -12 dead feed branches, +25 J26 reroute segments (Task A).
- 314 vias: -4 dead feed vias, +4 J26 reroute vias (Task A) = 314.
- 1180 -> 1178 segments: -14 capacitor pad stubs, +8 capacitor tracks, +2 replacement tracks, +2 +5V segments on F.Cu (Tasks C/E).
- 314 -> 313 vias: -14 old capacitor pad vias, +8 new GND vias, +2 -2 +5V feed vias (Tasks C/E).
- Footprints 159, zones 6, net names 134 unchanged throughout.

## 3. Task A - J26 candidate tables (measured before choosing)

347 candidates along the bottom row at y = 194.5: **0 legal**. The row's courtyards leave 6.6-7.8 mm
between ports against a 13.49 mm part; the one 35 mm gap is crossed by the /I2C0_SCL_CH0 diagonal at
x 218, has GND stitching vias at (207.43, 195.43) and (219.43, 195.43), and lies under the GY-521
outline (bottom 192.05). Second-row candidates at y 195-200 exist but cost 68-97 mm of reroute.

Left edge (A.3), rot 90: 756 candidates, **0 legal** - the pocket between J24 (courtyard bottom
150.245) and D4 (top 161.265) is 10.3 mm against a 13.49 mm courtyard.

Left edge rot 0: 20 legal. Best by reroute length (A.2):

| x, y | reroute | margin | edge | worst item |
|---|---|---|---|---|
| 135.0, 153.5 | 59.8 mm | 0.175 | 7.65 | B.Cu PE (144.12,132.38)-(144.12,156.88) |
| 134.5, 153.5 | 61.4 mm | 0.67 | 7.15 | same |
| 134.0, 153.5 | 63.1 mm | 1.175 | 6.65 | same |
| 133.0, 153.5 | 66.6 mm | 3.06 | 5.65 | B.Cu PE (146.12,154.88)-(142.62,158.38) |

**Chosen: (134.0, 153.5)**, courtyard 131.0-144.5 x 150.61-157.44: 0.36 mm below J24, 0.38 mm above R7,
outside every module outline, margin 1.175 mm. Reroute: 3V3_C 11.5 mm, /I2C1_SCL 27.3 mm (2 vias),
/I2C1_SDA 30.2 mm (2 vias), GND through the plane. DRC 0/0/0 after.

A.5: each J26 pad had a track ending **inside** the pad at 0.112 mm from its centre
(162.5/165.0/167.5/170.0, 181.25) - the fanout was 45-degree stubs, not a missing connection.

## 4. Task B - J5 candidate table

904 legal rot-0 positions outside the modem outline. Ranked by distance to the modem's power edge:

| x, y | dist | lead | margin | hole | edge |
|---|---|---|---|---|---|
| 223.5, 91.5 | 16.7 | 0.41 | 1.715 | 3.44 | 2.60 |
| 223.0, 91.5 | 17.2 | 0.91 | 2.078 | 3.80 | 2.60 |
| 222.0, 91.4 | 18.2 | 1.91 | 4.268 | 4.35 | 2.60 |
| 221.0, 91.5 | 19.2 | 2.91 | 4.641 | 4.90 | 2.60 |
| 276.0, 145.0 | 58.3 | 0.09 | free | 3.51 | 23.10 |

**Chosen: (222.0, 91.4) rot 0**, courtyard 217.65-226.55 x 87.86-99.45: 1.905 mm clear of the modem
outline, 0.355 mm from the board edge, 0.165 mm above D7's courtyard. Rotation was rejected because
it raises `lib_footprint_mismatch`. +5V feed rerouted 1.5 mm on In2 from (222, 91.4) to (232.92, 95.83);
return through the GND plane (DRC unconnected 0). D7's reference field moved to (220, 101).

## 5. Task C - decoupling

Measured with the CTO's verbatim thresholds (100 nF, 10 uF) and a corrected value parser:

| | pins | meet both | meet local | meet bulk | fail local | fail bulk |
|---|---|---|---|---|---|---|
| Before | 36 | 0 | 0 | 3 | 36 | 33 |
| After | 36 | 1 (J13.1) | 3 | 3 | 33 | 33 |

By class after: IC 6 pins / 0 both / 0 local; MOSFET 6 / 0 / 1; diode 3 / 0 / 1; connector 21 / 1 / 1.

MOVE done (3): C41 -> Q9.3 (2.75 mm), C14 -> D2.1 (4.50 mm), C33 -> J13.1 (4.00 mm).
MOVE blocked (13): each has a legal spot but no capacitor that can move without breaking a live
branch or without rotating the part - listed as T-59 with coordinates.
NONE (20): no legal spot inside the radius at all.

The old map's bulk column used `>= 1 uF` and parsed "100nF/16V" as 10 uF; both are corrected in
`pcb\_work_20261103\decoup.py`, which regenerated `revC\decoupling_map.csv`.

## 6. Task D - labels

D.1: 14 fields moved off the port band (J11-J17, J20-J22, J26, ESD3, ESD11, C45) and the board name,
`Rev C` and `S/N` moved into the empty gap at x 206-222. DRC 0 with fields alone.
D.2/D.4: 12 port labels + 8 J6 marks added at 1.0 mm / 0.15 mm stroke; DRC 0.
D.6: re-plotted; every one of the 20 texts has strokes in its own box in
`revC\silk_check\MoriShield_Carrier-F_Silkscreen.gto` (SOIL 76, FSR 66, SGP41 53, SHT45 43, SPS30 120,
BME688 169, BUZZ 61, REED 60, WIND 39, LED 31, RTC 56, IMU 28, M0 48, M1 18, TXD 32, RXD 50, AUX 28,
5V 38, GND 67, 1 24).
D.5: schematic and board Value fields set for J7, J8, J11-J16, J22, J26; ERC 0, parity 0.
Order: save 19:49:36 -> DRC 19:50:0x -> plot 19:51:2x.

Not printed: nothing was dropped. Every requested label landed.

## 7. Task E - report only

In2.Cu after the +5V move: **61 segments, 431.40 mm, 7 nets** (was 63 / 453.68 / 8).

| net | seg | mm | F.Cu corridor | B.Cu corridor |
|---|---|---|---|---|
| /LED_DRV2 | 14 | 109.84 | -0.30 | -0.30 |
| /LED_DRV1 | 8 | 100.95 | -0.30 | -0.30 |
| /+5V_SENS | 13 | 76.73 | -0.60 | -0.60 |
| 3V3_C | 10 | 63.07 | -0.35 | -0.35 |
| /SENS_EN | 7 | 52.62 | -0.35 | -0.35 |
| /I2C0_SCL | 7 | 22.53 | -0.30 | -0.30 |
| /I2C0_MUX_SC0 | 2 | 5.68 | -0.30 | -0.30 |

Only +5V had a free corridor (+0.24 mm, against the GND via at 229.43, 101.42); it was moved to F.Cu
and DRC stayed 0. The other seven need real rerouting.

Keep-outs: not drawn. The ESP32 antenna tab length is still owed by Aswin; the E22 area
(x 296.00-304.57, y 163.00-177.00) is still crossed by /3V3_SENS_SW and the CH3/CH6 runs; the modem
U.FL end is still unidentified.

## 8. Items changed and still open

Changed: J26 position and its four nets; J5 position and the +5V feed; three 100 nF capacitors and
their reference fields; D7, Q9, J6 reference fields; the board name block; 20 silk texts; ten Value
fields in the schematic and on the board; BOM, POS, vias_in_pads.txt regenerated.

Still open with reasons: 13 ADD capacitors (need symbols - T-59); 20 pins with no legal spot; the
ESP32 keep-out (needs the tab length); the E22 keep-out (needs /3V3_SENS_SW and CH3/CH6 moved);
T-55/T-56 (schematic); R4/U10; converter; BOM MPNs; stack-up; Gerbers; the zip.

## 9. Final state of the checks

C1 Met, C2 Met, C5 Met, C12 Met, C9 **Not met** (1 of 36 pins meets both), C10 **Not met**
(61 In2 items, no antenna rule area), C3/C4/C6/C7/C8/C11/C13 not met. Gate tally unchanged:
4 met, 2 partly, 7 not met. `pack.ps1` stops at GATE 5 PRODUCTION. `trace2.py`: 76/76/76, 0 status
disagreements, 0 priority mismatches. S3 is **not** declared complete.

## 10. Newly found

- A rotated placed footprint raises `lib_footprint_mismatch`; the library copy is the reference.
- The decoupling map's bulk test used 1 uF and mis-parsed "100nF/16V" as 10 uF.
- A 4-pin JST-XH cannot fit anywhere on the bottom port row (347 positions measured).
- The +5V 100 nF bank sat in one corner, 40-160 mm from every +5V load.
- Vias inside SMD pads: 67 of 313 (was 65 of 314).

## 11. Files and rollback

Snapshots, each with a census: `pcb\_snap\T_A_J26_20261103_185908`, `T_B_J5_20261103_190435`,
`T_C_caps_20261103_194152`, `T_D_silk_20261103_194442`, `T_E_in2_20261103_194933`.
Rollback is a copy of `MoriShield_Carrier.kicad_pcb` from the snapshot taken before the step.
Working scripts: `pcb\_work_20261103\`. Document backups: none were made this pass; the previous
session's `.bak-` copies remain in `_cto_extract\`.

---

