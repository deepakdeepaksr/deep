"""Snap the track ends that a via-centre check flags onto the via centre."""
import sys, json, math, re
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
DRC = sys.argv[1]

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]


def at(n):
    a = n.atoms()
    return (float(atom_str(a[0])), float(atom_str(a[1])))


segs = []
for c in root.children:
    if isinstance(c, Node) and c.head == "segment":
        segs.append({
            "node": c, "uuid": c.value("uuid"), "net": c.value("net"), "layer": c.value("layer"),
            "s": at(c.find("start")), "e": at(c.find("end")),
            "w": float(atom_str(c.find("width").atoms()[0])),
        })

drc = json.load(open(DRC, encoding="utf-8"))
edits = []
report = []
for v in drc["violations"]:
    if v["type"] != "track_not_centered_on_via":
        continue
    track_it = next((i for i in v["items"] if i["description"].startswith("Track")), None)
    via_it = next((i for i in v["items"] if i["description"].startswith("Via")), None)
    if not track_it or not via_it:
        continue
    m = re.search(r"Track \[([^\]]+)\] on ([^,]+), length ([0-9.]+) mm", track_it["description"])
    net, layer, length = m.group(1), m.group(2), float(m.group(3))
    tpos = (track_it["pos"]["x"], track_it["pos"]["y"])
    vpos = (via_it["pos"]["x"], via_it["pos"]["y"])

    best = None
    for s in segs:
        if s["net"] != net or s["layer"] != layer:
            continue
        L = math.hypot(s["e"][0] - s["s"][0], s["e"][1] - s["s"][1])
        if abs(L - length) > 1e-3:
            continue
        mid = ((s["s"][0] + s["e"][0]) / 2, (s["s"][1] + s["e"][1]) / 2)
        d = math.hypot(mid[0] - tpos[0], mid[1] - tpos[1])
        if best is None or d < best[0]:
            best = (d, s)
    if best is None:
        report.append((net, layer, length, "NO SEGMENT MATCH"))
        continue
    s = best[1]
    ds = math.hypot(s["s"][0] - vpos[0], s["s"][1] - vpos[1])
    de = math.hypot(s["e"][0] - vpos[0], s["e"][1] - vpos[1])
    which = "start" if ds <= de else "end"
    old = s["s"] if which == "start" else s["e"]
    node = s["node"].find(which)
    edits.append((node.start, node.end, "(%s %s %s)" % (which, round(vpos[0], 6), round(vpos[1], 6))))
    report.append((net, layer, length, "%s %s -> %s (moved %.3f mm)" % (which, old, vpos, min(ds, de))))
    s[which] = vpos

print("snapping %d track ends" % len(edits))
for r in report:
    print("   %-16s %-6s %8.4f  %s" % r)

out = text
for (st, en, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:st] + new + out[en:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
