"""Inset the TSSOP silk body, relocate its pin-1 dot, remove Q9's corner marks.

Applied identically to the board footprints and the library footprints so that
the library-match check stays clean.
"""
import sys
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
LIB = ROOT + r"\morishield\morishield_hardware\libraries\MoriShield_Carrier.pretty"


def apply(path, is_board):
    text = open(path, encoding="utf-8").read()
    root = parse(text)[0]
    edits = []
    targets = []
    if is_board:
        for fp in root.children:
            if isinstance(fp, Node) and fp.head == "footprint":
                for p in fp.children:
                    if isinstance(p, Node) and p.head == "property":
                        a = p.atoms()
                        if len(a) >= 2 and atom_str(a[0]) == "Reference":
                            r = atom_str(a[1])
                            if r in ("U7", "U8", "Q9"):
                                targets.append((r, fp))
    else:
        targets.append(("LIB", root))

    for name, fp in targets:
        for g in fp.children:
            if not (isinstance(g, Node) and g.head in ("fp_line", "fp_circle")):
                continue
            if g.value("layer") != "F.SilkS":
                continue
            s = g.find("start")
            e = g.find("end")
            c = g.find("center")
            if g.head == "fp_line" and s is not None and e is not None:
                sx, sy = [float(atom_str(x)) for x in s.atoms()[:2]]
                ex, ey = [float(atom_str(x)) for x in e.atoms()[:2]]
                if abs(sx - ex) < 1e-6 and abs(abs(sx) - 2.2) < 1e-6:
                    # TSSOP body line: inset to 1.9
                    newx = 1.9 if sx > 0 else -1.9
                    edits.append((s.start, s.end, "(start %s %s)" % (newx, sy)))
                    edits.append((e.start, e.end, "(end %s %s)" % (newx, ey)))
                elif name == "Q9":
                    # delete the whole Q9 silk line
                    lead = g.start
                    while lead > 0 and text[lead - 1] in " \t":
                        lead -= 1
                    if lead > 0 and text[lead - 1] == "\n":
                        lead -= 1
                    edits.append((lead, g.end, ""))
            elif g.head == "fp_circle" and c is not None and e is not None:
                cx, cy = [float(atom_str(x)) for x in c.atoms()[:2]]
                ex, ey = [float(atom_str(x)) for x in e.atoms()[:2]]
                if abs(cx + 2.1) < 1e-6:
                    # pin-1 dot: move inward, keep the radius
                    r = ((ex - cx) ** 2 + (ey - cy) ** 2) ** 0.5
                    edits.append((c.start, c.end, "(center -1.55 %s)" % cy))
                    edits.append((e.start, e.end, "(end %s %s)" % (round(-1.55 + r, 3), round(cy, 3))))

    out = text
    for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
        out = out[:s] + new + out[e:]
    open(path, "w", encoding="utf-8", newline="").write(out)
    return len(edits)


print("board edits: %d" % apply(PCB, True))
print("lib TSSOP edits: %d" % apply(LIB + r"\TSSOP-24_4.4x7.8mm_P0.65mm_HS.kicad_mod", False))
print("lib SOT-23_PMOS edits: %d" % apply(LIB + r"\SOT-23_PMOS_HS.kicad_mod", False))
