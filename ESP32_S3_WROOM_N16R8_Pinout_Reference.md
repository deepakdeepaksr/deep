# ESP32-S3-WROOM N16R8 — Complete Pinout & Hardware Connection Reference

Based on the supplied Edgehax ESP32-S3 PRO pinout diagram

## 1. Board overview

| Module / variant | ESP32-S3-WROOM-1 N16R8 |
| --- | --- |
| Processor | Dual-core Xtensa LX7, up to 240 MHz |
| Memory | 16 MB Flash + 8 MB PSRAM (as stated in the diagram) |
| Wireless | 2.4 GHz Wi-Fi 802.11 b/g/n; Bluetooth LE 5 |
| I/O | 3.3 V logic GPIO; ADC, touch, UART, SPI, I²C and USB functions |
| Connectors shown | USB Type-C connectors, 4-pin I²C header, 2-pin battery connector, microSD slot |

## 2. Left-side header pins (top to bottom)

| Pin | Diagram functions | What it is used for |
| --- | --- | --- |
| 3V3 | 3.3 V regulated supply output | Power for compatible 3.3 V sensors/modules. Do not apply 5 V. |
| 3V3 | Second 3.3 V supply pin | Same 3.3 V rail as the first 3V3 pin. |
| RST | Reset input | Reset the ESP32-S3; normally pulled high on the board. Do not use as GPIO. |
| GPIO4 | ADC1_CH3; TOUCH4 | General digital I/O, analog input, capacitive touch. |
| GPIO5 | ADC1_CH4; TOUCH5 | General digital I/O, analog input, capacitive touch. |
| GPIO6 | ADC1_CH5; TOUCH6 | General digital I/O, analog input, capacitive touch. |
| GPIO7 | ADC1_CH6; TOUCH7 | General digital I/O, analog input, capacitive touch. |
| GPIO15 | ADC2_CH4; U0RTS | Digital I/O, ADC2 input, UART0 RTS alternate function. |
| GPIO16 | ADC2_CH5; U0CTS | Digital I/O, ADC2 input, UART0 CTS alternate function. |
| GPIO17 | ADC2_CH6; U1TX | Digital I/O, ADC2 input, UART1 transmit alternate function. |
| GPIO18 | ADC2_CH7; U1RX | Digital I/O, ADC2 input, UART1 receive alternate function. |
| GPIO8 | ADC1_CH7; TOUCH8 | General digital I/O, analog input, capacitive touch. |
| GPIO3 | ADC1_CH2; TOUCH3; JTAG label | Digital I/O, ADC1 and touch. Treat cautiously because of boot/JTAG-related functions. |
| GPIO46 | LOG label | Special-purpose/strapping-related pin; avoid using as an ordinary output unless its boot behaviour is understood. |
| GPIO9 | ADC1_CH8; TOUCH9; FSPIHD | Digital I/O, ADC1/touch; also shown with flash-SPI alternate function. |
| GPIO10 | ADC1_CH9; TOUCH10; FSPI-CS0 | Digital I/O, ADC1/touch; SPI chip-select alternate function. |
| GPIO11 | ADC2_CH0; TOUCH11; FSPID | Digital I/O, ADC2/touch; SPI data alternate function. |
| GPIO12 | ADC2_CH1; TOUCH12; FSPICLK | Digital I/O, ADC2/touch; SPI clock alternate function. |
| GPIO13 | ADC2_CH2; TOUCH13; FSPIQ | Digital I/O, ADC2/touch; SPI data alternate function. |
| GPIO14 | ADC2_CH3; TOUCH14; FSPIWP | Digital I/O, ADC2/touch; SPI write-protect alternate function. |
| 5V | 5 V rail | Board 5 V supply/VBUS rail as implemented by this dev board. Check power-source direction/current limits. |
| GND | Ground | Common electrical reference and return path. |

## 3. Right-side header pins (top to bottom)

