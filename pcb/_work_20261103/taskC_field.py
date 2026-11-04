"""Move Q9's reference field clear of C41."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]
fp = None
for c in root.children:
    if isinstance(c, Node) and c.head == "footprint":
        for p in c.children:
            if isinstance(p, Node) and p.head == "property":
                a = p.atoms()
                if len(a) >= 2 and a[0][1] == "Reference" and a[1][1] == "Q9":
                    fp = c
if fp is None:
    raise SystemExit("Q9 not found")
for p in fp.children:
    if isinstance(p, Node) and p.head == "property":
        a = p.atoms()
        if len(a) >= 2 and a[0][1] == "Reference":
            at = p.find("at")
            text = text[:at.start] + "(at 157 105 0)" + text[at.end:]
            break
open(PCB, "w", encoding="utf-8", newline="").write(text)
print("Q9 reference -> (157,105)")
