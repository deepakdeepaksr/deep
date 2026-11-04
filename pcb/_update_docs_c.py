import re

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
EV = ROOT + r"\revC\EVIDENCE_RevC.md"
TT = ROOT + r"\TASK_TRACKER.md"
ST = ROOT + r"\STAGE_TRACKER.md"
RT = ROOT + r"\REPLY_TO_CTO.md"

# ---------------- EVIDENCE ----------------
e = open(EV, encoding="utf-8").read()
e = e.replace("""| Measure | Value |
|---|---|
| Ground links (GND vias and through-hole GND pads) | **87** |
| Plane samples | 19,514 |
| Farthest point of the plane from a ground link | **25.9 mm** |
| Share of the plane more than 10 mm from a link | **37.4 %** |

**E1 is not met.** The acceptance is "no point of either ground pour more than 10 mm from a
ground link (antenna keep-out excepted)". The plane is continuous and has 87 links, but more
than a third of it is beyond 10 mm and the worst point is 25.9 mm away. This contradicts the
earlier status of E1 as closed-on-design; it is recorded as open.""",
"""| Measure | Value |
|---|---|
| Ground links that touch the plane (GND vias and GND through-hole pads inside the fill) | **58** |
| Plane samples at 0.5 mm | 78,406 |
| Farthest point of the plane from a ground link | **35.36 mm** |
| Share of the plane more than 10 mm from a link | **55.6 %** |
| Plot | `revC\\E1_stitching_plot.png` |

**E1 is not met.** The acceptance is "no point of either ground pour more than 10 mm from a
ground link (antenna keep-out excepted)". The plane is continuous, but more than half of it is
beyond 10 mm and the worst point is 35.36 mm away.

**Correction to the earlier figure.** The previous 25.9 mm / 37.4 % counted 87 links by taking
every through-hole GND pad regardless of whether it lay inside the plane fill. A pad outside the
fill does not connect to the plane, so it is not a link. The strict set is 58, and the metric is
worse than reported.

**Why stitching vias cannot fix this.** 114 vias were planned at a 0.5 mm grid and added; DRC
reported **all 114 as `via_dangling`**. The board has GND copper only on In1 — there is no GND
pour on F.Cu or B.Cu — so a via dropped into the plane connects on one layer only and is
electrically a stub. This was proved by a control: one via placed **on** an existing F.Cu GND
track produced **0 violations**, while the same via in the pour alone was flagged. The best case
obtainable from existing copper, adding a link every 1 mm along every GND track, leaves
**33.1 % of the plane beyond 10 mm** and the same 24.12 mm worst point (measured with the looser
99-link set). Meeting E1 needs new ground copper on an outer layer, which is a stack-up and
layout decision and cannot be added through this build's zone API (it crashes on save).""")
e = e.replace("""| Total | | **37** | **127.8 mm** | **177.4 mΩ** |

It was 313 mΩ before this session. The remaining 112 mΩ sits in 55.4 mm of 0.5 mm In2 copper
along the J7 pad row: at 0.8 mm the track breaks J7's pad clearance, and the F.Cu corridor is
occupied. Widening it further needs J7 moved or the run rerouted.""",
"""| Total | | **37** | **127.7 mm** | **156.6 mΩ** |

It was 313 mΩ two sessions ago and 177.4 mΩ after the first widening. Every segment is now at
the 0.80 mm class floor except 12 that the corridors cap at 0.60 mm: the 55.4 mm In2 run along
the J7 pad row (93.2 mΩ) and the J13 pad-row runs. At 0.80 mm the In2 run breaks J7's 0.20 mm
pad clearance by 0.05 mm; the band below it is occupied by 3V3_C tracks and vias, U6 and Q4
pads, and the F.Cu corridor is occupied. **156.6 mΩ is the floor for this routing**; going lower
needs the run moved to an outer layer through a new corridor.""")
open(EV, "w", encoding="utf-8", newline="").write(e)

# ---------------- TASK_TRACKER ----------------
t = open(TT, encoding="utf-8").read()
t = t.replace("| GND plane distance to a ground link | **max 25.9 mm, 37.4 % beyond 10 mm, 87 links** | `revC\\_evidence_maps.json` |",
              "| GND plane distance to a ground link | **max 35.36 mm, 55.6 % beyond 10 mm, 58 links that touch the plane** | `revC\\E1_stitching_plot.png` |")
t = t.replace("| `/+5V_SENS` series resistance | **177.4 mΩ** (was 313 mΩ) | `revC\\EVIDENCE_RevC.md` §7 |",
              "| `/+5V_SENS` series resistance | **156.6 mΩ** (was 313, then 177.4) | `revC\\EVIDENCE_RevC.md` §7 |")
