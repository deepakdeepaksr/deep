"""List the PE segments that the PE floor flags, with their neighbours."""
import sys, json
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
DRC = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC\_drc_after3v3.json"
text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

def at(n):
    a = n.atoms()
    return (float(a[0]), float(a[1])) if len(a) >= 2 else None

flags = []
drc = json.load(open(DRC, encoding="utf-8"))
for v in drc["violations"]:
    if v["type"] == "track_width":
        it = v["items"][0]
        flags.append((it["pos"]["x"], it["pos"]["y"], v["description"]))

print("flagged positions:", flags)

for c in root.children:
    if not (isinstance(c, Node) and c.head == "segment"):
        continue
    if c.value("net") != "PE":
        continue
    w = float(c.value("width"))
    if w >= 0.6:
        continue
    s, e = at(c.find("start")), at(c.find("end"))
    print("SEG uuid=%s layer=%s width=%s start=%s end=%s" % (c.value("uuid"), c.value("layer"), w, s, e))
    # vias at either end
    for d in root.children:
        if isinstance(d, Node) and d.head == "via":
            p = at(d.find("at"))
            if p in (s, e):
                print("   via at %s uuid=%s net=%s" % (p, d.value("uuid"), d.value("net")))
    # other PE segments sharing an endpoint
    for d in root.children:
        if isinstance(d, Node) and d.head == "segment" and d is not c and d.value("net") == "PE":
            ds, de = at(d.find("start")), at(d.find("end"))
            if {ds, de} & {s, e}:
                print("   neighbour uuid=%s w=%s %s-%s layer=%s" % (d.value("uuid"), d.value("width"), ds, de, d.value("layer")))
