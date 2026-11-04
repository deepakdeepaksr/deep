"""T-59 batch 3, corrected: restore the snapshot, then place C52 on grid, at its own
position, with pad 1 on /+5V_ESP."""
import io
import os
import re
import shutil
import sys
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCH = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch")
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
SNAP = os.path.join(ROOT, "pcb", "_snap", "T59_5VESP_20261104_090758")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_sch"):
    shutil.copy(os.path.join(SNAP, f), os.path.join(ROOT, "pcb", f))
print("restored from", SNAP)

SX, SY = 454.66, 299.72          # both on the 1.27 mm grid
text = io.open(SCH, encoding="utf-8").read()
root = parse(text)[0]
blk = None
for s in root.find_all("symbol"):
    props = {av(p.atoms()[0]): av(p.atoms()[1]) for p in s.children
             if isinstance(p, Node) and p.head == "property" and len(p.atoms()) >= 2}
    if props.get("Reference") == "C41":
        blk = text[s.start:s.end]
        break
b = blk.replace('"C41"', '"C52"')
b = re.sub(r"\(at [-\d.]+ [-\d.]+ 0\)", "(at %s %s 0)" % (SX, SY), b, count=1)
b = re.sub(r'\(uuid "[0-9a-f-]+"\)', lambda m: '(uuid "%s")' % uuid.uuid4(), b, count=1)
add = b
add += ('\t(label "+5V_ESP"\n\t\t(at %s %s 0)\n\t\t(uuid "%s")\n\t\t(effects\n\t\t\t(font\n'
        '\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t)\n'
        % (SX, SY - 3.81, uuid.uuid4()))
gnd = None
for s in root.find_all("symbol"):
    if s.value("lib_id") == "MoriShield_Carrier:GND":
        gnd = text[s.start:s.end]
        break
g = re.sub(r"\(at [-\d.]+ [-\d.]+ 0\)", "(at %s %s 0)" % (SX, SY + 3.81), gnd, count=1)
g = re.sub(r'"#PWR\d+"', '"#PWR0931"', g)
g = re.sub(r'\(uuid "[0-9a-f-]+"\)', lambda m: '(uuid "%s")' % uuid.uuid4(), g, count=1)
add += g
tail = text.rstrip()
io.open(SCH, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
parse(io.open(SCH, encoding="utf-8").read())
print("schematic: C52 at (%s, %s), label and GND on the pin ends" % (SX, SY))

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
nb = blk.replace('"C41"', '"C52"')
nb = re.sub(r"\(at [-\d.]+ [-\d.]+ [-\d.]+\)", "(at 215.6 97.5 90)", nb, count=1)
nb = re.sub(r'\(net "\+5V"\)', '(net "/+5V_ESP")', nb)
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
print("board: C52 at (215.6, 97.5) rot 90, pad1 /+5V_ESP, track and own GND via")
