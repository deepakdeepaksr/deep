"""T-55/T-56 wrap: tracker rows, findings, stage numbers, reply rows, tally from gate_truth."""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = sys.executable


def replace_line(fname, startswith, new):
    path = os.path.join(ROOT, fname)
    lines = io.open(path, encoding="utf-8").read().split("\n")
    for i, l in enumerate(lines):
        if l.startswith(startswith):
            lines[i] = new
            io.open(path, "w", encoding="utf-8", newline="").write("\n".join(lines))
            return True
    print("MISS %s %r" % (fname, startswith))
    return False


def edit(fname, pairs):
    path = os.path.join(ROOT, fname)
    text = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in text:
            print("MISS %s: %r" % (fname, old[:60]))
            continue
        text = text.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8", newline="").write(text)


# ---- tally from the rows, never typed
out = subprocess.run([PY, os.path.join(ROOT, "_cto_extract", "gate_truth.py")],
                     capture_output=True, text=True).stdout
tally = None
for line in out.split("\n"):
    if line.strip().startswith("**Gate tally"):
        tally = line.strip()
print("gate_truth:", tally)

A7 = ("| A7 | P0 | 004 T9 | \"Nothing but pads on J1 pins 16 to 20; firmware map agrees.\" | Done | "
      "**Closed 2026-11-04.** The E22 mode pins no longer reach the header: `/E22_M0` and `/E22_M1` were "
      "deleted as nets, J1.16 and J1.17 are `unconnected-(J1-IO10-Pad16)` and `unconnected-(J1-IO11-Pad17)`, "
      "and M0/M1 are strapped to GND through 0 ohm R56/R57 at J6.6/J6.7. GPIO10 and GPIO11 are free for the "
      "microSD. DRC 0/0/0 with parity 0 | pad nets read back from the saved file; `revC\\drc_RevC.json` | T-55 |")
C2R = ("| C2 | P0 | 004 T9 | \"24-hour run; no corruption after 20 power cuts.\" | Partly | "
       "**The conflict is gone 2026-11-04**: GPIO10/11 no longer carry `/E22_M0`/`/E22_M1` (see A7), so the "
       "slot is usable. The 24-hour run and the 20 power cuts are still owed and still need a plan | pad nets; "
       "`revC\\drc_RevC.json` | T-23, T-55 |")
C5R = ("| C5 | P1 | 004 T9 | \"Firmware reads back channel, address, power and key.\" | Partly | "
       "M0 and M1 are now hard-strapped to GND through 0 ohm R56/R57 at J6.6/J6.7, so the mode is fixed at "
       "normal operation. Configuration mode is reached by lifting one strap with the module out of its socket, "
       "recorded in the assembly note. AUX and both UART lines are unaffected, so the read-back itself stays "
       "possible | `revC\\FAB_NOTES.md`; pad nets | T-23, T-55 |")
R11 = ("| R11 | P1 | 001 T13 | \"Pin map (C13); bench counts that match a reference at 1, 10 and 50 Hz.\" | New | "
       "**The pin is fixed 2026-11-04**: `/REED_PULSE_F` moved from J2.7 (GPIO41, output-only) to **J2.9 = "
       "GPIO39**, the only free usable input in that block; J2.7 is `unconnected-(J2-IO41-Pad7)`. The 1/10/50 Hz "
       "counts against a reference are still owed | pad nets; `revC\\drc_RevC.json` | T-56 |")

for (start, new) in (("| A7 | P0 |", A7), ("| C2 | P0 |", C2R), ("| C5 | P1 |", C5R), ("| R11 | P1 |", R11)):
    replace_line("TASK_TRACKER.md", start, new)

replace_line("TASK_TRACKER.md", "| T-55 |", "| T-55 | **DONE 2026-11-04.** E22 M0/M1 strapped to GND through 0 ohm "
             "R56/R57 (0603) at J6.6/J6.7; `/E22_M0` and `/E22_M1` deleted as nets; J1.16/J1.17 set to "
             "`unconnected-(J1-IO10-Pad16)`/`unconnected-(J1-IO11-Pad17)`. ERC 0, DRC 0/0/0 | A7, C2, C5, R11, C11 | DEV | M |")
replace_line("TASK_TRACKER.md", "| T-56 |", "| T-56 | **DONE 2026-11-04.** `/REED_PULSE_F` moved from J2.7 (GPIO41) "
             "to J2.9 (GPIO39); no-connect on J2.7 at the pin, not at the old label x. ERC 0, DRC 0/0/0 | R11, C11, C4 | DEV | S |")

# findings 45-46
FIND = """45. **A KiCad local label named X produces the net `/X`, and a board net without the leading slash
    raises `net_conflict` on the label side only.** Found 2026-11-04 while finishing T-55: the board had
    `E22_M1_STRAP`, the schematic's local label produced `/E22_M1_STRAP`, and DRC reported four
    `net_conflict` items - exactly the strap-side pins (J6.6, J6.7, R56.1, R57.1) and none of the GND pins.
    Renaming the board nets to carry the slash cleared all four on the first run. The tell is that only one
    side of a two-pin part conflicts; a pin-order error would conflict on both. Every other label net on this
    board already carries the slash (`/E22_AUX`, `/UART1_LORA_TX`, `/REED_PULSE_F`).

46. **A pcbnew Save re-issues every UUID and merges collinear or corner segments, so a segment count can fall
    with no copper lost.** Found 2026-11-04: the census read 1178 segments before a save and 1166 after, with
    no edit in between, and a UUID diff showed 139 gone / 127 new - i.e. the survivors were renumbered.
    Total copper length proved nothing was lost: 5306.342 mm -> 5306.609 mm (+0.266 mm, the chord shortening
    of merged corners). The guard is now a rule: re-run DRC immediately before text surgery to get current
    UUIDs, and record **total copper length** at every checkpoint alongside the counts.

"""
path = os.path.join(ROOT, "TASK_TRACKER.md")
text = io.open(path, encoding="utf-8").read()
idx = text.find("## Part 7")
if idx > 0 and "45. **A KiCad local label" not in text:
    io.open(path, "w", encoding="utf-8", newline="").write(text[:idx] + FIND + text[idx:])
    print("findings 45-46 inserted")

if tally:
    edit("TASK_TRACKER.md", [("**Gate tally, counted from the rows above:", "**Gate tally (gate_truth.py):")])
    replace_line("TASK_TRACKER.md", "**Gate tally", tally)
    replace_line("STAGE_TRACKER.md", "| Release gate |", "| Release gate | " + tally.strip("*") + " | `TASK_TRACKER.md` Part 2, `gate_truth.py` |")
print("done")
