"""Finish the repair-pass document edits: census, E1 in STAGE_TRACKER, findings 43-44, T-59 note."""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def replace_line(fname, startswith, new):
    path = os.path.join(ROOT, fname)
    lines = io.open(path, encoding="utf-8").read().split("\n")
    for i, l in enumerate(lines):
        if l.startswith(startswith):
            lines[i] = new
            io.open(path, "w", encoding="utf-8", newline="").write("\n".join(lines))
            print("replaced %s line %d" % (fname, i + 1))
            return
    print("MISS %s %r" % (fname, startswith))


replace_line("TASK_TRACKER.md", "| Census | 159 footprints",
             "| Census | 159 footprints \u00b7 1178 track segments \u00b7 **315 vias** \u00b7 **6 zones** \u00b7 134 net names "
             "(2026-11-03: J26 moved, J5 moved, 8 capacitor relocations, 2 +5V segments to F.Cu, 2 E1 stitching vias) | "
             "`pcb\\_census.ps1`, `pcbnew` |")

path = os.path.join(ROOT, "STAGE_TRACKER.md")
lines = io.open(path, encoding="utf-8").read().split("\n")
for i, l in enumerate(lines):
    if "GND plane distance to a ground link" in l:
        lines[i] = ("| GND plane distance to a ground link | max **10.00 mm**, **0.0 %** beyond 10 mm, **146 links** in "
                    "both pours (was 144 / 11.16 mm / 0.1 % after the 2026-11-03 moves; restored by two GND vias at "
                    "(277.00, 90.00) and (164.00, 186.00)) | `revC\\E1_stitching_plot.png` |")
        print("STAGE_TRACKER line %d replaced" % (i + 1))
        break
io.open(path, "w", encoding="utf-8", newline="").write("\n".join(lines))

FIND = """43. **The 3.3 V rail has no bulk capacitor at all, which is why no 3V3_C pin can pass C9.** Measured
    2026-11-03: every capacitor on 3V3_C is 100 nF (C4, C7, C8, C9, C10, C30, C36); the nearest 10 uF or
    larger on any other rail is C51 on /3V3_SENS_SW. Ten of the 36 supply pins are on 3V3_C, so ten of them
    can never meet "bulk 10 uF or more within 10 mm" by moving an existing part - a 10 uF has to be added.
    The same is true, one net at a time, for /3V3_SENS_SW: it has exactly one 10 uF (C51 at 186, 173), which
    already serves Q2.3 at 5.83 mm, so moving it to a port would trade one bulk pass for another.

44. **E1 was restored by two vias, not by a reroute.** The two over-10 mm clusters were x 276-279 / y 88-92
    (12 cells, worst 11.16 mm at (277, 90)) and one cell at (169, 180) at 10.07 mm. Both were the footprint
    of the 2026-11-03 work: the four +5V 100 nF capacitors left the top-right corner and took their GND vias
    with them, and the J26 reroute removed a GND link near (169, 180). Two 0.6/0.3 mm GND vias at (277, 90)
    and (164, 186) - both inside both pours - returned the metric to 146 links / 10.00 mm / 0.0 %.

"""
path = os.path.join(ROOT, "TASK_TRACKER.md")
text = io.open(path, encoding="utf-8").read()
marker = "## Part 7"
idx = text.find(marker)
if idx > 0 and "43. **The 3.3 V rail" not in text:
    text = text[:idx] + FIND + text[idx:]
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print("findings 43-44 inserted")
else:
    print("findings not inserted (marker or duplicate)")

# T-59 note: the bulk half
text = io.open(path, encoding="utf-8").read()
old = "| | **Also open** | 20 further pins have **no legal spot at all**"
new = ("| | **Bulk half** | for every 3V3_C pin the missing part is the **10 uF bulk**, not the 100 nF: the rail has "
       "none. For the /3V3_SENS_SW ports the 100 nF site is the blocker and C51 is the only 10 uF on the net. "
       "Both are recorded in `revC\\decoupling_map.csv` under `verdict_reason` | | | | |\n"
       "| | **Also open** | 20 further pins have **no legal spot at all**")
if old in text:
    text = text.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print("T-59 bulk note added")
else:
    print("T-59 note MISS")
