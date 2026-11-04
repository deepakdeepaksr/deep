"""FAB_NOTES + REPLY_TO_CTO updates for T-55/T-56."""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def edit(fname, pairs):
    path = os.path.join(ROOT, fname)
    text = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in text:
            print("MISS %s: %r" % (fname, old[:60]))
            continue
        text = text.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print("edited", fname)


STRAP = """
## E22 mode straps R56 and R57 (T-55, 2026-11-04)

The E22-900T22D's M0 and M1 pins are hard-strapped to GND through two 0 ohm 0603 resistors, R56 and R57,
at J6.6 (M1) and J6.7 (M0). This is deliberate: it fixes the module in normal (transparent) mode at every
power-up and frees GPIO10 and GPIO11, which the microSD slot uses for CS and MOSI.

**Configuration mode is reached by lifting one strap**, with the module out of its socket: remove R56 or
R57 and the corresponding pin floats high through the module's internal pull-up. The source for that
behaviour is the Ebyte E22-900T22D user manual, **sections 6.2 to 6.5** (M0/M1 mode table and the
configuration procedure). The verbatim text is **not reproduced here because the manual is not in the
workspace** - it is owed into `_cto_extract\\` before this note is quoted to anyone.

Each strap's GND pad has **its own via** to the ground plane at (269.40, 164.92) and (269.40, 162.38); the
straps do not share J6.1's return, which carries the module's own current. The strap runs are on B.Cu
because `/PWR_EN` occupies the F.Cu corridor at x 264.75.
"""

edit("revC/FAB_NOTES.md", [
    ("**67 of 315 vias sit inside an SMD pad on the current board.**",
     "**67 of 319 vias sit inside an SMD pad on the current board.**"),
    ("| Move all 67 off the pads |", "| Move all 67 off the pads |"),
])

path = os.path.join(ROOT, "revC", "FAB_NOTES.md")
text = io.open(path, encoding="utf-8").read()
if "## E22 mode straps R56 and R57" not in text:
    io.open(path, "w", encoding="utf-8", newline="").write(text.rstrip() + "\n" + STRAP)
    print("strap section added")

A7 = ("| A7 | **Closed 2026-11-04.** `/E22_M0` and `/E22_M1` are gone as nets; J1.16 and J1.17 are "
      "`unconnected-(J1-IO10-Pad16)` and `unconnected-(J1-IO11-Pad17)`; M0/M1 are strapped to GND through "
      "0 ohm R56/R57 at J6.6/J6.7, so GPIO10 and GPIO11 are free for the microSD | pad nets read back from "
      "the saved file; `revC\\drc_RevC.json` | Done |")
C2 = ("| C2 | **The conflict is closed 2026-11-04** - GPIO10/11 no longer carry the mode pins, so the slot is "
      "usable. The 24-hour run and the 20 power cuts are still owed and need a plan | pad nets | Partly |")
C5 = ("| C5 | M0 and M1 are now hard-strapped to GND through 0 ohm R56/R57 at J6.6/J6.7. Configuration mode is "
      "reached by lifting one strap with the module out of its socket; AUX and both UART lines are unaffected, "
      "so the read-back stays possible | `revC\\FAB_NOTES.md` | Partly |")
R11 = ("| R11 | **The pin is fixed 2026-11-04**: `/REED_PULSE_F` moved from J2.7 (GPIO41, output-only) to "
       "**J2.9 = GPIO39**; J2.7 is `unconnected-(J2-IO41-Pad7)`. The 1/10/50 Hz bench counts are still owed | "
       "pad nets | New |")
R16 = ("| R16 | **67 of 319 vias sit inside an SMD pad** - re-measured 2026-11-04 from the saved board; the four "
       "strap vias were moved clear, so the count did not rise. DRC cannot see it. Serigreen's written agreement "
       "to plug/fill/cap per IPC-4761 and a price are still owed | `revC\\vias_in_pads.txt` | Open |")

path = os.path.join(ROOT, "REPLY_TO_CTO.md")
lines = io.open(path, encoding="utf-8").read().split("\n")
n = 0
for i, l in enumerate(lines):
    for (start, new) in (("| A7 |", A7), ("| C2 |", C2), ("| C5 |", C5), ("| R11 |", R11), ("| R16 |", R16)):
        if l.startswith(start):
            lines[i] = new
            n += 1
io.open(path, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("reply rows replaced:", n)