| Pin | Diagram functions | What it is used for |
| --- | --- | --- |
| GND | Ground | Ground reference. |
| GPIO43 | TX_U0 / UART0 TX; CLK_OUT1 | UART0 transmit; often used for serial logging/programming depending on board routing. |
| GPIO44 | RX_U0 / UART0 RX; CLK_OUT2 | UART0 receive. |
| GPIO1 | ADC1_CH0; TOUCH1 | Digital I/O, ADC1 analog input, capacitive touch. |
| GPIO2 | ADC1_CH1; TOUCH2 | Digital I/O, ADC1 analog input, capacitive touch. |
| GPIO42 | MTMS; GRN_LED label | JTAG MTMS alternate function; board diagram also labels green LED. |
| GPIO41 | MTDI; CLK_OUT1; WHT_LED label | JTAG MTDI / clock output; board diagram labels white LED. |
| GPIO40 | MTDO; CLK_OUT2; ORNG_LED label | JTAG MTDO / clock output; board diagram labels orange LED. |
| GPIO39 | MTCK; CLK_OUT3; SUBSPICS1 | JTAG MTCK / clock output / SPI chip select alternate function. |
| GPIO38 | FSPIWP; SUBSPIWP | Flash-SPI write-protect alternate function; avoid repurposing without checking module routing. |
| GPIO37 | SPIDQS; FSPIQ; SUBSPIQ | Flash/PSRAM interface alternate functions; avoid repurposing. |
| GPIO36 | SPIIO7; FSPICLK; SUBSPICLK | Flash/PSRAM interface alternate functions; avoid repurposing. |
| GPIO35 | SPIIO6; PSPID; SUBSPID | Flash/PSRAM interface alternate functions; avoid repurposing. |
| GPIO0 | BOOT | Boot-mode strapping pin and BOOT button connection. Keep its reset-time level in mind. |
| GPIO45 | VSPI label | Strapping-related pin; avoid external circuits that force an unwanted level during reset. |
| GPIO48 | SPICLK_N | SPI clock-related alternate function; usable GPIO only after checking board design and peripheral conflicts. |
| GPIO47 | SPICLK_P | SPI clock-related alternate function; usable GPIO only after checking board design and peripheral conflicts. |
| GPIO21 | RTC | General digital I/O; diagram marks RTC-domain capability. |
| GPIO20 | USB D+; U1CTS; ADC2_CH9; CLK_OUT1 | Native USB D+ function. Avoid using as GPIO if native USB is needed. |
| GPIO19 | USB D-; U1RTS; ADC2_CH8; CLK_OUT2 | Native USB D- function. Avoid using as GPIO if native USB is needed. |
| GND | Ground | Ground reference. |
| GND | Ground | Second ground pin. |

## 4. On-board connectors and controls

| Connector / control | Description |
| --- | --- |
| I²C 4-pin header | SDA, SCL, 3V3, GND (as printed on the board). Connect I²C sensors such as IMUs, temperature sensors and IO expanders. Confirm the actual SDA/SCL GPIO mapping from the board schematic or continuity test; the diagram does not state the GPIO numbers. |
| Battery connector | 2-pin, 1.27 mm pitch. The diagram identifies the connector but does not specify battery chemistry, voltage range, polarity or charging circuit. Verify the board manual/schematic before connecting a battery. |
| USB Type-C connectors | One is labelled USB and the other UART on the PCB. Use the USB-labelled port for native USB functions where supported and UART-labelled port for serial/programming, subject to the board's circuit design. |
| microSD slot | On-board storage. The diagram shows FSPI-related signals and shared peripheral labels around GPIO9–GPIO14. Assume these pins may be reserved by the microSD/flash routing until the exact board schematic confirms otherwise. |
| BOOT button | Controls boot mode when held during reset/power-up. Do not attach circuitry that unintentionally pulls GPIO0 to the wrong level during startup. |
| RESET button | Resets the ESP32-S3. |
| TP pads | Test points; not identified as user GPIO in the diagram. |

## 5. ADC and touch pin reference

| Group | GPIO mapping | Notes |
| --- | --- | --- |
| ADC1_CH0–CH9 | GPIO1, GPIO2, GPIO3, GPIO4, GPIO5, GPIO6, GPIO7, GPIO8, GPIO9, GPIO10 | ADC1 channels shown in the diagram. |
| ADC2_CH0–CH9 | GPIO11, GPIO12, GPIO13, GPIO14, GPIO15, GPIO16, GPIO17, GPIO18, GPIO20, GPIO19 | ADC2 channels shown in the diagram. ADC2 availability can be affected by Wi-Fi and framework/driver limitations; prefer ADC1 where practical. |
| TOUCH1–TOUCH14 | GPIO1–GPIO14 (specific mapping: GPIO1=TOUCH1 ... GPIO14=TOUCH14, except no separate touch label for some pins in the diagram) | Capacitive touch sensing. Touch capability does not mean the pin is an analogue touch sensor in every framework; use ESP-IDF/Arduino support for this chip. |

