"""TASK C.1: for every failing supply pin, search for a legal 0805 capacitor placement
inside the CTO's limit radius (3 mm at an IC pin, 5 mm elsewhere)."""
import csv
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

CAP_PADS = [(-1.0375, 0.0, 1.175, 1.45, 0.0, "1", "NET"),
            (1.0375, 0.0, 1.175, 1.45, 0.0, "2", "GND")]
CAP_COURT = (-1.925, -1.025, 1.925, 1.025)
ROOT = os.path.dirname(os.path.dirname(HERE))


def caps_for(net):
    pads = [(dx, dy, w, h, d, num, (net if num == "1" else "GND"))
            for (dx, dy, w, h, d, num, _) in CAP_PADS]
    return pads


def search(px, py, net, radius, step=0.25):
    best = None
    y = py - radius - 2.0
    while y <= py + radius + 2.0:
        x = px - radius - 2.0
        while x <= px + radius + 2.0:
            for rot in (0.0, 90.0):
                s = clear.score((round(x, 2), round(y, 2)), rot, caps_for(net), CAP_COURT,
                                skip_ref=None)
                if not s["legal"]:
                    continue
                # distance from the supply pad to the pin
                p1 = [p for p in clear.candidate_pads((x, y), rot, caps_for(net)) if p["num"] == "1"][0]
                d = math.hypot(p1["x"] - px, p1["y"] - py)
                if d > radius:
                    continue
                if best is None or d < best[0]:
                    best = (d, s, rot, p1)
            x += step
        y += step
    return best


rows = list(csv.DictReader(open(os.path.join(ROOT, "revC", "decoupling_map.csv"), encoding="utf-8")))
out = []
for r in rows:
    px, py = float(r["pin_x"]), float(r["pin_y"])
    limit = 3.0 if r["class"] == "IC" else 5.0
    b = search(px, py, r["net"], limit)
    if b is None:
        out.append((r["class"], r["load_ref"], r["load_pad"], r["net"], None))
        print("%-9s %-5s.%-3s %-13s NO SPOT within %.0f mm" % (r["class"], r["load_ref"], r["load_pad"], r["net"], limit))
    else:
        d, s, rot, p1 = b
        out.append((r["class"], r["load_ref"], r["load_pad"], r["net"], (d, s["origin"], rot, s["margin"])))
        print("%-9s %-5s.%-3s %-13s spot (%.2f,%.2f) rot %3.0f  pad1 %.2f mm  margin %.2f" %
              (r["class"], r["load_ref"], r["load_pad"], r["net"], s["origin"][0], s["origin"][1],
               rot, d, s["margin"]))

json.dump([[a, b, c, d, e] for (a, b, c, d, e) in out],
          open(os.path.join(HERE, "taskC_spots.json"), "w"), indent=1)
