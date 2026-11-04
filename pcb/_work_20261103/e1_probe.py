"""E1 probe: reproduce the stitching metric and list every 1 mm cell beyond 10 mm."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e1_over10.json")
STEP = 1.0

b = pcbnew.LoadBoard(PCB)
filler = pcbnew.ZONE_FILLER(b)
filler.Fill(b.Zones())

z_in1 = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "In1.Cu")
z_bcu = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "B.Cu")
p_in1 = z_in1.GetFilledPolysList(z_in1.GetLayer())
p_bcu = z_bcu.GetFilledPolysList(z_bcu.GetLayer())

bb = b.GetBoardEdgesBoundingBox()
xs = np.arange(bb.GetX() / 1e6, bb.GetRight() / 1e6, STEP)
ys = np.arange(bb.GetY() / 1e6, bb.GetBottom() / 1e6, STEP)
X, Y = np.meshgrid(xs, ys)
m_in1 = np.zeros(X.shape, bool)
m_bcu = np.zeros(X.shape, bool)
for j in range(X.shape[0]):
    for i in range(X.shape[1]):
        v = pcbnew.VECTOR2I(int(round(X[j, i] * 1e6)), int(round(Y[j, i] * 1e6)))
        m_in1[j, i] = p_in1.Contains(v)
        m_bcu[j, i] = p_bcu.Contains(v)
m = m_in1 & m_bcu


def inside_both(px, py):
    v = pcbnew.VECTOR2I(int(round(px * 1e6)), int(round(py * 1e6)))
    return p_in1.Contains(v) and p_bcu.Contains(v)


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

D = np.full(X.shape, 1e9)
for (lx, ly) in links:
    D = np.minimum(D, np.hypot(X - lx, Y - ly))
Dm = np.where(m, D, np.nan)
mx = float(np.nanmax(Dm))
pct = 100.0 * np.nansum(Dm > 10) / m.sum()
print("links=%d cells=%d max=%.2f mm over10=%.1f %%" % (len(links), m.sum(), mx, pct))

# cluster the over-10 cells
over = [(float(X[j, i]), float(Y[j, i]), float(Dm[j, i]))
        for j in range(X.shape[0]) for i in range(X.shape[1])
        if m[j, i] and Dm[j, i] > 10.0]
over.sort(key=lambda c: -c[2])
print("cells over 10 mm: %d" % len(over))
for c in over[:40]:
    print("   (%.0f, %.0f)  %.2f mm" % c)

clusters = []
used = set()
for idx, (x, y, d) in enumerate(over):
    if idx in used:
        continue
    group = [(x, y, d)]
    used.add(idx)
    changed = True
    while changed:
        changed = False
        for jdx, (x2, y2, d2) in enumerate(over):
            if jdx in used:
                continue
            if any(abs(x2 - gx) <= 1.5 and abs(y2 - gy) <= 1.5 for (gx, gy, _) in group):
                group.append((x2, y2, d2))
                used.add(jdx)
                changed = True
    clusters.append(group)

print("\nclusters:")
summary = []
for g in clusters:
    gx = [c[0] for c in g]
    gy = [c[1] for c in g]
    worst = max(g, key=lambda c: c[2])
    summary.append({"n": len(g), "x0": min(gx), "x1": max(gx), "y0": min(gy), "y1": max(gy),
                    "worst_x": worst[0], "worst_y": worst[1], "worst": worst[2]})
    print("   %2d cells  x %.0f-%.0f  y %.0f-%.0f  worst %.2f at (%.0f, %.0f)" %
          (len(g), min(gx), max(gx), min(gy), max(gy), worst[2], worst[0], worst[1]))
json.dump(summary, open(OUT, "w"), indent=1)
