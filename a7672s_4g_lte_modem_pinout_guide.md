# Parry Technology A7672S 4G LTE Modem - Pinout Reference
**Part Number:** `PTG4GBOB-SC104V1`  
**Core Module:** SIMCom A7672S (LTE Cat-1 / GSM)

> **Direction Convention:**  
> * **Input:** Signal or power going **into** the modem board from your external power supply or Microcontroller (MCU).  
> * **Output:** Signal or power coming **out of** the modem board to your MCU or external peripherals.

---

## 1. Main Power Connector (`J1` - Top 2-Pin JST)

* **+5V SUPPLY** - **5V Power Input** - To power the modem PCB with $5\text{V} \pm 5\%$ input (requires a minimum $2\text{A}$ peak current capability).
* **GROUND** - **Power Ground** - Common ground reference for the main $5\text{V}$ power supply.

---

## 2. Left Header (`J3` - 12-Pin Header, Top to Bottom)

* **A7672_PWR_KEY** - **Digital Input ($3.3\text{V}$–$5\text{V}$ level-translated)** - Pulled via MCU to turn the A7672S cellular module ON or OFF via software pulse.
* **GROUND** - **Ground** - Common digital and signal ground reference.
* **VDD_IN_UART** - **Voltage Reference Input ($3.3\text{V}$ to $5\text{V}$)** - Connects to your MCU's logic supply ($3.3\text{V}$ or $5\text{V}$) to set the operating voltage of the onboard UART level translator.
* **A7672_TXD** - **UART Output (Level-translated to `VDD_IN_UART`)** - Serial data transmitted out from the modem (connect to your MCU's **RX** pin).
* **A7672_RXD** - **UART Input (Level-translated to `VDD_IN_UART`)** - Serial data received into the modem (connect to your MCU's **TX** pin).
* **GROUND** - **Ground** - Common digital ground reference for UART signals.
* **VDD_1V8** - **1.8V Power Output** - Regulated $1.8\text{V}$ reference output from the modem's internal LDO (for low-current $1.8\text{V}$ pull-ups/level-shifters only, max $\sim 50\text{mA}$).
* **A7672_RESET** - **Digital Input ($3.3\text{V}$–$5\text{V}$ level-translated)** - Hardware reset control pin used by an external MCU to force-restart the A7672S module.
* **GPIO1_1V8** - **Bidirectional Digital I/O ($1.8\text{V}$ logic)** - General-purpose input/output pin #1 for remote monitoring or control (strictly $1.8\text{V}$ logic level).
* **UART_LOG_RX** - **Debug UART Input ($1.8\text{V}$ logic)** - Diagnostic serial receive pin used exclusively for SIMCom firmware debugging.
* **UART_LOG_TX** - **Debug UART Output ($1.8\text{V}$ logic)** - Diagnostic serial transmit pin used for capturing internal modem boot and crash logs.
* **GROUND** - **Ground** - Common digital ground reference.

---

## 3. Right Header (`J4` - 12-Pin Header, Top to Bottom)

* **PWR_EN** - **Digital Input ($3.3\text{V}$–$5\text{V}$ level-translated)** - Controls the onboard power regulator to completely enable or cut off the main power supply to the modem PCB.
* **MIC_N** - **Analog Audio Input (-)** - Differential microphone negative input for analog voice calls.
* **MIC_P** - **Analog Audio Input (+)** - Differential microphone positive input for analog voice calls.
* **EAR_N** - **Analog Audio Output (-)** - Differential earpiece/speaker negative output for analog voice calls.
* **EAR_P** - **Analog Audio Output (+)** - Differential earpiece/speaker positive output for analog voice calls.
* **GROUND** - **Ground** - Common analog/digital ground reference (acts as shield ground between audio and I2C lines).
* **SDA_1V8** - **I2C Data Input/Output ($1.8\text{V}$ logic)** - Bidirectional serial data line for the I2C bus interface (operates at $1.8\text{V}$ logic).
* **SCL_1V8** - **I2C Clock Output ($1.8\text{V}$ logic)** - Serial clock line for the I2C bus interface (operates at $1.8\text{V}$ logic).
* **GROUND** - **Ground** - Common digital ground reference.
* **GPIO2_1V8** - **Bidirectional Digital I/O ($1.8\text{V}$ logic)** - General-purpose input/output pin #2 for remote monitoring or control (strictly $1.8\text{V}$ logic level).
* **ADC** - **Analog Input ($0\text{V}$ to $1.8\text{V}$ range)** - Analog-to-Digital Converter input pin to read external voltage levels via AT commands (`AT+CADC`).
* **GROUND** - **Ground** - Common analog/digital ground reference.

---

## 4. Onboard Ports, Jumpers & Indicators

* **J7 (Micro-USB Port)** - **Bidirectional USB Data** - USB 2.0 port for AT commands, PPP/NDIS cellular data, diagnostics, and firmware upgrades with a PC or Linux SBC.
* **E1 (LTE ANTENNA CON)** - **RF Input/Output ($50\ \Omega$)** - U.FL coaxial connector for attaching the external 4G LTE / GSM antenna.
* **J8 (SIM Socket)** - **SIM Interface (Back of PCB)** - Hinged Nano/Micro SIM card slot supporting $1.8\text{V}$ / $3.0\text{V}$ USIM cards.
* **J2 (`PWR_KEY` Jumper)** - **Hardware Jumper Input** - Shorting this 2-pin jumper automatically turns the A7672S module ON as soon as $5\text{V}$ power is supplied.
* **J5 (`BOOT` Jumper)** - **Hardware Jumper Input** - Shorting this 2-pin jumper before power-up forces the module into USB firmware download/recovery mode.
* **J6 (`RESET` Jumper)** - **Hardware Jumper Input** - Momentarily shorting this 2-pin header manually hard-resets the A7672S module.
* **D1 (`STATUS LED`)** - **Visual Output** - Illuminates to indicate the A7672S module is powered ON and active.
* **D2 (`POWER LED`)** - **Visual Output** - Illuminates to confirm the onboard power regulator (`VBAT`) is active and supplying power.
* **D3 (`NETLIGHT LED`)** - **Visual Output** - Blinks at specific intervals to indicate cellular network registration and data transmission status.