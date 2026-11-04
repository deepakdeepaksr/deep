"""Plan and add stitching vias on the E1 trial: link B.Cu GND pour to In1 GND plane."""
import pcbnew, numpy as np, math, json, uuid, sys

P = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\_snap\E1_trial_20261101_234720\proj\MoriShield_Carrier.kicad_pcb"
OUT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC"
STEP = 1.0

b = pcbnew.LoadBoard(P)
filler = pcbnew.ZONE_FILLER(b)
filler.Fill(b.Zones())

z_in1 = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "In1.Cu")
z_bcu = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "B.Cu")
p_in1 = z_in1.GetFilledPolysList(z_in1.GetLayer())
p_bcu = z_bcu.GetFilledPolysList(z_bcu.GetLayer())

bb = b.GetBoardEdgesBoundingBox()
x0, y0 = bb.GetX() / 1e6, bb.GetY() / 1e6
x1, y1 = bb.GetRight() / 1e6, bb.GetBottom() / 1e6
xs = np.arange(x0, x1, STEP)
ys = np.arange(y0, y1, STEP)
X, Y = np.meshgrid(xs, ys)

def mask_of(poly):
    m = np.zeros(X.shape, bool)
    for j in range(X.shape[0]):
        for i in range(X.shape[1]):
            m[j, i] = poly.Contains(pcbnew.VECTOR2I(int(round(X[j, i] * 1e6)), int(round(Y[j, i] * 1e6))))
    return m

m_in1 = mask_of(p_in1)
m_bcu = mask_of(p_bcu)
m = m_in1 & m_bcu
print("cells: In1 %d  B.Cu %d  both %d" % (m_in1.sum(), m_bcu.sum(), m.sum()))

def inside_both(px, py):
    v = pcbnew.VECTOR2I(int(round(px * 1e6)), int(round(py * 1e6)))
    return p_in1.Contains(v) and p_bcu.Contains(v)

# links: GND vias and GND PTH pads that lie in BOTH pours
links = []
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "GND":
        p = t.GetPosition()
        if inside_both(p.x / 1e6, p.y / 1e6):
            links.append((p.x / 1e6, p.y / 1e6))
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname() == "GND" and p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
            pt = p.GetPosition()
            if inside_both(pt.x / 1e6, pt.y / 1e6):
                links.append((pt.x / 1e6, pt.y / 1e6))
print("links in both pours:", len(links))

obstacles, holes = [], []
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_TRACE_T:
        s, e = t.GetStart(), t.GetEnd()
        if t.GetNetname() != "GND":
            obstacles.append(("seg", s.x / 1e6, s.y / 1e6, e.x / 1e6, e.y / 1e6, t.GetWidth() / 2e6))
    else:
        p = t.GetPosition()
        holes.append((p.x / 1e6, p.y / 1e6, t.GetDrill() / 2e6))
        if t.GetNetname() != "GND":
            obstacles.append(("pt", p.x / 1e6, p.y / 1e6, 0, 0, 0.3))
for f in b.GetFootprints():
    for p in f.Pads():
        pb = p.GetBoundingBox()
        cx, cy = p.GetPosition().x / 1e6, p.GetPosition().y / 1e6
        holes.append((cx, cy, max(p.GetDrillSize().x, p.GetDrillSize().y) / 2e6))
        if p.GetNetname() != "GND":
            obstacles.append(("box", pb.GetX() / 1e6, pb.GetY() / 1e6, pb.GetRight() / 1e6, pb.GetBottom() / 1e6, 0))

def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def box_dist(px, py, ax, ay, bx, by):
    return math.hypot(max(ax - px, 0, px - bx), max(ay - py, 0, py - by))

VIA_R, DRILL_R, CLEAR, EDGE = 0.3, 0.15, 0.25, 0.5

def free(px, py):
    if not (x0 + EDGE + VIA_R < px < x1 - EDGE - VIA_R and y0 + EDGE + VIA_R < py < y1 - EDGE - VIA_R):
        return False
    for (hx, hy, hr) in holes:
        if math.hypot(px - hx, py - hy) < DRILL_R + hr + 0.3:
            return False
    for ob in obstacles:
        if ob[0] == "seg":
            if seg_dist(px, py, ob[1], ob[2], ob[3], ob[4]) < VIA_R + ob[5] + CLEAR:
                return False
        elif ob[0] == "pt":
            if math.hypot(px - ob[1], py - ob[2]) < VIA_R + ob[5] + CLEAR:
                return False
        else:
            if box_dist(px, py, ob[1], ob[2], ob[3], ob[4]) < VIA_R + CLEAR:
                return False
    return True

D = np.full(X.shape, 1e9)
for (lx, ly) in links:
    D = np.minimum(D, np.hypot(X - lx, Y - ly))
D = np.where(m, D, 0.0)
print("before: max %.2f mm, %.1f %% over 10 mm" % (D[m].max(), 100.0 * (D[m] > 10).sum() / m.sum()))

new = []
blocked = 0
for _ in range(600):
    d = np.where(m, D, -1)
    idx = np.unravel_index(np.argmax(d), d.shape)
    if d[idx] <= 10.0:
        break
    wx, wy = X[idx], Y[idx]
    placed = False
    for rad in (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0):
        for k in range(1 if rad == 0 else 24):
            ang = 2 * math.pi * k / 24
            cx, cy = wx + rad * math.cos(ang), wy + rad * math.sin(ang)
            if not inside_both(cx, cy) or not free(cx, cy):
                continue
            if any(math.hypot(cx - vx, cy - vy) < 1.5 for (vx, vy) in new):
                continue
            new.append((round(cx, 3), round(cy, 3)))
            D = np.where(m, np.minimum(D, np.hypot(X - cx, Y - cy)), 0.0)
            placed = True
            break
        if placed:
            break
    if not placed:
        blocked += 1
        D[idx] = 9.99
        if blocked > 300:
            break

print("vias planned: %d  abandoned: %d" % (len(new), blocked))
print("after: max %.2f mm, %.1f %% over 10 mm" % (D[m].max(), 100.0 * (D[m] > 10).sum() / m.sum()))

# write them into the trial board
text = open(P, encoding="utf-8").read()
blocks = "".join(
    '\t(via\n\t\t(at %s %s)\n\t\t(size 0.6)\n\t\t(drill 0.3)\n\t\t(layers "F.Cu" "B.Cu")\n'
    '\t\t(net "GND")\n\t\t(uuid "%s")\n\t)\n' % (x, y, uuid.uuid4()) for (x, y) in new)
idx = text.rstrip().rfind(")")
open(P, "w", encoding="utf-8", newline="").write(text[:idx] + blocks + text[idx:])
json.dump({"vias": new, "links_before": len(links),
           "before_max": float(np.where(m, np.full(X.shape, 1e9), 0).max())},
          open(OUT + r"\_e1_trial_plan.json", "w"), indent=1)
print("trial board updated")
