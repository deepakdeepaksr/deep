"""Append the Task C ADD table to revC\\FAB_NOTES.md."""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(ROOT, "revC", "FAB_NOTES.md")

SECTION = """
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
report and in `pcb\\_work_20261103\\taskC_spots.json`.

Two notes for whoever places these:
- the five rot-90 rows need a **rotated 0805**. Rotating an existing footprint on the board raises
  `lib_footprint_mismatch`, so add these as new parts rather than turning a placed one;
- every coordinate above is a legal bare-footprint position measured against tracks, vias, pads, courtyards and
  the module outlines. The connecting track and the GND via still have to be routed.
"""

text = io.open(path, encoding="utf-8").read()
io.open(path, "w", encoding="utf-8", newline="").write(text.rstrip() + "\n" + SECTION)
print("FAB_NOTES updated")
