"""TASK C.2: relocate eight 100 nF capacitors onto the pins that need them.

Correct 0805 geometry: pad 1 at local (-1.0375, 0), pad 2 at (+1.0375, 0),
courtyard (-1.925,-1.025)-(1.925,1.025).
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

# ref, origin, rot, pad1, pad2, target pin, net, width, delete uuids
MOVES = [
    ("C41", (159.06, 103.0), 90.0, (159.06, 104.0375), (159.06, 101.9625),
     (161.06, 104.0), "+5V", 0.5, ["8d67fadd", "3258256d", "755cfaac", "67bf8957"]),
    ("C14", (169.1, 108.5), 0.0, (168.0625, 108.5), (170.1375, 108.5),
     (168.1, 104.0), "+5V", 0.5, ["d0724ba2", "3121e290", "150d4cfd", "42ddf187"]),
    ("C43", (163.94, 189.5), 90.0, (163.94, 190.5375), (163.94, 188.4625),
     (163.94, 194.5), "/3V3_SENS_SW", 0.5, ["00330a9a", "9e06db23", "b8cf2d20", "0ea2513e"]),
    ("C48", (266.75, 194.25), 90.0, (266.75, 195.2875), (266.75, 193.2125),
     (271.0, 194.5), "/3V3_SENS_SW", 0.5, ["4ff21a49", "94650d9e"]),
    ("C44", (187.75, 193.5), 90.0, (187.75, 194.5375), (187.75, 192.4625),
     (192.0, 194.5), "/3V3_SENS_SW", 0.5, ["1aa13ad5", "593e43cc", "f8db6651", "abd90ae2"]),
    ("C33", (233.5, 190.5), 90.0, (233.5, 191.5375), (233.5, 189.4625),
     (236.0, 194.5), "/+5V_SENS", 0.8, ["26083929", "949f64cf", "2b971380"]),
    ("C45", (146.13, 193.5), 90.0, (146.13, 194.5375), (146.13, 192.4625),
     (150.38, 194.5), "/3V3_SENS_SW", 0.5, ["1ef7e0fa", "309eaedc"]),
    ("C47", (171.75, 195.0), 90.0, (171.75, 196.0375), (171.75, 193.9625),
     (176.0, 194.5), "/3V3_SENS_SW", 0.5, ["780970b7", "da207b95"]),
]


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


def seg(net, w, layer, a, b):
    return ('\t(segment\n\t\t(start %s %s)\n\t\t(end %s %s)\n\t\t(width %s)\n'
            '\t\t(layer "%s")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (a[0], a[1], b[0], b[1], w, layer, net, uuid.uuid4()))


def via(net, p):
    return ('\t(via\n\t\t(at %s %s)\n\t\t(size 0.6)\n\t\t(drill 0.3)\n'
            '\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n' %
            (p[0], p[1], net, uuid.uuid4()))


def main():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    snap = os.path.join(SNAP, "T_C_caps_%s" % stamp)
    os.makedirs(snap, exist_ok=True)
    for f in ("MoriShield_Carrier.kicad_pcb", "MoriShield_Carrier.kicad_pro",
              "MoriShield_Carrier.kicad_sch", "MoriShield_Carrier.kicad_dru"):
        shutil.copy(os.path.join(ROOT, "pcb", f), os.path.join(snap, f))
    before = census(PCB)
    json.dump({"before": before, "snapshot": snap}, open(os.path.join(snap, "census.json"), "w"), indent=1)
    print("snapshot", snap, before)

    text = open(PCB, encoding="utf-8").read()
    for (ref, origin, rot, pad1, pad2, target, net, w, dels) in MOVES:
        root = parse(text)[0]
        fp = find_fp(root, ref)
        assert fp is not None, ref
        at = fp.find("at")
        text = text[:at.start] + "(at %s %s %s)" % (origin[0], origin[1], rot) + text[at.end:]
        for d in dels:
            root = parse(text)[0]
            hit = None
            for c in root.children:
                if isinstance(c, Node) and c.head in ("segment", "via") and (c.value("uuid") or "").startswith(d):
                    hit = c
                    break
            if hit is None:
                print("  WARN %s uuid %s not found" % (ref, d))
                continue
            s = hit.start
            while s > 0 and text[s - 1] in " \t":
                s -= 1
            if s > 0 and text[s - 1] == "\n":
                s -= 1
            text = text[:s] + text[hit.end:]
        tail = text.rstrip()
        text = tail[:-1] + seg(net, w, "F.Cu", pad1, target) + via("GND", pad2) + ")\n"
        print("moved %s to (%.2f,%.2f) rot %.0f  pad1 (%.4f,%.4f)" % (ref, origin[0], origin[1], rot, pad1[0], pad1[1]))

    open(PCB, "w", encoding="utf-8", newline="").write(text)
    after = census(PCB)
    print("after:", after)
    json.dump({"before": before, "after": after, "snapshot": snap},
              open(os.path.join(HERE, "taskC_census.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
