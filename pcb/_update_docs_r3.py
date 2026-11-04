import re

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
ST = ROOT + r"\STAGE_TRACKER.md"
RT = ROOT + r"\REPLY_TO_CTO.md"
EV = ROOT + r"\revC\EVIDENCE_RevC.md"

def repl_row(path, item, new, section=None):
    t = open(path, encoding="utf-8").read()
    if section:
        i = t.index(section[0]); j = t.index(section[1], i)
        sec = t[i:j].split("\n"); n = 0
        for k, line in enumerate(sec):
            if line.startswith("| %s |" % item):
                sec[k] = new; n += 1
        assert n == 1, "%s in %s: %d" % (item, section[0], n)
        t = t[:i] + "\n".join(sec) + t[j:]
    else:
        lines = t.split("\n"); n = 0
        for k, line in enumerate(lines):
            if line.startswith("| %s |" % item):
                lines[k] = new; n += 1
        assert n == 1, "%s: %d" % (item, n)
        t = "\n".join(lines)
    open(path, "w", encoding="utf-8", newline="").write(t)

# ---- TASK_TRACKER numbers ----
t = open(TT, encoding="utf-8").read()
t = t.replace("| Census | 159 footprints · 1171 track segments · 229 vias · 5 zones · 134 net names | `pcb\\_census.ps1`, `pcbnew` |",
              "| Census | 159 footprints · 1171 track segments · **314 vias** · **6 zones** · 134 net names | `pcb\\_census.ps1`, `pcbnew` |")
t = t.replace("| GND plane distance to a ground link | **max 35.36 mm, 55.6 % beyond 10 mm, 58 links that touch the plane** | `revC\\E1_stitching_plot.png` |",
              "| GND plane distance to a ground link | **max 10.00 mm, 0.0 % beyond 10 mm, 143 links in both pours** (was 35.36 mm / 55.6 % / 58) | `revC\\E1_stitching_plot.png` |")
t = t.replace("| `/+5V_SENS` series resistance | **156.6 mΩ** (was 313, then 177.4) | `revC\\EVIDENCE_RevC.md` §7 |",
              "| `/+5V_SENS` series resistance | **156.6 mΩ**; 0.70 mm tested and rejected (11 clearance items on F.Cu, 2 vias on In2) | `revC\\EVIDENCE_RevC.md` §7 |")
t = t.replace("| `min_text_thickness` | **0.15 mm** (was 0.08, our own number); DRC still 0, so every text meets it | `.kicad_pro`, `revC\\_drc_b3.json` |",
              "| `min_text_thickness` / `min_text_height` | **0.15 mm / 1.0 mm**, both at the CTO's silk rule; DRC still 0 | `.kicad_pro`, `revC\\drc_RevC.json` |")
open(TT, "w", encoding="utf-8", newline="").write(t)

repl_row(TT, "E1",
 "| E1 | P1 | 004 T9 | \"Stitching plot: no point of either ground pour more than 10 mm from a ground link (antenna keep-out excepted).\" | Done | "
 "A GND pour was added on B.Cu (15,174 mm² filled) and 85 stitching vias tie it to the In1 plane. With 143 links, the farthest plane point is "
 "**10.00 mm** and **0.0 %** is beyond 10 mm on the 1 mm grid. Trial first, then applied; DRC 0/0/0 with every check live | "
 "`revC\\E1_stitching_plot.png`; `revC\\_e1_trial_drc5.json` | — |",
 section=("## Part 1", "## Part 2"))

repl_row(TT, "B4",
 "| B4 | P1 | 004 T9 | \"G1 transient; bench capture.\" | Partly | Both input legs 1.5 mm (≈13 mΩ); the 3 mm pour of condition 3 is not met. "
 "`/+5V_SENS` is **156.6 mΩ** (313 → 177.4 → 156.6). 0.70 mm was tested and rejected: 11 clearance items on F.Cu and 2 on In2 (a +5V via and a "
 "3V3_C via), so 0.60 mm is the physical cap on the 55.4 mm In2 run | `revC\\EVIDENCE_RevC.md` §7 | T-06, T-18 |",
 section=("## Part 1", "## Part 2"))

# ---- STAGE_TRACKER ----
s = open(ST, encoding="utf-8").read()
s = s.replace("| Census | 159 footprints · 1171 segments · 229 vias · 5 zones · 134 nets | `pcb\\_census.ps1`, re-run and matched |",
              "| Census | 159 footprints · 1171 segments · 314 vias · 6 zones · 134 nets | `pcb\\_census.ps1` |")
s = s.replace("| GND plane distance to a ground link | max 35.36 mm, 55.6 % beyond 10 mm, 58 links that touch the plane | `revC\\E1_stitching_plot.png` |",
              "| GND plane distance to a ground link | max 10.00 mm, 0.0 % beyond 10 mm, 143 links in both pours | `revC\\E1_stitching_plot.png` |")
open(ST, "w", encoding="utf-8", newline="").write(s)

# ---- REPLY ----
repl_row(RT, "E1",
 "| E1 | A GND pour was added on B.Cu (15,174 mm² filled, PE priority raised so the earth pour keeps its copper) and **85 stitching vias** tie it "
 "to the In1 plane. With **143 links** the farthest point of the plane is **10.00 mm** from one and **0.0 %** is beyond 10 mm, on a 1 mm grid | "
 "`revC\\E1_stitching_plot.png`; `revC\\drc_RevC.json` | Done |")

r = open(RT, encoding="utf-8").read()
# unrequested changes
anchor = "| `min_text_thickness` raised from 0.08 to 0.15 mm | `.kicad_pro` | 0.08 was our own number, not the fab's; DRC still 0, so every text already met 0.15 | Done |"
add = anchor + """
| GND pour added on B.Cu, PE zone priority raised to 1, thermal gap 0.25 / bridge 0.4 | B.Cu, whole board | E1 cannot be met without outer-layer ground copper. PE was given priority so the earth pour cannot be starved; the tighter thermal features clear 7 starved thermals that the default settings produced | Done |
| 85 stitching vias added, 0.6/0.3 mm, GND | B.Cu pour to In1 plane | They are the links that make E1's 10 mm rule hold; each was placed clear of other-net copper and holes | Done |
| `min_text_height` raised from 0.8 to 1.0 mm | `.kicad_pro` | The CTO's silk rule is 1.0 mm; every text already met it, so DRC stayed 0 | Done |"""
assert anchor in r
r = r.replace(anchor, add)

# converter question in section 4
q_anchor = "8. **The 3 A at +70 °C clause (B2).**"
i = r.index(q_anchor)
j = r.index("\n", i)
newq = r[i:j] + "\n9. **Converter (condition 1).** Two candidates are named: the **LM2596HVS** (4.5–50 V in, 3 A peak / about 2 A continuous on its heatsink, multi-turn trim to 5.15 V) already quoted here, and an **XL4015** module (4–38 V in, 5 A, over-temperature shutdown) proposed on 2026-11-01. 38 V sits below the ~39 V surge clamp, so the XL4015 is the same deviation class as the LM2596HVS against the 40 V clause. Which do you want us to design around?"
r = r[:i] + newq + r[j:]
open(RT, "w", encoding="utf-8", newline="").write(r)
print("docs updated")
