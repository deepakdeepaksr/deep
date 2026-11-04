import re
ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
ST = ROOT + r"\STAGE_TRACKER.md"

t = open(TT, encoding="utf-8").read()
lines = t.split("\n")
for i, line in enumerate(lines):
    if line.startswith("| **C12** Silkscreen and marking |"):
        lines[i] = ('| **C12** Silkscreen and marking | "Every polarity mark sits beside the right pad on the plotted Gerber; '
          'the board carries name, revision and serial box; no silk over copper." | **Met** | Verified on the plotted Gerber '
          '`revC\\silk_check\\MoriShield_Carrier-F_Silkscreen.gto` (12,128 strokes), not in the editor: `+` centre y 107.20 vs '
          'pad 1 at 107.25 (Δ0.05 mm), `−` centre y 102.20 vs pad 2 at 102.25 (Δ0.05), both 6.3 mm beside their pads; board '
          'name, `Rev C` and `S/N` present; 29 polarity-bearing parts carry plotted silk; silk-over-copper and silk-overlap 0 '
          'in DRC with those checks enabled. Timestamps: save 23:50:46, DRC 18:00:32, plot 18:01:36 | `revC\\silk_check\\`, '
          '`revC\\drc_RevC.json` |')
    if line.startswith("| **C9** Placement |"):
        lines[i] = ('| **C9** Placement | "The decoupling map shows every supply pin inside the distance; the 3D check shows '
          'every module on its right socket with the box closed; nothing reachable sits under a module." | **Partly** | The map '
          'now carries `limit_mm`, `meets` and `basis` per row: 3 mm for an IC pin, 5 mm for a port pin, 10 mm for bulk, quoted '
          'from CHK C9/B7/B12. **27 supply pins tested, 0 meet, 27 fail** — worst J4.3 at 51.29 mm, best J14 at 5.11 mm against 5.0. '
          'Module outlines: the GY-521 and DS3231 labels were measured on each other\'s sockets and swapped, outlines resized to '
          '21×16 and 38×22; heights TBC (no vendor drawing). Enclosure 200×155×80, four M3 standoffs, base plate and 8 glands drawn '
          'on Dwgs.User. Renders regenerated but **the box and modules are not visible in 3D** — no 3D models attached. Under-module '
          'survey: modem socket has TP2, TP3, TP5 and J5 beneath it; DS3231 8 parts; GY-521 2 parts | `revC\\decoupling_map.csv`, '
          '`revC\\render_*.png` |')
open(TT, "w", encoding="utf-8", newline="").write("\n".join(lines))

# R12 table into Part 5 under T-08
t = open(TT, encoding="utf-8").read()
rows = [
 ("/LED_DRV2", 14, 109.8, "152.7-251.5", "141.1-166.1", -0.03, 0.19, 0.30, "no"),
 ("/LED_DRV1", 8, 100.9, "153.9-247.6", "149.1-165.8", -0.15, -0.01, 0.30, "no"),
 ("/+5V_SENS", 13, 76.7, "176.1-246.9", "166.0-176.0", -0.15, -0.01, 0.60, "no"),
 ("3V3_C", 10, 63.1, "245.0-269.6", "118.6-167.5", -0.01, 0.01, 0.35, "no"),
 ("/SENS_EN", 7, 52.6, "194.0-241.2", "179.2-183.3", -0.01, -0.19, 0.35, "no"),
 ("/I2C0_SCL", 7, 22.5, "241.8-256.4", "164.5-177.7", 0.00, 0.13, 0.30, "no"),
 ("+5V", 2, 17.1, "225.5-239.5", "95.8-103.2", 10.99, 6.93, 0.95, "yes"),
 ("/I2C0_MUX_SC0", 2, 5.7, "229.7-234.5", "179.3-181.5", -0.04, 0.15, 0.30, "no"),
]
tbl = ["", "**R12 per-net plan, measured 2026-11-02** (In2.Cu to an outer layer). Corridor is the clearance from the segment",
       "midpoint to the nearest other-net copper on that outer layer, minus that copper's half-width; `need` is the",
       "track half-width plus 0.20 mm. A negative corridor means the outer layer is already occupied at that point.", "",
       "| Net | Segments | Length mm | x span | y span | F.Cu corridor | B.Cu corridor | Need | Move without reroute |",
       "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    tbl.append("| `%s` | %d | %.1f | %s | %s | %.2f | %.2f | %.2f | **%s** |" % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]))
tbl += ["", "**Verdict: 1 of 8 nets can move without a reroute (`+5V`, 17.1 mm). The other seven have no free outer-layer",
        "corridor** — `/LED_DRV1` and `/+5V_SENS` are already overlapping other copper on F.Cu (−0.15 mm). R12 therefore needs",
        "real rerouting on seven nets, not a layer-token change; that is why nothing was moved today. Evidence:",
        "`revC\\_work\\_r12_plan.json`, `pcb\\_reach_and_r12.py`."]
anchor = "| T-08 | Move the 63 In2.Cu track items to outer layers | R12, C10 | HW | L |"
assert anchor in t
t = t.replace(anchor, anchor + "\n" + "\n".join(tbl))
open(TT, "w", encoding="utf-8", newline="").write(t)

# STAGE_TRACKER numbers + tally
s = open(ST, encoding="utf-8").read()
s = s.replace("| Release gate | 2 of 13 met (C1, C2), 2 partly (C5, C12) | `TASK_TRACKER.md` Part 2 |",
              "| Release gate | **4 of 13 met (C1, C2, C5, C12)**, 2 partly (C9, C10), 7 not met | `TASK_TRACKER.md` Part 2 |")
s = s.replace("| Vias in SMD pads | 65 | `revC\\vias_in_pads.txt` |",
              "| Vias in SMD pads | 65 of 314, fab note in place (check C5 met) | `revC\\vias_in_pads.txt`, `revC\\FAB_NOTES.md` |")
s = s.replace("| Title block | `Rev C`, `2026-11-01`, A0 sheet | `.kicad_sch` |",
              "| Title block | `Rev C`, `2026-11-01`, A0 sheet | `.kicad_sch` |\n| Silk verification plot | 12,128 strokes; J18 marks Δ0.05 mm; name/Rev/S-N present | `revC\\silk_check\\` |\n| Decoupling verdict | 27 supply pins tested, **0 meet**, 27 fail | `revC\\decoupling_map.csv` |")
open(ST, "w", encoding="utf-8", newline="").write(s)
print("trackers updated")
