"""Connectivity read-back from the saved board (rule 3)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))
conn = b.GetConnectivity()
conn.Build(b)

for ref in ("J26", "J8", "J7"):
    fp = b.FindFootprintByReference(ref)
    print("%s at (%.3f, %.3f)" % (ref, fp.GetPosition().x / 1e6, fp.GetPosition().y / 1e6))
    for p in fp.Pads():
        items = conn.GetConnectedItems(p)
        nets = sorted({i.GetNetname() for i in items})
        print("   pad %-2s %-22s connected items %3d  nets %s" %
              (p.GetNumber(), p.GetNetname(), len(items), nets[:4]))

# any ratsnest left?
print("ratsnest lines:", len(b.GetConnectivity().GetRatsnestForItems([]) or []))
