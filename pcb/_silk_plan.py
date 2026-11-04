"""Classify every silk violation into a fix: delete a graphic, or move a field."""
import sys, json, collections, re
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
DRC = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC\_drc_afterpe2.json"
text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

def at(n):
    a = n.atoms()
    return (float(atom_str(a[0])), float(atom_str(a[1]))) if len(a) >= 2 else None

# map ref -> footprint node
fps = {}
for fp in root.children:
    if isinstance(fp, Node) and fp.head == "footprint":
        for p in fp.children:
            if isinstance(p, Node) and p.head == "property":
                a = p.atoms()
                if len(a) >= 2 and atom_str(a[0]) == "Reference":
                    fps[atom_str(a[1])] = fp

drc = json.load(open(DRC, encoding="utf-8"))
graphic_re = re.compile(r"^(Segment|Polygon|Circle|Rectangle|Arc) of ([A-Z]+[0-9]+) on F\.Silkscreen$")
pad_re = re.compile(r"^Pad .* of ([A-Z]+[0-9]+) on F\.Cu$")
field_re = re.compile(r"^(Reference|Value) field of ([A-Z]+[0-9]+)$")

delete_graphics = collections.defaultdict(list)   # ref -> [(head, pos)]
move_fields = set()
unclassified = []

for v in drc["violations"]:
    if not v["type"].startswith("silk"):
        continue
    items = [it.get("description", "") for it in v.get("items", [])]
    pos = (v["items"][0]["pos"]["x"], v["items"][0]["pos"]["y"]) if v.get("items") else None
    kinds = []
    for d in items:
        m = graphic_re.match(d)
        if m:
            kinds.append(("graphic", m.group(2), m.group(1)))
            continue
        m = field_re.match(d)
        if m:
            kinds.append(("field", m.group(2), m.group(1)))
            continue
        m = pad_re.match(d)
        if m:
            kinds.append(("pad", m.group(1), None))
            continue
        kinds.append(("other", None, d))

    g = [k for k in kinds if k[0] == "graphic"]
    f = [k for k in kinds if k[0] == "field"]
    p = [k for k in kinds if k[0] == "pad"]

    if v["type"] == "silk_over_copper":
        if p and g:
            # the graphic crosses a pad: delete the graphic
            for k in g:
                delete_graphics[k[1]].append((k[2], pos))
        elif p and f:
            move_fields.add(f[0][1])
        else:
            unclassified.append((v["type"], items, pos))
    else:  # silk_overlap
        if f and g:
            move_fields.add(f[0][1])
        elif f and not g:
            move_fields.add(f[0][1])
        elif g and not f:
            # two graphics overlap: delete the one that is a field? both graphics.
            # delete the first one named
            delete_graphics[g[0][1]].append((g[0][2], pos))
        else:
            unclassified.append((v["type"], items, pos))

print("fields to move (%d): %s" % (len(move_fields), ", ".join(sorted(move_fields))))
print("graphics to delete:")
for ref, lst in sorted(delete_graphics.items()):
    print("  %-7s %d  %s" % (ref, len(lst), collections.Counter(h for h, _ in lst)))
print("unclassified: %d" % len(unclassified))
for u in unclassified[:10]:
    print("   ", u)

json.dump({"move_fields": sorted(move_fields),
           "delete_graphics": {k: [(h, list(p) if p else None) for h, p in v] for k, v in delete_graphics.items()},
           "unclassified": [[u[0], u[1], list(u[2]) if u[2] else None] for u in unclassified]},
          open(r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC\_silk_plan.json", "w"), indent=1)
