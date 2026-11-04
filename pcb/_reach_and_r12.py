"""STEP 4e reachability + STEP 5 R12 per-net corridor table."""
import pcbnew, math, collections, json

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
b = pcbnew.LoadBoard(PCB)

# ---------- reachability: what sits inside each module outline ----------
outlines = {
    "ESP32 (J1/J2)": (180.5, 91.5, 212.5, 159.5),
    "modem (J3/J4)": (228.5, 90.5, 277.5, 150.5),
    "E22 (J6)": (260.0, 158.62, 303.5, 181.12),
    "GY-521 (J7)": (209.35, 176.0, 230.35, 192.0),
    "DS3231 (J8)": (144.75, 163.0, 182.75, 185.0),
}
REACH = ("SW", "J", "TP", "U", "FID")
print("=== STEP 4e: parts under each module outline ===")
for name, (x0, y0, x1, y1) in outlines.items():
    under = []
    for f in b.GetFootprints():
        p = f.GetPosition()
        x, y = p.x / 1e6, p.y / 1e6
        if x0 <= x <= x1 and y0 <= y <= y1:
            under.append((f.GetReference(), round(x, 2), round(y, 2)))
    print("%-14s %d parts: %s" % (name, len(under), ", ".join(r for r, _, _ in under) or "none"))

# ---------- R12 corridors ----------
def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

obst = collections.defaultdict(list)
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_TRACE_T:
        s, e = t.GetStart(), t.GetEnd()
        obst[t.GetLayerName()].append((t.GetNetname(), s.x / 1e6, s.y / 1e6, e.x / 1e6, e.y / 1e6, t.GetWidth() / 2e6))
    else:
        p = t.GetPosition()
        obst["via"].append((t.GetNetname(), p.x / 1e6, p.y / 1e6, 0, 0, 0.3))

nets = collections.defaultdict(list)
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_TRACE_T and t.GetLayerName() == "In2.Cu":
        nets[t.GetNetname()].append(t)

print()
print("=== STEP 5: R12 per-net plan (In2.Cu -> outer layers) ===")
rows = []
for net, segs in sorted(nets.items(), key=lambda kv: -sum(t.GetLength() for t in kv[1])):
    total = sum(t.GetLength() for t in segs) / 1e6
    pts = [(t.GetStart().x / 1e6, t.GetStart().y / 1e6) for t in segs] + [(t.GetEnd().x / 1e6, t.GetEnd().y / 1e6) for t in segs]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    # corridor: worst-case clearance to other-net copper on F.Cu and B.Cu, sampled at segment midpoints
    worst = {}
    for lay in ("F.Cu", "B.Cu"):
        m = 99.0
        for t in segs:
            mx = (t.GetStart().x + t.GetEnd().x) / 2e6
            my = (t.GetStart().y + t.GetEnd().y) / 2e6
            for (n2, ax, ay, bx, by, hw) in obst[lay]:
                if n2 == net:
                    continue
                d = seg_dist(mx, my, ax, ay, bx, by) - hw
                if d < m:
                    m = d
        worst[lay] = round(m, 2)
    need = max(t.GetWidth() for t in segs) / 2e6 + 0.2
    verdict = "yes" if min(worst.values()) >= need else "no"
    rows.append({"net": net, "segments": len(segs), "length_mm": round(total, 1),
                 "x": (round(min(xs), 1), round(max(xs), 1)), "y": (round(min(ys), 1), round(max(ys), 1)),
                 "corridor_F": worst["F.Cu"], "corridor_B": worst["B.Cu"], "need_mm": round(need, 2), "verdict": verdict})
    print("%-16s n=%2d  %6.1f mm  x %5.1f..%5.1f y %5.1f..%5.1f  F %.2f  B %.2f  need %.2f  -> %s" % (
        net, len(segs), total, min(xs), max(xs), min(ys), max(ys), worst["F.Cu"], worst["B.Cu"], need, verdict))
json.dump(rows, open(ROOT + r"\revC\_work\_r12_plan.json", "w"), indent=1)
print("\nverdicts: %d yes, %d no" % (sum(1 for r in rows if r["verdict"] == "yes"), sum(1 for r in rows if r["verdict"] == "no")))
