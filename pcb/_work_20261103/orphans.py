"""List the exact text of every copper object in the old J26 feed branches."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402

P = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
text = open(P, encoding="utf-8").read()
root = parse(text)[0]


def at(n):
    a = n.atoms()
    return (a[0][1] if isinstance(a[0], tuple) else a[0],
            a[1][1] if isinstance(a[1], tuple) else a[1])


TARGETS = {
    # 3V3_C dead branch (was J26.1 -> via -> B.Cu -> via -> J8.5)
    "04e04363-5206-4": None,  # via 162.5 175.75
    "99c1fb15": None,         # B.Cu 162.5,175.75 - 165.25,166.75
    "488736aa": None,         # via 165.25 166.75
    "faf76439": None,         # F.Cu 165.25,166.75 - 167.75,161.5
    # SDA dead branch
    "f6800f7e": None,         # F.Cu 171.5,166.75 - 172.5,165.75
    "b7ae2b55": None,         # via 172.5 165.75
    "1d6f6c03": None,         # B.Cu 172.5,165.75 - 169.5,164.5
    "a6e56e2a": None,         # B.Cu 169.5,164.5 - 165.5,164.5
    "8879934d": None,         # B.Cu 165.5,164.5 - 164.75,163.75
    "ec6813dd": None,         # B.Cu 164.75,163.75 - 165.25,161.5
    # SCL dead branch
    "f8e2f164": None,         # via 168.5 169.75
    "ca8e5d89": None,         # B.Cu 168.5,169.75 - 168.5,166.5
    "c14aca4e": None,         # B.Cu 168.5,166.5 - 167.5,165.5
    "aefbbb43": None,         # B.Cu 167.5,165.5 - 164.5,165.5
    "48b48b3b": None,         # B.Cu 164.5,165.5 - 164,165
    "76956867": None,         # B.Cu 164,165 - 162.75,161.5
}

for c in root.children:
    if not (isinstance(c, Node) and c.head in ("segment", "via")):
        continue
    u = c.value("uuid") or ""
    for k in TARGETS:
        if u.startswith(k):
            TARGETS[k] = c
            break

for k, c in TARGETS.items():
    if c is None:
        print(k, "NOT FOUND")
        continue
    desc = c.head
    if c.head == "segment":
        s = c.find("start")
        e = c.find("end")
        desc += " %s -> %s  net %s  layer %s  w %s" % (at(s), at(e), c.value("net"),
                                                       c.find("layer").atoms()[0][1],
                                                       c.find("width").atoms()[0])
    else:
        desc += " at %s net %s" % (at(c.find("at")), c.value("net"))
    print("%-40s %s" % (c.value("uuid"), desc))

print()
print("--- exact text of the 3V3_C via at 143.55,159")
for c in root.children:
    if isinstance(c, Node) and c.head == "via":
        p = at(c.find("at"))
        if abs(float(p[0]) - 143.55) < 0.01 and abs(float(p[1]) - 159.0) < 0.01:
            print(repr(text[c.start:c.end]))
