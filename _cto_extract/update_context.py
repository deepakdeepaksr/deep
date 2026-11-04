import io

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\PROJECT_CONTEXT_RevC.md'
t = io.open(p, encoding='utf-8').read()

t = t.replace(
 '| **Verification note** | Every number in §3 and §4 below was reproduced by an independent tool '
 'run on 2026-11-02, not copied from a session report |',
 '| **Verification note** | §3 and §4 were verified 2026-11-02. **Read §8 first** - it carries the '
 '2026-11-02 late-session deltas and supersedes parts of §3, §4 and §7 |')

t += """

---

## 8. Deltas from 2026-11-02, late session - read this before §3, §4 and §7

Everything below was measured or read out of the files on 2026-11-02 and is current as of
23:55. Where it contradicts an earlier section, **this section wins**.

### 8.1 Verified state at the end of 2026-11-02

| Measure | Value | How it was checked |
|---|---|---|
| ERC | **0 violations, `ignored_checks []`** | own `kicad-cli` run |
| DRC | **0 violations, 0 unconnected, 0 parity, `ignored_checks []`** | own run with all four flags |
| Census | **159 footprints · 1171 segments · 314 vias · 6 zones · 134 net names** | own `pcbnew` count |
| Zones | PE on B.Cu · **GND on In1.Cu** · **GND on B.Cu** · /3V3_SENS_SW ×2 and +5V on In2.Cu | own run |
| E1 ground stitching | **Met.** 143 links inside both pours, worst distance 10.00 mm, 0.0 % beyond 10 mm | own re-run of `pcb\\_plot_stitching_final.py` |
| Vias inside SMD pads | **65** of 314, unchanged; IPC-4761 plug/fill/cap note present in `FAB_NOTES.md` | own geometric test |
| Release gate | **4 of 13 met** (C1, C2, C5, C12), 1 partly (C9), 8 not met | `STAGE_TRACKER.md` |
| Traceability | 76 ids in register, reply and CSV; **0 status disagreements, 0 priority mismatches** | `_cto_extract\\trace2.py` |
| `pack.ps1` | stops at **GATE 5 PRODUCTION** (no release Gerbers). Gates 1-4 pass | own run |
| Timestamps | board save 22:31:44 → DRC 22:45:13 → plot 22:45:15, the order C3 requires | `STAGE_TRACKER.md` |

### 8.2 The finding that reversed a day of work

**J6 is not mis-wired.** Read against the Ebyte E22-900T22D datasheet order
(1 M0, 2 M1, 3 RXD, 4 TXD, 5 AUX, 6 VCC, 7 GND) with the module inserted the obvious way, the
socket looked mirror-imaged - VCC on GPIO10, GND on GPIO11, 5 V on M1. **Inserted 180 degrees
the other way, all seven nets line up**, UART direction included, matching Aswin's working bench
wiring exactly. The net names themselves (`/E22_M0` on pad 7, `/E22_M1` on pad 6) prove the
designer intended it. Aswin then confirmed on the physical module: labels read M0, M1, RXD, TXD,
AUX, VCC, GND, and the GND pin is continuous with the SMA shell and the three mounting holes.

**What is actually wrong is that nothing marks or keys the orientation.** No silkscreen, footprint
pads named only 1 to 7, header unkeyed. Item A3's acceptance is "a reversed module cannot go in or
is obvious" - today it does neither. Devin also recorded the method lesson: a net rename kept
parity at 0 while breaking the copper, so **parity alone is not evidence**.

### 8.3 Measured pin facts (Aswin's multimeter, 2026-11-02)

| Fact | Result | Consequence |
|---|---|---|
| microSD slot | pin 2→**GPIO10**, 3→**GPIO11**, 5→**GPIO12**, 7→**GPIO13**, 4→3V3, 6→GND | CHK-001 C11 is **right about 10-13, wrong to include 14**. The card's CS and MOSI are being driven by `/E22_M1` and `/E22_M0` |
| GPIO9 | **not on the slot** | `/I2C0_SCL` on GPIO9 is **safe** - the whole I2C-0 bus (mux, expander, MPU, RTC) stands |
| GPIO35-38 | octal-PSRAM group on the N16R8 | unusable. **GPIO39 (J2.9) is the only free usable input** in that block - the reed's destination |
| Reed switch | `/REED_PULSE_F` → J2.7 = **GPIO41**, which C11 calls output-only | moves to J2.9 = GPIO39 (T-56) |
| Analog inputs | J15 soil → GPIO2 = **ADC1_CH1**; J16 → GPIO1 = **ADC1_CH0** | both on ADC1, which keeps working with Wi-Fi on. Luck, not a decision - recorded because it constrains future swaps |
| Capacitance sensor | **FDC1004 on J21 = I2C channel 5**, not on J15 | CH5 is not spare |
| J17 (CH4) and J20 (CH6) | fully wired ports, **no identified sensor anywhere** | J20 blocks the LoRa keep-out - question 8e |

### 8.4 Decisions taken, and the one still open

**Taken:** E22 M0 and M1 will be strapped to ground through **0 ohm 0603 resistors** (not dead
wire) so configuration mode stays reachable by lifting a strap with the module out of its socket.
This frees GPIO10/11 for the microSD. It was chosen over driving them from expander U8 because a
hard strap is deterministic at every power-up and does not put radio mode behind a muxed, cabled
I2C bus that item R17 already says is unreliable.

**Still open, and it changes parts:** whether Serigreen would rather have mode control from
firmware (expander pins) than a lift-a-strap service action - question 8c. Also the **E22 supply
rail**: the board feeds it 5 V, its TXD and AUX follow VCC, and the ESP32-S3 is not 5 V tolerant,
so we propose 3V3 (how it was bench-tested) - question 8d.

### 8.5 What is queued and not yet in the board

| Task | Change | Items |
|---|---|---|
| **T-55** | Strap E22 M0/M1 to GND through 0 ohm; delete `/E22_M0` and `/E22_M1`; J1.16/J1.17 become unconnected | A7, C2, C5, R11, C11 |
| **T-56** | Move `/REED_PULSE_F` from J2.7 (GPIO41) to J2.9 (GPIO39) | R11, C11 |
| **T-57** | Name every port in the schematic Value field **and print the names on F.SilkS**; mark J6 with pin functions and orientation | E5, C12, A3, C11 |
| **T-58** | Ask Serigreen to price a keyed or shrouded header at J6/J3/J4 | A3 |

**T-55 and T-56 are the highest-value remaining edits on the board** - they close the microSD
conflict, which is a P0 (A7, C2) and blocks the signed pin map (C11).

### 8.6 S3 status, corrected

| Check | State | Reason |
|---|---|---|
| C2 | **Met** | 0 unconnected, 0 parity, no dangling |
| C5 | **Met** on its own wording | mismatch 0, courtyard 0, silk 0, constraints met, 65 vias carry a fab note. Item R16 (agreement + price) stays open |
| C12 | **Met** | verified on the plotted Gerber, J18 marks 0.05 mm off pad centres, timestamps in order |
| C9 | **Partly - and harder than it looked** | **36 supply pins, 0 meeting the CTO's two-part rule** (21 connector, 6 MOSFET, 6 IC, 3 diode; 36 fail local 100 nF, 31 fail bulk). J5 sits under the modem outline; **J26, the AS5600 port added this revision, sits under the DS3231 outline** |
| C10 | **Not met** | 63 items on In2.Cu; no antenna rule area - the E22 zone is blocked by `/3V3_SENS_SW` and `/I2C0_SDA_CH3/CH6` in the same corridor; power copper 1.5 mm not the 3 mm pour of condition 3 |

**S3 is not reachable today.** C9 became a real layout problem (36 capacitor moves), and C10 needs
routing hours plus two answers. Deliverable now: **4 of 13 checks met, S3 partial with named
reasons.**

### 8.7 What is still owed by people, not by tools

| Who | Item |
|---|---|
| **Aswin** | ESP32 **antenna tip to nearest header pin**, in mm (fixes the outline and lets the keep-out be drawn) · what J17 and J20 are for · whether the ESP32 and modem antenna whips exit the lid (92 mm whip will not stand in an 80 mm box - two sealed SMA bulkheads proposed) · E22 physical pin-1 photo for the record |
| **Serigreen** | questions 1, 2, 4, 6, 7, 8/8a, 8b-8f in `REPLY_TO_CTO.md` |
| **Bench** | B1-B4, A1, A2, the B10 burst trace, the 24-hour run (C2), reed counts at 1/10/50 Hz (R11) |

### 8.8 Document state at handoff

| Document | Last written | Notes |
|---|---|---|
| `TASK_TRACKER.md` | 2026-11-02 23:55 | Part 6 renumbered **1-36 in file order, no duplicates**; rows A7, C2, C5, R11 rewritten with the measurements; T-55 to T-58 added |
| `REPLY_TO_CTO.md` | 2026-11-02 23:55 | questions 3 and 5 marked answered-by-us; **8b-8f added**; rows A7, C2, C5, E5, R11 rewritten |
| `STAGE_TRACKER.md` | 2026-11-02 23:55 | five new measured rows; E1 removed as an S3 blocker |
| `revC\\ResponseSheet_RevC.csv` | regenerated | 76 rows, generator reports 0 mismatches |
| `_cto_extract\\` | - | every verification script used here, plus timestamped `.bak-` copies of the three documents before this pass |

**Rollback:** `_cto_extract\\TASK_TRACKER.bak-*` and `_cto_extract\\REPLY_TO_CTO.bak-*` hold the
pre-edit versions of this pass. Board rollback: `pcb\\_snap\\T2_keepout_20261102_224411\\` and
`pcb\\_snap\\T4_geom_20261102_223102\\`.
"""

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('PROJECT_CONTEXT_RevC.md updated, lines', len(t.split('\n')))
