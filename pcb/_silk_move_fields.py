"""Silk cleanup: graphics edits in board + library, and reference-field placement."""
import sys, json, math, re
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str
import pcbnew

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
LIB = ROOT + r"\morishield\morishield_hardware\libraries\MoriShield_Carrier.pretty"
PLAN = json.load(open(ROOT + r"\revC\_silk_plan.json", encoding="utf-8"))

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

def at(n):
    if n is None:
        return None
    a = n.atoms()
    return (float(atom_str(a[0])), float(atom_str(a[1]))) if len(a) >= 2 else None

# ---------------------------------------------------------------- geometry
b = pcbnew.LoadBoard(PCB)
pads = []          # (x0,y0,x1,y1)
for f in b.GetFootprints():
    for p in f.Pads():
        bb = p.GetBoundingBox()
        pads.append((bb.GetX() / 1e6, bb.GetY() / 1e6, bb.GetRight() / 1e6, bb.GetBottom() / 1e6))

def fp_of(ref):
    for fp in root.children:
        if isinstance(fp, Node) and fp.head == "footprint":
            for p in fp.children:
                if isinstance(p, Node) and p.head == "property":
                    a = p.atoms()
                    if len(a) >= 2 and atom_str(a[0]) == "Reference" and atom_str(a[1]) == ref:
                        return fp
    return None

def fp_origin(fp):
    a = fp.find("at").atoms()
    return float(atom_str(a[0])), float(atom_str(a[1])), (float(atom_str(a[2])) if len(a) > 2 else 0.0)

def rot_pt(x, y, deg):
    r = math.radians(deg)
    return (x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r))

def graphic_bbox(g, ox, oy, rot):
    """absolute bbox of an fp_line / fp_circle / fp_poly, approximate"""
    head = g.head
    pts = []
    if head in ("fp_line", "fp_rect"):
        for k in ("start", "end"):
            p = at(g.find(k))
            if p:
                pts.append(rot_pt(p[0], p[1], rot))
    elif head == "fp_circle":
        c = at(g.find("center"))
        e = at(g.find("end"))
        if c and e:
            r = math.hypot(e[0] - c[0], e[1] - c[1])
            pts = [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]
    elif head in ("fp_poly", "fp_arc"):
        for n in g.find_all("xy"):
            p = at(n)
            if p:
                pts.append(rot_pt(p[0], p[1], rot))
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (ox + min(xs), oy + min(ys), ox + max(xs), oy + max(ys))

# obstacles: pads + all silk graphics + board texts
obstacles = list(pads)
for fp in root.children:
    if not (isinstance(fp, Node) and fp.head == "footprint"):
        continue
    ox, oy, rot = fp_origin(fp)
    for g in fp.children:
        if isinstance(g, Node) and g.head in ("fp_line", "fp_circle", "fp_poly", "fp_arc", "fp_rect"):
            if g.value("layer") != "F.SilkS":
                continue
            bb = graphic_bbox(g, ox, oy, rot)
            if bb:
                obstacles.append(bb)
for d in root.children:
    if isinstance(d, Node) and d.head == "gr_text" and d.value("layer") == "F.SilkS":
        p = at(d.find("at"))
        s = d.value("size") if d.find("size") else None
        t = d.value("text") or ""
        if p:
            obstacles.append((p[0] - 0.6 * len(t), p[1] - 0.8, p[0] + 0.6 * len(t), p[1] + 0.8))

def overlap(a, b_):
    dx = min(a[2], b_[2]) - max(a[0], b_[0])
    dy = min(a[3], b_[3]) - max(a[1], b_[1])
    return max(0.0, dx) * max(0.0, dy)

def text_bbox(cx, cy, s, h, rot):
    w = (len(s) * 0.80 + 0.4) * h
    hh = 1.35 * h
    if rot % 180 == 90:
        w, hh = hh, w
    return (cx - w / 2, cy - hh / 2, cx + w / 2, cy + hh / 2)

# ---------------------------------------------------------------- field moves
moved = []
for ref in PLAN["move_fields"]:
    fp = fp_of(ref)
    if fp is None:
        continue
    ox, oy, frot = fp_origin(fp)
    prop = None
    for p in fp.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and atom_str(a[0]) == "Reference":
                prop = p
                break
    if prop is None:
        continue
    rel = at(prop.find("at"))
    if rel is None:
        continue
    cur_abs = rot_pt(rel[0], rel[1], frot)
    cur_abs = (ox + cur_abs[0], oy + cur_abs[1])
    # obstacles near this part
    near = [o for o in obstacles
            if not (o[2] < ox - 25 or o[0] > ox + 25 or o[3] < oy - 25 or o[1] > oy + 25)]
    best = None
    for dx in [i * 0.5 for i in range(-24, 25)]:
        for dy in [i * 0.5 for i in range(-24, 25)]:
            for trot in (0, 90):
                cx, cy = ox + dx, oy + dy
                bb = text_bbox(cx, cy, ref, 1.0, trot)
                pen = 0.0
                for o in near:
                    pen += overlap(bb, o)
                score = pen * 1000 + math.hypot(dx, dy) + (3 if trot else 0)
                if best is None or score < best[0]:
                    best = (score, dx, dy, trot, pen)
    if best is None:
        continue
    score, dx, dy, trot, pen = best
    # relative offset back through the footprint rotation
    rx, ry = rot_pt(dx, dy, -frot)
    moved.append((ref, (round(rx, 3), round(ry, 3)), trot, round(pen, 3)))
    # rewrite the (at ...) inside the property
    atn = prop.find("at")
    inner = "(at %s %s %d)" % (round(rx, 3), round(ry, 3), trot)
    text = text[:atn.start] + inner + text[atn.end:]
    # ensure size 1.0 / thickness 0.15
    root = parse(text)[0]

print("fields moved: %d" % len(moved))
for m in moved:
    print("   %-6s rel=%-18s rot=%-3s penalty=%s" % m)

open(PCB, "w", encoding="utf-8", newline="").write(text)
print("board written")
json.dump(moved, open(ROOT + r"\revC\_silk_fields_moved.json", "w"), indent=1)
