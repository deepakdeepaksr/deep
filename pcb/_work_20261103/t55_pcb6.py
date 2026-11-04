"""T-55 board, final v2: insert the strap net declarations in the real net container,
and place the R56/R57 reference fields clear of the pads."""
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
BASE = os.path.join(SNAP, "T55_pcb_20261104_075500")
LIB = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty\R_0603_1608Metric.kicad_mod"
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


shutil.copy(os.path.join(BASE, "MoriShield_Carrier.kicad_pcb"), PCB)
text = io.open(PCB, encoding="utf-8").read()
stamp = time.strftime("%Y%m%d_%H%M%S")
snap = os.path.join(SNAP, "T55_pcb_%s" % stamp)
os.makedirs(snap, exist_ok=True)
for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
          "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
    shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))

removed = 0
while True:
    root = parse(text)[0]
    hit = None
    for c in root.children:
        if isinstance(c, Node) and c.head in ("segment", "via") and c.value("net") in ("/E22_M0", "/E22_M1"):
            hit = c
            break
    if hit is None:
        break
    s = hit.start
    while s > 0 and text[s - 1] in " \t":
        s -= 1
    if s > 0 and text[s - 1] == "\n":
        s -= 1
    text = text[:s] + text[hit.end:]
    removed += 1

text = text.replace('(net "/E22_M1")', '(net "unconnected-(J1-IO10-Pad16)")')
text = text.replace('(net "/E22_M0")', '(net "unconnected-(J1-IO11-Pad17)")')

# the real net container is the node with the most direct "net" children
root = parse(text)[0]
container = None
for n in [root] + [x for x in root.find_all("net")]:
    kids = [c for c in n.children if isinstance(c, Node) and c.head == "net"] if isinstance(n, Node) else []
    if len(kids) > 50:
        container = n
        break
if container is None:
    raise SystemExit("net container not found")
last = [c for c in container.children if isinstance(c, Node) and c.head == "net"][-1]
text = text[:last.end] + '\n\t\t(net "E22_M1_STRAP")\n\t\t(net "E22_M0_STRAP")' + text[last.end:]
print("net declarations added after node at", last.end)

root = parse(text)[0]
j6 = None
for c in root.children:
    if isinstance(c, Node) and c.head == "footprint":
        for p in c.children:
            if isinstance(p, Node) and p.head == "property":
                a = p.atoms()
                if len(a) >= 2 and av(a[0]) == "Reference" and av(a[1]) == "J6":
                    j6 = c
block = text[j6.start:j6.end]
for padnum, oldnet, newname in (("6", "unconnected-(J1-IO10-Pad16)", "E22_M1_STRAP"),
                                ("7", "unconnected-(J1-IO11-Pad17)", "E22_M0_STRAP")):
    mm = re.search(r'\(pad "%s"[\s\S]*?\(net "%s"\)' % (padnum, re.escape(oldnet)), block)
    seg = mm.group(0)
    block = block.replace(seg, seg[:seg.rindex("(net ")] + '(net "%s")' % newname, 1)
text = text[:j6.start] + block + text[j6.end:]

lib = io.open(LIB, encoding="utf-8").read()
lib = lib.replace('(footprint "R_0603_1608Metric"', '(footprint "Resistor_SMD:R_0603_1608Metric"', 1)
lib = re.sub(r"\t\(version [^)]*\)\n", "", lib, count=1)
lib = re.sub(r"\t\(generator \"[^\"]*\"\)\n", "", lib, count=1)
lib = lib.replace('(property "Value" "R_0603_1608Metric"', '(property "Value" "0"', 1)


def make_r(ref, x, y, refy, pad1, pad2):
    b = lib.replace('"REF**"', '"%s"' % ref, 1)
    b = b.replace('(property "Reference" "%s"\n\t\t(at 0 -1.43 0)' % ref,
                  '(property "Reference" "%s"\n\t\t(at 0 %s 0)' % (ref, refy), 1)
    b = b.replace('(layer "F.Cu")', '(layer "F.Cu")\n\t(uuid "%s")\n\t(at %s %s 0)' %
                  (uuid.uuid4(), x, y), 1)
    r = parse(b)[0]
    ins = []
    for p in [c for c in r.children if isinstance(c, Node) and c.head == "pad"]:
        num = av(p.atoms()[0])
        ins.append((p.end - 1, '\n\t\t\t(net "%s")\n\t\t\t(uuid "%s")\n\t\t' %
                    (pad1 if num == "1" else pad2, uuid.uuid4())))
    for (pos, s) in sorted(ins, reverse=True):
        b = b[:pos] + s + b[pos:]
    return b


add = make_r("R56", 267.5, 164.92, 1.9, "E22_M1_STRAP", "GND")
add += make_r("R57", 267.5, 162.38, -1.9, "E22_M0_STRAP", "GND")


def seg(net, w, layer, a, b):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width %s)\n'
            '\t\t(layer "%s")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (a[0], a[1], b[0], b[1], w, layer, net, uuid.uuid4()))


def via(net, p):
    return ('\t(via\n\t\t(at %s %s)\n\t\t(size 0.6)\n\t\t(drill 0.3)\n'
            '\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (p[0], p[1], net, uuid.uuid4()))


add += seg("E22_M1_STRAP", 0.3, "B.Cu", (263.5, 164.92), (266.5625, 164.92))
add += seg("E22_M0_STRAP", 0.3, "B.Cu", (263.5, 162.38), (266.5625, 162.38))
add += via("E22_M1_STRAP", (266.5625, 164.92))
add += via("E22_M0_STRAP", (266.5625, 162.38))
add += via("GND", (268.4375, 164.92))
add += via("GND", (268.4375, 162.38))

tail = text.rstrip()
io.open(PCB, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
parse(open(PCB, encoding="utf-8").read())
print("board written and parses; %d copper items removed; snapshot %s" % (removed, snap))