t = t.replace('| E1 | P1 | 004 T9 | "Stitching plot: no point of either ground pour more than 10 mm from a ground link (antenna keep-out excepted)." | New | **Measured and failing**: 87 ground links, but 37.4 % of the In1 plane is more than 10 mm from one and the worst point is 25.9 mm. The earlier "closed on design" status is withdrawn | `revC\\_evidence_maps.json`; `revC\\EVIDENCE_RevC.md` §3 | T-39 |',
'| E1 | P1 | 004 T9 | "Stitching plot: no point of either ground pour more than 10 mm from a ground link (antenna keep-out excepted)." | New | **Measured, failing, and not fixable by vias on this stack-up.** 58 links touch the plane; 55.6 % of it is beyond 10 mm, worst 35.36 mm. 114 stitching vias were added and DRC flagged all 114 as dangling: GND exists only on In1, so a via in the pour is a stub. A control via on a GND track was clean. Needs a GND pour on an outer layer | `revC\\E1_stitching_plot.png`; `revC\\EVIDENCE_RevC.md` §3 | T-39 |')
t = t.replace('| B4 | P1 | 004 T9 | "G1 transient; bench capture." | Partly | Both input legs now 1.5 mm (≈13 mΩ); the 3 mm pour of condition 3 is not met; `/+5V_SENS` widened to 0.5–0.8 mm, now **177.4 mΩ** against 313 mΩ before | `revC\\EVIDENCE_RevC.md` §7 | T-06, T-18 |',
'| B4 | P1 | 004 T9 | "G1 transient; bench capture." | Partly | Both input legs now 1.5 mm (≈13 mΩ); the 3 mm pour of condition 3 is not met; `/+5V_SENS` now **156.6 mΩ** (313 → 177.4 → 156.6), every segment at 0.80 mm except 12 capped at 0.60 mm by the J7 and J13 pad rows | `revC\\EVIDENCE_RevC.md` §7 | T-06, T-18 |')
t = t.replace("""11. **The `/+5V_SENS` rail is the most significant unreported electrical defect.** It was
    distributed on 0.20 mm inner-layer copper at about 313 mΩ in series, feeding eight sensor
    ports including a heated SPS30. It has been widened to 0.5–0.8 mm, which the measurement in
    `revC\\EVIDENCE_RevC.md` §7 puts at **177.4 mΩ**, and it still does not meet the 0.80 mm class
    floor along its whole length (55.4 mm of 0.5 mm In2 copper accounts for the rest).""",
"""11. **The `/+5V_SENS` rail is the most significant unreported electrical defect.** It was
    distributed on 0.20 mm inner-layer copper at about 313 mΩ in series, feeding eight sensor
    ports including a heated SPS30. It is now **156.6 mΩ**: every segment meets the 0.80 mm
    class floor except 12 that the corridors cap at 0.60 mm, of which the 55.4 mm In2 run along
    the J7 pad row accounts for 93.2 mΩ. At 0.80 mm that run breaks J7's pad clearance by
    0.05 mm and the band below it is occupied by 3V3_C, U6 and Q4 copper.""")
open(TT, "w", encoding="utf-8", newline="").write(t)

# ---------------- STAGE_TRACKER ----------------
s = open(ST, encoding="utf-8").read()
s = s.replace("| GND plane distance to a ground link | max 25.9 mm, 37.4 % beyond 10 mm, 87 links | `revC\\_evidence_maps.json` |",
              "| GND plane distance to a ground link | max 35.36 mm, 55.6 % beyond 10 mm, 58 links that touch the plane | `revC\\E1_stitching_plot.png` |")
s = s.replace("| `/+5V_SENS` series resistance | 177.4 mO (was 313 mO) | `revC\\EVIDENCE_RevC.md` §7 |",
              "| `/+5V_SENS` series resistance | 156.6 mΩ (was 313, then 177.4) | `revC\\EVIDENCE_RevC.md` §7 |")
open(ST, "w", encoding="utf-8", newline="").write(s)

# ---------------- REPLY ----------------
r = open(RT, encoding="utf-8").read()
r = r.replace('| E1 | **Measured and failing.** The In1 plane has 87 ground links, but 37.4 % of it is more than 10 mm from one and the farthest point is 25.9 mm, against your 10 mm acceptance | `revC\\_evidence_maps.json`; `revC\\EVIDENCE_RevC.md` §3 | Partly — the plane is continuous but the 10 mm rule is not met |',
'| E1 | **Measured and failing.** 58 links touch the In1 plane; 55.6 % of it is more than 10 mm from one and the farthest point is 35.36 mm, against your 10 mm acceptance. 114 stitching vias were tried and all 114 were reported dangling: GND exists only on In1, so a via in the pour connects on one layer and is a stub. Meeting 10 mm needs a GND pour on an outer layer | `revC\\E1_stitching_plot.png`; `revC\\EVIDENCE_RevC.md` §3 | Partly — the plane is continuous; the 10 mm rule cannot be met by vias on this stack-up |')
r = r.replace('| B4 | Both input legs widened to 1.5 mm (≈13 mΩ). The 3 mm pour of condition 3 is not met. `/+5V_SENS` widened to 0.5–0.8 mm, which takes it from 313 mΩ to **177.4 mΩ** | `revC\\EVIDENCE_RevC.md` §7 | Partly |',
'| B4 | Both input legs widened to 1.5 mm (≈13 mΩ). The 3 mm pour of condition 3 is not met. `/+5V_SENS` now meets the 0.80 mm class floor except 12 segments capped at 0.60 mm, taking it from 313 mΩ to **156.6 mΩ** | `revC\\EVIDENCE_RevC.md` §7 | Partly |')
open(RT, "w", encoding="utf-8", newline="").write(r)
print("docs updated")
