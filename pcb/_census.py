import sys, os
sys.path.insert(0, r"C:\Program Files\KiCad\10.0\bin")
import pcbnew

"""Census guard - counts, total copper length, and vias inside SMD pads.

A pcbnew Save re-issues every UUID and merges collinear/corner segments, so the
segment count alone can fall with no copper lost. Total copper length is the real
guard. Run before and after every board edit and compare all five numbers.
"""

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "MoriShield_Carrier.kicad_pcb")
b = pcbnew.LoadBoard(path)
tr = list(b.GetTracks())
segs = [t for t in tr if type(t).__name__ != "PCB_VIA"]
vias = [t for t in tr if type(t).__name__ == "PCB_VIA"]
zones = [z for z in b.Zones() if not z.GetIsRuleArea()]
length = sum(((t.GetEnd().x - t.GetStart().x) ** 2 +
              (t.GetEnd().y - t.GetStart().y) ** 2) ** 0.5 for t in segs) / 1e6
inpad = 0
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
            continue
        for v in vias:
            if p.HitTest(v.GetPosition()):
                inpad += 1
nets = set()
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname():
            nets.add(p.GetNetname())
for t in tr:
    if t.GetNetname():
        nets.add(t.GetNetname())
print("footprints %d | segments %d | vias %d | zones %d | nets %d"
      % (len(list(b.GetFootprints())), len(segs), len(vias), len(zones), len(nets)))
print("copper length %.3f mm | vias inside SMD pads %d" % (length, inpad))
