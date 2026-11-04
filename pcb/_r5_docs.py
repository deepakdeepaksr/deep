import re
ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
ST = ROOT + r"\STAGE_TRACKER.md"

t = open(TT, encoding="utf-8").read()

# B1: the pin order is now known; the correction is proven but not yet in copper
lines = t.split("\n")
for i, line in enumerate(lines):
    if line.startswith("| B1 |"):
        lines[i] = ('| B1 | P1 | 004 T9 | "Clamp simulation; no TVS current at the highest charge voltage." | Open | '
          'The E22 header order is now **known and proven wrong in copper**: the Ebyte manual gives pin 1 M0, 2 M1, 3 RXD, 4 TXD, '
          '5 AUX, 6 VCC, 7 GND, while J6 carries the reverse. A net-level correction was applied and reverted on 2026-11-02: parity '
          'stayed 0 but the copper fanout still landed on the old pads (**24 DRC items, 3 unconnected**), so the seven nets must be '
          'rerouted at J6 before the change can hold. Snapshot `pcb\\_snap\\T12_lora_20261102_223013` | '
          '`revC\\_work\\_r5_drc2.json` | T-53 |')
open(TT, "w", encoding="utf-8", newline="").write("\n".join(lines))

t = open(TT, encoding="utf-8").read()
# Part 6 additions
add = """
22. **The E22 antenna keep-out area is crossed by two B.Cu tracks — found 2026-11-02.** The area the brief
    specifies (x 296.00-304.57, y 163.00-177.00) contains no track endpoints, via or pad, but two long
    B.Cu segments pass through it: `/3V3_SENS_SW` (37.05 mm) and `/I2C0_SDA_CH3` (46.00 mm). A rule area
    with tracks, vias, pads and fill excluded therefore reports **2 `items_not_allowed` and 1 unconnected**.
    It was drawn, measured and removed rather than left in the file. E3 cannot close until those two runs
    are moved. Evidence: `revC\\_work\\_r5_drc5.json`.

23. **The J6 rewire is a reroute, not a net rename — measured 2026-11-02.** Applying the correct mapping to
    the pads and labels kept parity at 0, which proves the netlist change is right, but produced **24 DRC
    violations and 3 unconnected items** because every track still ends on the pad it was drawn to. Seven
    nets must swap positions in a vertical row, so they cross unless routed on two layers. Reverted.

24. **Two of the five module outlines were on the wrong sockets, measured 2026-11-01.** The `GY-521` label
    sat on J8 (the RTC socket) and `DS3231 RTC` on J7 (the IMU socket). Corrected, and the envelopes resized
    to the measured 21x16 and 38x22. The E22 outline was 43.5 x 22.5 mm against a 37 x 22 mm module and is
    now 37 x 22; the ESP32 32 x 68 is now 32 x 65; the modem 49 x 60 is now 43 x 60.
"""
t = t.replace("\n---\n\n## Part 7", add + "\n---\n\n## Part 7")
open(TT, "w", encoding="utf-8", newline="").write(t)

# C10 stays Not met, with the missing clause named
lines = t.split("\n")
for i, line in enumerate(lines):
    if line.startswith("| **C10** Layout |"):
        lines[i] = ('| **C10** Layout | "The plane layers show nothing but their planes; the antenna rule area is in the file '
          'and empty on every layer; the spacing rules are met with the rule file matching the board; the power copper meets '
          'check C7; stitching is in." | **Not met** | 63 items still on In2 (R12, 1 of 8 nets movable); **the antenna rule area '
          'clause is missing** - the E22 area is crossed by two B.Cu tracks and the modem U.FL and ESP32 antenna ends are still '
          'unidentified, so no area is in the file; spacing rules and `.kicad_dru` match the board; power copper still 1.5 mm; '
          'stitching is in and measured | `revC\\_work\\_r5_drc5.json` |')
open(TT, "w", encoding="utf-8", newline="").write("\n".join(lines))

# STAGE_TRACKER numbers
s = open(ST, encoding="utf-8").read()
s = s.replace("| Release gate | **4 of 13 met (C1, C2, C5, C12)**, 2 partly (C9, C10), 7 not met | `TASK_TRACKER.md` Part 2 |",
              "| Release gate | **4 of 13 met (C1, C2, C5, C12)**, 1 partly (C9), 8 not met (C10 now Not met: no antenna area in the file) | `TASK_TRACKER.md` Part 2 |")
open(ST, "w", encoding="utf-8", newline="").write(s)
print("trackers updated")
