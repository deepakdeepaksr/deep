"""TASK A: left edge with a horizontal J26 (rot 0), and the bottom second-row candidates."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

print("=== left edge rot 0 (horizontal), x 129..141, y 150..200")
rows = []
for y10 in range(1500, 2001, 5):
    for x10 in range(1290, 1411, 5):
        rows.append(clear.j26((x10 / 10.0, y10 / 10.0), 0.0))
legal = [r for r in rows if r["legal"]]
print("legal: %d of %d" % (len(legal), len(rows)))
for r in sorted(legal, key=lambda r: -r["margin"])[:15]:
    print("  (%.2f,%.2f) margin %.3f hole %.3f edge %.3f near %s %s" %
          (r["origin"][0], r["origin"][1], r["margin"], r["hole_margin"], r["edge"],
           ",".join(r["fp_near"]) or "-", (r["item"] or "-")[:55]))

print("\n=== bottom second row, every legal candidate y 198.5..200.5")
rows = []
for y10 in range(1985, 2006, 5):
    for x10 in range(2050, 2301, 5):
        rows.append(clear.j26((x10 / 10.0, y10 / 10.0), 0.0))
legal = [r for r in rows if r["legal"]]
print("legal: %d of %d" % (len(legal), len(rows)))
for r in sorted(legal, key=lambda r: -r["margin"])[:20]:
    print("  (%.2f,%.2f) margin %.3f hole %.3f edge %.3f near %s %s" %
          (r["origin"][0], r["origin"][1], r["margin"], r["hole_margin"], r["edge"],
           ",".join(r["fp_near"]) or "-", (r["item"] or "-")[:55]))
