"""Add a courtyard (land-pattern extent + 0.25 mm) to U4 and SW1, board and library."""
import sys, uuid
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
LIB = ROOT + r"\morishield\morishield_hardware\libraries\MoriShield_Carrier.pretty"

# (x0, y0, x1, y1) relative to the footprint origin, land extent + 0.25 mm
BOXES = {
    "U4": (-2.70, -1.50, 2.70, 1.50),
    "SW1": (-4.25, -3.25, 4.25, 3.25),
}


def rect(box):
    x0, y0, x1, y1 = box
    return ('\t(fp_rect\n'
            '\t\t(start %s %s)\n'
            '\t\t(end %s %s)\n'
            '\t\t(stroke\n\t\t\t(width 0.05)\n\t\t\t(type solid)\n\t\t)\n'
            '\t\t(fill none)\n'
            '\t\t(layer "F.CrtYd")\n'
            '\t\t(uuid "%s")\n'
            '\t)\n') % (x0, y0, x1, y1, uuid.uuid4())


def add_to(path, refs):
    text = open(path, encoding="utf-8").read()
    root = parse(text)[0]
    targets = []
    if refs is None:
        targets = [(None, root)]
    else:
        for fp in root.children:
            if isinstance(fp, Node) and fp.head == "footprint":
                for p in fp.children:
                    if isinstance(p, Node) and p.head == "property":
                        a = p.atoms()
                        if len(a) >= 2 and atom_str(a[0]) == "Reference" and atom_str(a[1]) in refs:
                            targets.append((atom_str(a[1]), fp))
    inserts = []
    for ref, fp in targets:
        key = ref if ref in BOXES else ("U4" if "SOT-23-5" in str(atom_str(fp.atoms()[0])) else "SW1")
        payload = rect(BOXES[key])
        # insert before the final closing paren of the footprint
        idx = fp.end - 1
        while idx > fp.start and text[idx] != ")":
            idx -= 1
        inserts.append((idx, payload))
    out = text
    for (idx, payload) in sorted(inserts, key=lambda x: -x[0]):
        out = out[:idx] + payload + out[idx:]
    open(path, "w", encoding="utf-8", newline="").write(out)
    return len(inserts)


print("board courtyards added:", add_to(PCB, {"U4", "SW1"}))
print("lib SOT-23-5_HS:", add_to(LIB + r"\SOT-23-5_HS.kicad_mod", None))
print("lib SW_6x6:", add_to(LIB + r"\SW_6x6.kicad_mod", None))
