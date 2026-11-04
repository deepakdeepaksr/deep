import re
ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
ST = ROOT + r"\STAGE_TRACKER.md"
EV = ROOT + r"\revC\EVIDENCE_RevC.md"

t = open(TT, encoding="utf-8").read()
lines = t.split("\n")
for i, line in enumerate(lines):
    if line.startswith("| **C9** Placement |"):
        lines[i] = ('| **C9** Placement | "The decoupling map shows every supply pin inside the distance; the 3D check '
          'shows every module on its right socket with the box closed; nothing reachable sits under a module." | **Partly** | '
          'The map now tests **both** CTO requirements per pin (`local_100nf_mm`/`local_limit_mm`/`local_meets` and '
          '`bulk_mm`/`bulk_meets`) with every row classified and no blank verdicts: **36 supply pins - 21 connector, 6 MOSFET, '
          '6 IC, 3 diode - 0 meet both, 36 fail the local 100 nF rule, 31 fail the bulk rule.** Worst local J25.1 at 173.11 mm; '
          'worst bulk J20.1 at 118.51 mm. Module outlines corrected; enclosure and two SMA bulkheads drawn; **modules and box '
          'still absent from the 3D view** (no 3D models). Accessibility: **J5 sits under the modem outline** and **J26 under '
          'the DS3231 outline** | `revC\\decoupling_map.csv` |')
    if line.startswith("| **C10** Layout |"):
        lines[i] = ('| **C10** Layout | "The plane layers show nothing but their planes; the antenna rule area is in the file '
          'and empty on every layer; the spacing rules are met with the rule file matching the board; the power copper meets '
          'check C7; stitching is in." | **Not met** | 63 items still on In2 (R12); **no antenna rule area in the file** - the '
          'E22 area cannot be cleared: the /3V3_SENS_SW B.Cu run at x 298.75 was dogtailed to x 293.0 on 2026-11-02 and produced '
          '**5 DRC items** (3 `tracks_crossing`, `shorting_items` with /I2C0_SDA_CH3 and /I2C0_SDA_CH6), so it was restored; the '
          'modem U.FL and ESP32 antenna ends are still unidentified; spacing rules and `.kicad_dru` match; power copper 1.5 mm; '
          'stitching in | `revC\\_work\\_s2_drc.json` |')
open(TT, "w", encoding="utf-8", newline="").write("\n".join(lines))

t = open(TT, encoding="utf-8").read()
add = """
25. **The J6 pin-1 confirmation does not exist in the workspace - 2026-11-02.** The run was gated on Aswin confirming that
    the E22 module's physical pin-1 mark matches the datasheet (pin 1 = M0). A search of every document, register and note
    modified in the last 24 hours found no such record. **The J6 correction was therefore not attempted**, and the socket
    remains in mirror image. This is a blocked gate, not a design decision.

26. **The E22 keep-out needs more than one track move - measured 2026-11-02.** The `/3V3_SENS_SW` B.Cu run at x 298.75
    (37.05 mm) was dogtailed to x 293.0 with the via at (298.75, 147.50) kept as the tap. DRC returned **5 items**: three
    `tracks_crossing` and `shorting_items` against `/I2C0_SDA_CH3` and `/I2C0_SDA_CH6`, which occupy that B.Cu corridor.
    Restored. Clearing the area needs those two runs moved as well.

27. **The decoupling map was measuring one requirement, not two.** CHK C9 asks for a 100 nF within 5 mm (3 mm at an IC pin)
    **and** bulk of 10 uF or more within 10 mm. The old map tested only "nearest capacitor of any value", which is why its
    count read 27. Rebuilt with both tests and a class per row: **36 supply pins, 0 meet both, 36 fail local, 31 fail bulk.**
"""
t = t.replace("\n---\n\n## Part 7", add + "\n---\n\n## Part 7")
open(TT, "w", encoding="utf-8", newline="").write(t)

s = open(ST, encoding="utf-8").read()
s = s.replace("| Decoupling verdict | 27 supply pins tested, **0 meet**, 27 fail | `revC\\decoupling_map.csv` |",
              "| Decoupling verdict | **36 supply pins (21 connector, 6 MOSFET, 6 IC, 3 diode): 0 meet both, 36 fail local 100 nF, 31 fail bulk** | `revC\\decoupling_map.csv` |")
s = s.replace("| Silk verification plot | 12,128 strokes; J18 marks Δ0.05 mm; name/Rev/S-N present | `revC\\silk_check\\` |",
              "| Silk verification plot | 12,128 strokes; J18 marks Δ0.05 mm; name/Rev/S-N present. Save 22:31:44, DRC 22:45:13, plot 22:45:15 | `revC\\silk_check\\` |")
open(ST, "w", encoding="utf-8", newline="").write(s)

e = open(EV, encoding="utf-8").read()
e += """
## 9. C3 timestamp record, 2026-11-02

| Event | Time |
|---|---|
| Board saved | 2026-11-02 22:31:44 |
| DRC on the saved file | 2026-11-02 22:45:13 |
| Gerber + drill plot into `revC\\silk_check\\` | 2026-11-02 22:45:15 |

The order save -> DRC -> plot is correct. J18 marks on this plot: `+` centre y 107.20 against pad 1 at 107.25
(**Delta 0.05 mm**), `-` centre y 102.20 against pad 2 at 102.25 (**Delta 0.05 mm**), both 6.3 mm beside their pads.
"""
open(EV, "w", encoding="utf-8", newline="").write(e)
print("docs updated")
