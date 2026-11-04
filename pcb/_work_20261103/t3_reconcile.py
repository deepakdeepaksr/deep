"""Name the 12 segments lost before T-55, and compute J2's real pin endpoints."""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402

SCH = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch")
E1 = os.path.join(ROOT, "pcb", "_snap", "T1_E1_20261103_204817", "MoriShield_Carrier.kicad_pcb")
BASE = os.path.join(ROOT, "pcb", "_snap", "T55_pcb_20261104_075500", "MoriShield_Carrier.kicad_pcb")


def av(v):
    return v[1] if isinstance(v, tuple) else v


def segs(path):
    text = io.open(path, encoding="utf-8").read()
    root = parse(text)[0]
    out = {}
    for c in root.find_all("segment"):
        a = c.find("start").atoms()
        e = c.find("end").atoms()
        out[c.value("uuid")] = ((av(a[0]), av(a[1])), (av(e[0]), av(e[1])), c.value("net"), c.value("layer"))
    return out


e1 = segs(E1)
base = segs(BASE)
gone = [u for u in e1 if u not in base]
new = [u for u in base if u not in e1]
print("E1 snapshot %d segments, base snapshot %d: %d gone, %d new" % (len(e1), len(base), len(gone), len(new)))
for u in gone:
    s, e, n, l = e1[u]
    print("  GONE %s %-14s %-6s %s -> %s" % (u[:8], n, l, s, e))
for u in new:
    s, e, n, l = base[u]
    print("  NEW  %s %-14s %-6s %s -> %s" % (u[:8], n, l, s, e))

# J2 pin table from the schematic
text = io.open(SCH, encoding="utf-8").read()
root = parse(text)[0]
jx = jy = rot = None
for s in root.find_all("symbol"):
    props = {av(p.atoms()[0]): av(p.atoms()[1]) for p in s.children
             if isinstance(p, Node) and p.head == "property" and len(p.atoms()) >= 2}
    if props.get("Reference") == "J2":
        a = s.find("at").atoms()
        jx, jy, rot = float(av(a[0])), float(av(a[1])), float(av(a[2])) if len(a) > 2 else 0.0
        libid = s.value("lib_id")
print("\nJ2 instance at (%.2f, %.2f) rot %.0f  %s" % (jx, jy, rot, libid))
libs = root.find("lib_symbols")
for s in libs.children:
    if isinstance(s, Node) and s.head == "symbol" and av(s.atoms()[0]) == libid:
        for p in s.find_all("pin"):
            num = av(p.find("number").atoms()[0])
            if num in ("5", "6", "7", "8", "9", "10"):
                a = p.find("at").atoms()
                px, py = float(av(a[0])), float(av(a[1]))
                name = av(p.find("name").atoms()[0])
                print("   pin %-2s %-8s local (%7.2f,%7.2f) -> abs (%7.2f,%7.2f)" %
                      (num, name, px, py, jx + px, jy - py))
        break
