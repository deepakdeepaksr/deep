"""Rebuild the decoupling map: choose the nearest capacitor by copper-path where a track
path exists, otherwise by straight line through the plane (a plane IS copper)."""
import pcbnew, math, collections, heapq, csv

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
OUT = ROOT + r"\revC\decoupling_map.csv"

b = pcbnew.LoadBoard(PCB)
SUPPLY = ["+5V", "+5V_IN", "+5V_F", "/+5V_ESP", "/+5V_SENS", "/+5V_E22", "/+5V_E22_IN",
          "3V3_C", "/3V3_SENS", "/3V3_SENS_SW"]

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
        if not p.GetNetname():
            continue
        pads.append({"ref": f.GetReference(), "pad": p.GetNumber(), "net": p.GetNetname(),
                     "x": p.GetPosition().x / 1e6, "y": p.GetPosition().y / 1e6,
                     "val": f.GetValue(), "fp": str(f.GetFPID().GetLibItemName())})

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

def dij(src, dst):
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
                dist[v] = nd; heapq.heappush(pq, (nd, v))
    return None

rows = []
for pd in pads:
    if pd["net"] not in SUPPLY or pd["fp"].startswith(("C_", "CP_")):
        continue
    caps = [q for q in pads if q["net"] == pd["net"] and q["fp"].startswith(("C_", "CP_"))]
    if not caps:
        continue
    src = padnode.get((pd["ref"], pd["pad"]))
    best = None
    for cp in caps:
        tr = dij(src, padnode.get((cp["ref"], cp["pad"])))
        sl = math.hypot(cp["x"] - pd["x"], cp["y"] - pd["y"])
        d = tr if tr is not None else sl
        meth = "track" if tr is not None else "plane-straight"
        if best is None or d < best[0]:
            best = (d, meth, cp, sl)
    d, meth, cp, sl = best
    rows.append({"net": pd["net"], "load_ref": pd["ref"], "load_pad": pd["pad"],
                 "nearest_cap": cp["ref"], "cap_value": cp["val"],
                 "copper_mm": round(d, 2), "straight_mm": round(sl, 2), "method": meth})

IC = ("U", "Q", "D")
for r in rows:
    ref = r["load_ref"]
    if ref.startswith("TP"):
        r["limit_mm"], r["meets"], r["basis"] = "", "", "test point, not a load - excluded"
    elif ref.startswith(IC):
        r["limit_mm"], r["meets"], r["basis"] = 3.0, ("yes" if r["copper_mm"] <= 3.0 else "no"), "IC supply pin: 100 nF within 3 mm (CHK C9)"
    elif ref.startswith("J"):
        r["limit_mm"], r["meets"], r["basis"] = 5.0, ("yes" if r["copper_mm"] <= 5.0 else "no"), "port supply pin: 100 nF within 5 mm (CHK C9)"
    else:
        r["limit_mm"], r["meets"], r["basis"] = 10.0, ("yes" if r["copper_mm"] <= 10.0 else "no"), "passive/other: bulk within 10 mm (B12)"

cols = ["net", "load_ref", "load_pad", "nearest_cap", "cap_value", "copper_mm", "straight_mm", "method", "limit_mm", "meets", "basis"]
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

tested = [r for r in rows if r["meets"] in ("yes", "no")]
ok = [r for r in tested if r["meets"] == "yes"]
bad = [r for r in tested if r["meets"] == "no"]
print("rows %d | tested %d | meet %d | fail %d | excluded %d" % (len(rows), len(tested), len(ok), len(bad), len(rows) - len(tested)))
for r in sorted(bad, key=lambda r: -r["copper_mm"]):
    print("  FAIL %-13s %-5s.%-3s %-9s %6.2f mm (limit %s, %s)" % (r["net"], r["load_ref"], r["load_pad"], r["cap_value"], r["copper_mm"], r["limit_mm"], r["method"]))
