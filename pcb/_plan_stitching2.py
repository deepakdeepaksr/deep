"""Plan ground stitching vias. Links = GND vias and GND PTH pads inside the In1 plane."""
import pcbnew, math, json
import numpy as np

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
OUT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC"
STEP = 0.5

b = pcbnew.LoadBoard(PCB)
zone = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "In1.Cu")
poly = zone.GetFilledPolysList(zone.GetLayer())
bb = poly.BBox()
x0, y0 = bb.GetX() / 1e6, bb.GetY() / 1e6
x1, y1 = bb.GetRight() / 1e6, bb.GetBottom() / 1e6
nx = int((x1 - x0) / STEP) + 1
ny = int((y1 - y0) / STEP) + 1
xs = x0 + np.arange(nx) * STEP
ys = y0 + np.arange(ny) * STEP
X, Y = np.meshgrid(xs, ys)
mask = np.zeros((ny, nx), dtype=bool)
for j in range(ny):
    for i in range(nx):
        mask[j, i] = poly.Contains(pcbnew.VECTOR2I(int(round(xs[i] * 1e6)), int(round(ys[j] * 1e6))))

def inside(px, py):
    return poly.Contains(pcbnew.VECTOR2I(int(round(px * 1e6)), int(round(py * 1e6))))

links = []
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "GND":
        p = t.GetPosition()
        if inside(p.x / 1e6, p.y / 1e6):
            links.append((p.x / 1e6, p.y / 1e6))
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname() == "GND" and p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
            pt = p.GetPosition()
            if inside(pt.x / 1e6, pt.y / 1e6):
                links.append((pt.x / 1e6, pt.y / 1e6))
print("links inside the plane:", len(links))

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
bb2 = b.GetBoardEdgesBoundingBox()
bx0, by0 = bb2.GetX() / 1e6, bb2.GetY() / 1e6
bx1, by1 = bb2.GetRight() / 1e6, bb2.GetBottom() / 1e6

def free(px, py):
    if not (bx0 + EDGE + VIA_R < px < bx1 - EDGE - VIA_R):
        return False
    if not (by0 + EDGE + VIA_R < py < by1 - EDGE - VIA_R):
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

D = np.full((ny, nx), 1e9)
for (lx, ly) in links:
    D = np.minimum(D, np.hypot(X - lx, Y - ly))
D = np.where(mask, D, 0.0)
before_max = float(D[mask].max())
before_pct = 100.0 * (D[mask] > 10).sum() / mask.sum()
print("before: max %.2f mm, %.1f %% over 10 mm" % (before_max, before_pct))

new_vias, blocked = [], 0
for _ in range(500):
    d = np.where(mask, D, -1)
    idx = np.unravel_index(np.argmax(d), d.shape)
    if d[idx] <= 10.0:
        break
    wx, wy = X[idx], Y[idx]
    placed = False
    for rad in (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0):
        for k in range(1 if rad == 0 else 24):
            ang = 2 * math.pi * k / 24
            cx, cy = wx + rad * math.cos(ang), wy + rad * math.sin(ang)
            if not inside(cx, cy) or not free(cx, cy):
                continue
            if any(math.hypot(cx - vx, cy - vy) < 1.5 for (vx, vy) in new_vias):
                continue
            new_vias.append((round(cx, 3), round(cy, 3)))
            D = np.where(mask, np.minimum(D, np.hypot(X - cx, Y - cy)), 0.0)
            placed = True
            break
        if placed:
            break
    if not placed:
        blocked += 1
        D[idx] = 9.99
        if blocked > 300:
            break

print("vias planned: %d   cells abandoned: %d" % (len(new_vias), blocked))
print("after: max %.2f mm, %.1f %% over 10 mm" % (D[mask].max(), 100.0 * (D[mask] > 10).sum() / mask.sum()))
json.dump({"vias": new_vias, "before_max": before_max, "before_pct": before_pct,
           "links": len(links), "after_max": float(D[mask].max())},
          open(OUT + r"\_stitch_plan.json", "w"), indent=1)
