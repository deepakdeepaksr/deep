import pcbnew, json, re, collections, os

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
DRC = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC\_reconfirm_drc.json"

b = pcbnew.LoadBoard(PCB)

out = {}

# --- silk violations grouped by refdes ---
drc = json.load(open(DRC, encoding="utf-8"))
silk = [v for v in drc["violations"] if v["type"].startswith("silk")]
byref = collections.Counter()
detail = []
for v in silk:
    refs = []
    for it in v.get("items", []):
        d = it.get("description", "")
        m = re.match(r"([A-Z]+[0-9]+)", d)
        if m:
            refs.append(m.group(1))
        if "Reference" in d or "Value" in d:
            refs.append("FIELD")
    key = ",".join(sorted(set(refs))) if refs else "?"
    byref[key] += 1
    detail.append({"type": v["type"], "sev": v["severity"], "items": [i.get("description", "") for i in v.get("items", [])],
                   "pos": [v["items"][0]["pos"]["x"], v["items"][0]["pos"]["y"]] if v.get("items") else None})
out["silk_total"] = len(silk)
out["silk_by_ref"] = byref.most_common(40)
out["silk_detail"] = detail

# --- tracks per layer, per net (In2) ---
lay = collections.Counter()
in2 = collections.Counter()
in2_len = collections.Counter()
for t in b.GetTracks():
    if t.Type() != pcbnew.PCB_TRACE_T:
        continue
    ln = t.GetLayerName()
    lay[ln] += 1
    if ln == "In2.Cu":
        n = t.GetNetname()
        in2[n] += 1
        in2_len[n] += t.GetLength() / 1e6
out["tracks_by_layer"] = dict(lay)
out["in2_by_net"] = in2.most_common()
out["in2_len_mm"] = {k: round(v, 2) for k, v in in2_len.most_common()}
out["in2_total_mm"] = round(sum(in2_len.values()), 2)

# --- per-net track widths ---
widths = collections.defaultdict(collections.Counter)
for t in b.GetTracks():
    if t.Type() != pcbnew.PCB_TRACE_T:
        continue
    widths[t.GetNetname()][round(t.GetWidth() / 1e6, 3)] += 1
for n in ["/+5V_SENS", "3V3_C", "PE", "+5V"]:
    out.setdefault("widths", {})[n] = dict(widths.get(n, {}))

# --- footprints of interest ---
fpinfo = {}
for f in b.GetFootprints():
    r = f.GetReference()
    if r in ("U7", "U8", "C31", "J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J11", "J12", "J13",
             "J14", "J15", "J16", "J17", "J20", "J21", "J22", "J23", "J24", "J25", "J26", "J18",
             "U4", "U6", "U10", "Q9", "ESD7", "ESD8", "ESD9", "ESD10", "ESD11", "ESD12", "ESD16",
             "ESD17", "ESD18", "ESD19", "ESD20", "ESD1", "ESD2", "ESD3", "ESD4"):
        p = f.GetPosition()
        fpinfo[r] = {
            "pos": [round(p.x / 1e6, 3), round(p.y / 1e6, 3)],
            "fpid": str(f.GetFPID().GetLibItemName()),
            "layer": f.GetLayerName(),
            "pads": [{"n": p.GetNumber(), "net": p.GetNetname(),
                      "pos": [round(p.GetPosition().x / 1e6, 3), round(p.GetPosition().y / 1e6, 3)]}
                     for p in f.Pads()],
        }
out["fps"] = fpinfo

# --- board outline ---
bb = b.GetBoardEdgesBoundingBox()
out["outline_mm"] = [round(bb.GetWidth() / 1e6, 3), round(bb.GetHeight() / 1e6, 3)]
out["outline_xy"] = [round(bb.GetX() / 1e6, 3), round(bb.GetY() / 1e6, 3)]

# --- rule areas ---
out["rule_areas"] = []
for d in b.GetDrawings():
    if d.Type() == pcbnew.PCB_SHAPE_T and d.GetLayerName() in ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu"):
        pass
# zones
out["zones"] = [{"net": z.GetNetname(), "layer": z.GetLayerName(), "area_mm2": round(z.GetFilledArea() / 1e12, 1)}
                for z in b.Zones()]

# --- text items on silk (board-level) ---
txt = []
for d in b.GetDrawings():
    if d.Type() == pcbnew.PCB_TEXT_T:
        txt.append({"layer": d.GetLayerName(), "text": d.GetText(),
                    "pos": [round(d.GetPosition().x / 1e6, 3), round(d.GetPosition().y / 1e6, 3)]})
out["board_texts"] = txt

print(json.dumps(out, indent=1))
