"""TASK A: move J26 from under the DS3231 to the left-edge pocket at (134.0, 153.5).

Board-only. Text surgery on the balanced blocks (rule 4); no board.Remove().
"""
import json
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

OLD = (162.45, 181.35)
NEW = (134.0, 153.5)
OLD_STUBS = {
    "9e33446e-adb8-4e74-bd8f-e9e082b0a09e": "3V3_C stub",
    "00cbbea6-dd06-46ee-9685-2aa2abbd6f22": "GND stub",
    "e52d0386-b974-42da-a5b4-faa15ce2117e": "/I2C1_SDA stub",
    "858dada0-c680-4d13-ae95-a980038c30c3": "/I2C1_SCL stub",
    # dead branches that existed only to feed the old J26 position
    "04e04363-5206-4dff-8b3f-90763adcdaf9": "3V3_C via 162.5,175.75",
    "99c1fb15-4cba-445c-b1ed-e65ea7084216": "3V3_C B.Cu 162.5,175.75-165.25,166.75",
    "488736aa-7f77-4c4f-bea1-32d14871af74": "3V3_C via 165.25,166.75",
    "faf76439-1ce5-495c-9060-163233e57447": "3V3_C F.Cu 165.25,166.75-167.75,161.5",
    "f6800f7e-eefe-40b8-8bae-41e5de6072c6": "SDA F.Cu 171.5,166.75-172.5,165.75",
    "b7ae2b55-8240-432d-8f90-1482dfdd43b3": "SDA via 172.5,165.75",
    "1d6f6c03-d74f-4334-9094-55203bbb0002": "SDA B.Cu 172.5,165.75-169.5,164.5",
    "a6e56e2a-7dd4-437f-8a23-cb13086b904b": "SDA B.Cu 169.5,164.5-165.5,164.5",
    "8879934d-5008-4614-8edb-c95f5e8fa035": "SDA B.Cu 165.5,164.5-164.75,163.75",
    "ec6813dd-ad18-43f2-8a63-573f2a4c91a3": "SDA B.Cu 164.75,163.75-165.25,161.5",
    "f8e2f164-ebde-4dcf-96e5-877337e0c4e2": "SCL via 168.5,169.75",
    "ca8e5d89-98b1-4ada-84db-796778cfc95c": "SCL B.Cu 168.5,169.75-168.5,166.5",
    "c14aca4e-456c-4bca-871b-5f1dbeb63101": "SCL B.Cu 168.5,166.5-167.5,165.5",
    "aefbbb43-6b93-4cd8-993a-98d7b1bfa865": "SCL B.Cu 167.5,165.5-164.5,165.5",
    "48b48b3b-8304-4c37-a92e-6baf8d0b06ac": "SCL B.Cu 164.5,165.5-164,165",
    "76956867-23de-4110-aa18-76f55e6bed7d": "SCL B.Cu 164,165-162.75,161.5",
}

# routed plan: (net, width, layer, [(x0,y0),(x1,y1)])
SEGS = [
    ("3V3_C", 0.30, "F.Cu", (134.00, 153.50), (136.80, 156.40)),
    ("3V3_C", 0.30, "F.Cu", (136.80, 156.40), (137.90, 156.40)),
    ("3V3_C", 0.30, "F.Cu", (137.90, 156.40), (140.20, 157.50)),
    ("3V3_C", 0.30, "F.Cu", (140.20, 157.50), (141.40, 157.60)),
    ("3V3_C", 0.30, "F.Cu", (141.40, 157.60), (142.20, 158.40)),
    ("3V3_C", 0.30, "F.Cu", (142.20, 158.40), (143.549999, 158.999999)),
    ("/I2C1_SCL", 0.25, "F.Cu", (139.00, 153.50), (141.80, 156.40)),
    ("/I2C1_SCL", 0.25, "F.Cu", (141.80, 156.40), (147.40, 156.50)),
    ("/I2C1_SCL", 0.25, "F.Cu", (147.40, 156.50), (152.00, 158.60)),
    ("/I2C1_SCL", 0.25, "F.Cu", (152.00, 158.60), (153.20, 159.80)),
    ("/I2C1_SCL", 0.25, "B.Cu", (153.20, 159.80), (153.50, 159.80)),
    ("/I2C1_SCL", 0.25, "B.Cu", (153.50, 159.80), (155.30, 161.60)),
    ("/I2C1_SCL", 0.25, "F.Cu", (155.30, 161.60), (156.50, 162.80)),
    ("/I2C1_SCL", 0.25, "F.Cu", (156.50, 162.80), (161.50, 162.80)),
    ("/I2C1_SCL", 0.25, "F.Cu", (161.50, 162.80), (162.73, 161.57)),
    ("/I2C1_SDA", 0.25, "F.Cu", (141.50, 153.50), (141.70, 153.70)),
    ("/I2C1_SDA", 0.25, "F.Cu", (141.70, 153.70), (142.40, 153.70)),
    ("/I2C1_SDA", 0.25, "F.Cu", (142.40, 153.70), (143.40, 154.70)),
    ("/I2C1_SDA", 0.25, "F.Cu", (143.40, 154.70), (156.90, 154.70)),
    ("/I2C1_SDA", 0.25, "F.Cu", (156.90, 154.70), (157.60, 155.40)),
    ("/I2C1_SDA", 0.25, "B.Cu", (157.60, 155.40), (158.80, 156.60)),
    ("/I2C1_SDA", 0.25, "F.Cu", (158.80, 156.60), (162.60, 160.20)),
    ("/I2C1_SDA", 0.25, "F.Cu", (162.60, 160.20), (163.90, 160.20)),
    ("/I2C1_SDA", 0.25, "F.Cu", (163.90, 160.20), (165.27, 160.20)),
    ("/I2C1_SDA", 0.25, "F.Cu", (165.27, 160.20), (165.27, 161.50)),
]
VIAS = [("/I2C1_SCL", (153.20, 159.80)), ("/I2C1_SCL", (155.30, 161.60)),
        ("/I2C1_SDA", (157.60, 155.40)), ("/I2C1_SDA", (158.80, 156.60))]


