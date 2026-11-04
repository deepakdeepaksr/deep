"""Swap the two wrong module labels, resize their outlines, add heights, draw the enclosure."""
import sys, uuid
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str
import pcbnew

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

b = pcbnew.LoadBoard(PCB)
holes = {}
for f in b.GetFootprints():
    if f.GetReference() in ("H1", "H2", "H3", "H4"):
        holes[f.GetReference()] = (f.GetPosition().x / 1e6, f.GetPosition().y / 1e6)
print("mounting holes:", {k: (round(v[0], 2), round(v[1], 2)) for k, v in holes.items()})

def find_text(s):
    for d in root.children:
        if isinstance(d, Node) and d.head == "gr_text":
            a = d.atoms()
            if a and atom_str(a[0]) == s:
                return d
    return None

edits = []
# 1. swap the two labels: GY-521 belongs on J7 (x~219.9), DS3231 on J8 (x~163.75)
for label, newpos in (("GY-521", (219.85, 184.0)), ("DS3231 RTC", (163.75, 174.0))):
    d = find_text(label)
    assert d is not None, label
    at = d.find("at")
    edits.append((at.start, at.end, "(at %s %s 0)" % newpos))

# 2. resize the two outlines to the module dimensions stated in the register
#    GY-521 21 x 16 on J7; DS3231 38 x 22 on J8 (both TBC until calipers confirm)
def rect_for(cx, cy, w, h):
    return (round(cx - w / 2, 2), round(cy - h / 2, 2), round(cx + w / 2, 2), round(cy + h / 2, 2))

newrects = {"GY-521": rect_for(219.85, 184.0, 21, 16), "DS3231": rect_for(163.75, 174.0, 38, 22)}
rect_nodes = [d for d in root.children if isinstance(d, Node) and d.head == "gr_rect" and d.value("layer") == "F.Fab"]
# rect 1 (x 154..173.5) is the J8 socket; rect 3 (x 207.35..232.35) is the J7 socket
for d in rect_nodes:
    s = d.find("start").atoms(); e = d.find("end").atoms()
    x0 = float(atom_str(s[0]))
    if abs(x0 - 154.0) < 0.01:
        box = newrects["DS3231"]
    elif abs(x0 - 207.35) < 0.01:
        box = newrects["GY-521"]
    else:
        continue
    edits.append((d.find("start").start, d.find("start").end, "(start %s %s)" % (box[0], box[1])))
    edits.append((d.find("end").start, d.find("end").end, "(end %s %s)" % (box[2], box[3])))
    # the Dwgs.User twin, same coordinates
    for d2 in root.children:
        if isinstance(d2, Node) and d2.head == "gr_rect" and d2.value("layer") == "Dwgs.User":
            s2 = d2.find("start").atoms()
            if abs(float(atom_str(s2[0])) - x0) < 0.01:
                edits.append((d2.find("start").start, d2.find("start").end, "(start %s %s)" % (box[0], box[1])))
                edits.append((d2.find("end").start, d2.find("end").end, "(end %s %s)" % (box[2], box[3])))

out = text
for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
print("label swap + outline resize applied:", len(edits), "edits")
