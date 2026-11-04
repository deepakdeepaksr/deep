"""Second documentation pass: E4 wording, T-59 ADD list, new findings."""
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


edit("REPLY_TO_CTO.md", [
    ("| E4 | 12 test points; three under the modem; none on I2C-1 or UART1; the +12 V point is obsolete |",
     "| E4 | 12 test points; none under the modem; none on I2C-1 or UART1; the +12 V point is obsolete |"),
])

ADD_ROWS = """| T-59 | **Place the 13 decoupling capacitors that cannot be moved** (Task C, 2026-11-03). Each row is a legal spot measured on the board; each needs a schematic symbol, so it is a GUI job. 100 nF, 0805 unless noted, one end to the net and one to GND:
| | pin | net | value | footprint | where it should sit | | |
|---|---|---|---|---|---|---|---|
| | J1.1 | 3V3_C | 100 nF | C_0805_2012Metric | (210.50, 157.75) rot 0 | | |
| | J4.3 | 3V3_C | 100 nF | C_0805_2012Metric | (273.50, 117.39) rot 0 | | |
| | J7.2 | 3V3_C | 100 nF | C_0805_2012Metric | (215.65, 163.00) rot 0 | | |
| | J7.8 | 3V3_C | 100 nF | C_0805_2012Metric | (229.14, 169.00) rot 0 | | |
| | J8.5 | 3V3_C | 100 nF | C_0805_2012Metric | (166.06, 157.25) rot 90 | | |
| | J26.1 | 3V3_C | 100 nF | C_0805_2012Metric | (129.75, 152.50) rot 90 | | |
| | J11.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (171.75, 195.00) rot 90 | | |
| | J12.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (187.75, 193.50) rot 90 | | |
| | J15.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (146.13, 193.50) rot 90 | | |
| | J16.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (163.94, 189.50) rot 90 | | |
| | J17.1 | /3V3_SENS_SW | 100 nF | C_0805_2012Metric | (266.75, 194.25) rot 90 | | |
| | J24.1 | +5V | 100 nF | C_0805_2012Metric | (138.97, 147.25) rot 0 | | |
| | D7.1 | /+5V_ESP | 100 nF | C_0805_2012Metric | (215.60, 97.50) rot 90 | | |
| | | | | | | | |
| | **Note** | the five rot-90 spots need a rotated 0805; rotating an existing footprint raises `lib_footprint_mismatch`, so these must be added as new parts, not by turning an existing one. Every spot is legal at the moment of measurement and was checked for copper clearance, hole-to-hole, courtyards and module outlines. | | | | | | |
| | **Also open** | 20 further pins have **no legal spot at all** inside the CTO's radius (6 IC pins at 3 mm, 14 others at 5 mm); they are listed in `revC\\FAB_NOTES.md` and in the Task C report | | | | | |
"""

edit("TASK_TRACKER.md", [
    ("| T-58 | **Ask for a keyed or shrouded header at J6**",
     ADD_ROWS + "| T-58 | **Ask for a keyed or shrouded header at J6**"),
])

FINDINGS = """
37. **A rotated 0805 footprint raises `lib_footprint_mismatch`.** Found 2026-11-03 while moving the decoupling
    capacitors: every cap that was turned from rot 0 to rot 90 produced one `lib_footprint_mismatch` warning,
    while the cap that was already at rot 90 (C43) and the one left at rot 0 (C14) did not. The library copy is
    the reference, so a placed footprint may not be rotated without editing the library too. Consequence: the
    Task C relocations were done at the parts' original rotation, and the five port-row ADD spots that only work
    at rot 90 are handed to Aswin as new parts (T-59).

38. **The decoupling map's bulk test was reading 1 uF as bulk, and "100nF/16V" as 10 uF.** The map's threshold
    was `>= 1 uF`, not the CTO's `10 uF or more`; and the value parser concatenated the voltage digits, so
    `100nF/16V` parsed as 10016 nF = 10.0 uF and counted as bulk. Re-measured with a proper parser and the
    verbatim thresholds the board reads **1 pin meeting both, 3 local, 3 bulk, 33 fail local, 33 fail bulk** -
    not the 31-fail-bulk figure the register carried. The old figure understated the bulk failures.

39. **A 4-pin JST-XH does not fit anywhere on the bottom port row.** Measured 2026-11-03: 347 positions along
    y = 194.5, none legal. The row's courtyards leave 6.6-7.8 mm between ports and the part's courtyard is
    13.49 mm wide; the one 35 mm gap (x 200.4-235.5) is crossed by the /I2C0_SCL_CH0 diagonal at x 218, has
    two GND stitching vias at 207.43 and 219.43, and sits under the GY-521 outline (bottom 192.05). J26 therefore
    went to the left-edge pocket at (134.0, 153.5), 0.36 mm below J24's courtyard and 0.38 mm above R7's.

40. **The +5V 100 nF bank sat in one corner.** C3, C14, C41 and C42 were all inside 16 mm of (282-297, 95),
    while every +5V load pin is 40-160 mm away - the "four 5 V 100 nF still sit together in a corner" finding in
    B12, now measured. Three of the four were relocated onto Q9.3, D2.1 and J24.1; the fourth (C3) has no legal
    spot within 5 mm of any remaining +5V pin.
"""

edit("TASK_TRACKER.md", [
    ("\n---\n\n## Part 7", FINDINGS + "\n---\n\n## Part 7"),
])
