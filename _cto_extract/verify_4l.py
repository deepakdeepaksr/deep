import sys, os, collections, datetime
sys.path.insert(0, r"C:\Program Files\KiCad\10.0\bin")
import pcbnew

PCB = r"c:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\4L\MoriShield_Carrier.kicad_pcb"
b = pcbnew.LoadBoard(PCB)
print("board:", os.path.basename(PCB), "mtime", datetime.datetime.fromtimestamp(os.path.getmtime(PCB)))

# 1. vias inside SMD pads
vias = [t for t in b.GetTracks() if isinstance(t, pcbnew.PCB_VIA)]
pads = []
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
            pads.append((fp.GetReference(), p))
inpad = []
for v in vias:
    vp = v.GetPosition()
    for ref, p in pads:
        if p.HitTest(vp):
            inpad.append((ref, p.GetNumber(), vp.x / 1e6, vp.y / 1e6))
            break
print("vias total:", len(vias), "vias in SMD pads:", len(inpad))

# 2. tracks per layer/net
by_layer = collections.defaultdict(lambda: collections.defaultdict(float))
for t in b.GetTracks():
    if isinstance(t, pcbnew.PCB_VIA):
        continue
    lname = b.GetLayerName(t.GetLayer())
    by_layer[lname][t.GetNetname()] += t.GetLength() / 1e6
for ln in ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu"):
    d = by_layer.get(ln, {})
    tot = sum(d.values())
    print(f"{ln}: {tot:.1f} mm on {len(d)} nets")
    if ln == "In2.Cu":
        for n, L in sorted(d.items(), key=lambda kv: -kv[1]):
            print(f"    {n}: {L:.1f} mm")

# 3. zone fills
for z in b.Zones():
    print("zone:", z.GetNetname(), b.GetLayerName(z.GetLayer()), "filled:", z.IsFilled(),
          "rulearea:", z.GetIsRuleArea(), "area_mm2:", round(z.GetFilledArea() / 1e12, 1) if z.IsFilled() else 0)

# 4. WDT_WDI items
def netitems(name):
    out = []
    for t in b.GetTracks():
        if t.GetNetname() == name:
            if isinstance(t, pcbnew.PCB_VIA):
                out.append(("via", t.GetPosition().x / 1e6, t.GetPosition().y / 1e6))
            else:
                out.append(("track", round(t.GetLength() / 1e6, 2),
                            round(t.GetStart().x / 1e6, 2), round(t.GetStart().y / 1e6, 2),
                            round(t.GetEnd().x / 1e6, 2), round(t.GetEnd().y / 1e6, 2)))
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.GetNetname() == name:
                out.append(("pad", fp.GetReference(), p.GetNumber(), round(p.GetPosition().x / 1e6, 2), round(p.GetPosition().y / 1e6, 2)))
    return out
for n in ("/WDT_WDI", "WDT_WDI"):
    it = netitems(n)
    if it:
        print("net", n, "items:", len(it))
        for i in it:
            print("   ", i)

# 5. J18 pads + silk text near it
for fp in b.GetFootprints():
    if fp.GetReference() in ("J18", "J5", "U4", "Q9", "F1", "J19"):
        pos = fp.GetPosition()
        print(f"{fp.GetReference()}: {fp.GetFPID().GetLibItemName()} at {pos.x/1e6:.2f},{pos.y/1e6:.2f} "
              f"BOM={fp.GetAttributes()} padcount={fp.GetPadCount()}")
        if fp.GetReference() == "J18":
            for p in fp.Pads():
                pp = p.GetPosition()
                print("   pad", p.GetNumber(), p.GetNetname(), f"{pp.x/1e6:.2f},{pp.y/1e6:.2f}")

# silk text items containing 5v
for d in b.GetDrawings():
    if d.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS) and hasattr(d, "GetText"):
        t = d.GetText()
        if "5" in t.lower() and len(t) < 12:
            p = d.GetPosition()
            print("silk:", repr(t), b.GetLayerName(d.GetLayer()), f"{p.x/1e6:.2f},{p.y/1e6:.2f}")

# 6. U4 flags
for fp in b.GetFootprints():
    if fp.GetReference() in ("U4", "U8", "U7"):
        a = fp.GetAttributes()
        print(fp.GetReference(), "attrs:", a,
              "exclBOM=", bool(a & pcbnew.FP_EXCLUDE_FROM_BOM),
              "exclPOS=", bool(a & pcbnew.FP_EXCLUDE_FROM_POS_FILES),
              "boardonly=", bool(a & pcbnew.FP_BOARD_ONLY))

# 7. keepout rule areas
print("rule areas:", len(list(b.Zones())), "zones total; keepouts:",
      sum(1 for z in b.Zones() if z.GetIsRuleArea()))
