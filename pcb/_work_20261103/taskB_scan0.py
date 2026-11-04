"""TASK B: legal J5 positions, rot 0 only (the library footprint cannot be rotated
without a lib_footprint_mismatch), ranked by distance to the modem's power edge."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

J5_PADS = [(0.0, 0.0, 2.8, 2.8, 1.3, "1", "+5V"),
           (0.0, 5.0, 2.8, 2.8, 1.3, "2", "GND")]
J5_COURT = (-4.355, -3.545, 4.545, 8.045)
MODEM = clear.OUTLINES["MODEM"]
TARGET = (240.0, 90.45)   # modem J1, "Top 2-Pin JST" per the A7672S guide


def j5(origin):
    s = clear.score(origin, 0.0, J5_PADS, J5_COURT, skip_ref="J5")
    c = s["court"]
    dx = max(MODEM[0] - c[2], c[0] - MODEM[2], 0.0)
    dy = max(MODEM[1] - c[3], c[1] - MODEM[3], 0.0)
    s["lead"] = (dx * dx + dy * dy) ** 0.5
    s["dist"] = math.hypot((c[0] + c[2]) / 2 - TARGET[0], (c[1] + c[3]) / 2 - TARGET[1])
    s["ok"] = s["legal"] and s["lead"] > 0.0
    return s


rows = []
y = 88.0
while y <= 200.0:
    x = 128.0
    while x <= 300.0:
        s = j5((round(x, 1), round(y, 1)))
        if s["ok"]:
            rows.append(s)
        x += 0.5
    y += 0.5

print("legal rot-0 candidates outside the modem: %d" % len(rows))
rows.sort(key=lambda s: s["dist"])
print("%-8s %-8s %-8s %-8s %-8s %-8s %-8s %s" %
      ("x", "y", "dist", "lead", "margin", "hole", "edge", "near"))
for s in rows[:25]:
    print("%-8.1f %-8.1f %-8.1f %-8.2f %-8.3f %-8.2f %-8.2f %s %s" %
          (s["origin"][0], s["origin"][1], s["dist"], s["lead"], s["margin"],
           s["hole_margin"], s["edge"], ",".join(s["fp_near"]) or "-",
           (s["item"] or "-")[:40]))
