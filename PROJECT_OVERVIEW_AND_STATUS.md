# MoriShield Carrier Rev C — Comprehensive Project Overview & Engineering Status Report

| Project Attribute | Details |
| :--- | :--- |
| **Project Title** | **MoriShield Carrier Board — Revision C** |
| **Document Purpose** | Executive Project Summary, Engineering History, Client Requirements, & PCB Update Log |
| **Client / Stakeholder** | **Serigreen Technologies** (Lead Reviewer: Aswin, CTO: Dr. Shanmugakumar) |
| **Document Classification** | Engineering Documentation & Release Tracking |
| **PCB Layout Target** | 4-Layer High-Reliability Agricultural IoT Carrier (`1.6 mm` FR4, $1\text{ oz}$ Cu outer / $1\text{ oz}$ inner) |
| **Design Toolchain** | KiCad 10.0.6 (Schematic Editor, PCBnew, Python API, `kicad-cli`) |
| **Document Date** | November 2026 |

---

## 1. What is Our Project?

### 1.1 System Purpose & Environmental Application
The **MoriShield Carrier** is a specialized, ruggedized industrial edge-computing gateway designed specifically for **precision sericulture and pesticide drift monitoring** in silk-farming regions (such as the mulberry farming belts in Karnataka and Tamil Nadu, India). 

Silkworms (*Bombyx mori*) are exceptionally vulnerable to sublethal or lethal drift from synthetic pyrethroids, organophosphates, and neonicotinoids sprayed on neighbouring cotton, vegetable, or fruit orchards. A drift cloud entering a rearing shed or settling on mulberry foliage can decimate an entire cocoon crop within hours.

The MoriShield system continuously measures microclimate data, ambient particulate drift plumes, wind vectors, and soil conditions to provide farmers with **early drift warnings, automated shed ventilation control, and telemetry logging**.

```
                   +-------------------------------------------------------+
                   |               MoriShield Carrier (Rev C)              |
                   |                                                       |
[ Solar / Battery ]---> [ Wide-Input Protection & Step-Down ]              |
                   |       (Over-voltage / Reverse Polarity)               |
                   |                      |                                |
                   |                      v                                |
                   |     +-----------------------------------+             |
                   |     |    EdgeHax / Keyestudio S3-PRO    |             |
                   |     |   (ESP32-S3-WROOM-1, N16R8)       |             |
                   |     +-----------------+-----------------+             |
                   |                       |                               |
                   |       +---------------+---------------+               |
                   |       |                               |               |
                   |       v                               v               |
                   |  [ Dedicated I2C-1 ]            [ Switched I2C-0 ]    |
                   |       |                               |               |
                   |       v                               v               |
                   |  +---------+                    +-----------+         |
                   |  | TCA9535 |                    |  TCA9548A |<--GPIO14|
                   |  | (U8 IO) |                    |  (U7 Mux) | (Active)|
                   |  +----+----+                    +-----+-----+         |
                   |       |                               |               |
                   |   Modem Power                    Field Sensors:       |
                   |   Switched Rails                - SPS30 Particle      |
                   |   Watchdog Kick                 - SHT31 Temp / RH     |
                   |   Status Lamps                  - BMP280 Barometer    |
                   |   Buzzer Alarm                  - MPU6050 IMU         |
                   |                                                       |
                   |  [ Cellular Telemetry ]         [ Long-Range Radio ]  |
                   |  Parry A7672S 4G LTE-Cat1       Ebyte E22-900T22D     |
                   |  (UART2, 100-ohm Reset)         (SX1262 LoRa UART1)   |
                   +-------------------------------------------------------+
```

### 1.2 Core Subsystems & Component Topology
1. **Host Microcontroller**:
   * **EdgeHax / Keyestudio S3-PRO Module** socketed onto dual 1x22 pin vertical headers (`J1` and `J2`).
   * Powered by **ESP32-S3-WROOM-1 N16R8** with **16 MB Octal Flash** and **8 MB Octal PSRAM**.
