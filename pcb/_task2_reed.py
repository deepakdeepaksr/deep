"""TASK 2 / T-56: move /REED_PULSE_F from J2.7 (GPIO41) to J2.9 (GPIO39)."""
import sys, uuid
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
SCH = ROOT + r"\pcb\MoriShield_Carrier.kicad_sch"

# ---- board ----
text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

def at(n):
    a = n.atoms(); return (round(float(atom_str(a[0])), 3), round(float(atom_str(a[1])), 3))

victim = None
for c in root.children:
    if isinstance(c, Node) and c.head == "segment" and c.value("net") == "/REED_PULSE_F":
        s, e = at(c.find("start")), at(c.find("end"))
        if (183.5, 138.76) in (s, e):
            victim = c; break
assert victim is not None, "segment to J2.7 not found"

def mk(x0, y0, x1, y1):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width 0.3)\n\t\t(layer "F.Cu")\n'
            '\t\t(net "/REED_PULSE_F")\n\t\t(uuid "%s")\n\t)\n') % (x0, y0, x1, y1, uuid.uuid4())

new = mk(182.25, 137.50, 181.50, 136.75) + mk(181.50, 136.75, 181.50, 133.68) + mk(181.50, 133.68, 183.50, 133.68)
s0 = victim.start
while s0 > 0 and text[s0-1] in " \t": s0 -= 1
if s0 > 0 and text[s0-1] == "\n": s0 -= 1
text = text[:s0] + new + text[victim.end:]
root = parse(text)[0]

edits = []
for fp in root.children:
    if isinstance(fp, Node) and fp.head == "footprint":
        ref = None
        for p in fp.children:
            if isinstance(p, Node) and p.head == "property":
                a = p.atoms()
                if len(a) >= 2 and atom_str(a[0]) == "Reference": ref = atom_str(a[1])
        if ref != "J2": continue
        for p in fp.children:
            if isinstance(p, Node) and p.head == "pad":
                num = atom_str(p.atoms()[0])
                if num == "7":
                    n = p.find("net"); edits.append((n.start, n.end, '(net "unconnected-(J2-IO41-Pad7)")'))
                elif num == "9":
                    n = p.find("net"); edits.append((n.start, n.end, '(net "/REED_PULSE_F")'))
for (s, e, newv) in sorted(edits, key=lambda x: -x[0]):
    text = text[:s] + newv + text[e:]
open(PCB, "w", encoding="utf-8", newline="").write(text)
print("board: 1 segment replaced by 3; J2.7 freed, J2.9 takes /REED_PULSE_F")

# ---- schematic ----
st = open(SCH, encoding="utf-8").read()
sroot = parse(st)[0]
sedits = []
for c in sroot.children:
    if isinstance(c, Node) and c.head in ("label", "global_label"):
        p = at(c.find("at"))
        if atom_str(c.atoms()[0]) == "REED_PULSE_F" and p == (154.94, 304.8):
            s0 = c.start
            while s0 > 0 and st[s0-1] in " \t": s0 -= 1
            if s0 > 0 and st[s0-1] == "\n": s0 -= 1
            sedits.append((s0, c.end, ""))
out = st
for (s, e, newv) in sorted(sedits, key=lambda x: -x[0]):
    out = out[:s] + newv + out[e:]
add = ('\t(label "REED_PULSE_F"\n\t\t(at 154.94 309.88 180)\n\t\t(uuid "%s")\n'
       '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify right bottom)\n\t\t)\n\t)\n'
       '\t(no_connect\n\t\t(at 154.94 304.8)\n\t\t(uuid "%s")\n\t)\n') % (uuid.uuid4(), uuid.uuid4())
idx = out.rstrip().rfind(")")
out = out[:idx] + add + out[idx:]
open(SCH, "w", encoding="utf-8", newline="").write(out)
print("schematic: label moved to pin 9, no_connect added at pin 7")
