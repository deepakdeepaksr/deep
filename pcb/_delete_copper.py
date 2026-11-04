"""Delete copper objects by UUID, as text. Usage: _delete_copper.py uuid [uuid ...]"""
import sys
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
want = set(sys.argv[1:])
text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

spans = []
for c in root.children:
    if isinstance(c, Node) and c.head in ("segment", "via", "arc"):
        u = c.value("uuid")
        if u in want:
            spans.append((c.start, c.end, u, c.head, c.value("net")))

found = {s[2] for s in spans}
print("requested %d, found %d" % (len(want), len(found)))
for s in spans:
    print("  %s %s net=%s span=%d-%d" % (s[3], s[2], s[4], s[0], s[1]))
missing = want - found
if missing:
    print("NOT FOUND:", ", ".join(sorted(missing)))

out = text
for (s, e, u, h, n) in sorted(spans, key=lambda x: -x[0]):
    # also swallow the preceding newline+indent to keep the file tidy
    lead = s
    while lead > 0 and out[lead - 1] in " \t":
        lead -= 1
    if lead > 0 and out[lead - 1] == "\n":
        lead -= 1
    out = out[:lead] + out[e:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
print("written")
