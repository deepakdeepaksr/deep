"""List the copper attached to each donor capacitor's pads."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(HERE, "geom.json"), encoding="utf-8"))

DONORS = ["C41", "C14", "C7", "C4", "C43", "C48", "C33", "C10", "C42", "C9", "C45", "C44", "C8", "C47", "C30"]

fps = {f["ref"]: f for f in g["footprints"]}
for ref in DONORS:
    f = fps[ref]
    print("%s at (%.2f,%.2f) rot %.0f  court %s" % (ref, f["x"], f["y"], f["rot"], [round(v, 2) for v in f["court"]]))
    for p in f["pads"]:
        print("   pad %s %-14s (%7.3f,%7.3f) %s" % (p["num"], p["net"], p["x"], p["y"], [round(v, 2) for v in p["bbox"]]))
        for c in g["copper"]:
            if c["kind"] == "seg":
                for (ex, ey) in ((c["x0"], c["y0"]), (c["x1"], c["y1"])):
                    if math.hypot(ex - p["x"], ey - p["y"]) < 1.3:
                        print("       SEG %-6s %-14s (%7.3f,%7.3f)-(%7.3f,%7.3f) w%.2f %s" %
                              (c["layer"], c["net"], c["x0"], c["y0"], c["x1"], c["y1"], c["width"], c["uuid"][:8]))
            else:
                if math.hypot(c["x"] - p["x"], c["y"] - p["y"]) < 1.3:
                    print("       VIA %-14s (%7.3f,%7.3f) d%.2f %s" % (c["net"], c["x"], c["y"], c["size"], c["uuid"][:8]))
