"""TASK A.2: reroute length from each legal candidate to the nearest existing copper of
the same net (the four J26 stubs excluded, because they are what gets replaced)."""
import json
import math
import os
import sys

from shapely.geometry import Point

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

G = clear.G
STUB_IDS = {"9e33446e-adb8-4e74-bd8f-e9e082b0a09e", "00cbbea6-dd06-46ee-9685-2aa2abbd6f22",
            "e52d0386-b974-42da-a5b4-faa15ce2117e", "858dada0-c680-4d13-ae95-a980038c30c3"}

# same-net copper, excluding the J26 stubs and J26's own pads
BY_NET = {}
for o in clear.OBST:
    if o["id"] in STUB_IDS or o["id"].startswith("J26."):
        continue
    BY_NET.setdefault(o["net"], []).append(o)


def nearest(net, x, y):
    best = (9e9, None)
    p = Point(x, y)
    for o in BY_NET.get(net, []):
        d = p.distance(o["poly"])
        if d < best[0]:
            best = (d, o["label"])
    return best


def reroute(origin, rot=0.0):
    pads = clear.candidate_pads(origin, rot, clear.J26_PADS)
    total = 0.0
    detail = []
    for p in pads:
        d, lab = nearest(p["net"], p["x"], p["y"])
        total += d
        detail.append((p["net"], round(d, 2), lab))
    return total, detail


if __name__ == "__main__":
    cands = []
    for y10 in range(1500, 1601, 5):
        for x10 in range(1290, 1411, 5):
            s = clear.j26((x10 / 10.0, y10 / 10.0), 0.0)
            if s["legal"]:
                cands.append(s)
    for y10 in range(1985, 2006, 5):
        for x10 in range(2150, 2301, 5):
            s = clear.j26((x10 / 10.0, y10 / 10.0), 0.0)
            if s["legal"]:
                cands.append(s)
    print("%d legal candidates" % len(cands))
    out = []
    for s in cands:
        t, det = reroute(s["origin"], s["rot"])
        out.append((t, s, det))
    for t, s, det in sorted(out, key=lambda r: r[0])[:14]:
        print("(%.2f,%.2f) reroute %6.1f mm  margin %5.2f edge %.2f court %s" %
              (s["origin"][0], s["origin"][1], t, s["margin"], s["edge"],
               [round(v, 2) for v in s["court"]]))
        for d in det:
            print("     %-11s %6.2f mm to %s" % (d[0], d[1], d[2][:64]))