2. **Cellular Connectivity (4G LTE)**:
   * **Parry A7672S LTE Cat-1 Module** (with 2G fallback) on dual 1x12 socket headers (`J3` and `J4`).
   * Dedicated UART2 communication, hardware reset line with $100\ \Omega$ series damping, and power control via discrete P-MOSFET switching.
3. **Long-Range LoRa Radio**:
   * **Ebyte E22-900T22D Transceiver** (Semtech SX1262 base, 868/915 MHz, $22\text{ dBm}$ / $160\text{ mW}$ output) for mesh networking across orchard plots.
4. **Primary External Sensor Bus (I²C-0)**:
   * **TI TCA9548A 8-Channel I²C Multiplexer (`U7`)** isolating 7 external sensor ports on robust cabled connectors:
     * Sensirion SPS30 Optical Particulate Spectrometer (dedicated channel).
     * Sensirion SHT31-DIS High-Accuracy Temperature & Relative Humidity.
     * Bosch BMP280 High-Precision Barometric Pressure.
     * GY-521 6-Axis Motion / IMU (MPU-6050) for shed vibration and pole tilt.
5. **Isolated Internal Peripheral Bus (I²C-1)**:
   * **TI TCA9535 16-Bit I/O Expander (`U8`)** dedicated to internal board controls: switched power gates, status LEDs, alarm buzzer, and external hardware watchdog kick (`WDI`).
6. **Auxiliary Agricultural Analog Inputs**:
   * High-voltage protected analog inputs for capacitive soil moisture probes (`J15`), piezoelectric droplet impact sensor (`J16`), and reed-switch cup anemometer (`J22`).
7. **Hardware Reliability & Supervisors**:
   * External hardware watchdog supervisor (**TI TPS3823 / TPS3828**) asserting a hard reset pulse on `/RST_ESP` if firmware fails to toggle `WDI`.

---

## 2. What Happened? (Project Background & Prior Issues)

### 2.1 The Rev B Review & Rejection
Prior to Revision C, the team submitted the **Revision B** design package to Serigreen Technologies for production sign-off. Following an in-depth audit by Serigreen’s engineering leadership, **Revision B was rejected**. 

The CTO issued a comprehensive audit report containing **76 technical findings** across 8 categories (A through H) and **13 mandatory release gate checks (C1 through C13)** that had to be satisfied before any manufacturing could proceed.

### 2.2 Critical Flaws Identified in Rev B
1. **Dual Driver Electrical Short on `/PWR_EN` (Item R7 / Task T-04)**:
   * Both the ESP32 microcontroller (`GPIO7` on `J1.7`) and the I/O expander (`U8.16`) were hard-wired together directly to `/PWR_EN`. If software configured one as HIGH and one as LOW, the resulting contention formed an unconstrained short across power domains, causing pin degradation or lockup.
2. **Ground Plane Choke & Copper Barrier at $x = 264.75\text{ mm}$**:
   * The board layout routed the redundant `/PWR_EN` trace from `U8.16` across the board in a 12-segment copper run, forming a continuous vertical barrier that severed top-layer copper and forced poor ground return paths.
3. **Catastrophic Bus Failure Dependency (Item R17 / Task T-14)**:
   * The internal TCA9535 I/O expander (`U8`) was placed on the same external bus (`I2C-0`) as all field sensors. If an outdoor cable connected to an orchard sensor was pinched, severed, or shorted to ground, the entire internal control architecture (power switching, watchdog service, fault indicators) was paralyzed.
4. **Passive RC Delay Lockup on I²C Switch Reset (Item R11 / Task T-14)**:
   * The TCA9548A switch (`U7`) reset pin relied solely on a passive resistor-capacitor circuit (`R24`/`C29`). When an external I²C bus hung (a frequent occurrence in agricultural cables exposed to lightning surges or motor noise), the firmware had no way to assert a reset pulse to recover the multiplexer without power-cycling the whole device.
