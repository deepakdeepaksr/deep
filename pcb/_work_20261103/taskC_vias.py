"""For each via of interest, list every copper item touching it."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(HERE, "geom.json"), encoding="utf-8"))

VIAS = [(281.0, 94.0), (291.0, 94.0), (286.0, 94.0), (263.712, 191.25),
        (235.463, 190.0), (248.963, 189.5), (180.0, 188.5)]
for (vx, vy) in VIAS:
    print("VIA (%.3f,%.3f)" % (vx, vy))
    for c in g["copper"]:
        if c["kind"] == "seg":
            for (ex, ey, tag) in ((c["x0"], c["y0"], "s"), (c["x1"], c["y1"], "e")):
                if math.hypot(ex - vx, ey - vy) < 0.15:
                    print("   SEG %-6s %-14s (%7.3f,%7.3f)-(%7.3f,%7.3f) w%.2f %s" %
                          (c["layer"], c["net"], c["x0"], c["y0"], c["x1"], c["y1"], c["width"], c["uuid"][:8]))
        else:
            if abs(c["x"] - vx) < 1e-3 and abs(c["y"] - vy) < 1e-3:
                print("   VIA %-14s d%.2f drill %.2f %s" % (c["net"], c["size"], c["drill"], c["uuid"][:8]))
