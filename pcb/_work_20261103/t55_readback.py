"""T-55 read-backs: strap pad nets, via-in-pad count, census vs the base snapshot."""
import io
import os
import sys

import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
BASE = os.path.join(ROOT, "pcb", "_snap", "T55_pcb_20261104_075500", "MoriShield_Carrier.kicad_pcb")
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


b = pcbnew.LoadBoard(PCB)
print("== strap pad-net read-back")
for ref, pads in (("J6", ("6", "7")), ("R56", ("1", "2")), ("R57", ("1", "2"))):
    f = b.FindFootprintByReference(ref)
    for p in f.Pads():
        if p.GetNumber() in pads:
            print("  %s.%-2s %-16s (%7.3f,%7.3f)" % (ref, p.GetNumber(), p.GetNetname(),
                                                      p.GetPosition().x / 1e6, p.GetPosition().y / 1e6))

smd = []
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
            bb = p.GetBoundingBox()
            smd.append((f.GetReference(), p.GetNumber(), bb.GetX() / 1e6, bb.GetY() / 1e6,
                        bb.GetRight() / 1e6, bb.GetBottom() / 1e6))
inpad = []
nvias = 0
for t in b.GetTracks():
    if t.Type() != pcbnew.PCB_VIA_T:
        continue
    nvias += 1
    vx, vy = t.GetPosition().x / 1e6, t.GetPosition().y / 1e6
    for (ref, num, x0, y0, x1, y1) in smd:
        if x0 <= vx <= x1 and y0 <= vy <= y1:
            inpad.append((ref, num, vx, vy, t.GetNetname()))
            break
print("\n== vias in SMD pads: %d of %d" % (len(inpad), nvias))
for r in inpad:
    if r[0] in ("R56", "R57"):
        print("   %s.%s (%7.3f,%7.3f) %s" % r)

print("\n== the four new vias")
for t in b.GetTracks():
    if t.Type() != pcbnew.PCB_VIA_T:
        continue
    vx, vy = t.GetPosition().x / 1e6, t.GetPosition().y / 1e6
    if 265.0 <= vx <= 270.0 and 161.0 <= vy <= 166.0:
        print("   (%7.3f,%7.3f) %-16s %s-%s d%.2f" % (vx, vy, t.GetNetname(),
                                                      b.GetLayerName(t.TopLayer()), b.GetLayerName(t.BottomLayer()),
                                                      t.GetWidth(t.TopLayer()) / 1e6))

# segment census vs base
def segs(path):
    text = io.open(path, encoding="utf-8").read()
    root = parse(text)[0]
    out = {}
    for c in root.children:
        if isinstance(c, Node) and c.head == "segment":
            a = c.find("start").atoms()
            e = c.find("end").atoms()
            out[c.value("uuid")] = ((av(a[0]), av(a[1])), (av(e[0]), av(e[1])), c.value("net"), c.value("layer"))
    return out


cur = segs(PCB)
base = segs(BASE)
print("\n== segments: base %d, current %d, delta %d" % (len(base), len(cur), len(cur) - len(base)))
gone = [u for u in base if u not in cur]
new = [u for u in cur if u not in base]
print("   removed %d:" % len(gone))
for u in gone:
    (s, e, n, l) = base[u]
    print("     %s %-16s %s %s -> %s" % (u[:8], n, l, s, e))
print("   added %d:" % len(new))
for u in new:
    (s, e, n, l) = cur[u]
    print("     %s %-16s %s %s -> %s" % (u[:8], n, l, s, e))