5. **Microcontroller Boot Failure via Strapping Pin (Item R10 / Task T-16)**:
   * The user-facing event/calibration button (`/EVENT_BTN`) was wired to `GPIO3`. In the ESP32-S3, `GPIO3` is a critical strapping pin tied to JTAG / boot configuration. If a farm operator held down the button while powering on the unit, the processor refused to boot user firmware.
6. **Missing Series Damping on Cellular Reset (Item B2 / Task T-05)**:
   * The `/MODEM_RST` line ran directly from the MCU to the A7672S module header without damping resistance. Cellular transmission bursts (up to $2\text{ A}$ pulses) induced ringing on adjacent high-impedance reset traces, triggering sporadic modem reboots.
7. **Unverified BOM & Non-Industrial Dielectrics (Check C6 / Task T-26)**:
   * The Rev B BOM had blank manufacturer part numbers (MPNs), non-industrial temperature ratings ($65^\circ\text{C}$ / $85^\circ\text{C}$ parts in an enclosure rated for $70^\circ\text{C}$ ambient air), and unstable $Y5V/Z5U$ ceramic capacitor dielectrics.
8. **Incomplete Quality Evidence (Checks C11, C13)**:
   * Missing signed GPIO pin map, lack of a formalized Failure Mode and Effects Analysis (FMEA), and no documented, staged hardware bring-up plan.

---

## 3. What Does the Client Want? (CTO Requirements & Release Gates)

Serigreen Technologies established **13 formal release gate checks (C1–C13)** and **76 technical review items** that govern acceptable hardware delivery:

### The 13 Release Gates (C1 to C13):
* **Gate C1 (Rule Verification)**: Clean KiCad ERC and DRC with zero errors, zero warnings, zero suppressions, and zero schematic parity mismatches.
* **Gate C2 (Plane Integrity)**: Unbroken ground return planes on `In1.Cu`, symmetric copper pour balance, and zero high-speed antenna traces routed over split planes.
* **Gate C3 (Release Traceability)**: Manufacturing Gerbers, drill files, and reports must strictly post-date the schematic and board saves.
* **Gate C4 (Pin & Subsystem Safety)**: All strapping pins (`GPIO0`, `GPIO3`, `GPIO45`, `GPIO46`) and high-speed PSRAM pins (`GPIO35–37`) freed from external loads; dedicated status lights and buzzers.
* **Gate C5 (Library Self-Containment)**: Design packages must stage all custom footprint (`.pretty`) and symbol (`.kicad_sym`) libraries with portable `${KIPRJMOD}/libraries/...` path declarations.
* **Gate C6 (Industrial BOM Sourcing)**: Fully populated BOM with exact orderable MPNs, rated from $-40^\circ\text{C}$ to $+85^\circ\text{C}$ or $+105^\circ\text{C}$, industrial $X7R/X5R$ capacitor dielectrics, and appropriate voltage safety derating ($\ge 50\%$).
* **Gate C7 (Transient Resilience)**: Continuous $5\text{ V}$ power delivery during modem $2\text{ A}$ RF attach bursts and external fan/pump starts.
* **Gate C8 (ESD Hardening)**: Full IEC 61000-4-2 ESD protection ($\pm 4\text{ kV}$ contact, $\pm 8\text{ kV}$ air) on all field-facing connector lines with TVS arrays located close to port entries.
* **Gate C9 (Unassigned Ports)**: Written architectural justification or removal of all legacy test headers and jumpers.
* **Gate C10 (Plane Cleanliness)**: No high-current or sensitive signal tracks routed on the internal ground/power reference plane (`In2.Cu`).
* **Gate C11 (Signed Pin Map & Control Truth Table)**: Fully signed GPIO allocation table, single driver per signal line, defined boot-up states, and watchdog survival through resets.
* **Gate C12 (Automated Verification Scripts)**: Automated verification (`trace2.py`, `gate_truth.py`, `final_verify.py`) running with zero discrepancies.
* **Gate C13 (Engineering Evidence Package)**: Hardware FMEA containing at least 20 documented failure modes and a numbered 7-stage Hardware Bring-Up Plan with stop limits.

---

## 4. What Has Been Updated in the PCB & Package?

