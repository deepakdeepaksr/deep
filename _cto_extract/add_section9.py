import io, subprocess

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\PROJECT_CONTEXT_RevC.md'
t = io.open(p, encoding='utf-8').read()

t = t.replace(
 '| **Verification note** | §3 and §4 were verified 2026-11-02. **Read §8 first** - it carries the '
 '2026-11-02 late-session deltas and supersedes parts of §3, §4 and §7 |',
 '| **Verification note** | **Read §9 first, then §8.** Both supersede parts of §3, §4 and §7. '
 'Last verified 2026-11-03 by an independent tool run |')

t += """

---

## 9. Session 2026-11-03 - what landed, and the two regressions it caused

### 9.1 Board work completed (all verified by re-running the tools)

| Change | Result |
|---|---|
| **J26** (the AS5600 wind-vane port) moved out from under the RTC | 347 bottom-row positions measured, **0 legal** - courtyards leave 6.6-7.8 mm for a 13.49 mm part. Left-edge rot-90: 0 legal. Left-edge rot-0: **20 legal**. Placed at **(134.00, 153.50)**, 61.4 mm reroute, 1.175 mm margin |
| **J5** (modem 5 V terminal) moved out from under the modem | 904 legal positions; placed at **(222.00, 91.40)**, 1.91 mm outside the outline. Rotation rejected - it raises `lib_footprint_mismatch` |
| **Decoupling**: three capacitors relocated | C41 to Q9.3, C14 to D2.1, C33 to J13.1 |
| **Silkscreen**: 14 reference fields moved, 12 port labels + 8 J6 pin/orientation marks added | all at 1.0 mm / 0.15 mm stroke font, **DRC 0**, every one confirmed present in the plotted Gerber by stroke count |
| **Schematic Value fields** for 10 ports | parity stayed 0 - a property edit, not netlist surgery |
| **In2.Cu**: +5V moved to F.Cu | 63 to **61 segments**, 448.41 to **431.40 mm**, 8 to **7 nets**. Only +5V had a free corridor (+0.24 mm) |

### 9.2 Two regressions - found by re-measuring, not reported by the run

**These are the important part of this section.**

1. **E1 ground stitching has regressed and is no longer met.** Re-running
   `pcb\\_plot_stitching_final.py` gives **144 links, worst 11.16 mm, 0.1 % beyond 10 mm** -
   against the 143 / 10.00 mm / 0.0 % that every document still carried. The copper moves
   above broke it. **E1 is now recorded as `New` (regressed) in `TASK_TRACKER.md`, and
   `REPLY_TO_CTO.md` says so openly.** The cause is structural: the stitching metric is not
   a DRC check, so DRC 0 gives no warning. **Standing rule: re-run the stitching measurement
   after every copper or via change, before any document repeats a number.**
2. **Vias inside SMD pads went 65 to 67.** Two were introduced by the reroutes.
   `revC\\vias_in_pads.txt` and the fab note in `revC\\FAB_NOTES.md` still say 65 of 314, so
   **check C5's evidence quotes a number the board no longer matches.** Both files need
   regenerating. C5's *wording* is still satisfied (a fab note exists), but the count in it
   is wrong.

### 9.3 Verified state at the end of 2026-11-03

| Measure | Value |
|---|---|
| ERC | 0 violations, `ignored_checks []` |
| DRC | 0 violations, 0 unconnected, 0 parity, `ignored_checks []` |
| Census | 159 footprints / **1178** segments / **313** vias / 6 zones / 134 nets |
| Vias in SMD pads | **67** of 314 |
| E1 stitching | **11.16 mm worst, 0.1 % beyond 10 mm - FAILING** |
| Decoupling | 36 supply pins: **1 meets both, 3 meet local, 33 fail** |
| Under-module | modem: J3, J4 only. DS3231: 7 parts, J26 gone. GY-521: R31, R32. ESP32: J1, J2. E22: J6 |
| In2.Cu | 61 segments, 431.40 mm, 7 nets |
| Gate | **4 met** (C1, C2, C5, C12), 2 partly, 7 not met. **C9 and C10 not met** |
| Traceability | 76 / 76 / 76 ids, 0 disagreements, 0 priority mismatches |
| pack.ps1 | stops at GATE 5 PRODUCTION, no zip |

### 9.4 A methodology bug worth knowing about

The old decoupling map **counted 1 uF as "bulk" and parsed the string "100nF/16V" as
10 uF**. So the earlier published numbers (36 fail local, 31 fail bulk, worst 173.11 mm)
were partly wrong. The current map uses the CTO's verbatim thresholds and every row carries
a verdict. **Do not quote the pre-2026-11-03 decoupling figures anywhere.**

### 9.5 What is owed by whom, right now

**Aswin, in the KiCad GUI - nothing else can move these:**
- **T-55** the E22 M0/M1 0 ohm straps to GND (closes the microSD conflict, a P0)
- **T-56** the reed from GPIO41 to **GPIO39** at J2 pin 9
- **T-59** 13 decoupling pins that have a legal capacitor site but no movable donor -
  they need new parts added in the schematic; coordinates are in `TASK_TRACKER.md`
- ESP32 antenna **tab tip to nearest header pin**, in mm
- What **J17 and J20** are for (J20 blocks the LoRa keep-out)
- GY-521 and DS3231 **heights**

**Devin, board-only:**
- Fix E1: add stitching vias where the plane exceeds 10 mm, then re-measure
- Regenerate `revC\\vias_in_pads.txt` and the count in `revC\\FAB_NOTES.md` to 67
- The remaining 20 connector-class decoupling pins, board-only moves

**Serigreen:** questions 1, 2, 4, 6, 7 (now 67 vias), 8/8a, 8b to 8f in `REPLY_TO_CTO.md`.

### 9.6 Rollback for this session

`pcb\\_snap\\T_A_J26_*`, `T_B_J5_*`, `T_C_caps_*`, `T_D_silk_*`, `T_E_in2_*`.
Document backups before the 2026-11-03 corrections:
`_cto_extract\\TT.bak3`, `_cto_extract\\RT.bak3`.
"""

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('PROJECT_CONTEXT_RevC.md now', len(t.splitlines()), 'lines')

for s in (r'\pcb\_make_response_sheet.py', r'\_cto_extract\trace2.py', r'\_cto_extract\final_verify.py'):
    r = subprocess.run(['python', P + s], capture_output=True, text=True, cwd=P)
    keep = [l for l in (r.stdout or r.stderr).splitlines()
            if any(k in l for k in ('rows=', 'disagree', 'priority', 'prototype', 'Part 6', 'item rows'))]
    print(s, '->', ' | '.join(keep[:3])[:170])
