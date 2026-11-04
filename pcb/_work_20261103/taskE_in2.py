"""TASK E.1: measure the In2.Cu copper by net, and the outer-layer corridor for each."""
import collections
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))

by = collections.defaultdict(list)
for t in b.GetTracks():
    if t.Type() != pcbnew.PCB_TRACE_T:
        continue
    if b.GetLayerName(t.GetLayer()) != "In2.Cu":
        continue
    p0, p1 = t.GetStart(), t.GetEnd()
    by[t.GetNetname()].append((p0.x / 1e6, p0.y / 1e6, p1.x / 1e6, p1.y / 1e6, t.GetWidth() / 1e6))

total = sum(math.hypot(c[2] - c[0], c[3] - c[1]) for v in by.values() for c in v)
n = sum(len(v) for v in by.values())
print("In2.Cu: %d segments, %.2f mm, %d nets" % (n, total, len(by)))
for net, items in sorted(by.items(), key=lambda kv: -sum(math.hypot(c[2] - c[0], c[3] - c[1]) for c in kv[1])):
    L = sum(math.hypot(c[2] - c[0], c[3] - c[1]) for c in items)
    xs = [c[0] for c in items] + [c[2] for c in items]
    ys = [c[1] for c in items] + [c[3] for c in items]
    w = sorted({round(c[4], 2) for c in items})
    print("  %-16s %2d seg %7.2f mm  x %.1f-%.1f  y %.1f-%.1f  widths %s" %
          (net, len(items), L, min(xs), max(xs), min(ys), max(ys), w))
