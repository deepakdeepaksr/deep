"""Repair the Value property edit: the property NAME was overwritten instead of the value."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402

VALUES = {
    "J7": "GY-521_MPU6050", "J8": "DS3231_RTC", "J11": "SGP41", "J12": "SHT45",
    "J13": "SPS30_5V", "J14": "BME688", "J15": "SOIL_ANALOG", "J16": "FSR_ANALOG",
    "J22": "REED_WIND_SPEED", "J26": "AS5600_WIND_DIR",
}


def av(v):
    return v[1] if isinstance(v, tuple) else v


def repair(path, head):
    text = open(path, encoding="utf-8").read()
    for ref, want in VALUES.items():
        root = parse(text)[0]
        target = None
        for c in root.children:
            if isinstance(c, Node) and c.head == head:
                props = [p for p in c.children if isinstance(p, Node) and p.head == "property"]
                names = {}
                for p in props:
                    a = p.atoms()
                    if len(a) >= 2:
                        names[av(a[0])] = av(a[1])
                if names.get("Reference") == ref:
                    target = props
                    break
        if target is None:
            print("  %s not found" % ref)
            continue
        for p in target:
            a = p.atoms()
            if len(a) < 2:
                continue
            key = av(a[0])
            if key == want:
                q1 = text.find('"', p.start)
                q2 = text.find('"', q1 + 1)
                q3 = text.find('"', q2 + 1)
                q4 = text.find('"', q3 + 1)
                text = text[:q1] + '"Value"' + text[q2 + 1:q3] + '"%s"' % want + text[q4 + 1:]
                print("  %s repaired -> Value=%s" % (ref, want))
                break
    open(path, "w", encoding="utf-8", newline="").write(text)


repair(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch"), "symbol")
repair(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"), "footprint")