## 6. Communication and special-function summary

| Interface | Pin/function mapping |
| --- | --- |
| UART0 | GPIO43 = TX; GPIO44 = RX. GPIO15/16 are labelled U0RTS/U0CTS. |
| UART1 | GPIO17 = TX; GPIO18 = RX. GPIO19/20 have U1RTS/U1CTS alternate labels in the diagram. |
| Native USB | GPIO20 = USB D+; GPIO19 = USB D-. Keep these free if using native USB. |
| JTAG | GPIO39=MTCK, GPIO40=MTDO, GPIO41=MTDI, GPIO42=MTMS. GPIO3 also carries a JTAG label in the diagram. |
| SPI / memory signals | GPIO9–GPIO14 and GPIO35–GPIO38 carry FSPI/PSPI-related labels. Confirm which are connected to on-board storage or module memory before assigning them to external SPI devices. |
| Clock outputs | CLK_OUT labels appear on GPIO18, GPIO39–GPIO41, GPIO43 and GPIO44 in the diagram. |

## 7. Practical pin-selection recommendations

- **General digital inputs/outputs:** GPIO4, GPIO5, GPIO6, GPIO7, GPIO8, GPIO1, GPIO2, GPIO21 are reasonable starting candidates, subject to checking your firmware and board routing.
- **Analog sensors:** Prefer ADC1 pins such as GPIO1–GPIO10 where available. Use a suitable voltage divider/conditioning circuit and keep the input within the chip's allowed range.
- **UART sensor/module:** A convenient UART1 pair shown is GPIO17 (TX) and GPIO18 (RX). Cross TX-to-RX and RX-to-TX; share GND. Confirm voltage levels.
- **I²C sensors:** Use the board's dedicated 4-pin I²C header (SDA/SCL/3V3/GND). Verify its GPIO mapping before configuring software.
- **Native USB:** Reserve GPIO19 and GPIO20 for USB D-/D+ when using native USB.
- **Avoid until verified:** GPIO0, GPIO3, GPIO45, GPIO46 (boot/strapping/JTAG-related considerations); GPIO35–GPIO38 and GPIO9–GPIO14 (flash/PSRAM/microSD-related alternate functions); GPIO39–GPIO42 (JTAG functions).
- **Motors, relays and high-current loads:** Never drive a motor, relay coil, solenoid or other high-current load directly from a GPIO. Use a suitable MOSFET/driver, flyback protection where required, and an appropriate external supply. Connect grounds appropriately unless the design intentionally uses isolation.

## 8. Electrical and safety notes

- ESP32-S3 GPIO uses 3.3 V logic. GPIO pins are not 5 V tolerant; do not apply 5 V directly to any GPIO or ADC pin.
- 3V3 is the 3.3 V rail; 5V is the board's 5 V rail. The maximum current available from either rail depends on the board regulator, USB source and thermal conditions.
- All external logic signals should share a common ground unless galvanic isolation is intentionally used.
- ADC inputs require a voltage within the ESP32-S3 ADC input range. Use a correctly calculated divider or signal-conditioning circuit for higher voltages.
- Do not assume every pin shown as GPIO is freely available. Module flash/PSRAM connections, on-board microSD, LEDs, USB, boot straps and debug functions may reserve or load pins.
- GPIO labels for LEDs and peripheral signals in the diagram are alternate functions or board-level labels; they do not guarantee that every function is enabled or routed exactly as a generic ESP32-S3 module would be.

## 9. Important verification note

This reference transcribes the supplied Edgehax S3-PRO diagram. It is not a substitute for the exact board schematic or ESP32-S3-WROOM-1 datasheet. The diagram does not provide the I²C header's GPIO numbers, battery voltage/polarity, regulator current limits, or complete on-board microSD routing. Verify those details from the board schematic or with continuity measurements before final PCB wiring or applying power.