def seg_block(net, width, layer, a, b):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width %s)\n'
            '\t\t(layer "%s")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (a[0], a[1], b[0], b[1], width, layer, net, uuid.uuid4()))


def via_block(net, p):
    return ('\t(via\n\t\t(at %s %s)\n\t\t(size 0.6)\n\t\t(drill 0.3)\n'
            '\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (p[0], p[1], net, uuid.uuid4()))


def census(path):
    out = {"footprints": 0, "segments": 0, "vias": 0, "zones": 0}
    for line in open(path, encoding="utf-8"):
        t = line.strip()
        if t == "(segment":
            out["segments"] += 1
        elif t == "(via":
            out["vias"] += 1
        elif t == "(zone":
            out["zones"] += 1
        elif t.startswith("(footprint "):
            out["footprints"] += 1
    return out


def main():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    snap = os.path.join(SNAP, "T_A_J26_%s" % stamp)
    os.makedirs(snap, exist_ok=True)
    for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
              "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
        shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
    before = census(PCB)
    json.dump({"before": before, "snapshot": snap}, open(os.path.join(snap, "census.json"), "w"), indent=1)
    print("snapshot", snap, before)

    text = open(PCB, encoding="utf-8").read()
    root = parse(text)[0]

    # 1. move the J26 footprint origin
    fp = None
    for c in root.children:
        if isinstance(c, Node) and c.head == "footprint":
            for p in c.children:
                if isinstance(p, Node) and p.head == "property":
                    a = p.atoms()
                    if len(a) >= 2 and a[0][1] == "Reference" and a[1][1] == "J26":
                        fp = c
                        break
    assert fp is not None, "J26 footprint not found"
    at = fp.find("at")
    assert at is not None
    s0, e0 = at.start, at.end
    text = text[:s0] + "(at %s %s)" % (NEW[0], NEW[1]) + text[e0:]
    print("moved J26 origin to", NEW)

    # 2. delete the four old stubs by UUID (balanced blocks)
    removed = 0
    for uid, net in OLD_STUBS.items():
        root = parse(text)[0]
        target = None
        for c in root.children:
            if isinstance(c, Node) and c.head in ("segment", "via") and c.value("uuid") == uid:
                target = c
                break
        if target is None:
            print("  WARN stub not found", uid)
            continue
        s = target.start
        while s > 0 and text[s - 1] in " \t":
            s -= 1
        if s > 0 and text[s - 1] == "\n":
            s -= 1
        text = text[:s] + text[target.end:]
        removed += 1
    print("removed %d old stubs" % removed)

    # 3. append new copper just before the closing paren of the board
    tail = text.rstrip()
    assert tail.endswith(")")
    body = tail[:-1]
    add = "".join(seg_block(n, w, l, a, b) for (n, w, l, a, b) in SEGS)
    add += "".join(via_block(n, p) for (n, p) in VIAS)
    text = body + add + ")\n"
    open(PCB, "w", encoding="utf-8", newline="").write(text)
    after = census(PCB)
    print("after text surgery:", after)
    json.dump({"before": before, "after": after, "snapshot": snap},
              open(os.path.join(HERE, "taskA_census.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
