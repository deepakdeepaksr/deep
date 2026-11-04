"""TASK 3: for the failing connector pins, re-confirm the rot-0 spots and inspect donors."""
import csv
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402
import taskC_spots as t  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
rows = list(csv.DictReader(open(os.path.join(ROOT, "revC", "decoupling_map.csv"), encoding="utf-8")))
CONN = [r for r in rows if r["class"] == "connector" and not (r["local_meets"] == "yes" and r["bulk_meets"] == "yes")]
print("failing connector pins: %d" % len(CONN))

fps = {f["ref"]: f for f in clear.G["footprints"]}


def caps_on(net):
    out = []
    for f in clear.G["footprints"]:
        if not f["ref"].startswith("C"):
            continue
        if not any(p["net"] == net for p in f["pads"]):
            continue
        val = f["value"].upper()
        if "NF" in val:
            out.append(f["ref"])
    return out


for r in CONN:
    px, py, net = float(r["pin_x"]), float(r["pin_y"]), r["net"]
    best = None
    y = py - 7.0
    while y <= py + 7.0:
        x = px - 7.0
        while x <= px + 7.0:
            s = clear.score((round(x, 2), round(y, 2)), 0.0, t.caps_for(net), t.CAP_COURT, skip_ref=None)
            if s["legal"]:
                p1 = [p for p in clear.candidate_pads((x, y), 0.0, t.caps_for(net)) if p["num"] == "1"][0]
                d = math.hypot(p1["x"] - px, p1["y"] - py)
                if d <= 5.0 and (best is None or d < best[0]):
                    best = (d, (round(x, 2), round(y, 2)), s["margin"], p1)
            x += 0.25
        y += 0.25
    donors = caps_on(net)
    if best:
        print("%-5s.%-3s %-13s SPOT (%6.2f,%6.2f) pad1 %4.2f margin %5.2f  donors %s" %
              (r["load_ref"], r["load_pad"], net, best[1][0], best[1][1], best[0], best[2], donors))
    else:
        print("%-5s.%-3s %-13s NO rot-0 SPOT within 5 mm                     donors %s" %
              (r["load_ref"], r["load_pad"], net, donors))
