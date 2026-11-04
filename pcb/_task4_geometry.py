"""TASK 4: correct module outlines to measured envelopes, add heights and SMA bulkheads."""
import sys, uuid
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

# target envelopes (x0, y0, x1, y1) from the manual / calipers in the brief
TARGET = {
    (180.5, 91.5): (180.5, 91.5, 212.5, 156.5),   # ESP32 32 x 65 (was 32 x 68)
    (228.5, 90.5): (228.5, 90.5, 271.5, 150.5),   # modem 43 x 60 (was 49 x 60)
    (260.0, 158.62): (260.0, 158.62, 297.0, 180.62),  # E22 37 x 22 (was 43.5 x 22.5)
}
edits = []
for d in root.children:
    if isinstance(d, Node) and d.head == "gr_rect" and d.value("layer") in ("F.Fab", "Dwgs.User"):
        s = d.find("start").atoms(); e = d.find("end").atoms()
        key = (round(float(atom_str(s[0])), 2), round(float(atom_str(s[1])), 2))
        if key in TARGET:
            x0, y0, x1, y1 = TARGET[key]
            edits.append((d.find("start").start, d.find("start").end, "(start %s %s)" % (x0, y0)))
            edits.append((d.find("end").start, d.find("end").end, "(end %s %s)" % (x1, y1)))
out = text
for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]

def txt(s, x, y, layer="F.Fab", size=1.2):
    return ('\t(gr_text "%s"\n\t\t(at %s %s 0)\n\t\t(layer "%s")\n\t\t(uuid "%s")\n\t\t(effects\n\t\t\t(font\n'
            '\t\t\t\t(size %s %s)\n\t\t\t\t(thickness 0.15)\n\t\t\t)\n\t\t)\n\t)\n') % (s, x, y, layer, uuid.uuid4(), size, size)

def circle(cx, cy, r, layer="Dwgs.User", w=0.2):
    return ('\t(gr_circle\n\t\t(center %s %s)\n\t\t(end %s %s)\n\t\t(stroke\n\t\t\t(width %s)\n\t\t\t(type default)\n\t\t)\n'
            '\t\t(fill none)\n\t\t(layer "%s")\n\t\t(uuid "%s")\n\t)\n') % (cx, cy, round(cx + r, 3), cy, w, layer, uuid.uuid4())

blk = ""
# heights from the brief; GY-521 and DS3231 have no source, so TBC
blk += txt("E22 37x22x13", 262.0, 183.5)
blk += txt("ESP32 32x65x14", 184.0, 89.5)
blk += txt("MODEM 43x60x12", 233.0, 88.5)
blk += txt("GY-521 21x16 h TBC", 210.0, 195.0)
blk += txt("DS3231 38x22 h TBC", 146.0, 162.0)
blk += txt("STACK = socket plastic TBC + module board + components", 240.0, 186.5, "F.Fab", 1.0)
# two panel-mount SMA bulkheads in the lid, drawn above their antenna ends
blk += circle(299.0, 62.0, 3.2, "Dwgs.User", 0.25)
blk += txt("SMA BULKHEAD 1 - E22, sealed", 262.0, 58.0, "Dwgs.User", 1.3)
blk += circle(272.0, 62.0, 3.2, "Dwgs.User", 0.25)
blk += txt("SMA BULKHEAD 2 - modem U.FL, sealed", 236.0, 54.0, "Dwgs.User", 1.3)
blk += txt("IP65 requires sealed bulkheads - a drilled hole is not IP65", 190.0, 48.0, "Dwgs.User", 1.2)

idx = out.rstrip().rfind(")")
open(PCB, "w", encoding="utf-8", newline="").write(out[:idx] + blk + out[idx:])
print("outline rects edited:", len(edits) // 2, "| graphics added:", blk.count("(gr_"))
