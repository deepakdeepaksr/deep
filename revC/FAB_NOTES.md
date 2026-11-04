# Fabrication and assembly notes - MoriShield Carrier, Rev C

**Status: draft.** Written from our own rule set, not from a fab capability sheet.
Everything marked ASSUMPTION must be confirmed against Serigreen's or the fab's
document before a release package is built (dependency D-7).

**Regenerated 2026-11-01 from the saved board** (`MoriShield_Carrier.kicad_pcb`,
saved 23:29:58). Supersedes the 16:54 copy.

## Board
| | |
|---|---|
| Layers | 4 |
| Finished thickness | 1.6 mm |
| Copper, outer | 1 oz (35 um) - ASSUMPTION |
| Copper, inner | 1/2 oz (17.5 um), half-etched - ASSUMPTION |
| Laminate | Tg 150 C or better |
| Build standard | IPC-6012 Class 2 |
| Solder mask | Green, LPI |
| Silkscreen | White, minimum stroke 0.15 mm, minimum height 1.0 mm |
| Surface finish | ENIG - to be confirmed (F3) |

## Minimum features (our rules, not the fab's)
| | |
|---|---|
| Track / gap | 0.20 mm |
| Via | 0.60 mm pad / 0.30 mm drill, annular 0.15 mm minimum |
| Copper to board edge | 0.50 mm |
| Clearance, signal | 0.20 mm |
| Clearance, 5 V power | 0.25 mm |
| Clearance, PE to any other net | 0.30 mm |
| Silk text | 1.0 mm height / 0.15 mm stroke, enforced in the project rules |

## Vias in SMD pads - measured, not estimated

**67 of 319 vias sit inside an SMD pad on the current board.** The count rose from 65 to 67 during the
2026-11-03 reroutes (two new GND vias landed on existing SMD pads), so it is no longer "the same" as
Rev B. That is the same
count Rev B was cited for in finding R16, so the item is unaddressed rather than
partly done. The count was produced by testing every via against every SMD pad,
and it is invisible to DRC because KiCad does not flag via-in-pad by default.

Two ways out, and the second is the right one for this board:

| | | |
|---|---|---|
| Move all 67 off the pads | weeks of re-routing on the densest part of the board | rejected |
| **Specify via-fill and cap** | one line on the fab drawing and a cost line | **recommended** |

**Requirement to the fab: all vias inside SMD pads to be plugged, filled and capped
per IPC-4761 Class B (filled with epoxy) or Class C (filled with non-conductive
epoxy and capped), so that no open barrel remains under a solderable termination.**
Hand assembly makes this non-optional: an unfilled via under a pad wicks solder away
and leaves a starved joint, and 20 of the 67 are under passives on the 3V3 and sensor
rails where a dry joint would look like a field failure.

The 67 positions are listed in `revC/vias_in_pads.txt` (one row per via, with reference, pad, net,
position and via size) and must be re-counted after
any layout change. That file was regenerated from the saved board on 2026-11-01.

## Power copper
The 5 V input run from J18 through the protection to the plane is required to be a
**pour of 3 mm or more with six or more 0.3 mm vias at every layer change**
(condition 3, MS-CAR-CHK-001 C10). Today it is a 1.5 mm track. This is open.

The `/+5V_SENS` rail is 156.6 mOhm at 20 C, measured from the board file. Every
segment meets the 0.80 mm class floor except 12 capped at 0.60 mm by the J7 and
J13 pad rows.

## U10 - do not populate
U10 (`Package_TO_SOT_SMD:SOT-23-6` at 141.00, 100.80, reference value `eFuse`) is a
**positioned placeholder, not a circuit**. Verified from the saved board on
2026-11-01: all six pads carry local unconnected names and no pad has a circuit
net (`pcb/_evidence/power_chain_pads.json`). Leave it unpopulated.

It is the intended home of the reverse-polarity and over-voltage cut-off that
MS-CAR-REV-B-001 condition 2 requires and that Rev C does not yet have (item R4),
so nothing in this note may be read as saying J18 is protected. **This is also the
item on which the deviation from the named TPS26630 is still owed** (question 2 in
`REPLY_TO_CTO.md`). The converter decision below does not settle it: TPS26630 was
named for the board's cut-off at J18, a different function from the buck, and it is
unaffected by which off-board module is chosen.

## Off-board converter and the input lead (assembly, not fabrication)
The carrier takes **5 V at J18**. The buck is a separate module inside the
enclosure and is not a board part, so it belongs in this note rather than in the
BOM. Audited 2026-11-01: `revC/BUCK_AUDIT_XL4015_20261101.md`.

