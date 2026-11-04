"""T-56 board: J2.7 -> unconnected-(J2-IO41-Pad7), J2.9 -> /REED_PULSE_F, reroute."""
import io
import os
import re
import shutil
import sys
import time
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
SNAP = os.path.join(ROOT, "pcb", "_snap")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


text = io.open(PCB, encoding="utf-8").read()
stamp = time.strftime("%Y%m%d_%H%M%S")
snap = os.path.join(SNAP, "T56_board_%s" % stamp)
os.makedirs(snap, exist_ok=True)
for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
          "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
    shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
print("snapshot", snap)

# 1. delete the segment that attached the net to J2.7
root = parse(text)[0]
hit = None
for c in root.children:
    if isinstance(c, Node) and c.head == "segment":
        s = c.find("start").atoms()
        e = c.find("end").atoms()
        pts = {(round(float(av(s[0])), 2), round(float(av(s[1])), 2)),
               (round(float(av(e[0])), 2), round(float(av(e[1])), 2))}
        if pts == {(183.5, 138.76), (182.25, 137.5)}:
            hit = c
            break
assert hit is not None, "J2.7 stub not found"
st = hit.start
while st > 0 and text[st - 1] in " \t":
    st -= 1
if st > 0 and text[st - 1] == "\n":
    st -= 1
text = text[:st] + text[hit.end:]
print("deleted the J2.7 stub")

# 2. repoint J2 pads 7 and 9
root = parse(text)[0]
j2 = None
for c in root.children:
    if isinstance(c, Node) and c.head == "footprint":
        for p in c.children:
            if isinstance(p, Node) and p.head == "property":
                a = p.atoms()
                if len(a) >= 2 and av(a[0]) == "Reference" and av(a[1]) == "J2":
                    j2 = c
block = text[j2.start:j2.end]
for padnum, newname in (("7", "unconnected-(J2-IO41-Pad7)"), ("9", "/REED_PULSE_F")):
    mm = re.search(r'\(pad "%s"[\s\S]*?\(net "[^"]*"\)' % padnum, block)
    seg = mm.group(0)
    block = block.replace(seg, seg[:seg.rindex("(net ")] + '(net "%s")' % newname, 1)
text = text[:j2.start] + block + text[j2.end:]


def seg(net, w, a, b):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width %s)\n'
            '\t\t(layer "F.Cu")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (a[0], a[1], b[0], b[1], w, net, uuid.uuid4()))


add = seg("/REED_PULSE_F", 0.3, (183.5, 133.68), (182.25, 134.93))
add += seg("/REED_PULSE_F", 0.3, (182.25, 134.93), (182.25, 137.5))

tail = text.rstrip()
io.open(PCB, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
parse(io.open(PCB, encoding="utf-8").read())
print("J2 pads repointed and 2 reroute segments added; file parses")
