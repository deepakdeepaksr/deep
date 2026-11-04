import pcbnew, json, math, collections, heapq

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
b = pcbnew.LoadBoard(PCB)

# ---------- 1. vias inside SMD pads ----------
smd_pads = []
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
            bb = p.GetBoundingBox()
            smd_pads.append((f.GetReference(), p.GetNumber(), p.GetNetname(),
                             bb.GetX() / 1e6, bb.GetY() / 1e6,
                             bb.GetRight() / 1e6, bb.GetBottom() / 1e6,
                             p.GetPosition().x / 1e6, p.GetPosition().y / 1e6))
vias = [t for t in b.GetTracks() if t.Type() == pcbnew.PCB_VIA_T]
hits = []
for v in vias:
    vx, vy = v.GetPosition().x / 1e6, v.GetPosition().y / 1e6
    for (ref, num, net, x0, y0, x1, y1, px, py) in smd_pads:
        if x0 <= vx <= x1 and y0 <= vy <= y1:
            hits.append({"via": [round(vx, 3), round(vy, 3)], "size": None,
                         "drill": round(v.GetDrill() / 1e6, 2), "net": v.GetNetname(),
                         "pad": "%s.%s" % (ref, num), "padnet": net})
            break

# ---------- 2. copper graph per net ----------
def seg_dist(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))

# nodes: quantised coordinates; edges: tracks and vias
def key(x, y):
    return (round(x, 3), round(y, 3))

graph = collections.defaultdict(list)   # node -> [(node, length, layer)]
segments = collections.defaultdict(list)
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_TRACE_T:
        s, e = t.GetStart(), t.GetEnd()
        a = key(s.x / 1e6, s.y / 1e6)
        c = key(e.x / 1e6, e.y / 1e6)
        L = math.hypot(c[0] - a[0], c[1] - a[1])
        graph[a].append((c, L, t.GetLayerName()))
        graph[c].append((a, L, t.GetLayerName()))
        segments[t.GetNetname()].append((a, c, t.GetLayerName()))
    elif t.Type() == pcbnew.PCB_VIA_T:
        p = t.GetPosition()
        a = key(p.x / 1e6, p.y / 1e6)
        graph[a].append((a, 0.0, "VIA"))
        graph[a].append((a, 0.0, "VIA"))

# pads as nodes: snap each pad centre to the nearest track endpoint on the same net
padnode = {}
for f in b.GetFootprints():
    for p in f.Pads():
        n = p.GetNetname()
        if not n:
            continue
        px, py = p.GetPosition().x / 1e6, p.GetPosition().y / 1e6
        best = None
        for (a, c, lay) in segments.get(n, []):
            for q in (a, c):
                d = math.hypot(q[0] - px, q[1] - py)
                if best is None or d < best[0]:
                    best = (d, q)
        if best and best[0] < 1.5:
            padnode[(f.GetReference(), p.GetNumber())] = best[1]

def dijkstra(src, dst):
    if src not in graph or dst not in graph:
        return None
    dist = {src: 0.0}
    pq = [(0.0, src)]
    seen = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == dst:
            return d
        for (v, w, lay) in graph[u]:
            nd = d + w
            if nd < dist.get(v, 1e18):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return None

# ---------- 3. ESD distance for field connectors ----------
field = ["J11", "J12", "J13", "J14", "J15", "J16", "J17", "J20", "J21", "J22", "J23", "J24", "J25", "J26"]
esd_by_net = collections.defaultdict(list)
for f in b.GetFootprints():
    r = f.GetReference()
    if r.startswith("ESD"):
        for p in f.Pads():
            if p.GetNetname() and p.GetNetname() not in ("GND", "PE"):
                esd_by_net[p.GetNetname()].append((r, p.GetNumber()))

esd_rows = []
for ref in field:
    fp = b.FindFootprintByReference(ref) if hasattr(b, "FindFootprintByReference") else None
    if fp is None:
        for f in b.GetFootprints():
            if f.GetReference() == ref:
                fp = f
                break
    if fp is None:
        esd_rows.append({"conn": ref, "status": "missing"})
        continue
    rows = []
    for p in fp.Pads():
        n = p.GetNetname()
        if not n or n in ("GND", "PE"):
            continue
        cand = [e for e in esd_by_net.get(n, []) if e[0] != ref]
        if not cand:
            rows.append({"pin": p.GetNumber(), "net": n, "esd": None})
            continue
        src = padnode.get((ref, p.GetNumber()))
        bestd, bestp = None, None
        for (er, en) in cand:
            dst = padnode.get((er, en))
            if src is None or dst is None:
                continue
            d = dijkstra(src, dst)
            if d is not None and (bestd is None or d < bestd):
                bestd, bestp = d, er
        # straight line fallback
        sl = None
        for (er, en) in cand:
            efp = None
            for f in b.GetFootprints():
                if f.GetReference() == er:
                    efp = f
                    break
            for ep in efp.Pads():
                if ep.GetNumber() == en:
                    sl = math.hypot(ep.GetPosition().x - p.GetPosition().x, ep.GetPosition().y - p.GetPosition().y) / 1e6
        rows.append({"pin": p.GetNumber(), "net": n, "esd": bestp,
                     "copper_mm": round(bestd, 2) if bestd is not None else None,
                     "straight_mm": round(sl, 2) if sl else None})
    esd_rows.append({"conn": ref, "pads": rows})

open(r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC\_esd_measure.json","w",encoding="utf-8").write(json.dumps({
    "via_count": len(vias),
    "vias_in_pads": len(hits),
    "vias_in_pads_detail": hits,
    "esd": esd_rows,
}, indent=1))

