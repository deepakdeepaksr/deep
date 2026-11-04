"""Prove whether the 12 segments lost before T-55 are merges (length preserved) and
print J2's real pin endpoints."""
import io
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402

E1 = os.path.join(ROOT, "pcb", "_snap", "T1_E1_20261103_204817", "MoriShield_Carrier.kicad_pcb")
BASE = os.path.join(ROOT, "pcb", "_snap", "T55_pcb_20261104_075500", "MoriShield_Carrier.kicad_pcb")


def av(v):
    return v[1] if isinstance(v, tuple) else v


def stats(path):
    text = io.open(path, encoding="utf-8").read()
    root = parse(text)[0]
    per = {}
    for c in root.find_all("segment"):
        a = c.find("start").atoms()
        e = c.find("end").atoms()
        x0, y0 = float(av(a[0])), float(av(a[1]))
        x1, y1 = float(av(e[0])), float(av(e[1]))
        k = (c.value("net"), c.value("layer"))
        L = math.hypot(x1 - x0, y1 - y0)
        per[k] = per.get(k, [0, 0.0])
        per[k][0] += 1
        per[k][1] += L
    return per


a = stats(E1)
b = stats(BASE)
ta = sum(v[1] for v in a.values())
tb = sum(v[1] for v in b.values())
ca = sum(v[0] for v in a.values())
cb = sum(v[0] for v in b.values())
print("E1  : %d segments, %.3f mm" % (ca, ta))
print("BASE: %d segments, %.3f mm" % (cb, tb))
print("delta: %d segments, %+.3f mm" % (cb - ca, tb - ta))
print("\nper-net count/length where the count changed:")
for k in sorted(set(a) | set(b)):
    x = a.get(k, [0, 0.0])
    y = b.get(k, [0, 0.0])
    if x[0] != y[0]:
        print("  %-16s %-6s %3d -> %3d seg   %8.3f -> %8.3f mm  (%+.3f)" %
              (k[0], k[1], x[0], y[0], x[1], y[1], y[1] - x[1]))

text = io.open(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch"), encoding="utf-8").read()
root = parse(text)[0]
jx = jy = rot = None
for s in root.find_all("symbol"):
    props = {av(p.atoms()[0]): av(p.atoms()[1]) for p in s.children
             if isinstance(p, Node) and p.head == "property" and len(p.atoms()) >= 2}
    if props.get("Reference") == "J2":
        at = s.find("at").atoms()
        jx, jy = float(av(at[0])), float(av(at[1]))
        rot = float(av(at[2])) if len(at) > 2 else 0.0
        libid = s.value("lib_id")
print("\nJ2 instance at (%.2f, %.2f) rot %.0f  %s" % (jx, jy, rot, libid))
for s in root.find("lib_symbols").children:
    if isinstance(s, Node) and s.head == "symbol" and av(s.atoms()[0]) == libid:
        for p in s.find_all("pin"):
            num = av(p.find("number").atoms()[0])
            if num in ("5", "6", "7", "8", "9", "10"):
                at = p.find("at").atoms()
                px, py = float(av(at[0])), float(av(at[1]))
                nm = av(p.find("name").atoms()[0])
                print("   pin %-2s %-8s local (%7.2f,%7.2f) -> abs (%7.2f,%7.2f)" %
                      (num, nm, px, py, jx + px, jy - py))
        break
