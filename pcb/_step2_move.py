"""STEP 2: move the /3V3_SENS_SW B.Cu run clear of x 296-304.57, y 163-177."""
import sys, uuid
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

P = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
TARGET_UUID = "e427c0f1-8264-4c0d-8394-fc159ef07235"

text = open(P, encoding="utf-8").read()
root = parse(text)[0]
seg = None
for c in root.children:
    if isinstance(c, Node) and c.head == "segment" and c.value("uuid") == TARGET_UUID:
        seg = c
        break
assert seg is not None, "target segment not found"

def mk(x0, y0, x1, y1):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width 0.5)\n\t\t(layer "B.Cu")\n'
            '\t\t(net "/3V3_SENS_SW")\n\t\t(uuid "%s")\n\t)\n') % (x0, y0, x1, y1, uuid.uuid4())

# A horizontal at y 178.80 (below the keep-out band), then up at x 293.0, then 45 deg
# to the existing via at (298.75, 147.50), then the last vertical to 141.75.
new = (mk(298.75, 178.80, 293.0, 178.80) + mk(293.0, 178.80, 293.0, 153.25) +
       mk(293.0, 153.25, 298.75, 147.50) + mk(298.75, 147.50, 298.75, 141.75))

s0 = seg.start
while s0 > 0 and text[s0 - 1] in " \t":
    s0 -= 1
if s0 > 0 and text[s0 - 1] == "\n":
    s0 -= 1
out = text[:s0] + new + text[seg.end:]
open(P, "w", encoding="utf-8", newline="").write(out)
print("replaced 1 segment (37.05 mm) with 4 segments totalling %.2f mm" % (5.75 + 25.55 + 7.17 + 5.75))
