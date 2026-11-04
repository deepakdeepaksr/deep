import sys, math
sys.path.insert(0, r"C:\Program Files\KiCad\10.0\bin")
import pcbnew

b = pcbnew.LoadBoard(r"c:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\4L\MoriShield_Carrier.kicad_pcb")
A = (244.5, 173.5)
B = (257.0, 168.1)
M = 0.6  # corridor half-width, mm
X0, X1, Y0, Y1 = 238.0, 263.0, 162.0, 180.0


def seg_dist(p, q, r, s):
    # min distance between segment pq and rs, sampled
    best = 1e9
    for i in range(41):
        t = i / 40.0
        px, py = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        for j in range(41):
            u = j / 40.0
            rx, ry = r[0] + (s[0] - r[0]) * u, r[1] + (s[1] - r[1]) * u
            d = math.hypot(px - rx, py - ry)
            if d < best:
                best = d
    return best


hits = []
for t in b.GetTracks():
    p = t.GetPosition() if isinstance(t, pcbnew.PCB_VIA) else None
    if isinstance(t, pcbnew.PCB_VIA):
        x, y = t.GetPosition().x / 1e6, t.GetPosition().y / 1e6
        if X0 <= x <= X1 and Y0 <= y <= Y1:
            d = seg_dist((x, y), (x, y), A, B)
            hits.append((d, "via", t.GetNetname(), b.GetLayerName(t.GetLayer()), f"{x:.2f},{y:.2f}"))
        continue
    p1 = (t.GetStart().x / 1e6, t.GetStart().y / 1e6)
    p2 = (t.GetEnd().x / 1e6, t.GetEnd().y / 1e6)
    if max(p1[0], p2[0]) < X0 or min(p1[0], p2[0]) > X1 or max(p1[1], p2[1]) < Y0 or min(p1[1], p2[1]) > Y1:
        continue
    d = seg_dist(p1, p2, A, B)
    hits.append((d, "track", t.GetNetname(), b.GetLayerName(t.GetLayer()), f"{p1[0]:.1f},{p1[1]:.1f}->{p2[0]:.1f},{p2[1]:.1f}"))

for fp in b.GetFootprints():
    for pad in fp.Pads():
        x, y = pad.GetPosition().x / 1e6, pad.GetPosition().y / 1e6
        if not (X0 <= x <= X1 and Y0 <= y <= Y1):
            continue
        sz = pad.GetSize()
        d = seg_dist((x, y), (x, y), A, B)
        hits.append((d, "pad", pad.GetNetname(), f"{fp.GetReference()}.{pad.GetNumber()}", f"{x:.2f},{y:.2f} {sz.x/1e6:.2f}x{sz.y/1e6:.2f}"))

hits.sort(key=lambda h: h[0])
print(f"items in box {X0}-{X1} x {Y0}-{Y1}: {len(hits)}")
print("--- within 1.5 mm of the straight line ---")
for h in hits:
    if h[0] <= 1.5:
        print(f"{h[0]:5.2f} mm  {h[1]:5s} {h[2]:22s} {h[3]:28s} {h[4]}")
print("--- 1.5 to 3 mm ---")
for h in hits:
    if 1.5 < h[0] <= 3.0:
        print(f"{h[0]:5.2f} mm  {h[1]:5s} {h[2]:22s} {h[3]:28s} {h[4]}")
