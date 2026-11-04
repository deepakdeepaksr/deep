"""TASK D fixes: drop the bottom labels below the existing silk rectangle, move J6's
reference out of the RXD mark, and lift REED clear of J23."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402

BOTTOM = {"SOIL": 150.38, "FSR": 163.94, "SGP41": 176.0, "SHT45": 192.0,
          "SPS30": 236.0, "BME688": 250.0, "BUZZ": 139.31}
MOVES = {"REED": (135.5, 123.5), "RXD": (261.6, 170.0)}

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]
edits = []
for c in root.children:
    if not (isinstance(c, Node) and c.head == "gr_text"):
        continue
    txt = c.atoms()[0][1] if c.atoms() else ""
    at = c.find("at")
    a = at.atoms()
    def av(v):
        return v[1] if isinstance(v, tuple) else v
    x, y = float(av(a[0])), float(av(a[1]))
    if txt in BOTTOM and abs(y - 201.3) < 0.01:
        edits.append((at.start, at.end, "(at %s 202.6 0)" % BOTTOM[txt]))
    elif txt == "REED":
        edits.append((at.start, at.end, "(at 135.5 123.5 0)"))
for (s, e, new) in sorted(edits, reverse=True):
    text = text[:s] + new + text[e:]

# J6 reference field
root = parse(text)[0]
for c in root.children:
    if isinstance(c, Node) and c.head == "footprint":
        for p in c.children:
            if isinstance(p, Node) and p.head == "property":
                a = p.atoms()
                if len(a) >= 2 and a[0][1] == "Reference" and a[1][1] == "J6":
                    at = p.find("at")
                    text = text[:at.start] + "(at 266.5 181.5 0)" + text[at.end:]
                    break
open(PCB, "w", encoding="utf-8", newline="").write(text)
print("moved %d labels, J6 reference" % len(edits))
