"""TASK A: full bottom-band sweep (y 194.5 .. 203.0) and the left edge, legal counts."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

print("y      legal  best-margin  at x     blocker of the best")
for y10 in range(1945, 2035, 5):
    y = y10 / 10.0
    rows = []
    x = 130.0
    while x <= 303.0:
        rows.append(clear.j26((round(x, 2), y)))
        x += 0.5
    legal = [r for r in rows if r["legal"]]
    best = max(rows, key=lambda r: r["margin"])
    print("%-6.1f %-6d %-12.3f %-8.2f %s %s" %
          (y, len(legal), best["margin"], best["origin"][0],
           ",".join(best["outlines"]) or "-", (best["item"] or "-")[:60]))
    if legal:
        for r in sorted(legal, key=lambda r: -r["margin"])[:6]:
            print("    legal x %.2f margin %.3f hole %.3f edge %.3f %s" %
                  (r["origin"][0], r["margin"], r["hole_margin"], r["edge"], r["item"][:50]))
