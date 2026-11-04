"""Move the two no-connect flags onto J1's actual pin 16/17 endpoints."""
import io
import os
import re
import sys
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCH = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


text = io.open(SCH, encoding="utf-8").read()
root = parse(text)[0]
libs = root.find("lib_symbols")

# J1 instance position
jx = jy = None
for s in root.find_all("symbol"):
    props = {av(p.atoms()[0]): av(p.atoms()[1]) for p in s.children
             if isinstance(p, Node) and p.head == "property" and len(p.atoms()) >= 2}
    if props.get("Reference") == "J1":
        a = s.find("at").atoms()
        jx, jy = float(av(a[0])), float(av(a[1]))
        libid = s.value("lib_id")
print("J1 at", jx, jy, libid)

pins = {}
for s in libs.children:
    if isinstance(s, Node) and s.head == "symbol" and av(s.atoms()[0]) == libid:
        for p in s.find_all("pin"):
            num = p.find("number")
            at = p.find("at")
            if num is None or at is None:
                continue
            n = av(num.atoms()[0])
            a = at.atoms()
            pins[n] = (float(av(a[0])), float(av(a[1])))
        break
for n in ("16", "17"):
    px, py = pins[n]
    print("pin %s local (%.2f, %.2f) -> absolute (%.2f, %.2f)" % (n, px, py, jx + px, jy - py))

# drop the two dangling no-connects and re-add them at the pin ends
blocks = []
for c in root.children:
    if isinstance(c, Node) and c.head == "no_connect":
        at = c.find("at").atoms()
        if abs(float(av(at[0])) - 113.03) < 0.01:
            blocks.append(c)
for c in sorted(blocks, key=lambda n: -n.start):
    s = c.start
    while s > 0 and text[s - 1] in " \t":
        s -= 1
    if s > 0 and text[s - 1] == "\n":
        s -= 1
    text = text[:s] + text[c.end:]

add = ""
for n in ("16", "17"):
    px, py = pins[n]
    add += ('\t(no_connect\n\t\t(at %s %s)\n\t\t(uuid "%s")\n\t)\n' %
            (round(jx + px, 2), round(jy - py, 2), uuid.uuid4()))
tail = text.rstrip()
io.open(SCH, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
print("no-connects moved onto the pins")
