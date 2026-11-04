"""For candidate GND via positions: clearance margin AND whether the point is inside both pours."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402
import pcbnew  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))
filler = pcbnew.ZONE_FILLER(b)
filler.Fill(b.Zones())
z_in1 = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "In1.Cu")
z_bcu = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "B.Cu")
p_in1 = z_in1.GetFilledPolysList(z_in1.GetLayer())
p_bcu = z_bcu.GetFilledPolysList(z_bcu.GetLayer())

VIA = [(0.0, 0.0, 0.6, 0.6, 0.3, "1", "GND")]
COURT = (-0.3, -0.3, 0.3, 0.3)


def inside_both(px, py):
    v = pcbnew.VECTOR2I(int(round(px * 1e6)), int(round(py * 1e6)))
    return p_in1.Contains(v) and p_bcu.Contains(v)


CAND = [(277.0, 89.0), (277.0, 90.0), (278.0, 90.0), (276.5, 90.5), (277.5, 91.0),
        (276.0, 89.5), (278.5, 91.5), (279.0, 89.0),
        (163.0, 187.0), (164.0, 186.0), (165.0, 185.0), (162.0, 188.0), (166.0, 184.0)]
for (x, y) in CAND:
    s = clear.score((x, y), 0.0, VIA, COURT, skip_ref=None)
    print("(%7.2f,%7.2f) legal=%-5s margin %7.2f hole %6.2f edge %5.2f  inside_both=%s" %
          (x, y, s["legal"], s["margin"], s["hole_margin"], s["edge"], inside_both(x, y)))
