"""TASK E.1: move the +5V In2.Cu feed to F.Cu (it is the only In2 net with a free
outer corridor). Reverts are a file copy from the snapshot."""
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


def seg(net, w, layer, a, b):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width %s)\n'
            '\t\t(layer "%s")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (a[0], a[1], b[0], b[1], w, layer, net, uuid.uuid4()))


def main():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    snap = os.path.join(SNAP, "T_E_in2_%s" % stamp)
    os.makedirs(snap, exist_ok=True)
    for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
              "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
        shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
    before = census(PCB)
    print("snapshot", snap, before)

    text = open(PCB, encoding="utf-8").read()
    root = parse(text)[0]
    found = []
    for c in root.children:
        if isinstance(c, Node) and c.head == "segment" and c.value("net") == "+5V":
            if c.find("layer") and c.find("layer").atoms()[0][1] == "In2.Cu":
                found.append(c)
    print("In2 +5V segments:", len(found))
    adds = []
    for c in sorted(found, key=lambda n: -n.start):
        def av(v):
            return v[1] if isinstance(v, tuple) else v
        s = c.find("start").atoms()
        e = c.find("end").atoms()
        a = (av(s[0]), av(s[1]))
        b = (av(e[0]), av(e[1]))
        adds.append((a, b))
        st = c.start
        while st > 0 and text[st - 1] in " \t":
            st -= 1
        if st > 0 and text[st - 1] == "\n":
            st -= 1
        text = text[:st] + text[c.end:]
    tail = text.rstrip()
    text = tail[:-1] + "".join(seg("+5V", 1.5, "F.Cu", a, b) for (a, b) in adds) + ")\n"
    open(PCB, "w", encoding="utf-8", newline="").write(text)
    print("moved %d +5V segments to F.Cu" % len(adds), adds)
    print("after:", census(PCB))


if __name__ == "__main__":
    main()
