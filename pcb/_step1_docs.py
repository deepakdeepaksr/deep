import re

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
ST = ROOT + r"\STAGE_TRACKER.md"
TT = ROOT + r"\TASK_TRACKER.md"

# ---------------- STAGE_TRACKER ----------------
s = open(ST, encoding="utf-8").read()

reps = [
 ("| **Package build** | **blocked** — `revC\\ResponseSheet_RevC.csv` does not exist, so `revC\\pack.ps1` throws by design | `pack.ps1` gate 3 |",
  "| **Package build** | **stops at GATE 5 PRODUCTION** — the response sheet exists and the derived files are current, so the build reaches the production gate and refuses: no release Gerber set at `revC\\gerber`. Correct for this stage | `revC\\pack.ps1` |"),
 ("| **`pack.ps1` does not stage** | `MoriShield_Carrier.kicad_dru` and `MoriShield_Carrier.pretty` — so the receiver cannot re-run our width floors and cannot resolve the project footprints | `pack.ps1` file list |",
  "| **`pack.ps1` stages** | `MoriShield_Carrier.kicad_sym`, `MoriShield_Carrier.kicad_dru` and the whole `MoriShield_Carrier.pretty` into `project\\libraries\\`, with `${KIPRJMOD}/libraries/...` tables in forward slashes — so the receiver can re-run our width floors and resolve the footprints | `revC\\pack.ps1` |"),
 ("| **Derived files older than the design** | BOM, POS front, POS back, `FAB_NOTES.md`, `vias_in_pads.txt` (all 16:54–17:14) and the Gerber preview (16:58) vs board saved 17:49:53 | timestamps, `_cto_extract\\doc_check.py` |",
  "| **Derived files vs the design** | Regenerated from the saved board: BOM 23:51:39, POS front/back 23:51:40, `vias_in_pads.txt` 23:51:32, `FAB_NOTES.md` rewritten; board saved 23:50:46. Gate 4 passes | timestamps |"),
 ("| `/+5V_SENS` series resistance | 177.4 mΩ (was 313 mΩ) | `revC\\EVIDENCE_RevC.md` §7 |",
  "| `/+5V_SENS` series resistance | **156.6 mΩ** (313 → 177.4 → 156.6); 25 segments at 0.80 mm, 12 capped at 0.60 mm | `revC\\EVIDENCE_RevC.md` §7 |"),
 ("| **ERC if the receiver's symbol library is the stale one** | **336 `lib_symbol_issues`** — measured by pointing `sym-lib-table` at `morishield\\...\\libraries\\MoriShield_Carrier.kicad_sym` (153,623 B) instead of the project's own (157,936 B). With the project's own library the count is 0 | `_cto_extract\\erc_x.py` |",
  "| **ERC against the release-layout library** | **0 `lib_symbol_issues`** — was 336 against the stale 153,623 B copy; the copy was refreshed to 157,936 B and the package stages it | `revC\\_work\\scratch\\libtest_after` |"),
 ("| **ERC if the footprint library does not travel** | **124 `footprint_link_issues`** — `fp-lib-table` resolves `../morishield/...`, which only exists in this folder layout | `_cto_extract\\erc_variants.py` |",
  "| **ERC when the footprint library does not travel** | **0 `footprint_link_issues`** — was 124; `pack.ps1` now stages the `.pretty` beside the project | `revC\\pack.ps1` |"),
]
for a, b in reps:
    assert a in s, a[:70]
    s = s.replace(a, b)

# S3 blocked-by: E1 is met, name the real blockers
old_block = "E3 (antenna position unknown); R16 (65 vias in pads, no written agreement); R12 (63 In2 items); E1 (stitching fails the 10 mm rule); C8 (no ESD at J24/J25/J26)"
new_block = "R12 (63 In2.Cu items, needs rerouting); E3 (antenna position unknown, awaiting Aswin's photo); condition-3 copper (3 mm pour and via arrays at J18, blocked on R4); C8 (no ESD at J24/J25/J26)"
assert old_block in s
s = s.replace(old_block, new_block)
open(ST, "w", encoding="utf-8", newline="").write(s)

# ---------------- TASK_TRACKER findings ----------------
t = open(TT, encoding="utf-8").read()
i = t.index("## Part 6")
j = t.index("## Part 7", i)
sec = t[i:j]

new7 = """7. **Nine suppressed checks — found and fixed 2026-11-01.** All nine are re-enabled and nothing
   is set to `ignore`. What they hid: `missing_courtyard` 2 (U4 and SW1 had no courtyard at all),
   `track_not_centered_on_via` 13. Both classes were fixed rather than re-suppressed; the other
   seven report zero items on this board.
"""
new18 = """18. **Two footprints had no courtyard — found and fixed 2026-11-01.** `U4` (SOT-23-5) and `SW1`
    (6 × 6 tact switch) were drawn with no courtyard on either side, so no spacing rule could see
    them. Courtyards were added to the board **and** to the library footprints (`SOT-23-5_HS`,
    `SW_6x6`) at the land extent plus 0.25 mm: U4 x ±2.70, y ±1.50; SW1 x ±4.25, y ±3.25. With
    `missing_courtyard` enabled, both clear and **no courtyard overlaps a neighbour**.
    Evidence: `revC\\_work\\_drc_b12.json` (13 items) → `revC\\drc_RevC.json` (0).
"""
new19 = """19. **The release layout's symbol library was stale — found and fixed 2026-11-01.** ERC against
    the project's own `pcb\\MoriShield_Carrier.kicad_sym` (157,936 B) gave 0 violations; against
    `morishield\\morishield_hardware\\libraries\\MoriShield_Carrier.kicad_sym` (153,623 B) it gave
    **336 `lib_symbol_issues`**. That copy was refreshed to 157,936 B and `pack.ps1` now stages it.
    Measured after the fix: **0 / 0**. Evidence: `revC\\_work\\scratch\\libtest_before|after`.
"""
new20 = """20. **`fp-lib-table` resolved only inside this folder layout — found and fixed 2026-11-01.** The
    project footprint library was reached through `${KIPRJMOD}/../morishield/...`, so anywhere else
    ERC reported **124 `footprint_link_issues`**. `pack.ps1` now stages the `.pretty` inside
    `project\\libraries\\` and rewrites both tables to `${KIPRJMOD}/libraries/...` in forward
    slashes. Measured after the fix: **0**. Evidence: `revC\\pack.ps1`, `revC\\_work\\scratch\\`.
"""

def replace_para(sec, num, new):
    # a paragraph starts with "num. " and ends before the next "NN. " or blank-then-number
    pat = re.compile(r"(?ms)^%d\. .*?(?=^\d+\. |\Z)" % num)
    m = pat.search(sec)
    assert m, "finding %d not found" % num
    return sec[:m.start()] + new + sec[m.end():]

for num, new in ((7, new7), (18, new18), (19, new19), (20, new20)):
    sec = replace_para(sec, num, new)
t = t[:i] + sec + t[j:]
open(TT, "w", encoding="utf-8", newline="").write(t)
print("stage + task tracker updated")
