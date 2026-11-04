"""TASK 3: classify every decoupling row MOVE / ADD / NONE and add the verdict column.

MOVE = an existing capacitor can be relocated so the pin meets BOTH requirements, board-only.
ADD  = a legal site exists but a NEW part is needed (no movable capacitor can satisfy both).
NONE = no legal site at all inside the CTO's radius.
"""
import csv
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402
import taskC_spots as t  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
MAP = os.path.join(ROOT, "revC", "decoupling_map.csv")

# pins whose only legal site is at rot 90 (a new part; a rotated placed part raises
# lib_footprint_mismatch) or which need a bulk capacitor that does not exist on the net
ADD = {
    "J1.1": "3V3_C has no 10 uF capacitor at all; 100 nF site at (210.50,157.75) rot 0",
    "J4.3": "3V3_C has no 10 uF; 100 nF site at (273.50,117.39) rot 0",
    "J7.2": "3V3_C has no 10 uF; 100 nF site at (215.65,163.00) rot 0",
    "J7.8": "3V3_C has no 10 uF; 100 nF site at (229.14,169.00) rot 0",
    "J8.5": "3V3_C has no 10 uF; 100 nF site at (166.06,157.25) rot 90 only",
    "J26.1": "3V3_C has no 10 uF; 100 nF site at (129.75,152.50) rot 90 only",
    "J11.1": "bulk C51 is 23.1 mm and the only 10 uF on the net (moving it breaks Q2.3); 100 nF site rot 90 only",
    "J12.1": "bulk C51 is 22.8 mm and unique on the net; 100 nF site rot 90 only",
    "J15.1": "bulk C51 is 40.3 mm and unique on the net; 100 nF site rot 90 only",
    "J16.1": "bulk C51 is 29.7 mm and unique on the net; 100 nF site rot 90 only",
    "J17.1": "bulk C51 is 89.2 mm and unique on the net; 100 nF site rot 90 only",
    "J24.1": "bulk C13 could move within 10 mm, but the 100 nF site at (138.97,147.25) cannot be reached: the track crosses /LED1_K (132.975,144.75)-(136.705,148.48)",
    "D7.1": "/+5V_ESP has no 100 nF at all (C28 is 10 uF); 100 nF site at (215.60,97.50) rot 90 only",
}
MOVE_DONE = {"Q9.3": "C41 relocated to (162.06,106.75), 2.75 mm",
             "D2.1": "C14 relocated to (169.10,108.50), 4.50 mm",
             "J13.1": "C33 relocated to (237.00,198.50), 4.00 mm"}


def key(r):
    return "%s.%s" % (r["load_ref"], r["load_pad"])


def nearest_blockers(px, py, net, n=3):
    out = []
    for o in clear.OBST:
        if o["net"] == net:
            continue
        d = math.hypot(o["poly"].centroid.x - px, o["poly"].centroid.y - py)
        out.append((d, o["label"]))
    out.sort(key=lambda x: x[0])
    return out[:n]


rows = list(csv.DictReader(open(MAP, encoding="utf-8")))
for r in rows:
    k = key(r)
    if k in MOVE_DONE:
        r["verdict"] = "MOVE"
        r["verdict_reason"] = MOVE_DONE[k]
    elif k in ADD:
        r["verdict"] = "ADD"
        r["verdict_reason"] = ADD[k]
    elif r["local_meets"] == "yes" and r["bulk_meets"] == "yes":
        r["verdict"] = "MOVE"
        r["verdict_reason"] = "already meets both"
    else:
        r["verdict"] = "NONE"
        bl = nearest_blockers(float(r["pin_x"]), float(r["pin_y"]), r["net"])
        r["verdict_reason"] = "no legal site within %s mm; nearest copper: %s" % (
            r["local_limit_mm"], "; ".join("%s at %.1f mm" % (lab.split(" ")[0] + " " + lab.split(" ")[1], d)
                                           for (d, lab) in bl))

cols = list(rows[0].keys())
with open(MAP, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

import collections
by = collections.defaultdict(lambda: collections.Counter())
for r in rows:
    by[r["class"]][r["verdict"]] += 1
print("rows %d" % len(rows))
for c in sorted(by):
    print("  %-10s %s" % (c, dict(by[c])))
print("total", dict(collections.Counter(r["verdict"] for r in rows)))
print("blank verdicts:", sum(1 for r in rows if not r["verdict"]))
print("\nNONE rows and their blockers:")
for r in rows:
    if r["verdict"] == "NONE":
        print("  %-6s %-13s %s" % (key(r), r["net"], r["verdict_reason"][:150]))
