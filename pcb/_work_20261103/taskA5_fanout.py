"""TASK A.5: print every copper endpoint near J26's pads and whether it lands inside the pad."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(HERE, "geom.json"), encoding="utf-8"))

j26 = [f for f in g["footprints"] if f["ref"] == "J26"][0]
pads = {p["num"]: p for p in j26["pads"]}
print("J26 pads:")
for p in j26["pads"]:
    print("  pad %s net %-12s centre (%7.3f,%7.3f) size %.2fx%.2f drill %.2f" %
          (p["num"], p["net"], p["x"], p["y"], p["w"], p["h"], p["drill"]))

print("\nsegment endpoints within 2.0 mm of a J26 pad centre:")
for c in g["copper"]:
    if c["kind"] != "seg":
        continue
    for (ex, ey, tag) in ((c["x0"], c["y0"], "start"), (c["x1"], c["y1"], "end")):
        for num, p in pads.items():
            d = math.hypot(ex - p["x"], ey - p["y"])
            if d <= 2.0:
                inside = (abs(ex - p["x"]) <= p["w"] / 2) and (abs(ey - p["y"]) <= p["h"] / 2)
                print("  pad %s  %-5s (%7.4f,%7.4f) d=%.4f inside_pad=%s  %-10s %-16s w%.2f %s" %
                      (num, tag, ex, ey, d, inside, c["layer"], c["net"], c["width"], c["uuid"]))

print("\nvias within 2.0 mm of a J26 pad centre:")
for c in g["copper"]:
    if c["kind"] != "via":
        continue
    for num, p in pads.items():
        d = math.hypot(c["x"] - p["x"], c["y"] - p["y"])
        if d <= 2.0:
            print("  pad %s  via (%7.4f,%7.4f) d=%.4f %-16s d%.2f drill%.2f %s" %
                  (num, c["x"], c["y"], d, c["net"], c["size"], c["drill"], c["uuid"]))
