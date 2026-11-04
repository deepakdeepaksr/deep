import os
import sys

import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))
for ref in ("R56", "R57"):
    f = b.FindFootprintByReference(ref)
    if not f:
        print(ref, "MISSING")
        continue
    print("%s at (%.3f, %.3f)" % (ref, f.GetPosition().x / 1e6, f.GetPosition().y / 1e6))
    for p in f.Pads():
        print("   pad %s %-14s (%.3f, %.3f)" % (p.GetNumber(), p.GetNetname(),
                                                p.GetPosition().x / 1e6, p.GetPosition().y / 1e6))
print("J6.6", [p.GetNetname() for p in b.FindFootprintByReference("J6").Pads() if p.GetNumber() == "6"])
print("J6.7", [p.GetNetname() for p in b.FindFootprintByReference("J6").Pads() if p.GetNumber() == "7"])
