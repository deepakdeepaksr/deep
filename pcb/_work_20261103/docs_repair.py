"""Document pass for the 2026-11-03 repair session: measured numbers, E1, C9, C10."""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def replace_line(fname, startswith, newline_text):
    path = os.path.join(ROOT, fname)
    lines = io.open(path, encoding="utf-8").read().split("\n")
    hit = None
    for i, l in enumerate(lines):
        if l.startswith(startswith):
            hit = i
            break
    if hit is None:
        print("MISS %s: %r" % (fname, startswith))
        return
    lines[hit] = newline_text
    io.open(path, "w", encoding="utf-8", newline="").write("\n".join(lines))
    print("replaced %s line %d" % (fname, hit + 1))


def edit(fname, pairs):
    path = os.path.join(ROOT, fname)
    text = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in text:
            print("MISS %s: %r" % (fname, old[:60]))
            continue
        text = text.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print("edited", fname)


E1_ROW = ('| E1 | P1 | 004 T9 | "Stitching plot: no point of either ground pour more than 10 mm from a ground '
          'link (antenna keep-out excepted)." | **Done** | **Restored 2026-11-03.** The regression to 144 links / '
          '11.16 mm / 0.1 % was fixed by two GND stitching vias, 0.6/0.3 mm, at **(277.00, 90.00)** and '
          '**(164.00, 186.00)**; both sit inside both pours and connect In1 and B.Cu. Re-measured: **146 links, '
          'worst 10.00 mm, 0.0 % beyond 10 mm** on the 1 mm grid. Plot regenerated at '
          '`revC\\E1_stitching_plot.png`; DRC 0/0/0 after. Standing rule: re-run the metric after every copper or '
          'via change | `revC\\E1_stitching_plot.png`, `pcb\\_work_20261103\\T1_drc.json` | — |')

C9_ROW = ('| **C9** Placement | "The decoupling map shows every supply pin inside the distance; the 3D check '
          'shows every module on its right socket with the box closed; nothing reachable sits under a module." | '
          '**Partly** | Every row now carries a verdict (`verdict` column, no blanks): **3 MOVE, 13 ADD, 20 NONE** '
          'of 36 supply pins. Measured with the CTO\'s verbatim 100 nF / 10 uF thresholds: **1 meets both '
          '(J13.1), 3 meet local, 3 meet bulk, 33 fail local, 33 fail bulk.** The blocker is the bulk half: '
          '**3V3_C has no 10 uF capacitor anywhere on the rail** (10 of the 36 pins), and every other net has '
          'exactly one, on the far side of the board, so moving it would break another pin\'s bulk pass. '
          '**J5 is out from under the modem** (222.00, 91.40) and **J26 out from under the DS3231** (134.00, '
          '153.50). Under-module re-test: modem J3/J4 only, ESP32 J1/J2 only, GY-521 R31/R32, E22 J6 only, '
          'DS3231 seven passives (Q2, Q3, C26, C27, R20, R21, R26) | `revC\\decoupling_map.csv` |')

C10_ROW = ('| **C10** Layout | "The plane layers show nothing but their planes; the antenna rule area is in the '
           'file and empty on every layer; the spacing rules are met with the rule file matching the board; the '
           'power copper meets check C7; stitching is in." | **Not met** | **In2.Cu is down to 61 segments / '
           '431.40 mm / 7 nets** (was 63 / 448.41 / 8; +5V moved to F.Cu). Every remaining net has a negative '
           'outer corridor: /+5V_SENS -0.60, /SENS_EN -0.35, 3V3_C -0.35, /I2C0_SCL -0.30, /LED_DRV1 -0.30, '
           '/LED_DRV2 -0.30, /I2C0_MUX_SC0 -0.30 mm. **No antenna rule area in the file**: the E22 area '
           '(x 296.00-304.57, y 163.00-177.00) is still crossed by /3V3_SENS_SW and the CH3/CH6 runs; the ESP32 '
           'tab length and the modem U.FL position are still owed by Aswin. Spacing rules and `.kicad_dru` '
           'match; power copper 1.5 mm; **stitching now met** (E1) | `pcb\\_work_20261103\\taskE_in2.py` |')

replace_line("TASK_TRACKER.md", "| E1 | P1 |", E1_ROW)
replace_line("TASK_TRACKER.md", "| **C9** Placement |", C9_ROW)
replace_line("TASK_TRACKER.md", "| **C10** Layout |", C10_ROW)

edit("TASK_TRACKER.md", [
    ("| Vias inside SMD pads | **67 of 315**", "| Vias inside SMD pads | **67 of 315**"),
    ("| Census | 159 footprints \u00b7 1178 segments \u00b7 **313 vias** \u00b7 **6 zones** \u00b7 134 net names |",
     "| Census | 159 footprints \u00b7 1178 segments \u00b7 **315 vias** \u00b7 **6 zones** \u00b7 134 net names |"),
])

edit("STAGE_TRACKER.md", [
    ("| Census | **159 footprints \u00b7 1178 segments \u00b7 313 vias \u00b7 6 zones \u00b7 134 nets**",
     "| Census | **159 footprints \u00b7 1178 segments \u00b7 315 vias \u00b7 6 zones \u00b7 134 nets**"),
    ("| E1 ground stitching | **Met.** 143 links inside both pours, worst distance 10.00 mm, 0.0 % beyond 10 mm",
     "| E1 ground stitching | **Met, restored 2026-11-03.** 146 links inside both pours, worst distance 10.00 mm, 0.0 % beyond 10 mm"),
])
