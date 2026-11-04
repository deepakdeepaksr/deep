"""Probe /REED_PULSE_F copper at J2 (pads 7 and 9) before the T-56 board edit."""
import os
import sys

import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))
print("all /REED_PULSE_F tracks (net /REED_PULSE_F):")
for t in b.GetTracks():
    if t.GetNetname() != "/REED_PULSE_F":
        continue
    if t.Type() == pcbnew.PCB_VIA_T:
        p = t.GetPosition()
        print("   VIA (%7.2f,%7.2f)" % (p.x / 1e6, p.y / 1e6))
    else:
        s, e = t.GetStart(), t.GetEnd()
        print("   %-6s (%7.2f,%7.2f)-(%7.2f,%7.2f) w%.2f %s" %
              (b.GetLayerName(t.GetLayer()), s.x / 1e6, s.y / 1e6, e.x / 1e6, e.y / 1e6,
               t.GetWidth() / 1e6, t.m_Uuid.AsString()[:8]))
print("\nother copper within 3 mm of J2.9 (183.50,133.68):")
for t in b.GetTracks():
    if t.Type() != pcbnew.PCB_TRACE_T:
        continue
    s, e = t.GetStart(), t.GetEnd()
    for (x, y) in ((s.x / 1e6, s.y / 1e6), (e.x / 1e6, e.y / 1e6)):
        if abs(x - 183.5) < 3 and abs(y - 133.68) < 3 and t.GetNetname() != "/REED_PULSE_F":
            print("   %-6s %-16s (%7.2f,%7.2f) w%.2f" % (b.GetLayerName(t.GetLayer()),
                                                          t.GetNetname(), x, y, t.GetWidth() / 1e6))
            break
