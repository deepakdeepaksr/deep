"""Probe the schematic region around the two strap labels before placing R56/R57."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


root = parse(open(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch"), encoding="utf-8").read())[0]

print("symbols in x 455-510, y 295-340:")
for s in root.find_all("symbol"):
    at = s.find("at")
    if at is None:
        continue
    a = at.atoms()
    x, y = float(av(a[0])), float(av(a[1]))
    if 455 <= x <= 510 and 295 <= y <= 340:
        props = {av(p.atoms()[0]): av(p.atoms()[1]) for p in s.children
                 if isinstance(p, Node) and p.head == "property" and len(p.atoms()) >= 2}
        print("  %-8s %-32s (%.2f, %.2f)" % (props.get("Reference"), s.value("lib_id"), x, y))

print("\nwires with an endpoint in x 470-500, y 305-335:")
for w in root.find_all("wire"):
    pts = [(float(av(p.atoms()[0])), float(av(p.atoms()[1]))) for p in w.find_all("xy")]
    if any(470 <= px <= 500 and 305 <= py <= 335 for (px, py) in pts):
        print("  ", pts)

print("\nlabels at x 478-486:")
for n in root.find_all("label"):
    a = n.find("at").atoms()
    x, y = float(av(a[0])), float(av(a[1]))
    if 478 <= x <= 486:
        print("  %-16s (%.2f, %.2f) rot %s" % (av(n.atoms()[0]), x, y, av(a[2])))
