"""TASK D.1/D.2/D.4: clear the port band, then print the port labels and the J6 marking."""
import os
import shutil
import sys
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
SNAP = os.path.join(ROOT, "pcb", "_snap")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402

# reference fields to move off the port band: ref -> new (x, y, rot)
FIELDS = {
    "J11": (176.0, 203.9, 0), "J12": (192.0, 203.9, 0), "J13": (236.0, 203.9, 0),
    "J14": (250.0, 203.9, 0), "J15": (150.38, 203.9, 0), "J16": (163.94, 203.9, 0),
    "J17": (271.0, 203.9, 0), "J21": (285.0, 203.9, 0),
    "J20": (291.0, 144.6, 0), "J22": (128.6, 116.0, 0), "J26": (135.0, 156.0, 0),
    "ESD3": (148.0, 186.5, 0), "ESD11": (231.0, 186.0, 0), "C45": (233.0, 191.0, 0),
}
# board texts moved into the empty gap between J12 and J13
BOARD_TEXTS = {
    "MoriShield Carrier": (206.0, 200.0),
    "Rev C": (206.0, 202.6),
    "S/N": (219.0, 202.6),
}
# port labels: text, x, y, rot
LABELS = [
    ("SOIL", 150.38, 201.3, 0), ("FSR", 163.94, 201.3, 0), ("SGP41", 176.0, 201.3, 0),
    ("SHT45", 192.0, 201.3, 0), ("SPS30", 236.0, 201.3, 0), ("BME688", 250.0, 201.3, 0),
    ("BUZZ", 139.31, 201.3, 0),
    ("REED", 135.2, 125.0, 0), ("WIND", 134.0, 158.8, 0), ("LED", 128.6, 147.0, 90),
    ("RTC", 157.65, 164.4, 0), ("IMU", 212.11, 169.3, 0),
]
# J6 marking: pin functions down the left of the pads and the pin-1 end marked
J6 = [("1", 260.9, 160.6, 0), ("M0", 261.6, 162.38, 0), ("M1", 261.6, 164.92, 0),
      ("TXD", 261.6, 167.46, 0), ("RXD", 261.6, 170.0, 0), ("AUX", 261.6, 172.54, 0),
      ("5V", 261.6, 175.08, 0), ("GND", 261.6, 177.62, 0)]


def find_fp(root, ref):
    for c in root.children:
        if isinstance(c, Node) and c.head == "footprint":
            for p in c.children:
                if isinstance(p, Node) and p.head == "property":
                    a = p.atoms()
                    if len(a) >= 2 and a[0][1] == "Reference" and a[1][1] == ref:
                        return c
    return None


def text_block(txt, x, y, rot):
    return ('\t(gr_text "%s"\n\t\t(at %s %s %s)\n\t\t(layer "F.SilkS")\n'
            '\t\t(uuid "%s")\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1 1)\n'
            '\t\t\t\t(thickness 0.15)\n\t\t\t)\n\t\t\t(justify right)\n\t\t)\n\t)\n' %
            (txt, x, y, rot, uuid.uuid4()))


def main():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    snap = os.path.join(SNAP, "T_D_silk_%s" % stamp)
    os.makedirs(snap, exist_ok=True)
    for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
              "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
        shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
    print("snapshot", snap)

    text = open(PCB, encoding="utf-8").read()

    for ref, (x, y, rot) in FIELDS.items():
        root = parse(text)[0]
        fp = find_fp(root, ref)
        if fp is None:
            print("WARN no footprint", ref)
            continue
        for p in fp.children:
            if isinstance(p, Node) and p.head == "property":
                a = p.atoms()
                if len(a) >= 2 and a[0][1] == "Reference":
                    at = p.find("at")
                    text = text[:at.start] + "(at %s %s %s)" % (x, y, rot) + text[at.end:]
                    break

    # board texts
    for txt, (x, y) in BOARD_TEXTS.items():
        root = parse(text)[0]
        for c in root.children:
            if isinstance(c, Node) and c.head == "gr_text" and c.atoms() and c.atoms()[0][1] == txt:
                at = c.find("at")
                text = text[:at.start] + "(at %s %s 0)" % (x, y) + text[at.end:]
                break

    tail = text.rstrip()
    if os.environ.get("FIELDS_ONLY"):
        open(PCB, "w", encoding="utf-8", newline="").write(text)
        print("fields moved only (no labels)")
        return
    add = "".join(text_block(t, x, y, r) for (t, x, y, r) in LABELS)
    add += "".join(text_block(t, x, y, r) for (t, x, y, r) in J6)
    text = tail[:-1] + add + ")\n"
    open(PCB, "w", encoding="utf-8", newline="").write(text)
    print("fields moved, %d labels + %d J6 marks added" % (len(LABELS), len(J6)))


if __name__ == "__main__":
    main()
