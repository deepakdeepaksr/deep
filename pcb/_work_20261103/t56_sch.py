"""T-56 schematic: move REED_PULSE_F from J2 pin 7 to pin 9.

Pin 9 already carries a no_connect flag, and the label sits at the end of a short wire
from the pin, so all three objects have to move together.
"""
import io
import os
import re
import shutil
import sys
import time
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCH = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch")
SNAP = os.path.join(ROOT, "pcb", "_snap")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


text = io.open(SCH, encoding="utf-8").read()
stamp = time.strftime("%Y%m%d_%H%M%S")
snap = os.path.join(SNAP, "T56_reedmove_%s" % stamp)
os.makedirs(snap, exist_ok=True)
for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
          "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
    shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
print("snapshot", snap)

root = parse(text)[0]
label_block = None
label_node = None
for n in root.find_all("label"):
    a = n.find("at").atoms()
    if av(n.atoms()[0]) == "REED_PULSE_F" and abs(float(av(a[0])) - 154.94) < 0.01:
        label_node = n
        label_block = text[n.start:n.end]
        break
assert label_node is not None, "label not found"

# 1. delete the label and the wire that fed it
dels = [label_node]
for w in root.find_all("wire"):
    pts = [(float(av(p.atoms()[0])), float(av(p.atoms()[1]))) for p in w.find_all("xy")]
    if (152.4, 304.8) in pts and (154.94, 304.8) in pts:
        dels.append(w)
# 2. delete the no_connect sitting on pin 9
for n in root.find_all("no_connect"):
    a = n.find("at").atoms()
    if abs(float(av(a[0])) - 152.4) < 0.01 and abs(float(av(a[1])) - 309.88) < 0.01:
        dels.append(n)
for c in sorted(dels, key=lambda n: -n.start):
    s = c.start
    while s > 0 and text[s - 1] in " \t":
        s -= 1
    if s > 0 and text[s - 1] == "\n":
        s -= 1
    text = text[:s] + text[c.end:]
print("deleted label, its wire and the pin-9 no_connect")

# 3. re-create the label on pin 9 and a no_connect on pin 7
new_label = re.sub(r"\(at 154\.94 304\.8 0\)", "(at 152.4 309.88 0)", label_block, count=1)
new_label = re.sub(r'\(uuid "[0-9a-f-]+"\)', '(uuid "%s")' % uuid.uuid4(), new_label, count=1)
add = new_label
add += ('\t(no_connect\n\t\t(at 152.4 304.8)\n\t\t(uuid "%s")\n\t)\n' % uuid.uuid4())

tail = text.rstrip()
io.open(SCH, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
parse(io.open(SCH, encoding="utf-8").read())
print("label placed on pin 9, no_connect on pin 7; file parses")
