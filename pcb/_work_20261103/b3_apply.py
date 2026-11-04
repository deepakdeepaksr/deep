"""T-59 batch 3: add C52, 100 nF on /+5V_ESP, to serve D7.1 (the net has no 100 nF at all)."""
import io
import os
import re
import shutil
import sys
import time
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCH = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch")
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
SNAP = os.path.join(ROOT, "pcb", "_snap")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


stamp = time.strftime("%Y%m%d_%H%M%S")
snap = os.path.join(SNAP, "T59_5VESP_%s" % stamp)
os.makedirs(snap, exist_ok=True)
for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
          "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
    shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
print("snapshot", snap)

# ---------------- schematic
text = io.open(SCH, encoding="utf-8").read()
root = parse(text)[0]
blk = None
for s in root.find_all("symbol"):
    props = {av(p.atoms()[0]): av(p.atoms()[1]) for p in s.children
             if isinstance(p, Node) and p.head == "property" and len(p.atoms()) >= 2}
    if props.get("Reference") == "C41":
        blk = text[s.start:s.end]
        break
assert blk, "C41 symbol not found"
b = blk.replace('"C41"', '"C52"')
b = b.replace("(at 497.84 129.54 0)", "(at 455 300 0)")
b = re.sub(r'\(uuid "[0-9a-f-]+"\)', lambda m: '(uuid "%s")' % uuid.uuid4(), b, count=1)
add = b
add += ('\t(label "+5V_ESP"\n\t\t(at 455 296.19 0)\n\t\t(uuid "%s")\n\t\t(effects\n\t\t\t(font\n'
        '\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t)\n' % uuid.uuid4())
gnd = None
for s in root.find_all("symbol"):
    if s.value("lib_id") == "MoriShield_Carrier:GND":
        gnd = text[s.start:s.end]
        break
g = gnd.replace("(at 134.62 483.87 0)", "(at 455 303.81 0)")
g = re.sub(r'"#PWR\d+"', '"#PWR0931"', g)
g = re.sub(r'\(uuid "[0-9a-f-]+"\)', lambda m: '(uuid "%s")' % uuid.uuid4(), g, count=1)
add += g
tail = text.rstrip()
io.open(SCH, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
parse(io.open(SCH, encoding="utf-8").read())
print("schematic: C52 added with label +5V_ESP and GND")

# ---------------- board
text = io.open(PCB, encoding="utf-8").read()
root = parse(text)[0]
blk = None
for c in root.children:
    if isinstance(c, Node) and c.head == "footprint":
        for p in c.children:
            if isinstance(p, Node) and p.head == "property":
                a = p.atoms()
                if len(a) >= 2 and av(a[0]) == "Reference" and av(a[1]) == "C41":
                    blk = text[c.start:c.end]
                    break
    if blk:
        break
assert blk, "C41 footprint not found"
nb = blk.replace('"C41"', '"C52"')
nb = re.sub(r"\(at 162\.06 106\.75 0\)", "(at 215.6 97.5 90)", nb, count=1)
nb = re.sub(r'\(net "3V3_C"\)', '(net "/+5V_ESP")', nb)
nb = re.sub(r'\(uuid "[0-9a-f-]+"\)', lambda m: '(uuid "%s")' % uuid.uuid4(), nb)
add = nb


def seg(net, w, a, b):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width %s)\n'
            '\t\t(layer "F.Cu")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (a[0], a[1], b[0], b[1], w, net, uuid.uuid4()))


def via(net, p):
    return ('\t(via\n\t\t(at %s %s)\n\t\t(size 0.6)\n\t\t(drill 0.3)\n'
            '\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (p[0], p[1], net, uuid.uuid4()))


add += seg("/+5V_ESP", 0.5, (215.6, 98.54), (215.6, 103.0))
add += seg("GND", 0.3, (215.6, 96.46), (213.5, 96.46))
add += via("GND", (213.5, 96.46))
tail = text.rstrip()
io.open(PCB, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
parse(io.open(PCB, encoding="utf-8").read())
print("board: C52 footprint added, track to D7.1, own GND via")
