"""T-55 board, take 3: name-based net replacement (declaration and pad refs together)."""
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
LIB = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty\R_0603_1608Metric.kicad_mod"
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


text = io.open(PCB, encoding="utf-8").read()
stamp = time.strftime("%Y%m%d_%H%M%S")
snap = os.path.join(SNAP, "T55_pcb_%s" % stamp)
os.makedirs(snap, exist_ok=True)
for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
          "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
    shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
print("snapshot", snap)

# 1. delete every /E22_M0 and /E22_M1 track or via
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
print("deleted", removed, "copper items")

# 2. rename the two nets everywhere (declaration + J1 pads), then repoint J6 pads
text = text.replace('(net "/E22_M1")', '(net "unconnected-(J1-IO10-Pad16)")')
text = text.replace('(net "/E22_M0")', '(net "unconnected-(J1-IO11-Pad17)")')

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
    if not mm:
        raise SystemExit("pad %s net line not found" % padnum)
    seg = mm.group(0)
    block = block.replace(seg, seg[:seg.rindex("(net ")] + '(net "%s")' % newname, 1)
text = text[:j6.start] + block + text[j6.end:]

# 3. R56 / R57 from the library footprint
lib = io.open(LIB, encoding="utf-8").read()
lib = lib.replace('(footprint "R_0603_1608Metric"', '(footprint "Resistor_SMD:R_0603_1608Metric"', 1)
lib = re.sub(r"\t\(version [^)]*\)\n", "", lib, count=1)
lib = re.sub(r"\t\(generator \"[^\"]*\"\)\n", "", lib, count=1)
lib = lib.replace('(property "Value" "R_0603_1608Metric"', '(property "Value" "0"', 1)


def make_r(ref, x, y, rot, pad1, pad2):
    b = lib.replace('"REF**"', '"%s"' % ref, 1)
    b = b.replace('(layer "F.Cu")', '(layer "F.Cu")\n\t(uuid "%s")\n\t(at %s %s %s)' %
                  (uuid.uuid4(), x, y, rot), 1)
    r = parse(b)[0]
    ins = []
    for p in [c for c in r.children if isinstance(c, Node) and c.head == "pad"]:
        num = av(p.atoms()[0])
        ins.append((p.end - 1, '\n\t\t\t(net "%s")\n\t\t\t(uuid "%s")\n\t\t' %
                    (pad1 if num == "1" else pad2, uuid.uuid4())))
    for (pos, s) in sorted(ins, reverse=True):
        b = b[:pos] + s + b[pos:]
    return b


add = make_r("R56", 265.5, 164.92, 270, "E22_M1_STRAP", "GND")
add += make_r("R57", 265.5, 162.38, 270, "E22_M0_STRAP", "GND")


def seg(net, w, a, b):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width %s)\n'
            '\t\t(layer "F.Cu")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (a[0], a[1], b[0], b[1], w, net, uuid.uuid4()))


def via(net, p):
    return ('\t(via\n\t\t(at %s %s)\n\t\t(size 0.6)\n\t\t(drill 0.3)\n'
            '\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (p[0], p[1], net, uuid.uuid4()))


add += seg("E22_M1_STRAP", 0.3, (263.5, 164.92), (264.5625, 164.92))
add += seg("E22_M0_STRAP", 0.3, (263.5, 162.38), (264.5625, 162.38))
add += via("GND", (266.4375, 164.92))
add += via("GND", (266.4375, 162.38))

tail = text.rstrip()
io.open(PCB, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
parse(open(PCB, encoding="utf-8").read())
print("board written and parses; %d copper items removed" % removed)
