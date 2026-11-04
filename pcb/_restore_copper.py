"""Restore named copper objects from the snapshot into the current board."""
import sys, json
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
SNAP = ROOT + r"\pcb\_snap\S3_3v3width_20261101_173547\MoriShield_Carrier.kicad_pcb"

want = set(sys.argv[1:])
snap_text = open(SNAP, encoding="utf-8").read()
snap_root = parse(snap_text)[0]
blocks = []
for c in snap_root.children:
    if isinstance(c, Node) and c.head in ("segment", "via", "arc"):
        if c.value("uuid") in want:
            blocks.append((c.value("uuid"), snap_text[c.start:c.end]))

print("found %d of %d in the snapshot" % (len(blocks), len(want)))
missing = want - {b[0] for b in blocks}
if missing:
    print("MISSING:", ", ".join(sorted(missing)))

cur = open(PCB, encoding="utf-8").read()
root = parse(cur)[0]
existing = set()
for c in root.children:
    if isinstance(c, Node) and c.head in ("segment", "via", "arc"):
        existing.add(c.value("uuid"))
to_add = [(u, b) for (u, b) in blocks if u not in existing]
print("adding %d" % len(to_add))
payload = "".join("\t" + b.replace("\n", "\n\t") + "\n" for (u, b) in to_add)
idx = cur.rstrip().rfind(")")
out = cur[:idx] + payload + cur[idx:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
