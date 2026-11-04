"""Find legal positions for new GND stitching vias near the two failing clusters."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

VIA = [(0.0, 0.0, 0.6, 0.6, 0.3, "1", "GND")]
COURT = (-0.3, -0.3, 0.3, 0.3)


def scan(cx, cy, half, step=0.25):
    out = []
    y = cy - half
    while y <= cy + half:
        x = cx - half
        while x <= cx + half:
            s = clear.score((round(x, 2), round(y, 2)), 0.0, VIA, COURT, skip_ref=None)
            if s["legal"] and s["margin"] > 0.05:
                out.append((round(x, 2), round(y, 2), s["margin"], s["hole_margin"], s["edge"]))
            x += step
        y += step
    return out


for (cx, cy, label) in ((277.5, 90.0, "top-right cluster"), (169.0, 180.0, "R11/D6 cell")):
    rows = scan(cx, cy, 7.0)
    rows.sort(key=lambda r: -(r[2]))
    print("== %s: %d legal spots" % (label, len(rows)))
    for r in rows[:12]:
        print("   (%7.2f,%7.2f) margin %.2f hole %.2f edge %.2f" % r)
