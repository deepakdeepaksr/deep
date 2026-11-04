"""Plan ground stitching vias: greedy placement until no plane point is >10 mm from a link."""
import pcbnew, math, json, sys
import numpy as np

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
OUT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC"
STEP = 0.5

b = pcbnew.LoadBoard(PCB)
zone = None
for z in b.Zones():
    if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "In1.Cu":
        zone = z
poly = zone.GetFilledPolysList(zone.GetLayer())
bb = poly.BBox()
x0, y0 = bb.GetX() / 1e6, bb.GetY() / 1e6
x1, y1 = bb.GetRight() / 1e6, bb.GetBottom() / 1e6
nx = int((x1 - x0) / STEP) + 1
ny = int((y1 - y0) / STEP) + 1
print("grid %d x %d over %.2f x %.2f mm" % (nx, ny, x1 - x0, y1 - y0))

xs = x0 + np.arange(nx) * STEP
ys = y0 + np.arange(ny) * STEP
X, Y = np.meshgrid(xs, ys)
mask = np.zeros((ny, nx), dtype=bool)
for j in range(ny):
    for i in range(nx):
        p = pcbnew.VECTOR2I(int(round(xs[i] * 1e6)), int(round(ys[j] * 1e6)))
        mask[j, i] = poly.Contains(p)
print("plane cells:", int(mask.sum()))

# links: GND vias + GND through-hole pads inside the plane
links = []
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "GND":
        p = t.GetPosition(); links.append((p.x / 1e6, p.y / 1e6, "via"))
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname() != "GND":
            continue
        if p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
            pt = p.GetPosition()
            v = pcbnew.VECTOR2I(pt.x, pt.y)
            if poly.Contains(v):
                links.append((pt.x / 1e6, pt.y / 1e6, "pad"))
print("ground links:", len(links))

# other-net copper, for clearance
obstacles = []   # (kind, x, y, r) for pads/vias, (kind, ax, ay, bx, by, hw)
for t in b.GetTracks():
    if t.GetNetname() == "GND":
        continue
    if t.Type() == pcbnew.PCB_TRACE_T:
        s, e = t.GetStart(), t.GetEnd()
        obstacles.append(("seg", s.x / 1e6, s.y / 1e6, e.x / 1e6, e.y / 1e6, t.GetWidth() / 2e6))
    else:
        p = t.GetPosition()
        obstacles.append(("pt", p.x / 1e6, p.y / 1e6, 0, 0, t.GetWidth() / 2e6 if hasattr(t, "GetWidth") else 0.3))
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname() == "GND":
            continue
        pb = p.GetBoundingBox()
        obstacles.append(("box", pb.GetX() / 1e6, pb.GetY() / 1e6, pb.GetRight() / 1e6, pb.GetBottom() / 1e6, 0))

def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def box_dist(px, py, x0_, y0_, x1_, y1_):
    dx = max(x0_ - px, 0, px - x1_)
    dy = max(y0_ - py, 0, py - y1_)
    return math.hypot(dx, dy)

VIA_R = 0.3
CLEAR = 0.25
EDGE = 0.5
board_bb = b.GetBoardEdgesBoundingBox()
bx0, by0 = board_bb.GetX() / 1e6, board_bb.GetY() / 1e6
bx1, by1 = board_bb.GetRight() / 1e6, board_bb.GetBottom() / 1e6

def free(px, py):
    if px - VIA_R < bx0 + EDGE or px + VIA_R > bx1 - EDGE:
        return False
    if py - VIA_R < by0 + EDGE or py + VIA_R > by1 - EDGE:
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

# distance field
D = np.full((ny, nx), 1e9)
for (lx, ly, _k) in links:
    D = np.minimum(D, np.hypot(X - lx, Y - ly))
D = np.where(mask, D, 0.0)
print("before: max %.2f mm, %.1f%% over 10 mm" % (D[mask].max(), 100.0 * (D[mask] > 10).sum() / mask.sum()))

new_vias = []
blocked = 0
for _ in range(400):
    d = np.where(mask, D, -1)
    idx = np.unravel_index(np.argmax(d), d.shape)
    worst = d[idx]
    if worst <= 10.0:
        break
    wx, wy = X[idx], Y[idx]
    placed = False
    for rad in (0.0, 0.5, 1.0, 1.5, 2.0, 3.0):
        for k in range(1 if rad == 0 else 16):
            ang = 2 * math.pi * k / 16
            cx, cy = wx + rad * math.cos(ang), wy + rad * math.sin(ang)
            p = pcbnew.VECTOR2I(int(round(cx * 1e6)), int(round(cy * 1e6)))
            if not poly.Contains(p):
                continue
            if not free(cx, cy):
                continue
            if any(math.hypot(cx - vx, cy - vy) < 2.0 for (vx, vy) in new_vias):
                continue
            new_vias.append((round(cx, 3), round(cy, 3)))
            D = np.minimum(D, np.hypot(X - cx, Y - cy))
            D = np.where(mask, D, 0.0)
            placed = True
            break
        if placed:
            break
    if not placed:
        blocked += 1
        D[idx] = 9.99   # give up on this cell, move to the next worst
        if blocked > 200:
            break

print("vias planned: %d   cells abandoned: %d" % (len(new_vias), blocked))
print("after: max %.2f mm, %.1f%% over 10 mm" % (D[mask].max(), 100.0 * (D[mask] > 10).sum() / mask.sum()))
json.dump({"vias": new_vias, "max_before": float(np.hypot(X - links[0][0], Y - links[0][1]).max())},
          open(OUT + r"\_stitch_plan.json", "w"), indent=1)
