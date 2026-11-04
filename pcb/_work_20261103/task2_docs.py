"""TASK 2.3: bring the via-in-pad numbers in the three live documents onto the board.

Via count is now 315 (313 + the two E1 stitching vias added in Task 1); 67 sit in SMD pads.
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def edit(fname, pairs):
    path = os.path.join(ROOT, fname)
    text = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in text:
            print("MISS %s: %r" % (fname, old[:70]))
            continue
        text = text.replace(old, new)
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print("updated", fname)


edit("TASK_TRACKER.md", [
    ("**67 of 314**", "**67 of 315**"),
    ("| T-09 | Resolve the 65 vias in SMD pads: move them, or agree filled-and-capped in writing | R16, C5 | HW | L |",
     "| T-09 | Resolve the 67 vias in SMD pads: move them, or agree filled-and-capped in writing | R16, C5 | HW | L |"),
    ("1. **65 vias inside SMD pads.** Unchanged from Rev B's number (R16 quotes 65), so the item is",
     "1. **67 vias inside SMD pads** (65 in Rev B; two appeared in the 2026-11-03 reroutes). The item is"),
    ("re-counted today at 65 of 314. The recommended fix is one fab note - plug, fill and cap per",
     "re-counted 2026-11-03 at 67 of 315. The recommended fix is one fab note - plug, fill and cap per"),
    ("`revC\\FAB_NOTES.md` still state 65 of 314, so check C5's evidence is now",
     "`revC\\FAB_NOTES.md` were regenerated to 67 of 315 on 2026-11-03, so check C5's evidence now"),
])

edit("STAGE_TRACKER.md", [
    ("| Vias in SMD pads | **67 of 314** (was 65); the fab note still says 65 and must be regenerated | `revC\\vias_in_pads.txt`, `revC\\FAB_NOTES.md` |",
     "| Vias in SMD pads | **67 of 315** (was 65 of 314); `revC\\vias_in_pads.txt` and `revC\\FAB_NOTES.md` regenerated 2026-11-03 and agree with the board | `revC\\vias_in_pads.txt`, `revC\\FAB_NOTES.md` |"),
])

edit("REPLY_TO_CTO.md", [
    ("**67 of 314 vias sit inside an SMD pad**", "**67 of 315 vias sit inside an SMD pad**"),
    ("7. **Vias in SMD pads (R16), now 67 of 314.**", "7. **Vias in SMD pads (R16), now 67 of 315.**"),
])
