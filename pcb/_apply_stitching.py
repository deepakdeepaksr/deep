"""Add the planned stitching vias to the board as text."""
import json, uuid, sys

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
PLAN = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC\_stitch_plan.json"

plan = json.load(open(PLAN, encoding="utf-8"))
vias = plan["vias"]
print("adding %d vias" % len(vias))

blocks = []
for (x, y) in vias:
    blocks.append(
        '\t(via\n'
        '\t\t(at %s %s)\n'
        '\t\t(size 0.6)\n'
        '\t\t(drill 0.3)\n'
        '\t\t(layers "F.Cu" "B.Cu")\n'
        '\t\t(net "GND")\n'
        '\t\t(uuid "%s")\n'
        '\t)\n' % (x, y, uuid.uuid4()))

text = open(PCB, encoding="utf-8").read()
idx = text.rstrip().rfind(")")
out = text[:idx] + "".join(blocks) + text[idx:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
print("written")
