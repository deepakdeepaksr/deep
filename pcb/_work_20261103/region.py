"""Dump every pad and copper item in a rectangle with exact numbers."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(HERE, "geom.json"), encoding="utf-8"))
x0, y0, x1, y1 = (float(a) for a in sys.argv[1:5])


def inter(b):
    return not (b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1)


print("== pads")
for f in sorted(g["footprints"], key=lambda f: f["ref"]):
    for p in f["pads"]:
        if inter(p["bbox"]):
            print("  %-5s.%-2s %-14s (%7.3f,%7.3f) %.2fx%.2f drill %.2f bbox [%.2f,%.2f,%.2f,%.2f]" %
                  (f["ref"], p["num"], p["net"][:14], p["x"], p["y"], p["w"], p["h"], p["drill"],
                   p["bbox"][0], p["bbox"][1], p["bbox"][2], p["bbox"][3]))
print("== copper")
for c in g["copper"]:
    if c["kind"] == "seg":
        b = [min(c["x0"], c["x1"]), min(c["y0"], c["y1"]), max(c["x0"], c["x1"]), max(c["y0"], c["y1"])]
        if inter(b):
            print("  %-6s %-15s (%7.3f,%7.3f)-(%7.3f,%7.3f) w%.2f %s" %
                  (c["layer"], c["net"][:15], c["x0"], c["y0"], c["x1"], c["y1"], c["width"], c["uuid"][:8]))
    else:
        b = [c["x"] - c["size"] / 2, c["y"] - c["size"] / 2, c["x"] + c["size"] / 2, c["y"] + c["size"] / 2]
        if inter(b):
            print("  VIA    %-15s (%7.3f,%7.3f) d%.2f drill %.2f %s" %
                  (c["net"][:15], c["x"], c["y"], c["size"], c["drill"], c["uuid"][:8]))
