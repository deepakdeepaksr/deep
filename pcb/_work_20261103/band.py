"""List footprints and copper density in a rectangle (default the bottom band)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(HERE, "geom.json"), encoding="utf-8"))

x0, y0, x1, y1 = (float(a) for a in sys.argv[1:5]) if len(sys.argv) >= 5 else (126.0, 185.0, 305.0, 206.0)


def inter(b):
    return not (b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1)


print("== footprints intersecting (%.1f,%.1f)-(%.1f,%.1f)" % (x0, y0, x1, y1))
for f in sorted(g["footprints"], key=lambda f: f["x"]):
    if inter(f["bbox"]):
        print("  %-5s %-16s (%8.3f,%8.3f) bbox %s" % (f["ref"], f["value"][:16], f["x"], f["y"],
                                                      [round(v, 2) for v in f["bbox"]]))

print("== copper segments/vias intersecting")
for c in g["copper"]:
    if c["kind"] == "seg":
        bx = [min(c["x0"], c["x1"]), min(c["y0"], c["y1"]), max(c["x0"], c["x1"]), max(c["y0"], c["y1"])]
        if not inter(bx):
            continue
        print("  SEG %-10s %-16s (%7.2f,%7.2f)-(%7.2f,%7.2f) w %.2f %s" %
              (c["layer"], c["net"][:16], c["x0"], c["y0"], c["x1"], c["y1"], c["width"], c["uuid"][:8]))
    else:
        bx = [c["x"] - c["size"] / 2, c["y"] - c["size"] / 2, c["x"] + c["size"] / 2, c["y"] + c["size"] / 2]
        if not inter(bx):
            continue
        print("  VIA %-16s (%7.2f,%7.2f) d %.2f drill %.2f %s" %
              (c["net"][:16], c["x"], c["y"], c["size"], c["drill"], c["uuid"][:8]))
