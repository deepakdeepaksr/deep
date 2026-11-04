"""TASK 1: add GND stitching vias to restore E1."""
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

VIAS = [(277.0, 90.0), (164.0, 186.0)]


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


def via_block(x, y):
    return ('\t(via\n\t\t(at %s %s)\n\t\t(size 0.6)\n\t\t(drill 0.3)\n'
            '\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "GND")\n\t\t(uuid "%s")\n\t)\n' %
            (x, y, uuid.uuid4()))


def main():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    snap = os.path.join(SNAP, "T1_E1_%s" % stamp)
    os.makedirs(snap, exist_ok=True)
    for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
              "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
        shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
    before = census(PCB)
    json.dump({"before": before, "snapshot": snap}, open(os.path.join(snap, "census.json"), "w"), indent=1)
    print("snapshot", snap, before)

    text = open(PCB, encoding="utf-8").read()
    tail = text.rstrip()
    text = tail[:-1] + "".join(via_block(x, y) for (x, y) in VIAS) + ")\n"
    open(PCB, "w", encoding="utf-8", newline="").write(text)
    print("added %d GND vias:" % len(VIAS), VIAS)
    print("after:", census(PCB))


if __name__ == "__main__":
    main()
