"""STEP 3: two-requirement decoupling map (local 100 nF and bulk 10 uF), every row classified."""
import pcbnew, math, collections, heapq, csv

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
OUT = ROOT + r"\revC\decoupling_map.csv"

b = pcbnew.LoadBoard(PCB)
SUPPLY = ["+5V", "+5V_IN", "+5V_F", "/+5V_ESP", "/+5V_SENS", "/+5V_E22", "/+5V_E22_IN",
          "3V3_C", "/3V3_SENS", "/3V3_SENS_SW"]

def key(x, y): return (round(x, 3), round(y, 3))

graph = collections.defaultdict(list); segs = collections.defaultdict(list)
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_TRACE_T:
        s, e = t.GetStart(), t.GetEnd()
        a, c = key(s.x/1e6, s.y/1e6), key(e.x/1e6, e.y/1e6)
        L = math.hypot(c[0]-a[0], c[1]-a[1])
        graph[a].append((c, L)); graph[c].append((a, L)); segs[t.GetNetname()].append((a, c))
    elif t.Type() == pcbnew.PCB_VIA_T:
        p = t.GetPosition(); a = key(p.x/1e6, p.y/1e6)
        graph[a].append((a, 0.0)); graph[a].append((a, 0.0))

pads = []
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname():
            pads.append({"ref": f.GetReference(), "pad": p.GetNumber(), "net": p.GetNetname(),
                         "x": p.GetPosition().x/1e6, "y": p.GetPosition().y/1e6,
                         "val": f.GetValue(), "fp": str(f.GetFPID().GetLibItemName())})
padnode = {}
for pd in pads:
    best = None
    for (a, c) in segs.get(pd["net"], []):
        for q in (a, c):
            d = math.hypot(q[0]-pd["x"], q[1]-pd["y"])
            if best is None or d < best[0]: best = (d, q)
    if best and best[0] < 1.5: padnode[(pd["ref"], pd["pad"])] = best[1]

def dij(src, dst):
    if src is None or dst is None or src not in graph or dst not in graph: return None
    dist = {src: 0.0}; pq = [(0.0, src)]; seen = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in seen: continue
        seen.add(u)
        if u == dst: return d
        for (v, w) in graph[u]:
            nd = d + w
            if nd < dist.get(v, 1e18): dist[v] = nd; heapq.heappush(pq, (nd, v))
    return None

def is_cap(pd): return pd["fp"].startswith(("C_", "CP_"))
def val_uf(v):
    v = v.upper().replace("UF", "").replace("NF", "").replace("PF", "")
    try:
        f = float("".join(ch for ch in v if ch.isdigit() or ch == "."))
    except Exception:
        return 0.0
    if "N" in v or "N" in v: pass
    return f

def cap_uf(pd):
    s = pd["val"].upper()
    num = "".join(ch for ch in s if ch.isdigit() or ch == ".")
    try: f = float(num)
    except Exception: return 0.0
    if "NF" in s: return f/1000.0
    if "PF" in s: return f/1e6
    if "UF" in s: return f
    return f

CLASS = {"U": "IC", "Q": "MOSFET", "D": "diode", "J": "connector"}
rows = []
for pd in pads:
    if pd["net"] not in SUPPLY or is_cap(pd): continue
    cls = CLASS.get(pd["ref"][:1])
    if cls is None: continue
    caps = [q for q in pads if q["net"] == pd["net"] and is_cap(q)]
    if not caps: continue
    src = padnode.get((pd["ref"], pd["pad"]))
    def nearest(subset):
        best = None
        for cp in subset:
            tr = dij(src, padnode.get((cp["ref"], cp["pad"])))
            sl = math.hypot(cp["x"]-pd["x"], cp["y"]-pd["y"])
            d = tr if tr is not None else sl
            meth = "track" if tr is not None else "plane"
            if best is None or d < best[0]: best = (d, meth, cp)
        return best
    small = [c for c in caps if cap_uf(c) <= 0.22]
    bulk = [c for c in caps if cap_uf(c) >= 1.0]
    ns = nearest(small) if small else None
    nb = nearest(bulk) if bulk else None
    llim = 3.0 if cls == "IC" else 5.0
    rows.append({
        "net": pd["net"], "load_ref": pd["ref"], "load_pad": pd["pad"], "class": cls,
        "local_cap": ns[2]["ref"] if ns else "", "local_val": ns[2]["val"] if ns else "",
        "local_100nf_mm": round(ns[0], 2) if ns else "", "local_method": ns[1] if ns else "",
        "local_limit_mm": llim, "local_meets": ("yes" if ns and ns[0] <= llim else "no"),
        "bulk_cap": nb[2]["ref"] if nb else "", "bulk_val": nb[2]["val"] if nb else "",
        "bulk_mm": round(nb[0], 2) if nb else "", "bulk_meets": ("yes" if nb and nb[0] <= 10.0 else "no"),
        "pin_x": round(pd["x"], 2), "pin_y": round(pd["y"], 2),
        "local_x": round(ns[2]["x"], 2) if ns else "", "local_y": round(ns[2]["y"], 2) if ns else "",
    })

cols = ["net", "load_ref", "load_pad", "class", "local_cap", "local_val", "local_100nf_mm", "local_method",
        "local_limit_mm", "local_meets", "bulk_cap", "bulk_val", "bulk_mm", "bulk_meets",
        "pin_x", "pin_y", "local_x", "local_y"]
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

by = collections.defaultdict(lambda: [0, 0, 0])
for r in rows:
    by[r["class"]][0] += 1
    if r["local_meets"] == "yes" and r["bulk_meets"] == "yes": by[r["class"]][1] += 1
    else: by[r["class"]][2] += 1
print("rows %d" % len(rows))
for k, v in by.items():
    print("  %-10s pins %2d  both meet %2d  fail %2d" % (k, v[0], v[1], v[2]))
lf = sum(1 for r in rows if r["local_meets"] == "no")
bf = sum(1 for r in rows if r["bulk_meets"] == "no")
print("local 100nF failures: %d | bulk failures: %d | rows meeting both: %d" % (lf, bf, sum(v[1] for v in by.values())))
print("worst local:", [(r["load_ref"]+"."+r["load_pad"], r["local_100nf_mm"]) for r in sorted([x for x in rows if x["local_100nf_mm"] != ""], key=lambda x: -float(x["local_100nf_mm"]))[:4]])
print("worst bulk :", [(r["load_ref"]+"."+r["load_pad"], r["bulk_mm"]) for r in sorted([x for x in rows if x["bulk_mm"] != ""], key=lambda x: -float(x["bulk_mm"]))[:4]])
