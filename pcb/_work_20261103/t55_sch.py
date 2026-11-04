"""T-55 schematic: two no-connect flags at J1.16/J1.17, and R56/R57 0R straps to GND."""
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
root = parse(text)[0]

# highest #PWR reference
pw = []
for s in root.find_all("symbol"):
    for p in s.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and av(a[0]) == "Reference" and av(a[1]).startswith("#PWR"):
                tail_ref = av(a[1])[4:]
                if tail_ref.isdigit():
                    pw.append(int(tail_ref))
base_pwr = max(pw) + 1

# clone the R55 symbol block
r_block = None
for s in root.find_all("symbol"):
    props = {av(p.atoms()[0]): av(p.atoms()[1]) for p in s.children
             if isinstance(p, Node) and p.head == "property" and len(p.atoms()) >= 2}
    if props.get("Reference") == "R55":
        r_block = text[s.start:s.end]
        break
assert r_block, "R55 block not found"

gnd_block = None
for s in root.find_all("symbol"):
    if s.value("lib_id") == "MoriShield_Carrier:GND":
        gnd_block = text[s.start:s.end]
        break
assert gnd_block, "GND block not found"


def make_r(ref, x, y):
    b = r_block
    b = b.replace('"R55"', '"%s"' % ref)
    b = b.replace('"100k"', '"0"')
    b = b.replace("Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder",
                  "Resistor_SMD:R_0603_1608Metric")
    b = b.replace("(at 784.86 140.97 0)", "(at %s %s 90)" % (x, y))
    b = b.replace("(at 784.86 132.08 0)", "(at %s %s 0)" % (x, y - 5.08))
    b = b.replace("(at 784.86 149.86 0)", "(at %s %s 0)" % (x, y + 5.08))
    b = re.sub(r'\(uuid "[0-9a-f-]+"\)', lambda m: '(uuid "%s")' % uuid.uuid4(), b, count=1)
    # pin uuids must be unique too
    b = re.sub(r'\(pin "(\d)"\n\t\t\t\(uuid "[0-9a-f-]+"\)',
               lambda m: '(pin "%s"\n\t\t\t(uuid "%s")' % (m.group(1), uuid.uuid4()), b)
    return b


def make_gnd(ref, x, y):
    b = gnd_block
    b = re.sub(r'"#PWR\d+"', '"%s"' % ref, b)
    b = re.sub(r"\(at [-0-9.]+ [-0-9.]+ 0\)", "(at %s %s 0)" % (x, y), b, count=1)
    b = re.sub(r'\(uuid "[0-9a-f-]+"\)', lambda m: '(uuid "%s")' % uuid.uuid4(), b, count=1)
    return b


stamp = time.strftime("%Y%m%d_%H%M%S")
snap = os.path.join(SNAP, "T55_sch_%s" % stamp)
os.makedirs(snap, exist_ok=True)
for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
          "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
    shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
print("snapshot", snap)

add = ""
add += ('\t(no_connect\n\t\t(at 113.03 327.66)\n\t\t(uuid "%s")\n\t)\n' % uuid.uuid4())
add += ('\t(no_connect\n\t\t(at 113.03 330.2)\n\t\t(uuid "%s")\n\t)\n' % uuid.uuid4())
add += make_r("R56", 478.79, 314.96)
add += make_r("R57", 478.79, 317.5)
add += make_gnd("#PWR%04d" % base_pwr, 474.98, 314.96)
add += make_gnd("#PWR%04d" % (base_pwr + 1), 474.98, 317.5)

tail = text.rstrip()
assert tail.endswith(")")
io.open(SCH, "w", encoding="utf-8", newline="").write(tail[:-1] + add + ")\n")
print("inserted 2 no-connects, R56, R57, 2 GND symbols (#PWR%04d, #PWR%04d)" % (base_pwr, base_pwr + 1))
