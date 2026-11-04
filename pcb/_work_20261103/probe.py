"""Dump the board geometry to JSON for offline candidate analysis. Read-only."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geom.json")


def mm(v):
    return round(v / 1e6, 4)


b = pcbnew.LoadBoard(PCB)

fps = []
for f in b.GetFootprints():
    pads = []
    for p in f.Pads():
        bb = p.GetBoundingBox()
        pads.append({
            "num": p.GetNumber(),
            "net": p.GetNetname(),
            "x": mm(p.GetPosition().x),
            "y": mm(p.GetPosition().y),
            "w": mm(p.GetSize().x),
            "h": mm(p.GetSize().y),
            "drill": mm(p.GetDrillSize().x),
            "shape": int(p.GetShape()),
            "type": int(p.GetAttribute()),
            "layers": [b.GetLayerName(l) for l in p.GetLayerSet().Seq()],
            "bbox": [mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetRight()), mm(bb.GetBottom())],
        })
    fpbb = f.GetBoundingBox(False, False)
    cy = f.GetCourtyard(pcbnew.F_CrtYd).BBox()
    fps.append({
        "ref": f.GetReference(),
        "value": f.GetValue(),
        "x": mm(f.GetPosition().x),
        "y": mm(f.GetPosition().y),
        "rot": f.GetOrientationDegrees(),
        "layer": b.GetLayerName(f.GetLayer()),
        "bbox": [mm(fpbb.GetX()), mm(fpbb.GetY()), mm(fpbb.GetRight()), mm(fpbb.GetBottom())],
        "court": [mm(cy.GetX()), mm(cy.GetY()), mm(cy.GetRight()), mm(cy.GetBottom())],
        "pads": pads,
    })

segs = []
for t in b.GetTracks():
    if isinstance(t, pcbnew.PCB_VIA):
        segs.append({
            "kind": "via",
            "uuid": t.m_Uuid.AsString(),
            "net": t.GetNetname(),
            "x": mm(t.GetPosition().x),
            "y": mm(t.GetPosition().y),
            "size": mm(t.GetWidth(t.TopLayer())),
            "drill": mm(t.GetDrillValue()),
            "layers": [b.GetLayerName(l) for l in (t.TopLayer(), t.BottomLayer())],
        })
    else:
        segs.append({
            "kind": "seg",
            "uuid": t.m_Uuid.AsString(),
            "net": t.GetNetname(),
            "layer": b.GetLayerName(t.GetLayer()),
            "x0": mm(t.GetStart().x),
            "y0": mm(t.GetStart().y),
            "x1": mm(t.GetEnd().x),
            "y1": mm(t.GetEnd().y),
            "width": mm(t.GetWidth()),
        })

zones = []
for i in range(b.GetAreaCount()):
    z = b.GetArea(i)
    bb = z.GetBoundingBox()
    zones.append({
        "net": z.GetNetname(),
        "layers": [b.GetLayerName(l) for l in z.GetLayerSet().Seq()],
        "bbox": [mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetRight()), mm(bb.GetBottom())],
        "filled": z.IsFilled(),
        "priority": z.GetAssignedPriority(),
    })

# board outline from Edge.Cuts drawings
edge = []
for d in b.GetDrawings():
    if b.GetLayerName(d.GetLayer()) != "Edge.Cuts":
        continue
    bb = d.GetBoundingBox()
    edge.append({"shape": d.GetClass(), "bbox": [mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetRight()), mm(bb.GetBottom())]})

# silkscreen texts (board + footprint) with layer and position
silk = []
for d in b.GetDrawings():
    if isinstance(d, pcbnew.PCB_TEXT):
        ln = b.GetLayerName(d.GetLayer())
        if ln in ("F.SilkS", "B.SilkS", "F.Fab"):
            p = d.GetPosition()
            bb = d.GetBoundingBox()
            silk.append({"where": "board", "layer": ln, "text": d.GetText(),
                         "x": mm(p.x), "y": mm(p.y),
                         "bbox": [mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetRight()), mm(bb.GetBottom())]})
for f in b.GetFootprints():
    for g in f.GraphicalItems():
        if isinstance(g, pcbnew.PCB_TEXT):
            ln = b.GetLayerName(g.GetLayer())
            if ln in ("F.SilkS", "B.SilkS", "F.Fab"):
                p = g.GetPosition()
                bb = g.GetBoundingBox()
                silk.append({"where": f.GetReference(), "layer": ln, "text": g.GetText(),
                             "x": mm(p.x), "y": mm(p.y),
                             "bbox": [mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetRight()), mm(bb.GetBottom())]})

# reference/value field positions
fields = []
for f in b.GetFootprints():
    for name, it in (("Reference", f.Reference()), ("Value", f.Value())):
        if it is None:
            continue
        p = it.GetPosition()
        bb = it.GetBoundingBox()
        fields.append({"ref": f.GetReference(), "field": name, "text": it.GetText(),
                       "layer": b.GetLayerName(it.GetLayer()), "visible": it.IsVisible(),
                       "x": mm(p.x), "y": mm(p.y), "h": mm(it.GetTextHeight()),
                       "thick": mm(it.GetTextThickness()),
                       "bbox": [mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetRight()), mm(bb.GetBottom())]})

json.dump({
    "footprints": fps, "copper": segs, "zones": zones, "edge": edge,
    "silk": silk, "fields": fields,
}, open(OUT, "w", encoding="utf-8"), indent=1)
print("wrote", OUT, "fps", len(fps), "copper", len(segs), "zones", len(zones))
print("edge:", edge)
