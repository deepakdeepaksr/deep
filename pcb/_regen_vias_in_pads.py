"""Regenerate revC\\vias_in_pads.txt from the saved board."""
import pcbnew, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
            rows.append((ref, num, net, fpname, t.GetNetname(), vx, vy, t.GetDrill() / 1e6))
            break

rows.sort(key=lambda r: (r[0], str(r[1])))
lines = ["Vias inside SMD pads - MoriShield Carrier Rev C",
         "source: every via centre tested against every SMD pad on the board",
         "count:  %d of %d vias" % (len(rows), nvias), "",
         "ref      pad  pad net          footprint                          via net              x mm     y mm via drill"]
for (ref, num, net, fpname, vnet, vx, vy, drill) in rows:
    lines.append("%-8s %-4s %-16s %-34s %-20s %7.2f  %7.2f   %.2f" %
                 (ref, num, net, fpname[:34], vnet, vx, vy, drill))
lines += ["",
          "Fix: specify plug/fill/cap per IPC-4761 Class B or C on the fab drawing",
          "(see FAB_NOTES.md). Re-count after any layout change."]
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("wrote %d rows of %d vias" % (len(rows), nvias))
