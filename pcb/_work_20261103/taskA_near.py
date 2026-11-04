"""TASK A: report the least-bad candidates and exactly what blocks them."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

def show(label, gen):
    rows = list(gen)
    rows.sort(key=lambda s: -min(s["margin"], 1.0))
    print("=== %s: %d candidates, best 18" % (label, len(rows)))
    for s in rows[:18]:
        print("  (%7.2f,%7.2f) rot %3.0f margin %7.3f hole %6.3f edge %5.2f out %-6s near %-14s %s" %
              (s["origin"][0], s["origin"][1], s["rot"], s["margin"], s["hole_margin"], s["edge"],
               ",".join(s["outlines"]) or "-", ",".join(s["fp_near"]) or "-", (s["item"] or "-")[:60]))

show("left edge rot90", (
    clear.j26((x / 2.0, y / 2.0), 90.0)
    for y in range(296, 403, 2) for x in range(256, 283, 2)))
show("bottom row y=194.5", (clear.j26((x / 2.0, 194.5)) for x in range(260, 607, 2)))
