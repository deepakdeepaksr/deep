import os
import sys

import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))

print("a board 0805 at rot 90, pads vs origin:")
for f in b.GetFootprints():
    if str(f.GetFPID().GetLibItemName()).startswith("R_0805") and abs(f.GetOrientationDegrees() - 90) < 1:
        ox, oy = f.GetPosition().x / 1e6, f.GetPosition().y / 1e6
        print("  %s at (%.2f,%.2f) rot 90" % (f.GetReference(), ox, oy))
        for p in f.Pads():
            print("     pad %s local (%.4f, %.4f)" % (p.GetNumber(),
                                                     p.GetPosition().x / 1e6 - ox,
                                                     p.GetPosition().y / 1e6 - oy))
        break

print("\nB.Cu copper near x 262-270, y 160-168:")
for t in b.GetTracks():
    if t.Type() != pcbnew.PCB_TRACE_T:
        continue
    if b.GetLayerName(t.GetLayer()) != "B.Cu":
        continue
    s, e = t.GetStart(), t.GetEnd()
    xs, ys, xe, ye = s.x / 1e6, s.y / 1e6, e.x / 1e6, e.y / 1e6
    if max(xs, xe) >= 262 and min(xs, xe) <= 270 and max(ys, ye) >= 160 and min(ys, ye) <= 168:
        print("   %-16s (%7.2f,%7.2f)-(%7.2f,%7.2f) w%.2f" % (t.GetNetname(), xs, ys, xe, ye, t.GetWidth() / 1e6))
