"""TASK D.5: name the ports in the schematic Value field (property edit only) and keep
the board footprint Value in step."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SCH = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch")
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402

VALUES = {
    "J7": "GY-521_MPU6050", "J8": "DS3231_RTC", "J11": "SGP41", "J12": "SHT45",
    "J13": "SPS30_5V", "J14": "BME688", "J15": "SOIL_ANALOG", "J16": "FSR_ANALOG",
    "J22": "REED_WIND_SPEED", "J26": "AS5600_WIND_DIR",
}


def av(v):
    return v[1] if isinstance(v, tuple) else v


def set_value(path, head, ref_key, wanted):
    text = open(path, encoding="utf-8").read()
    changed = 0
    for ref, val in wanted.items():
        root = parse(text)[0]
        target = None
        for c in root.children:
            if isinstance(c, Node) and c.head == head:
                props = [p for p in c.children if isinstance(p, Node) and p.head == "property"]
                r = None
                for p in props:
                    a = p.atoms()
                    if len(a) >= 2 and av(a[0]) == "Reference":
                        r = av(a[1])
                if r == ref:
                    target = (c, props)
                    break
        if target is None:
            print("  %s not found in %s" % (ref, os.path.basename(path)))
            continue
        c, props = target
        for p in props:
            a = p.atoms()
            if len(a) >= 2 and av(a[0]) == "Value":
                old = av(a[1])
                if old == val:
                    continue
                s = p.start
                # replace only the quoted value atom
                q = text.find('"', s)
                q2 = text.find('"', q + 1)
                text = text[:q] + '"%s"' % val + text[q2 + 1:]
                changed += 1
                print("  %s: %s -> %s" % (ref, old, val))
                break
    open(path, "w", encoding="utf-8", newline="").write(text)
    return changed


n1 = set_value(SCH, "symbol", "Reference", VALUES)
n2 = set_value(PCB, "footprint", "Reference", VALUES)
print("schematic %d, board %d" % (n1, n2))