### 4.1 Schematic Hardening Updates
All changes applied to [`pcb/MoriShield_Carrier.kicad_sch`](file:///c:/Users/pradeesh/Music/morishield_frimware/New%20folder/new%20pcb/pcb/MoriShield_Carrier.kicad_sch):

| Task / Item | Schematic Modification | Engineering Benefit |
| :--- | :--- | :--- |
| **Task T-04**<br>*(Item R7)* | Removed duplicate `/PWR_EN` label from `U8` pin 16; replaced with KiCad `no_connect`. | ESP32 `GPIO7` (`J1.7`) is now the **sole designated hardware driver**. Eliminates driver contention short. |
| **Task T-14**<br>*(Item R17)* | Remapped `U8` pins 22 & 23 from `/I2C0_SCL` and `/I2C0_SDA` to **`/I2C1_SCL`** and **`/I2C1_SDA`**. | Moves the TCA9535 expander to internal `I2C-1`. Prevents cabled field sensor shorts from locking up internal board functions. |
| **Task T-14**<br>*(Item R17)* | Wired `U7` TCA9548A reset to ESP32 **`GPIO14` (`J1.20`)** via label `/I2C_SW_RST`; marked `C29` ($100\text{ nF}$) as **`(dnp yes)`**. | Enables firmware to dynamically pulse reset the I²C multiplexer to recover from frozen sensor channels without fighting a capacitive hold. |
| **Task T-16**<br>*(Item R10)* | Disconnected `/EVENT_BTN` from strapping pin `GPIO3` (`J1.13`) and placed `no_connect`; relocated `/EVENT_BTN` to **`GPIO15` (`J1.8`)**. | Eliminates boot-mode and JTAG hardware strapping conflicts. Operator button presses can never hang MCU boot. |
| **Task T-05**<br>*(Item B2)* | Added series damping resistor **`R58` ($100\ \Omega$, 0603)** between MCU `GPIO6` (`J1.6`) and modem reset pad `J4.8`. | Suppresses high-frequency ringing and prevents spurious cellular resets during high-current LTE bursts. |

* **Electrical Rules Check (ERC)**: Verified with `kicad-cli sch erc --severity-all` $\rightarrow$ **0 violations, 0 warnings** (ERC 100% clean).

---

### 4.2 Board Net, Copper & Footprint Reconciliation
All changes applied to [`pcb/MoriShield_Carrier.kicad_pcb`](file:///c:/Users/pradeesh/Music/morishield_frimware/New%20folder/new%20pcb/pcb/MoriShield_Carrier.kicad_pcb):

1. **Eliminated the $x = 264.75\text{ mm}$ Copper Barrier**:
   * Removed all 17 track segments of the redundant `/PWR_EN` copper branch starting from `U8.16` (`(255.0, 168.625)`) through to `(232.25, 140.25)`. Top-layer copper pours and ground return paths are now unchoked.
2. **Updated Pad Nets on ICs**:
   * `U8.16` $\rightarrow$ `unconnected-(U8-P13-Pad16)`
   * `U8.22` $\rightarrow$ `/I2C1_SCL`
   * `U8.23` $\rightarrow$ `/I2C1_SDA`
   * `J1.13` $\rightarrow$ `unconnected-(J1-IO3-Pad13)` (`GPIO3` isolated)
   * `J1.8` $\rightarrow$ `/EVENT_BTN` (`GPIO15` active input)
   * `J1.20` $\rightarrow$ `/I2C_SW_RST` (`GPIO14` active output)
3. **Clean Footprint Integration of `R58`**:
   * Added physical SMD footprint for **`R58`** ($100\ \Omega$) at `(260.00, 131.34)` on `F.Cu`.
   * Wired Pad 1 to `/MODEM_RST` and Pad 2 to `Net-(J4-RESET)` on `J4.8`.
4. **Orthogonal Rerouting of `/EVENT_BTN` to `J1.8`**:
   * Rerouted `/EVENT_BTN` using a clean 3-segment orthogonal trace along the open west corridor: `(183.48, 97.50)` $\rightarrow$ `(206.50, 120.52)` $\rightarrow$ `(206.50, 136.22)` $\rightarrow$ `(209.50, 136.22)`.
   * **Result**: Zero track crossings, zero clearance violations against `/UART2_MOD_TX`.
5. **Board Attributes**:
   * `C29` marked as `Do Not Populate (DNP)` on the board.
   * **Schematic Parity Check**: **0 schematic parity mismatches** (100% agreement between schematic and board).

---

### 4.3 Documentation & Deliverables Centralized in [`c:\Users\pradeesh\Music\morishield_frimware\doc\`](file:///c:/Users/pradeesh/Music/morishield_frimware/doc)

All formal project documentation has been consolidated into the dedicated top-level directory:

| Document File | Purpose & Verification Scope | Gate Check / Item |
| :--- | :--- | :--- |
| [`MoriShield_Carrier_RevC_bom.csv`](file:///c:/Users/pradeesh/Music/morishield_frimware/doc/MoriShield_Carrier_RevC_bom.csv) | Full 75-component bill of materials with orderable MPNs, industrial dielectric specs ($X7R/X5R$), and $-40^\circ\text{C}$ to $+85^\circ\text{C}/+105^\circ\text{C}$ ratings. | **Check C6**<br>*(Task T-26)* |
| [`FMEA_RevC.md`](file:///c:/Users/pradeesh/Music/morishield_frimware/doc/FMEA_RevC.md) | 25-row comprehensive Hardware Failure Mode & Effects Analysis covering reversed polarity, over-voltage, bus shorting, and RF noise. | **Check C13**<br>*(Task T-43)* |
| [`BRINGUP_PLAN_RevC.md`](file:///c:/Users/pradeesh/Music/morishield_frimware/doc/BRINGUP_PLAN_RevC.md) | Numbered 7-stage assembly and electrical test procedure with safety limits, current thresholds, and stop criteria. | **Check C13**<br>*(Task T-41)* |
| [`PIN_MAP_RevC.md`](file:///c:/Users/pradeesh/Music/morishield_frimware/doc/PIN_MAP_RevC.md) | Formally signed GPIO pin allocation table and system reset truth table covering ESP32-S3, A7672S, TCA9535, and TCA9548A. | **Check C11**<br>*(Task T-22)* |
| [`CTO_CLARIFICATION_MESSAGE.md`](file:///c:/Users/pradeesh/Music/morishield_frimware/doc/CTO_CLARIFICATION_MESSAGE.md) | Formatted 9-point technical inquiry prepared for Dr. Shanmugakumar addressing open design selections. | Engineering Alignment |
| [`ResponseSheet_RevC.csv`](file:///c:/Users/pradeesh/Music/morishield_frimware/doc/ResponseSheet_RevC.csv) | Master 76-item response register with exact evidence file links for every CTO audit finding. | Release Gate 3 |
| [`vias_in_pads.txt`](file:///c:/Users/pradeesh/Music/morishield_frimware/doc/vias_in_pads.txt) | Coordinate audit identifying all 67 via-in-pad locations for PCB fabricator hole-plugging / capping instructions. | **Finding R4** |
| [`TASK_TRACKER.md`](file:///c:/Users/pradeesh/Music/morishield_frimware/doc/TASK_TRACKER.md) | Live register tracking the status of all 76 audit items and 13 release gates. | Audit Alignment |

---

### 4.4 Phase 1 Layout & Routing Closure (Completed 2026-11-13)

Phase 1 physical PCB layout and routing closure has been achieved with **clean DRC (0 violations, 0 unconnected, 0 parity issues)** on [`pcb/MoriShield_Carrier.kicad_pcb`](file:///c:/Users/pradeesh/Music/morishield_frimware/New%20folder/new%20pcb/pcb/MoriShield_Carrier.kicad_pcb):

1. **All 4 Unconnected Nets Fully Routed**:
   * **`/I2C_SW_RST`**: Routed from `J1.20` $(209.5, 105.74)$ along B.Cu to $(240.5, 174.5)$, transitioning with a single $0.6/0.3\text{ mm}$ via to F.Cu to connect to `U7.3` $(239.5, 173.0)$.
   * **`/I2C0_SCL`**: Fanout from `U7.22` $(243.0, 177.725)$ on F.Cu past the TSSOP footprint boundary to $(247.0, 178.97)$, via to B.Cu, and routed cleanly to the main clock trunk at $(234.0, 149.75)$.
   * **`/I2C1_SCL`**: Fanout from `U8.22` $(255.0, 164.725)$ on F.Cu past the TSSOP pad boundary ($x \ge 256.0\text{ mm}$), via to B.Cu, and routed through the dedicated south-east corridor to `J7.6` $(224.81, 166.00)$.
   * **`/I2C1_SDA`**: Fanout from `U8.23` $(255.0, 164.075)$ on F.Cu past $x = 256.0\text{ mm}$, turning to $(256.50, 162.75)$, and routed cleanly through outer layers to `J7.5` $(221.02, 167.25)$.
2. **Item R12 / Check C10 Closed (0 Signal Tracks on Internal Plane `In2.Cu`)**:
   * All **54 signal track segments** across all 6 nets (`/I2C0_MUX_SC0`, `/SENS_EN`, `3V3_C`, `/+5V_SENS`, `/LED_DRV1`, `/LED_DRV2`) have been completely relocated off internal power plane `In2.Cu` to outer signal layers `F.Cu` and `B.Cu`.
   * **`In2.Cu` Census**: **0.00 mm in 0 track segments** (100% plane integrity restored).
   * **`In1.Cu` Census**: **0.00 mm in 0 track segments** (100% ground reference plane integrity).
3. **Port Silkscreen Verification (Task T-57 / Check C12)**:
   * Verified all 29 text objects on `F.SilkS` (`Rev C`, `S/N` box, `MODEM THIS WAY UP`, `MoriShield Carrier`, all 11 sensor port labels J11..J26, and J6 pin orientation markers `M0`..`GND`).
4. **Comprehensive Rules & DRC Execution**:
   * DRC executed with `--refill-zones --schematic-parity --severity-all --all-track-errors`:
     * **DRC Violations**: **0**
     * **Unconnected Items**: **0**
     * **Schematic Parity Issues**: **0**
   * ERC executed with `kicad-cli sch erc --severity-all`:
     * **ERC Violations**: **0 errors, 0 warnings**

---

## 5. Current Verification Status & Next Steps

### 5.1 Verification Script Pass Summary
* **Schematic ERC**: **0 violations, 0 warnings**.
* **DRC Violations**: **0 violations**.
* **DRC Unconnected Items**: **0 unconnected items**.
* **Schematic Parity**: **0 mismatches** (`kicad-cli pcb drc`).
* **In2.Cu Signal Tracks**: **0 track segments** (Item R12 closed).
* **Traceability (`trace2.py`)**: **0 status disagreements** across all 76 register rows.
* **Gate Truth (`gate_truth.py`)**: 13 release gate statuses accurately counted and verified.
* **Compliance (`final_verify.py`)**: Document integrity confirmed, zero banned vocabulary occurrences.

### 5.2 Next Engineering Milestones (Phase 2 & Phase 3)
1. **Power Stage Bulk Decoupling & Protection Circuit (Check C7 / Check C8 / Task T-19 / Task T-53)**:
   * Position $470\ \mu\text{F}$ low-ESR bulk capacitance within $10\text{ mm}$ of modem connector `J5`.
   * Finalize the over-voltage / reverse-polarity input protection circuit at `U10`/`J18`.
2. **Decoupling Capacitors Placement (Task T-59 / Check C9)**:
   * Coordinate placement of the 13 legal decoupling capacitor sites (C52–C64) between schematic and layout.
3. **Gerber, Drill & Fabrication Package Build (Release Gate S4 / Check C3 / Check C4)**:
   * Refill all copper zones $\rightarrow$ run final verification DRC $\rightarrow$ export Gerbers and drill files $\rightarrow$ execute release packaging (`pack.ps1`).