| | |
|---|---|
| **Not acceptable as a substitute** | **XL4015 5 A module, including the LED-voltmeter variant (Robu SKU 12253).** The XLSEMI data sheet gives 8-36 V operating input with a 40 V absolute maximum, which does not meet condition 1's "input rated 40 V or more", and no TVS that holds off at the 22-25 V battery-disconnect event clamps below 36 V. The XL4016 has the same 36 V/40 V window and is rejected for the same reason. The meter variant additionally carries a +65 C-rated display and 85 C electrolytics in a box the design takes to +70 C |
| Named part pending | LM2596HVS module (4.5-50 V page claim). **The die marking must be read before assembly:** TI's LM2596 is 40 V operating / 45 V absolute, an LM2596HV is 60 V / 63 V, so the surge plan below only holds with the HV die or with a signed deviation |
| Set point | 5.15 V, measured at the module's own terminals on a 4 1/2-digit meter. **The module's LED display is not evidence** - 0.1 V resolution, about ±1 % + 1 digit. Lock the pot after trimming (epoxy or two-part seal) and record the value on the build sheet |
| Fuse in the lead | One fuse at the module input, sized to the converter's own current limit, not to the load. F1 on the carrier is a 4 A-hold device needing about 8 A to trip, so it does not protect this lead |
| Surge part in the lead | SMBJ24A or SMCJ24A (standoff 24 V, breakdown minimum 26.7 V, clamp 38.9 V at rated pulse) at the module input, on the battery side of the fuse. This is the part condition 1 asks the converter to own; **neither module carries it** |
| Lead | 0.75 mm2 minimum, 200 mm maximum each way. 200 mm of 0.75 mm2 is 9.3 mOhm there and back at 20 C, inside condition 5's 15 mOhm; the same run in 0.5 mm2 at 300 mm each way is 21 mOhm and must not be used |
| Thermal | Heatsink fitted, 5 mm air gap, mounted so the diode and inductor heat is not driven into the carrier or the acrylic plate. Estimated module loss at 3 A is 2.5-3 W, of which about 1.1 W is the catch diode |
| Electrolytics | Any module chosen must be opened and its input capacitor verified at 105 C long-life and at least twice the highest voltage it can see, per item B3. General-purpose 85 C stock is not acceptable in this box |
| Polarity | J18 legend is `+` on pad 1 (`+5V_IN`) and `-` on pad 2 (`GND`). Neither the module nor the board has polarity protection until U10's circuit exists |

## Ground stitching
The In1 plane has 58 links that touch it. 55.6 % of the plane is more than 10 mm
from one and the farthest point is 35.36 mm, against E1's 10 mm acceptance. The
board has no GND pour on an outer layer, so a stitching via placed in the pour
connects on one layer only and DRC reports it as dangling. E1 is open; see
`revC/E1_stitching_plot.png`.

## Resistances used in the design justification
0.505 mOhm per square outer, 1.01 mOhm per square inner, at 1 oz / 1/2 oz and 20 C.
Add 0.39 % per C. **These follow from the copper weights above, which are assumptions.**


## Port map - what the silkscreen cannot carry

The bottom silk band is occupied by reference fields, so most port names cannot be printed at the 1.0 mm /
0.15 mm rule without moving those fields first. This table is the assembly-side answer (item E5): a builder
reads the port here, not from the board.

| Connector | Module / sensor | Pin 1 | Pin 2 | Pin 3 | Pin 4 | Pin 5 |
|---|---|---|---|---|---|---|
| J5 | modem 5 V in | +5V | GND | | | |
| J6 | E22-900T22D LoRa | GND (module pin 7) | /+5V_E22 (6) | /E22_AUX (5) | /UART1_LORA_RX (4) | /UART1_LORA_TX (3) |
| J7 | GY-521 MPU-6050 | MPU_INT | 3V3_C | XCL (NC) | XDA (NC) | /I2C1_SDA |
| J8 | DS3231 RTC | 32K (NC) | SQW (NC) | /I2C1_SCL | /I2C1_SDA | 3V3_C |
| J11 | SGP41 VOC/NOx | 3V3_SENS_SW | GND | /I2C0_SCL_CH0 | /I2C0_SDA_CH0 | |
| J12 | SHT45 T/RH | 3V3_SENS_SW | GND | /I2C0_SCL_CH1 | /I2C0_SDA_CH1 | |
| J13 | SPS30 PM | +5V_SENS | /I2C0_SDA_CH2 | /I2C0_SCL_CH2 | GND | GND |
| J14 | BME688 gas | 3V3_SENS_SW | GND | /I2C0_SCL_CH3 | /I2C0_SDA_CH3 | |
| J15 | soil probe (analog) | 3V3_SENS_SW | GND | /SOIL_ADC_RAW | | |
| J16 | FSR (analog) | 3V3_SENS_SW | /FSR_ADC_RAW | | | |
| J17 | cabled I2C port, CH4 | 3V3_SENS_SW | GND | /I2C0_SCL_CH4 | /I2C0_SDA_CH4 | |
| J20 | cabled I2C port, CH6 | 3V3_SENS_SW | GND | /I2C0_SCL_CH6 | /I2C0_SDA_CH6 | |
| J21 | FDC1004 capacitance | 3V3_SENS_SW | GND | /I2C0_SCL_CH5 | /I2C0_SDA_CH5 | |
| J22 | reed wind speed | /REED_PULSE | GND | | | |
| J23 | external button | /EVENT_BTN | GND | | | |
| J24 | panel LEDs | +5V | /LED1_K | /LED2_K | GND | |
| J25 | buzzer | +5V | /BZ_NEG | | | |
| J26 | AS5600 wind direction | 3V3_C | GND | /I2C1_SCL | /I2C1_SDA | |
| J18 | 5 V input | +5V_IN | GND | | | |
| J19 | protective earth | PE | GND | | | |

