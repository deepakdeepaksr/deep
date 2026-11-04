"""Update the three live documents from this session's tool output."""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def edit(fname, pairs):
    path = os.path.join(ROOT, fname)
    text = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in text:
            print("MISS in %s: %r" % (fname, old[:70]))
            continue
        text = text.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print("updated", fname)


edit("TASK_TRACKER.md", [
    # R10: J5 has moved
    ("| R10 | P1 | 001 T13 | \"3D check with the modem fitted.\" | Partly | J5 outside the modem outline "
     "(y 95.83 against a socket row at 113.56); test points under the modem unverified; no standoffs | `pcbnew` positions | T-21 |",
     "| R10 | P1 | 001 T13 | \"3D check with the modem fitted.\" | Partly | **J5 moved out from under the modem "
     "on 2026-11-03**: (239.51, 95.83) -> (222.0, 91.4), courtyard 217.65-226.55 x 87.86-99.45, 1.91 mm clear of "
     "the 228.45 modem edge; DRC 0. TP2/TP3/TP5 stay outside the outline. No standoffs, no 3D models | `pcbnew` "
     "positions, `pcb\\_work_20261103\\B2_drc.json` | T-21 |"),
    # E4 in the reply is wrong about three test points under the modem
    ("| E4 | 12 test points; three under the modem; none on I2C-1 or UART1; the +12 V point is obsolete | TP2\u2013TP12 | Open \u2014 answer requested |",
     "| E4 | 12 test points; **none under the modem** (TP2 274.75, TP3 275.75, TP5 276.25 are outside the "
     "228.50-271.50 outline); none on I2C-1 or UART1; the +12 V point is obsolete | TP2\u2013TP12 | Open \u2014 answer requested |"),
    # C9 row: new measured numbers
    ("**36 supply pins - 21 connector, 6 MOSFET, 6 IC, 3 diode - 0 meet both, 36 fail the local 100 nF rule, 31 fail the bulk rule.** Worst local J25.1 at 173.11 mm; worst bulk J20.1 at 118.51 mm.",
     "**36 supply pins - 21 connector, 6 MOSFET, 6 IC, 3 diode. Re-measured 2026-11-03 with the CTO's verbatim "
     "thresholds (100 nF, 10 uF): 1 meets both (J13.1), 3 meet local, 3 meet bulk, 33 fail local, 33 fail bulk.** "
     "Three capacitors were relocated (C41 -> Q9.3, C14 -> D2.1, C33 -> J13.1) which took local passes 0 -> 3 and "
     "both 0 -> 1. Worst local J25.1 at 90.40 mm; worst bulk J20.1 at 118.51 mm. **J5 is no longer under the modem "
     "and J26 is no longer under the DS3231.** The 13 remaining ADD pins are T-59"),
    # J6 wording: never "mirror image"
    ("    obvious way, J6 looked mirror-imaged - VCC on GPIO10, GND on GPIO11, 5 V on M1.",
     "    obvious way, J6 appeared reversed - VCC on GPIO10, GND on GPIO11, 5 V on M1."),
])

edit("REPLY_TO_CTO.md", [
    ("| R10 | J5 outside the modem outline (y 95.83 against a socket row at 113.56); test points under the modem unverified; no standoffs | `pcbnew` positions | Partly |",
     "| R10 | **J5 moved out from under the modem 2026-11-03** to (222.0, 91.4), 1.91 mm clear of the modem "
     "outline, DRC 0; TP2/TP3/TP5 unchanged; no standoffs, no 3D models | `pcbnew` positions | Partly |"),
])

edit("STAGE_TRACKER.md", [
    ("| Census | 159 footprints \u00b7 1171 segments \u00b7 314 vias \u00b7 6 zones \u00b7 134 nets | `pcb\\_census.ps1` |",
     "| Census | **159 footprints \u00b7 1178 segments \u00b7 313 vias \u00b7 6 zones \u00b7 134 nets** (2026-11-03: "
     "J26 moved, J5 moved, 8 capacitor relocations, 2 +5V segments moved to F.Cu) | `pcb\\_census.ps1` |"),
    ("| Track on In2.Cu | 448.41 mm / 63 segments / 8 nets | `pcbnew` |",
     "| Track on In2.Cu | **431.40 mm / 61 segments / 7 nets** (was 448.41 / 63 / 8; the +5V feed moved to F.Cu) | `pcbnew` |"),
    ("| Decoupling verdict | **36 supply pins (21 connector, 6 MOSFET, 6 IC, 3 diode): 0 meet both, 36 fail local 100 nF, 31 fail bulk** | `revC\\decoupling_map.csv` |",
     "| Decoupling verdict | **36 supply pins (21 connector, 6 MOSFET, 6 IC, 3 diode): 1 meets both (J13.1), 3 meet local, 3 meet bulk, 33 fail local, 33 fail bulk.** Measured with the CTO's verbatim 100 nF / 10 uF thresholds; the earlier 31-fail-bulk figure used 1 uF as bulk and mis-parsed \"100nF/16V\" as 10 uF | `revC\\decoupling_map.csv` |"),
])
