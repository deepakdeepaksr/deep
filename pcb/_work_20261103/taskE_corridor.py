"""TASK E.1: outer-layer corridor for each In2.Cu net, measured from the board file."""
import collections
import json
import math
import os
import sys

from shapely.geometry import LineString

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

LAYERS = ["F.Cu", "B.Cu"]
segs = collections.defaultdict(list)
for c in clear.G["copper"]:
    if c["kind"] == "seg" and c["layer"] == "In2.Cu":
        segs[c["net"]].append(c)

for net, items in sorted(segs.items()):
    out = {}
    for layer in LAYERS:
        worst = (9e9, None)
        for c in items:
            ls = LineString([(c["x0"], c["y0"]), (c["x1"], c["y1"])])
            length = ls.length
            steps = max(2, int(length / 0.5))
            for i in range(steps + 1):
                p = ls.interpolate(i / steps, normalized=True)
                # nearest other-net copper on this layer, as a distance from the point
                best = 9e9
                lab = None
                for o in clear.OBST:
                    if o["net"] == net or layer not in o["layers"]:
                        continue
                    if o["poly"].distance(p) < best:
                        best = o["poly"].distance(p)
                        lab = o["label"]
                need = clear.clearance_for(net, "GND")
                corridor = best - c["width"] / 2 - 0.2
                if corridor < worst[0]:
                    worst = (corridor, lab)
        out[layer] = worst
    print("%-16s F.Cu corridor %7.2f (%s)" % (net, out["F.Cu"][0], (out["F.Cu"][1] or "-")[:44]))
    print("%-16s B.Cu corridor %7.2f (%s)" % ("", out["B.Cu"][0], (out["B.Cu"][1] or "-")[:44]))
