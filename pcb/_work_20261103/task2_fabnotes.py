"""TASK 2.2: update the via-in-pad count in revC\\FAB_NOTES.md from 65/314 to 67/315."""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(ROOT, "revC", "FAB_NOTES.md")
text = io.open(path, encoding="utf-8").read()

PAIRS = [
    ("**65 of 314 vias sit inside an SMD pad on the current board.** That is the same",
     "**67 of 315 vias sit inside an SMD pad on the current board.** The count rose from 65 to 67 during the\n"
     "2026-11-03 reroutes (two new GND vias landed on existing SMD pads), so it is no longer \"the same\" as\n"
     "Rev B. That is the same"),
    ("| Move all 65 off the pads | weeks of re-routing on the densest part of the board | rejected |",
     "| Move all 67 off the pads | weeks of re-routing on the densest part of the board | rejected |"),
    ("and leaves a starved joint, and 20 of the 65 are under passives on the 3V3 and sensor",
     "and leaves a starved joint, and 20 of the 67 are under passives on the 3V3 and sensor"),
    ("The 65 positions are listed in `revC/vias_in_pads.txt` and must be re-counted after",
     "The 67 positions are listed in `revC/vias_in_pads.txt` (one row per via, with reference, pad, net,\n"
     "position and via size) and must be re-counted after"),
]
for old, new in PAIRS:
    if old not in text:
        print("MISS:", old[:60])
        continue
    text = text.replace(old, new, 1)
io.open(path, "w", encoding="utf-8", newline="").write(text)
print("FAB_NOTES updated")
