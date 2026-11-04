"""TASK 2: regenerate revC\\vias_in_pads.txt from the saved board.

One row per via that sits inside an SMD pad: reference, pad, pad net, position and via size.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
OUT = os.path.join(ROOT, "revC", "vias_in_pads.txt")

b = pcbnew.LoadBoard(PCB)
smd = []
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
            bb = p.GetBoundingBox()
            smd.append((f.GetReference(), p.GetNumber(), p.GetNetname(),
                        str(f.GetFPID().GetLibItemName()),
                        bb.GetX() / 1e6, bb.GetY() / 1e6, bb.GetRight() / 1e6, bb.GetBottom() / 1e6))

rows = []
nvias = 0
for t in b.GetTracks():
    if t.Type() != pcbnew.PCB_VIA_T:
        continue
    nvias += 1
    vx, vy = t.GetPosition().x / 1e6, t.GetPosition().y / 1e6
    for (ref, num, net, fpname, x0, y0, x1, y1) in smd:
        if x0 <= vx <= x1 and y0 <= vy <= y1:
            rows.append((ref, num, net, fpname, t.GetNetname(), vx, vy,
                         t.GetWidth(t.TopLayer()) / 1e6, t.GetDrill() / 1e6))
            break

rows.sort(key=lambda r: (r[0], str(r[1])))
lines = ["Vias inside SMD pads - MoriShield Carrier Rev C",
         "source: every via centre tested against every SMD pad on the board",
         "count:  %d of %d vias" % (len(rows), nvias),
         "note:   the count rose from 65 to %d during the 2026-11-03 reroutes; the IPC-4761" % len(rows),
         "        plug/fill/cap requirement in FAB_NOTES.md is unchanged", "",
         "ref      pad  pad net          footprint                          via net              x mm     y mm  via size  via drill"]
for (ref, num, net, fpname, vnet, vx, vy, size, drill) in rows:
    lines.append("%-8s %-4s %-16s %-34s %-20s %7.2f  %7.2f    %.2f     %.2f" %
                 (ref, num, net, fpname[:34], vnet, vx, vy, size, drill))
lines += ["",
          "Fix: specify plug/fill/cap per IPC-4761 Class B or C on the fab drawing",
          "(see FAB_NOTES.md). Re-count after any layout change."]
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("wrote %d rows of %d vias" % (len(rows), nvias))
