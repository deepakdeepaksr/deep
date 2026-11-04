import sys, json, collections
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
text = open(PCB, encoding="utf-8").read()
roots = parse(text)
root = roots[0]
print("root:", root.head, "children:", len(root.children))

fps = [c for c in root.children if isinstance(c, Node) and c.head == "footprint"]
print("footprints:", len(fps))

def ref_of(fp):
    for p in fp.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and a[0] == "Reference":
                return a[1][1] if isinstance(a[1], tuple) else a[1]
    return None

info = {}
for fp in fps:
    r = ref_of(fp)
    silks = [n for n in fp.children if isinstance(n, Node) and n.head in ("fp_line", "fp_arc", "fp_circle", "fp_poly", "fp_rect")
             and any(isinstance(c, Node) and c.head == "layer" and c.atoms() and c.atoms()[0] == ("q", "F.SilkS") for c in n.children)]
    texts = [n for n in fp.children if isinstance(n, Node) and n.head == "fp_text"]
    info[r] = {"block": (fp.start, fp.end), "lines": text.count("\n", fp.start, fp.end) + 1,
               "silk_graphics": len(silks), "fp_text": len(texts),
               "fpid": fp.atoms()[0][1] if fp.atoms() and isinstance(fp.atoms()[0], tuple) else None}

for r in ["U7", "U8", "C31", "C4", "Q9", "ESD11", "C44"]:
    print(r, info.get(r))
print("total silk graphics items:", sum(v["silk_graphics"] for v in info.values()))
print("largest blocks:")
for r, v in sorted(info.items(), key=lambda kv: -kv[1]["lines"])[:8]:
    print("  ", r, v["lines"], v["silk_graphics"], v["fpid"])
