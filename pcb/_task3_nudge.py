"""Move the newly added port labels that DRC flags, choosing a clear offset geometrically."""
import sys, json, uuid, re
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str
import pcbnew

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
DRC = ROOT + r"\revC\_t3_drc.json"

b = pcbnew.LoadBoard(PCB)
pads = []
for f in b.GetFootprints():
    for p in f.Pads():
        bb = p.GetBoundingBox()
        pads.append((bb.GetX()/1e6, bb.GetY()/1e6, bb.GetRight()/1e6, bb.GetBottom()/1e6))

drc = json.load(open(DRC, encoding="utf-8"))
bad = set()
for v in drc["violations"]:
    for it in v.get("items", []):
        m = re.search(r"PCB text '([^']+)'", it.get("description", ""))
        if m: bad.add(m.group(1))
print("labels to move:", sorted(bad))

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

def at(n):
    a = n.atoms(); return (float(atom_str(a[0])), float(atom_str(a[1])))

# existing text boxes, to avoid overlapping each other
boxes = []
for d in root.children:
    if isinstance(d, Node) and d.head == "gr_text" and d.value("layer") == "F.SilkS":
        nm = atom_str(d.atoms()[0]); p = at(d.find("at"))
        boxes.append((nm, p[0], p[1]))

def clash(cx, cy, name, w=6.0, h=1.6):
    for (x0, y0, x1, y1) in pads:
        if not (cx + w/2 < x0 or cx - w/2 > x1 or cy + h/2 < y0 or cy - h/2 > y1):
            return True
    for (nm, x, y) in boxes:
        if nm == name: continue
        if abs(cx - x) < w and abs(cy - y) < 2.0:
            return True
    if cx < 128 or cx > 303 or cy < 90 or cy > 204:
        return True
    return False

edits = []
moved = []
for d in root.children:
    if isinstance(d, Node) and d.head == "gr_text" and d.value("layer") == "F.SilkS":
        nm = atom_str(d.atoms()[0])
        if nm not in bad: continue
        p = at(d.find("at"))
        best = None
        for (dx, dy) in [(0,-2.6),(0,2.6),(-3.5,0),(3.5,0),(0,-5.2),(0,5.2),(-5,2.6),(5,2.6),(0,-7.8),(0,7.8)]:
            cx, cy = round(p[0]+dx,2), round(p[1]+dy,2)
            if not clash(cx, cy, nm):
                best = (cx, cy); break
        if best:
            atn = d.find("at")
            edits.append((atn.start, atn.end, "(at %s %s 0)" % best))
            moved.append((nm, p, best))
        else:
            moved.append((nm, p, None))

out = text
for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
for (nm, old, new) in moved:
    print("  %-8s %s -> %s" % (nm, old, new))
