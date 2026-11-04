"""Set the width of every segment on a net, optionally only those near given points."""
import sys, json, math, re
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
net = sys.argv[1]
target = float(sys.argv[2])
only_near = sys.argv[3] if len(sys.argv) > 3 else None   # path to a DRC json

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

def at(n):
    a = n.atoms()
    return (float(atom_str(a[0])), float(atom_str(a[1])))

near = []
if only_near:
    drc = json.load(open(only_near, encoding="utf-8"))
    for v in drc["violations"]:
        if v["type"] in ("clearance", "shorting_items", "track_crossing", "tracks_same_net"):
            if any(net in it.get("description", "") for it in v.get("items", [])):
                near.append((v["items"][0]["pos"]["x"], v["items"][0]["pos"]["y"]))

edits = []
n_changed = 0
for c in root.children:
    if not (isinstance(c, Node) and c.head == "segment"):
        continue
    if c.value("net") != net:
        continue
    s, e = at(c.find("start")), at(c.find("end"))
    mid = ((s[0] + e[0]) / 2, (s[1] + e[1]) / 2)
    if near:
        if not any(math.hypot(mid[0] - p[0], mid[1] - p[1]) < 1.6 for p in near):
            continue
    w = c.find("width")
    cur = float(atom_str(w.atoms()[0]))
    if abs(cur - target) < 1e-9:
        continue
    edits.append((w.start, w.end, "(width %s)" % target))
    n_changed += 1

out = text
for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
print("net %s: %d segments set to %s mm%s" % (net, n_changed, target,
      (" (near %d flagged points)" % len(near)) if near else ""))
