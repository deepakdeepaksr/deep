"""Decoupling map and ground-stitching analysis, measured from the board file."""
import pcbnew, json, math, collections, heapq

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
OUT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC"
b = pcbnew.LoadBoard(PCB)

# ---------------------------------------------------------------- copper graph
def key(x, y):
    return (round(x, 3), round(y, 3))

graph = collections.defaultdict(list)
segs = collections.defaultdict(list)
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_TRACE_T:
        s, e = t.GetStart(), t.GetEnd()
        a, c = key(s.x / 1e6, s.y / 1e6), key(e.x / 1e6, e.y / 1e6)
        L = math.hypot(c[0] - a[0], c[1] - a[1])
        graph[a].append((c, L)); graph[c].append((a, L))
        segs[t.GetNetname()].append((a, c))
    elif t.Type() == pcbnew.PCB_VIA_T:
        p = t.GetPosition(); a = key(p.x / 1e6, p.y / 1e6)
        graph[a].append((a, 0.0)); graph[a].append((a, 0.0))

pads = []
for f in b.GetFootprints():
    for p in f.Pads():
        n = p.GetNetname()
        if not n:
            continue
        pads.append({"ref": f.GetReference(), "pad": p.GetNumber(), "net": n,
                     "x": p.GetPosition().x / 1e6, "y": p.GetPosition().y / 1e6,
                     "val": f.GetValue() if hasattr(f, "GetValue") else "",
                     "fp": str(f.GetFPID().GetLibItemName())})

padnode = {}
for pd in pads:
    best = None
    for (a, c) in segs.get(pd["net"], []):
        for q in (a, c):
            d = math.hypot(q[0] - pd["x"], q[1] - pd["y"])
            if best is None or d < best[0]:
                best = (d, q)
    if best and best[0] < 1.5:
        padnode[(pd["ref"], pd["pad"])] = best[1]

def dijkstra(src, dst):
    if src is None or dst is None or src not in graph or dst not in graph:
        return None
    dist = {src: 0.0}; pq = [(0.0, src)]; seen = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == dst:
            return d
        for (v, w) in graph[u]:
            nd = d + w
            if nd < dist.get(v, 1e18):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return None

SUPPLY = ["+5V", "+5V_IN", "+5V_F", "/+5V_ESP", "/+5V_SENS", "/+5V_E22", "/+5V_E22_IN",
          "3V3_C", "/3V3_SENS", "/3V3_SENS_SW", "/5V_PROT"]
rows = []
for pd in pads:
    if pd["net"] not in SUPPLY:
        continue
    if pd["fp"].startswith(("C_", "CP_")):
        continue
    caps = [q for q in pads if q["net"] == pd["net"] and q["fp"].startswith(("C_", "CP_"))]
    if not caps:
        rows.append({"net": pd["net"], "ref": pd["ref"], "pad": pd["pad"], "cap": None})
        continue
    src = padnode.get((pd["ref"], pd["pad"]))
    best = None
    for cp in caps:
        d = dijkstra(src, padnode.get((cp["ref"], cp["pad"])))
        sl = math.hypot(cp["x"] - pd["x"], cp["y"] - pd["y"])
        cand = (d if d is not None else 1e9, sl, cp)
        if best is None or cand[0] < best[0]:
            best = cand
    rows.append({"net": pd["net"], "ref": pd["ref"], "pad": pd["pad"],
                 "cap": best[2]["ref"], "capval": best[2]["val"],
                 "copper_mm": round(best[0], 2) if best[0] < 1e9 else None,
                 "straight_mm": round(best[1], 2)})

with open(OUT + r"\decoupling_map.csv", "w", encoding="utf-8", newline="") as fh:
    fh.write("net,load_ref,load_pad,nearest_cap,cap_value,copper_mm,straight_mm\n")
    for r in rows:
        fh.write("%s,%s,%s,%s,%s,%s,%s\n" % (r["net"], r["ref"], r["pad"], r.get("cap") or "",
                                             r.get("capval", ""), r.get("copper_mm", ""), r.get("straight_mm", "")))
over10 = [r for r in rows if r.get("copper_mm") is None or r["copper_mm"] > 10]
print("decoupling rows: %d   over 10 mm or no cap: %d" % (len(rows), len(over10)))
for r in over10[:15]:
    print("   %-14s %-5s.%-2s -> %-5s %-10s %s mm" % (r["net"], r["ref"], r["pad"],
          r.get("cap") or "-", r.get("capval", ""), r.get("copper_mm")))

# ---------------------------------------------------------------- stitching
links = []
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "GND":
        p = t.GetPosition(); links.append((p.x / 1e6, p.y / 1e6))
for pd in pads:
    if pd["net"] == "GND" and pd["fp"].startswith(("PinSocket", "PinHeader", "JST", "TerminalBlock", "MountingHole")):
        links.append((pd["x"], pd["y"]))
print("ground links (GND vias + through-hole GND pads): %d" % len(links))

res = {}
for z in b.Zones():
    if z.GetNetname() != "GND":
        continue
    lay = b.GetLayerName(z.GetLayer())
    poly = z.GetFilledPolysList(z.GetLayer())
    bb = poly.BBox()
    step = 1.0
    worst = 0.0
    n = 0
    over = 0
    x = bb.GetX() / 1e6
    while x < bb.GetRight() / 1e6:
        y = bb.GetY() / 1e6
        while y < bb.GetBottom() / 1e6:
            pt = pcbnew.VECTOR2I(int(round(x * 1e6)), int(round(y * 1e6)))
            if poly.Contains(pt):
                n += 1
                d = min(math.hypot(x - lx, y - ly) for (lx, ly) in links) if links else 999
                if d > worst:
                    worst = d
                if d > 10.0:
                    over += 1
            y += step
        x += step
    res[lay] = {"layer": lay, "samples": n, "max_mm": round(worst, 2),
                "over_10mm_pct": round(100.0 * over / n, 1) if n else None}
    print("zone GND on %s: %d samples, max distance %.1f mm, %.1f%% over 10 mm" %
          (lay, n, worst, 100.0 * over / n if n else 0))

json.dump({"decoupling_over_10mm": over10, "stitching": res},
          open(OUT + r"\_evidence_maps.json", "w"), indent=1)
