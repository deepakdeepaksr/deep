"""T-56 recon: label position, wires at J2 pins 7 and 9, and board pad nets before."""
import io
import os
import sys

import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


text = io.open(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch"), encoding="utf-8").read()
root = parse(text)[0]
for n in root.find_all("label"):
    if av(n.atoms()[0]) == "REED_PULSE_F":
        a = n.find("at").atoms()
        print("label REED_PULSE_F at", [av(x) for x in a], "uuid", n.value("uuid"))
print("wires with an endpoint at x 150-158, y 303-311:")
for w in root.find_all("wire"):
    pts = [(float(av(p.atoms()[0])), float(av(p.atoms()[1]))) for p in w.find_all("xy")]
    if any(150 <= px <= 158 and 303 <= py <= 311 for (px, py) in pts):
        print("   ", pts)
print("no_connect at x 150-158, y 303-311:",
      [(float(av(p.atoms()[0])), float(av(p.atoms()[1]))) for n in root.find_all("no_connect")
       for p in [n.find("at")] if 150 <= float(av(p.atoms()[0])) <= 158 and 303 <= float(av(p.atoms()[1])) <= 311])

b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))
f = b.FindFootprintByReference("J2")
print("board J2 pads 5-10:")
for p in f.Pads():
    if p.GetNumber() in ("5", "6", "7", "8", "9", "10"):
        print("   %s %-28s (%7.2f,%7.2f)" % (p.GetNumber(), p.GetNetname(),
                                              p.GetPosition().x / 1e6, p.GetPosition().y / 1e6))
