"""Downgrade the /+5V_SENS segments that a DRC clearance violation actually touches."""
import sys, json, math
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
DRC = sys.argv[1]
NET = sys.argv[2]
NEW = float(sys.argv[3])

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

def at(n):
    a = n.atoms()
    return (float(atom_str(a[0])), float(atom_str(a[1])))

def seg_dist(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(p[0] - ax, p[1] - ay)
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - (ax + t * dx), p[1] - (ay + t * dy))

pts = []
drc = json.load(open(DRC, encoding="utf-8"))
for v in drc["violations"]:
    if v["type"] in ("clearance", "shorting_items", "track_crossing"):
        if any(NET in it.get("description", "") for it in v.get("items", [])):
            pts.append((v["items"][0]["pos"]["x"], v["items"][0]["pos"]["y"]))

segs = []
for c in root.children:
    if isinstance(c, Node) and c.head == "segment" and c.value("net") == NET:
        segs.append((c, at(c.find("start")), at(c.find("end"))))

hit = []
for (c, s, e) in segs:
    if any(seg_dist(p, s, e) < 0.9 for p in pts):
        w = c.find("width")
        cur = float(atom_str(w.atoms()[0]))
        if cur > NEW:
            hit.append((w.start, w.end, "(width %s)" % NEW, s, e, cur))

print("downgrading %d segments to %s" % (len(hit), NEW))
for h in hit:
    print("   %s-%s was %s" % (h[3], h[4], h[5]))

out = text
for (s, e, new, *_rest) in sorted(hit, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