**J17 and J20 carry no sensor name** - they are generic cabled I2C ports on CH4 and CH6. Naming them is an
open question for Aswin; they are not invented here.

**J6 orientation.** The module has no pin-1 dot and our socket is 1x7, so nothing keys it. The socket is
numbered for a 180-degree insertion and all seven nets line up that way; the marking, not the wiring, is the
missing protection. A keyed shrouded header is the proper fix and is a cost decision for Serigreen.

## Assembly
Hand soldered, no panelisation, individual boards. Fiducials not required.
The modem board on J3/J4 is **not keyed** - the silkscreen now carries a `1` mark at
each socket's pin 1 and the note `MODEM THIS WAY UP`. Confirm during assembly that
the modem's UART row lands on the carrier's J4.

The BOM exported with this note has Manufacturer, MPN, Rating, Temp and Variant
columns that are **empty**. Part numbers, ratings and temperature ranges are not
sourced yet, so check C6 remains not met whatever the file timestamp says.

## Decoupling capacitors still to be added (Task C, 2026-11-03)

The CTO rule is: nearest 100 nF within 5 mm along the copper (3 mm at an IC's own pin), and bulk of 10 uF or
more within 10 mm. Measured on the saved board with those exact thresholds: **36 supply pins, 1 meets both
(J13.1), 3 meet the local rule, 3 meet the bulk rule.** Three capacitors were relocated on the board
(C41 -> Q9.3, C14 -> D2.1, C33 -> J13.1). Thirteen pins have a legal spot but no existing capacitor that can be
moved onto them, so they need a **new part and a schematic symbol** - a GUI job, not a board edit:

| pin | net | value | footprint | where it should sit | why not moved |
|---|---|---|---|---|---|
| J1.1 | 3V3_C | 100 nF | C_0805_2012Metric | (210.50, 157.75) rot 0 | every 3V3_C 100 nF is load-bearing for another pin |
| J4.3 | 3V3_C | 100 nF | C_0805_2012Metric | (273.50, 117.39) rot 0 | as above |
| J7.2 | 3V3_C | 100 nF | C_0805_2012Metric | (215.65, 163.00) rot 0 | as above |
| J7.8 | 3V3_C | 100 nF | C_0805_2012Metric | (229.14, 169.00) rot 0 | as above |
| J8.5 | 3V3_C | 100 nF | C_0805_2012Metric | (166.06, 157.25) rot 90 | needs a rotated part |
| J26.1 | 3V3_C | 100 nF | C_0805_2012Metric | (129.75, 152.50) rot 90 | needs a rotated part |
| J11.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (171.75, 195.00) rot 90 | needs a rotated part |
| J12.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (187.75, 193.50) rot 90 | needs a rotated part |
| J15.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (146.13, 193.50) rot 90 | needs a rotated part |
| J16.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (163.94, 189.50) rot 90 | needs a rotated part |
| J17.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (266.75, 194.25) rot 90 | needs a rotated part |
| J24.1 | +5V | 100 nF | C_0805_2012Metric | (138.97, 147.25) rot 0 | no +5V 100 nF left that can move |
| D7.1 | /+5V_ESP | 100 nF | C_0805_2012Metric | (215.60, 97.50) rot 90 | the net has no 100 nF at all (only C28, 10 uF) |

**Twenty further pins have no legal spot at all** inside the CTO's radius and cannot be fixed without moving
other parts or rerouting: U4.5, U6.1, U6.3, U6.5, U7.24, U8.24 (the six IC pins, 3 mm), Q2.2, Q2.3, Q3.2, Q3.3,
Q7.2, J1.2, J1.21, J5.1, J6.2, J14.1, J20.1, J21.1, J25.1, D7.2 (5 mm). The measured blockers are in the Task C
report and in `pcb\_work_20261103\taskC_spots.json`.

Two notes for whoever places these:
- the five rot-90 rows need a **rotated 0805**. Rotating an existing footprint on the board raises
  `lib_footprint_mismatch`, so add these as new parts rather than turning a placed one;
- every coordinate above is a legal bare-footprint position measured against tracks, vias, pads, courtyards and
  the module outlines. The connecting track and the GND via still have to be routed.

## E22 mode straps R56 and R57 (T-55, 2026-11-04)

The E22-900T22D's M0 and M1 pins are hard-strapped to GND through two 0 ohm 0603 resistors, R56 and R57,
at J6.6 (M1) and J6.7 (M0). This is deliberate: it fixes the module in normal (transparent) mode at every
power-up and frees GPIO10 and GPIO11, which the microSD slot uses for CS and MOSI.

**Configuration mode is reached by lifting one strap**, with the module out of its socket: remove R56 or
R57 and the corresponding pin floats high through the module's internal pull-up. The source for that
behaviour is the Ebyte E22-900T22D user manual, **sections 6.2 to 6.5** (M0/M1 mode table and the
configuration procedure). The verbatim text is **not reproduced here because the manual is not in the
workspace** - it is owed into `_cto_extract\` before this note is quoted to anyone.

Each strap's GND pad has **its own via** to the ground plane at (269.40, 164.92) and (269.40, 162.38); the
straps do not share J6.1's return, which carries the module's own current. The strap runs are on B.Cu
because `/PWR_EN` occupies the F.Cu corridor at x 264.75.

## E22 mode selection - quoted verbatim from the manufacturer manual

Source: `_cto_extract\E22-900T22D-UserManual.txt` (Ebyte E22-900T22D User Manual,
26 pages, from cdebyte.com). Copied into the workspace on 2026-11-04 so this is
checkable without the internet. Previously the note cited sections 6.2-6.5 without
quoting them because the manual was not in the repo - that gap is closed.

| Mode | M0 | M1 | What the manual says |
|---|---|---|---|
| 6.2 Normal (Mode 0) | 0 | 0 | "Users can input data through the serial port and the module will start wireless transmission." Receiving on, output on TXD. |
| 6.3 WOR (Mode 1) | 1 | 0 | Transmitter adds a preamble automatically; receiving "the same as mode 0". |
| 6.4 Configuration (Mode 2) | 0 | 1 | "Wireless transmitting off / Wireless receiving off / Users can access the registers to configure the module's operation state." |
| 6.5 Deep sleep (Mode 3) | 1 | 1 | "Unable to transmit wireless data / Unable to receive wireless data". |

Verbatim extract, sections 6.2 to 6.5:

```
6.2 Normal mode（Mode 0）
Type
M0 = 0，M1 = 0
Transmitting
Users can input data through the serial port and the module will start wireless transmission.
Receiving
The module wireless receiving function is turned on, and after receiving the wireless data, it will be output through the serial
port TXD pin.
6.3 WOR mode（Mode 1）
Type
M0 = 1，M1 =0
Chengdu Ebyte Electronic Technology Co., Ltd.
E22-900T22D User Manual
Copyright ©2012–2018，Chengdu Ebyte Electronic Technology Co.,Ltd.
14
Transmitting
When defined as a transmitting party, a preamble is automatically added before transmitting.
Receiving
It can receive data normally, the receiving function is the same as mode 0.
6.4 Configuration mode（Mode 2）
Type
M0 = 0，M1 = 1
Transmitting
Wireless transmitting off
Receiving
Wireless receiving off
Configuration
Users can access the registers to configure the module's operation state.
6.5 Deep sleep mode（Mode 3）
Type
M0 = 1，M1 = 1
Transmitting
Unable to transmit wireless data
Receiving
Unable to receive wireless data
Note
When from the sleep mode to other modes, the module will reconfigure the parameters. During the configuration process,
AUX will remain low; After configuration,it outputs high level, we suggest that user test rising edge AUX.
```

### What this means for the straps on this board

- R56 and R57 hold M0 and M1 low, so the module powers into **Mode 0, normal
  transmission** - the configuration Aswin proved over the air.
- **Configuration mode is M0 = 0, M1 = 1.** So removing **R56** (the M1 strap) and
  leaving R57 fitted gives Mode 2, which is the only way to change channel, speed,
  power or address. Both straps fitted is Mode 0; removing R57 alone gives Mode 1
  (WOR), not configuration.
- Section 7.1 adds a constraint for whoever configures a unit: in Mode 2 the module
  supports **9600 8N1 only**, and the register command format is
  `C0 + start address + length + parameters`.
- Note in 6.5: leaving sleep mode re-reads the parameters and holds AUX low during
  that window - relevant to how firmware uses AUX.

