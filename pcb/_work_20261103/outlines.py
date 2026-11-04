"""Dump board-level drawings (module outlines etc.) and texts."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
b = pcbnew.LoadBoard(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"))


def mm(v):
    return round(v / 1e6, 3)


for d in b.GetDrawings():
    ln = b.GetLayerName(d.GetLayer())
    if ln in ("Edge.Cuts",):
        continue
    if isinstance(d, pcbnew.PCB_SHAPE):
        bb = d.GetBoundingBox()
        print("SHAPE %-10s %-12s bbox (%8.3f,%8.3f)-(%8.3f,%8.3f)" %
              (d.GetShapeStr() if hasattr(d, "GetShapeStr") else d.GetClass(), ln,
               mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetRight()), mm(bb.GetBottom())))
    elif isinstance(d, pcbnew.PCB_TEXT):
        p = d.GetPosition()
        print("TEXT  %-10s %-12s '%s' at (%8.3f,%8.3f)" % ("text", ln, d.GetText(), mm(p.x), mm(p.y)))
