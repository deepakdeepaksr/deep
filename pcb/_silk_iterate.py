"""Iteratively place the reference fields that the latest DRC still flags."""
import sys, json, math, os, glob
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str
import pcbnew

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
DRC = sys.argv[1]

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]

def at(n):
    if n is None:
        return None
    a = n.atoms()
    return (float(atom_str(a[0])), float(atom_str(a[1]))) if len(a) >= 2 else None

b = pcbnew.LoadBoard(PCB)
obstacles = []
for f in b.GetFootprints():
    for p in f.Pads():
        bb = p.GetBoundingBox()
        obstacles.append((bb.GetX() / 1e6, bb.GetY() / 1e6, bb.GetRight() / 1e6, bb.GetBottom() / 1e6))

def fp_origin(fp):
    a = fp.find("at").atoms()
    return float(atom_str(a[0])), float(atom_str(a[1])), (float(atom_str(a[2])) if len(a) > 2 else 0.0)

def rot_pt(x, y, deg):
    r = math.radians(deg)
    return (x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r))

def graphic_bbox(g, ox, oy, rot):
    pts = []
    if g.head in ("fp_line", "fp_rect"):
        for k in ("start", "end"):
            p = at(g.find(k))
            if p:
                pts.append(rot_pt(p[0], p[1], rot))
    elif g.head == "fp_circle":
        c, e = at(g.find("center")), at(g.find("end"))
        if c and e:
            r = math.hypot(e[0] - c[0], e[1] - c[1])
            pts = [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]
    elif g.head == "fp_arc":
        for k in ("start", "mid", "end"):
            p = at(g.find(k))
            if p:
                pts.append(rot_pt(p[0], p[1], rot))
    elif g.head == "fp_poly":
        for n in g.find_all("xy"):
            p = at(n)
            if p:
                pts.append(rot_pt(p[0], p[1], rot))
    if not pts:
        return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    m = 0.12
    return (ox + min(xs) - m, oy + min(ys) - m, ox + max(xs) + m, oy + max(ys) + m)

fps = {}
for fp in root.children:
    if not (isinstance(fp, Node) and fp.head == "footprint"):
        continue
    ref = None
    for p in fp.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and atom_str(a[0]) == "Reference":
                ref = atom_str(a[1])
    if ref is None:
        continue
    fps[ref] = fp
    ox, oy, rot = fp_origin(fp)
    for g in fp.children:
        if isinstance(g, Node) and g.head in ("fp_line", "fp_circle", "fp_poly", "fp_arc", "fp_rect") and g.value("layer") == "F.SilkS":
            bb = graphic_bbox(g, ox, oy, rot)
            if bb:
                obstacles.append(bb)
for d in root.children:
    if isinstance(d, Node) and d.head == "gr_text" and d.value("layer") == "F.SilkS":
        p = at(d.find("at"))
        t = d.value("text") or ""
        if p:
            obstacles.append((p[0] - 0.65 * len(t), p[1] - 0.9, p[0] + 0.65 * len(t), p[1] + 0.9))

def field_pos(ref):
    fp = fps[ref]
    ox, oy, rot = fp_origin(fp)
    for p in fp.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and atom_str(a[0]) == "Reference":
                rel = at(p.find("at"))
                r = rot_pt(rel[0], rel[1], -rot)
                return (ox + r[0], oy + r[1], p)
    return None

# other reference fields as obstacles
other_fields = []
for ref in fps:
    fp = fps[ref]
    ox, oy, rot = fp_origin(fp)
    for p in fp.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and atom_str(a[0]) == "Reference":
                rel = at(p.find("at"))
                r = rot_pt(rel[0], rel[1], -rot)
                other_fields.append((ref, ox + r[0], oy + r[1]))

def tbox(cx, cy, s, rot):
    w = (len(s) * 0.95 + 0.7)
    h = 1.8
    if rot % 180 == 90:
        w, h = h, w
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)

def ov(a, c):
    dx = min(a[2], c[2]) - max(a[0], c[0])
    dy = min(a[3], c[3]) - max(a[1], c[1])
    return max(0.0, dx) * max(0.0, dy)

drc = json.load(open(DRC, encoding="utf-8"))
todo = set()
for v in drc["violations"]:
    for it in v.get("items", []):
        d = it.get("description", "")
        if d.startswith("Reference field of "):
            todo.add(d.split("Reference field of ")[1])
print("fields to place: %s" % ", ".join(sorted(todo)))

edits = []
for ref in sorted(todo):
    if ref not in fps:
        continue
    pos = field_pos(ref)
    if pos is None:
        continue
    cx0, cy0, prop = pos
    ox, oy, rot = fp_origin(fps[ref])
    near = [o for o in obstacles if not (o[2] < cx0 - 20 or o[0] > cx0 + 20 or o[3] < cy0 - 20 or o[1] > cy0 + 20)]
    nearf = [(r, x, y) for (r, x, y) in other_fields if r != ref and abs(x - cx0) < 20 and abs(y - cy0) < 20]
    best = None
    for radius in [i * 0.5 for i in range(0, 25)]:
        cands = []
        if radius == 0:
            cands = [(0.0, 0.0)]
        else:
            n = max(8, int(2 * math.pi * radius / 0.5))
            for k in range(n):
                ang = 2 * math.pi * k / n
                cands.append((radius * math.cos(ang), radius * math.sin(ang)))
        for (dx, dy) in cands:
            for trot in (0, 90):
                cx, cy = cx0 + dx, cy0 + dy
                bb = tbox(cx, cy, ref, trot)
                pen = sum(ov(bb, o) for o in near)
                for (r2, x2, y2) in nearf:
                    pen += ov(bb, tbox(x2, y2, r2, 0))
                if pen == 0:
                    best = (dx, dy, trot)
                    break
            if best:
                break
        if best:
            break
    if not best:
        print("  %-6s NO CLEAR SPOT" % ref)
        continue
    dx, dy, trot = best
    rx, ry = rot_pt(cx0 + dx - ox, cy0 + dy - oy, rot)
    atn = prop.find("at")
    edits.append((atn.start, atn.end, "(at %s %s %d)" % (round(rx, 3), round(ry, 3), trot)))
    print("  %-6s -> (%s, %s) rot %s  (moved %.1f mm)" % (ref, round(rx, 2), round(ry, 2), trot, math.hypot(dx, dy)))
    other_fields = [(r, (cx0 + dx) if r == ref else x, (cy0 + dy) if r == ref else y) for (r, x, y) in other_fields]

out = text
for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
print("written %d edits" % len(edits))
