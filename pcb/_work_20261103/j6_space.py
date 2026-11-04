import os
import sys

import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))
f = b.FindFootprintByReference("J6")
bb = f.GetCourtyard(pcbnew.F_CrtYd).BBox()
print("J6 courtyard x %.2f-%.2f y %.2f-%.2f" % (bb.GetX() / 1e6, bb.GetRight() / 1e6,
                                                bb.GetY() / 1e6, bb.GetBottom() / 1e6))
print("copper on F.Cu within x 255-275, y 158-170:")
for t in b.GetTracks():
    if t.Type() != pcbnew.PCB_TRACE_T:
        continue
    if b.GetLayerName(t.GetLayer()) != "F.Cu":
        continue
    s, e = t.GetStart(), t.GetEnd()
    xs, ys, xe, ye = s.x / 1e6, s.y / 1e6, e.x / 1e6, e.y / 1e6
    if max(xs, xe) >= 255 and min(xs, xe) <= 275 and max(ys, ye) >= 158 and min(ys, ye) <= 170:
        print("   %-16s (%7.2f,%7.2f)-(%7.2f,%7.2f) w%.2f" % (t.GetNetname(), xs, ys, xe, ye, t.GetWidth() / 1e6))
