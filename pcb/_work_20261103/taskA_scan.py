"""TASK A: enumerate legal J26 positions along the bottom port row and the left edge."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

rows = []
x = 130.0
while x <= 303.0:
    s = clear.j26((round(x, 2), 194.5))
    rows.append(s)
    x += 0.5

legal = [r for r in rows if r["legal"]]
print("=== bottom row y=194.5: %d candidates, %d legal" % (len(rows), len(legal)))
print("%-8s %-8s %-8s %-9s %-7s %-6s %-26s %s" %
      ("x", "margin", "hole", "edge", "outline", "near", "worst item", "zone d"))
for r in rows:
    if r["legal"] or r["margin"] > -0.35:
        print("%-8.2f %-8.3f %-8.3f %-9.3f %-7s %-6s %-26s %.2f" %
              (r["origin"][0], r["margin"], r["hole_margin"], r["edge"],
               ",".join(r["outlines"]) or "-", ",".join(r["fp_near"]) or "-",
               (r["item"] or "-")[:26], r["zone_d"]))

print("\n=== contiguous legal x ranges at y=194.5")
runs = []
cur = None
for r in rows:
    if r["legal"]:
        if cur is None:
            cur = [r["origin"][0], r["origin"][0], r["margin"]]
        else:
            cur[1] = r["origin"][0]
            cur[2] = min(cur[2], r["margin"])
    else:
        if cur:
            runs.append(cur)
            cur = None
if cur:
    runs.append(cur)
for a in runs:
    print("  x %.2f .. %.2f  (width %.2f mm) worst margin %.3f" % (a[0], a[1], a[1] - a[0], a[2]))
