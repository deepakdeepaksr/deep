"""T-55 Task 1: the board net names are missing the leading slash a local label produces."""
import io
import os
import shutil
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
SNAP = os.path.join(ROOT, "pcb", "_snap")

stamp = time.strftime("%Y%m%d_%H%M%S")
snap = os.path.join(SNAP, "T55_rename_%s" % stamp)
os.makedirs(snap, exist_ok=True)
for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
          "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
    shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
print("snapshot", snap)

text = io.open(PCB, encoding="utf-8").read()
n1 = text.count('"E22_M1_STRAP"')
n2 = text.count('"E22_M0_STRAP"')
text = text.replace('"E22_M1_STRAP"', '"/E22_M1_STRAP"')
text = text.replace('"E22_M0_STRAP"', '"/E22_M0_STRAP"')
io.open(PCB, "w", encoding="utf-8", newline="").write(text)
print("renamed %d M1 and %d M0 occurrences" % (n1, n2))

for f in ("MoriShield_Carrier.kicad_pro", "MoriShield_Carrier.kicad_dru"):
    p = os.path.join(ROOT, "pcb", f)
    s = io.open(p, encoding="utf-8").read()
    print("%-28s references old name: %s" % (f, "E22_M_STRAP" in s or "E22_M0_STRAP" in s or "E22_M1_STRAP" in s))
