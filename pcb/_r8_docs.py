ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
ST = ROOT + r"\STAGE_TRACKER.md"

t = open(TT, encoding="utf-8").read()
add = """
28. **T-55 could not be completed in this run — 2026-11-03.** The strap correction needs two new schematic symbols and
    two board footprints, two new nets, and the removal of the whole `/E22_M0` and `/E22_M1` copper (13 F.Cu segments,
    82.3 mm, and 10 B.Cu segments, 93.1 mm, **no vias**), plus J1.16/J1.17 freed in both files. The copper half is
    tractable — no vias means no orphaned barrels — but the symbol/footprint/net addition could not be completed and
    verified inside this run's budget. Nothing was changed; the board is as it was at run start.

29. **T-56 was attempted and reverted — 2026-11-03.** The board half applied cleanly (one segment to J2.7 replaced by
    three reaching J2.9, J2.9 taking `/REED_PULSE_F`). The schematic half failed: the label grid for J2 is x 154.94 with
    pads 4-7 at y 297.18, 299.72, 302.26, 304.80, but a label placed at **y 309.88 for pad 9 came back `label_dangling`**,
    so pad 9 is not on that grid. Removing what looked like the pin-9 no-connect actually removed the one at
    **(152.40, 314.96)** and produced ERC 2 / parity 1. Restored from `_snap\\T56_reed_20261103_181533`. J2's symbol pin
    geometry needs the GUI.

30. **T-57 was attempted and reverted — 2026-11-03.** Ten port labels and four J6 marks were placed on F.SilkS at
    1.0 mm / 0.15 mm. DRC returned **15 items** (silk_overlap against connector outlines, ESD parts and reference fields,
    plus silk_over_copper), and two geometric repositioning passes still left 15. Restored from
    `_snap\\T57_silk_20261103_181704`. The bottom edge is too dense for automatic placement; the labels need GUI placement
    or a deliberate silk re-plan that moves the reference fields first.
"""
t = t.replace("\n---\n\n## Part 7", add + "\n---\n\n## Part 7")
open(TT, "w", encoding="utf-8", newline="").write(t)

s = open(ST, encoding="utf-8").read()
s = s.replace("| Release gate | **4 of 13 met (C1, C2, C5, C12)**, 1 partly (C9), 8 not met (C10 now Not met: no antenna area in the file) | `TASK_TRACKER.md` Part 2 |",
              "| Release gate | **4 of 13 met (C1, C2, C5, C12)**, 1 partly (C9), 8 not met (C10: no antenna area in the file) | `TASK_TRACKER.md` Part 2 |")
open(ST, "w", encoding="utf-8", newline="").write(s)
print("trackers updated")
