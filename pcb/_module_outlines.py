"""STEP 4b/4c: identify the module outlines against their sockets, swap the two wrong labels,
and draw the enclosure, standoffs, base plate and gland exits on Dwgs.User."""
import sys, uuid
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str
import pcbnew

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"

b = pcbnew.LoadBoard(PCB)
sock = {}
for f in b.GetFootprints():
    r = f.GetReference()
    if r in ("J1", "J2", "J3", "J4", "J6", "J7", "J8"):
        sock[r] = (f.GetPosition().x / 1e6, f.GetPosition().y / 1e6)
print("sockets:", {k: (round(v[0], 2), round(v[1], 2)) for k, v in sock.items()})

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

rects = []
for d in root.children:
    if isinstance(d, Node) and d.head == "gr_rect" and d.value("layer") == "F.Fab":
        s = d.find("start").atoms(); e = d.find("end").atoms()
        rects.append((float(atom_str(s[0])), float(atom_str(s[1])), float(atom_str(e[0])), float(atom_str(e[1])), d))
print("F.Fab module rectangles:")
for (x0, y0, x1, y1, d) in rects:
    print("  x %.2f..%.2f  y %.2f..%.2f  (%.1f x %.1f mm)" % (x0, x1, y0, y1, x1 - x0, y1 - y0))

texts = []
for d in root.children:
    if isinstance(d, Node) and d.head == "gr_text" and d.value("layer") == "F.Fab":
        a = d.atoms(); at = d.find("at").atoms()
        texts.append((atom_str(a[0]), float(atom_str(at[0])), float(atom_str(at[1])), d))
print("F.Fab labels:")
for (t, x, y, d) in texts:
    print("  %-22r at (%.2f, %.2f)" % (t, x, y))
