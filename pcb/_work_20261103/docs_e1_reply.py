"""Update the two E1 rows in REPLY_TO_CTO.md to the restored state."""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(ROOT, "REPLY_TO_CTO.md")
lines = io.open(path, encoding="utf-8").read().split("\n")

NEW = ('| E1 | **Restored on 2026-11-03, and the way it broke is recorded.** A GND pour was added on B.Cu with 85 '
       'stitching vias, which took the worst distance to 10.00 mm and 0.0 % beyond. The placement and reroute work '
       'then moved copper again and re-measurement gave **144 links, worst 11.16 mm, 0.1 % beyond 10 mm** - outside '
       'your 10 mm acceptance. The stitching metric is not a DRC check, so a clean DRC gave no warning. Two GND '
       'stitching vias (0.6/0.3 mm) at **(277.00, 90.00)** and **(164.00, 186.00)** returned it to **146 links, worst '
       '10.00 mm, 0.0 % beyond 10 mm**, plot regenerated. The measurement is now re-run after every copper or via '
       'change | `revC\\E1_stitching_plot.png` | Done |')

n = 0
for i, l in enumerate(lines):
    if l.startswith("| E1 |"):
        lines[i] = NEW
        n += 1
io.open(path, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("replaced %d E1 rows" % n)
