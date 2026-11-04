ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
RT = ROOT + r"\REPLY_TO_CTO.md"
FN = ROOT + r"\revC\FAB_NOTES.md"

# ---- 1. remove the "mirror image" wording from the tracker ----
t = open(TT, encoding="utf-8").read()
import re
lines = t.split("\n")
for i, line in enumerate(lines):
    if "mirror" in line:
        lines[i] = line.replace("the socket remains in mirror image", "the socket carries no orientation mark (item A3)")
        lines[i] = lines[i].replace("socket is still in mirror image", "socket still carries no orientation mark")
        lines[i] = lines[i].replace("still in mirror image", "unmarked (A3)")
        lines[i] = lines[i].replace("in mirror image", "unmarked (A3)")
t = "\n".join(lines)
# J6 is not mis-wired: state the corrected fact once, near finding 25
t = t.replace("25. **The J6 pin-1 confirmation does not exist in the workspace - 2026-11-02.**",
              "25. **J6 is NOT mis-wired - corrected 2026-11-03.** It is numbered for a 180-degree insertion and all seven nets\n    line up that way; the defect is that nothing marks or keys the orientation (item A3). Earlier notes that called it a\n    mirror-image wiring fault are withdrawn. What follows is only about the absent pin-1 confirmation.\n\n25a. **The J6 pin-1 confirmation does not exist in the workspace - 2026-11-02.**")
open(TT, "w", encoding="utf-8", newline="").write(t)

# ---- 2. under-module counts: only J3, J4, J5 are inside the modem outline ----
t = open(TT, encoding="utf-8").read()
t = t.replace("| E4 | P2 | 004 T9 | \"Layout.\" | Open | 12 test points; three under the modem; none on I2C-1 or UART1; the +12 V point is obsolete |",
              "| E4 | P2 | 004 T9 | \"Layout.\" | Open | 12 test points; **none under the modem** - TP2 (274.75), TP3 (275.75) and TP5 (276.25) are outside the 228.50-271.50 outline; none on I2C-1 or UART1; the +12 V point is obsolete |")
open(TT, "w", encoding="utf-8", newline="").write(t)

r = open(RT, encoding="utf-8").read()
r = r.replace("| E4 | 12 test points; three under the modem; none on I2C-1 or UART1; the +12 V point is obsolete | TP2-TP12 | Open - an",
              "| E4 | 12 test points; **none under the modem** (TP2/TP3/TP5 sit outside the modem outline); none on I2C-1 or UART1; the +12 V point is obsolete | TP2-TP12 | Open - an")
open(RT, "w", encoding="utf-8", newline="").write(r)

# ---- 3. port map table in FAB_NOTES (the legitimate answer where silk cannot fit) ----
fn = open(FN, encoding="utf-8").read()
table = """
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
"""
fn = fn.replace("## Assembly", table + "\n## Assembly")
open(FN, "w", encoding="utf-8", newline="").write(fn)
print("docs corrected; port map added")
