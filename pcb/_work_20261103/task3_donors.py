"""Compact: what is attached to each candidate donor capacitor's two pads."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(HERE, "geom.json"), encoding="utf-8"))

DONORS = ["C36", "C4", "C30", "C42", "C3", "C9", "C8", "C7", "C10"]
fps = {f["ref"]: f for f in g["footprints"]}
for ref in DONORS:
    f = fps[ref]
    print("%s (%7.2f,%7.2f) rot %.0f" % (ref, f["x"], f["y"], f["rot"]))
    for p in f["pads"]:
        hits = []
        for c in g["copper"]:
            if c["kind"] == "seg":
                for (ex, ey) in ((c["x0"], c["y0"]), (c["x1"], c["y1"])):
                    if math.hypot(ex - p["x"], ey - p["y"]) < 0.2:
                        hits.append("%s %s w%.2f" % (c["layer"], c["net"], c["width"]))
                        break
            else:
                if math.hypot(c["x"] - p["x"], c["y"] - p["y"]) < 0.2:
                    hits.append("VIA %s d%.2f" % (c["net"], c["size"]))
        print("   pad %s %-10s %-40s %s" % (p["num"], p["net"], " | ".join(hits) if hits else "-", ""))
