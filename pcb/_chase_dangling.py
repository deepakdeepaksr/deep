"""Delete the copper object that a DRC dangling item points at, by position."""
import sys, json, math
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
DRC = sys.argv[1]
NET = sys.argv[2] if len(sys.argv) > 2 else None

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

def at(n):
    a = n.atoms()
    return (float(atom_str(a[0])), float(atom_str(a[1])))

def seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx == 0 and dy == 0:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy))

drc = json.load(open(DRC, encoding="utf-8"))
targets = []
for v in drc["violations"]:
    if v["type"] in ("track_dangling", "via_dangling"):
        it = v["items"][0]
        targets.append((it["pos"]["x"], it["pos"]["y"], v["type"]))

if not targets:
    print("nothing dangling")
    sys.exit(0)

spans = []
for (px, py, kind) in targets:
    best = None
    for c in root.children:
        if not (isinstance(c, Node) and c.head in ("segment", "via")):
            continue
        if NET and c.value("net") != NET:
            continue
        if c.head == "segment":
            a, b = at(c.find("start")), at(c.find("end"))
            d = seg_dist((px, py), a, b)
        else:
            p = at(c.find("at"))
            d = math.hypot(p[0] - px, p[1] - py)
        if best is None or d < best[0]:
            best = (d, c)
    if best and best[0] < 1.0:
        c = best[1]
        s = c.start
        while s > 0 and text[s - 1] in " \t":
            s -= 1
        if s > 0 and text[s - 1] == "\n":
            s -= 1
        spans.append((s, c.end, c.head, c.value("uuid"), round(best[0], 3)))
    else:
        print("no object within 1 mm of", px, py, kind)

print("deleting:")
for sp in spans:
    print("   %s %s (dist %s)" % (sp[2], sp[3], sp[4]))
out = text
for (s, e, *_r) in sorted(spans, key=lambda x: -x[0]):
    out = out[:s] + out[e:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
