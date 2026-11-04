"""Print the key footprints and their pads from geom.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(HERE, "geom.json"), encoding="utf-8"))

want = ["J26", "J5", "J15", "J16", "J25", "J21", "J22", "J23", "J24", "J11", "J12",
        "J13", "J14", "J17", "J20", "J7", "J8", "J6", "U6", "U4", "U8", "U7"]
for f in g["footprints"]:
    if f["ref"] not in want:
        continue
    print("%-5s %-18s at (%8.3f,%8.3f) rot %6.1f layer %s" %
          (f["ref"], f["value"][:18], f["x"], f["y"], f["rot"], f["layer"]))
    for p in f["pads"]:
        print("      pad %-3s net %-22s (%8.3f,%8.3f) %5.2fx%5.2f drill %5.2f bbox %s" %
              (p["num"], p["net"][:22], p["x"], p["y"], p["w"], p["h"], p["drill"], p["bbox"]))
