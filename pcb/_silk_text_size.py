"""Raise every F.SilkS reference field to 1.0 mm height / 0.15 mm stroke,
and remove empty board-level silk texts."""
import sys, re
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

edits = []
raised = 0
for fp in root.children:
    if not (isinstance(fp, Node) and fp.head == "footprint"):
        continue
    ref = None
    for p in fp.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and atom_str(a[0]) == "Reference":
                ref = atom_str(a[1])
    if ref is None:
        continue
    for p in fp.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and atom_str(a[0]) == "Reference" and p.value("layer") == "F.SilkS":
                font = p.find("effects").find("font")
                size = font.find("size")
                thick = font.find("thickness")
                h = float(atom_str(size.atoms()[1]))
                t = float(atom_str(thick.atoms()[0]))
                if h < 1.0 or t < 0.15:
                    edits.append((size.start, size.end, "(size 1 1)"))
                    edits.append((thick.start, thick.end, "(thickness 0.15)"))
                    raised += 1

deleted = 0
for d in root.children:
    if isinstance(d, Node) and d.head == "gr_text" and d.value("layer") == "F.SilkS":
        t = d.value("text")
        if not t or not str(t).strip():
            s = d.start
            while s > 0 and text[s - 1] in " \t":
                s -= 1
            if s > 0 and text[s - 1] == "\n":
                s -= 1
            edits.append((s, d.end, ""))
            deleted += 1

out = text
for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
print("fields raised: %d   empty texts deleted: %d   edits: %d" % (raised, deleted, len(edits)))
