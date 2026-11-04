"""TASK B: move J5 out from under the modem to (222.0, 91.4) rot 0; reroute the
1.5 mm +5V feed on In2; move D7's reference field off J5's silk. Board-only.
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

NEW = (222.0, 91.4)
DELETE_UUID_PREFIX = "36c320bc"      # +5V In2 239.51,95.83-232.92,95.83 (fed old J5.1)
ADD_SEG = ("+5V", 1.5, "In2.Cu", (222.0, 91.4), (232.92, 95.83))
D7_REF = (220.0, 101.0)


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


def find_fp(root, ref):
    for c in root.children:
        if isinstance(c, Node) and c.head == "footprint":
            for p in c.children:
                if isinstance(p, Node) and p.head == "property":
                    a = p.atoms()
                    if len(a) >= 2 and a[0][1] == "Reference" and a[1][1] == ref:
                        return c
    return None


def main():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    snap = os.path.join(SNAP, "T_B_J5_%s" % stamp)
    os.makedirs(snap, exist_ok=True)
    for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
              "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
        shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
    before = census(PCB)
    json.dump({"before": before, "snapshot": snap}, open(os.path.join(snap, "census.json"), "w"), indent=1)
    print("snapshot", snap, before)

    text = open(PCB, encoding="utf-8").read()

    # 1. move J5
    root = parse(text)[0]
    fp = find_fp(root, "J5")
    at = fp.find("at")
    text = text[:at.start] + "(at %s %s)" % NEW + text[at.end:]
    print("moved J5 to", NEW)

    # 2. D7 reference field
    root = parse(text)[0]
    fp = find_fp(root, "D7")
    for p in fp.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and a[0][1] == "Reference":
                at = p.find("at")
                text = text[:at.start] + "(at %s %s 0)" % D7_REF + text[at.end:]
                print("moved D7 reference to", D7_REF)
                break

    # 3. delete the old feed segment
    root = parse(text)[0]
    for c in root.children:
        if isinstance(c, Node) and c.head == "segment" and (c.value("uuid") or "").startswith(DELETE_UUID_PREFIX):
            s = c.start
            while s > 0 and text[s - 1] in " \t":
                s -= 1
            if s > 0 and text[s - 1] == "\n":
                s -= 1
            text = text[:s] + text[c.end:]
            print("deleted old feed segment")
            break

    # 4. add the new feed
    net, width, layer, a, b = ADD_SEG
    blk = ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width %s)\n'
           '\t\t(layer "%s")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
           (a[0], a[1], b[0], b[1], width, layer, net, uuid.uuid4()))
    tail = text.rstrip()
    text = tail[:-1] + blk + ")\n"
    open(PCB, "w", encoding="utf-8", newline="").write(text)
    after = census(PCB)
    print("after text surgery:", after)
    json.dump({"before": before, "after": after, "snapshot": snap},
              open(os.path.join(HERE, "taskB_census.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
