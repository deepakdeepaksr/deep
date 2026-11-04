"""Draw the enclosure, standoffs, base plate, gland exits and module heights on Dwgs.User / F.Fab."""
import uuid, math

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"

def rect(x0, y0, x1, y1, layer, width=0.15):
    return ('\t(gr_rect\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(stroke\n\t\t\t(width %s)\n\t\t\t(type default)\n\t\t)\n'
            '\t\t(fill none)\n\t\t(layer "%s")\n\t\t(uuid "%s")\n\t)\n') % (x0, y0, x1, y1, width, layer, uuid.uuid4())

def circle(cx, cy, r, layer, width=0.15):
    return ('\t(gr_circle\n\t\t(center %s %s)\n\t\t(end %s %s)\n\t\t(stroke\n\t\t\t(width %s)\n\t\t\t(type default)\n\t\t)\n'
            '\t\t(fill none)\n\t\t(layer "%s")\n\t\t(uuid "%s")\n\t)\n') % (cx, cy, round(cx + r, 3), cy, width, layer, uuid.uuid4())

def txt(s, x, y, layer, size=1.2):
    return ('\t(gr_text "%s"\n\t\t(at %s %s 0)\n\t\t(layer "%s")\n\t\t(uuid "%s")\n\t\t(effects\n\t\t\t(font\n'
            '\t\t\t\t(size %s %s)\n\t\t\t\t(thickness 0.15)\n\t\t\t)\n\t\t)\n\t)\n') % (s, x, y, layer, uuid.uuid4(), size, size)

blk = ""
# enclosure 200 x 155 mm, centred on the 178.15 x 118.15 board
blk += rect(115.5, 69.0, 315.5, 224.0, "Dwgs.User", 0.2)
blk += txt("ENCLOSURE 200 x 155 x 80 mm (internal)", 118.0, 66.5, "Dwgs.User", 1.6)
# acrylic base plate, 3 mm smaller than the box
blk += rect(118.5, 72.0, 312.5, 221.0, "Dwgs.User")
blk += txt("ACRYLIC BASE 3 mm", 118.0, 226.0, "Dwgs.User", 1.4)
# M3 standoffs at the four mounting holes
for (ref, (x, y)) in (("H1", (131.5, 92.5)), ("H2", (299.5, 92.5)), ("H3", (131.5, 200.5)), ("H4", (299.5, 200.5))):
    blk += circle(x, y, 3.0, "Dwgs.User")
    blk += txt(ref, x + 3.6, y - 0.8, "Dwgs.User", 1.0)
# gland / cable exits along the bottom edge: 6 sensor + supply + earth
for i in range(8):
    x = 140.0 + i * 20.0
    blk += circle(x, 224.0, 3.0, "Dwgs.User")
blk += txt("GLANDS: 6 sensor + 5V supply + earth", 150.0, 228.5, "Dwgs.User", 1.4)
# module heights - no vendor drawing in the repo, so TBC
for (label, x, y) in (("ESP32 h TBC", 184.0, 90.0), ("MODEM h TBC", 232.0, 88.5),
                      ("E22 h TBC", 296.0, 157.0), ("GY-521 h TBC", 208.0, 206.5), ("DS3231 h TBC", 146.0, 189.0)):
    blk += txt(label, x, y, "F.Fab", 1.2)

text = open(PCB, encoding="utf-8").read()
idx = text.rstrip().rfind(")")
open(PCB, "w", encoding="utf-8", newline="").write(text[:idx] + blk + text[idx:])
print("enclosure graphics added: %d blocks" % blk.count("(gr_"))
