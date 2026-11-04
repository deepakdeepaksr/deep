"""Widen the 3V3_C tracks that the live DRC floor flags.

The floor in force is the custom rule "3V3 class floor" (min 0.30 mm) in
MoriShield_Carrier.kicad_dru, not the 3V3 net-class routing default of 0.20 mm.
"""
import sys, re
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
TARGET = 0.3
text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

edits = []
changed = []
for c in root.children:
    if not (isinstance(c, Node) and c.head == "segment"):
        continue
    net = c.value("net")
    if net != "3V3_C":
        continue
    w = c.find("width")
    if w is None:
        continue
    val = float(w.atoms()[0])
    if val >= TARGET:
        continue
    a = w.atoms()[0]
    # replace the atom text only
    s = w.start
    e = w.end
    inner = text[s:e]
    new_inner = re.sub(r"\(width\s+[0-9.]+\)", "(width %s)" % TARGET, inner)
    edits.append((s, e, new_inner))
    changed.append((c.value("layer"), val, c.value("start"), c.value("end")))

print("segments to widen: %d" % len(changed))
for ch in changed:
    print("  layer=%s width=%s start=%s end=%s" % ch)

# apply from the end
out = text
for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]

open(PCB, "w", encoding="utf-8", newline="").write(out)
print("written")
