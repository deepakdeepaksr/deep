"""T-55 Task 2: move the four strap vias out of the resistor pads and connect by track."""
import io
import os
import shutil
import time
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
SNAP = os.path.join(ROOT, "pcb", "_snap")

stamp = time.strftime("%Y%m%d_%H%M%S")
snap = os.path.join(SNAP, "T55_vias_%s" % stamp)
os.makedirs(snap, exist_ok=True)
for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
          "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
    shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
print("snapshot", snap)

text = io.open(PCB, encoding="utf-8").read()
subs = [
    ("(at 266.5625 164.92)", "(at 265.95 164.92)"),
    ("(at 266.5625 162.38)", "(at 265.95 162.38)"),
    ("(at 268.4375 164.92)", "(at 269.4 164.92)"),
    ("(at 268.4375 162.38)", "(at 269.4 162.38)"),
    ("(end 266.5625 164.92)", "(end 265.95 164.92)"),
    ("(end 266.5625 162.38)", "(end 265.95 162.38)"),
]
for a, b in subs:
    n = text.count(a)
    text = text.replace(a, b)
    print("%-28s -> %-24s x%d" % (a, b, n))


def seg(net, w, layer, a, b):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width %s)\n'
            '\t\t(layer "%s")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (a[0], a[1], b[0], b[1], w, layer, net, uuid.uuid4()))


add = ""
add += seg("/E22_M1_STRAP", 0.3, "F.Cu", (265.95, 164.92), (266.675, 164.92))
add += seg("/E22_M0_STRAP", 0.3, "F.Cu", (265.95, 162.38), (266.675, 162.38))
add += seg("GND", 0.3, "F.Cu", (268.325, 164.92), (269.4, 164.92))
add += seg("GND", 0.3, "F.Cu", (268.325, 162.38), (269.4, 162.38))

tail = text.rstrip()
io.open(PCB, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
print("four connecting tracks added")
