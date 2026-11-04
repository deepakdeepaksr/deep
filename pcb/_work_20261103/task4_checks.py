"""TASK 4.2/4.3: under-module test over the five outlines, and J26 reachability."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))

OUTLINES = {
    "DS3231": (144.70, 162.95, 182.80, 185.05),
    "ESP32": (180.45, 91.45, 212.55, 156.55),
    "GY521": (209.30, 175.95, 230.40, 192.05),
    "MODEM": (228.45, 90.45, 271.55, 150.55),
    "E22": (259.95, 158.57, 297.05, 180.67),
}
# the socket each module plugs into is expected to be inside its own outline
OWN = {"DS3231": "J8", "ESP32": ("J1", "J2"), "GY521": "J7", "MODEM": ("J3", "J4"), "E22": "J6"}

print("== under-module test: footprints whose body centre is inside an outline")
for name, (x0, y0, x1, y1) in OUTLINES.items():
    hits = []
    for f in b.GetFootprints():
        p = f.GetPosition()
        px, py = p.x / 1e6, p.y / 1e6
        if x0 <= px <= x1 and y0 <= py <= y1:
            hits.append(f.GetReference())
    own = OWN[name]
    own = (own,) if isinstance(own, str) else own
    other = [h for h in hits if h not in own]
    print("  %-7s inside: %d parts; own socket %s; OTHER: %s" %
          (name, len(hits), ",".join(own), ", ".join(other) if other else "none"))

print("\n== J26 reachability")
f = b.FindFootprintByReference("J26")
bb = f.GetCourtyard(pcbnew.F_CrtYd).BBox()
print("  J26 courtyard x %.2f-%.2f y %.2f-%.2f" % (bb.GetX() / 1e6, bb.GetRight() / 1e6,
                                                   bb.GetY() / 1e6, bb.GetBottom() / 1e6))
for name in ("DS3231", "GY521", "ESP32"):
    x0, y0, x1, y1 = OUTLINES[name]
    ov = not (x1 < bb.GetX() / 1e6 or x0 > bb.GetRight() / 1e6 or y1 < bb.GetY() / 1e6 or y0 > bb.GetBottom() / 1e6)
    print("  overlaps %-7s outline: %s" % (name, ov))
c = b.GetConnectivity()
c.Build(b)
for p in f.Pads():
    print("  pad %s %-12s connected items %3d" % (p.GetNumber(), p.GetNetname(), len(c.GetConnectedItems(p))))
