"""TASK A step A.3: enumerate legal J26 positions on the left edge (rot 90/270)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

for rot in (90.0, 270.0):
    print("=== left edge, rot %.0f" % rot)
    best = []
    y = 148.0
    while y <= 201.0:
        x = 128.0
        while x <= 141.0:
            s = clear.j26((round(x, 2), round(y, 2)), rot)
            if s["legal"]:
                best.append(s)
            x += 0.5
        y += 0.5
    print("legal candidates: %d" % len(best))
    for s in sorted(best, key=lambda s: -s["margin"])[:25]:
        print("  (%.2f,%.2f) margin %.3f hole %.3f edge %.3f worst %s" %
              (s["origin"][0], s["origin"][1], s["margin"], s["hole_margin"], s["edge"],
               (s["item"] or "-")[:52]))
