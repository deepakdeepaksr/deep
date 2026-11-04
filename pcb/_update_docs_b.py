import re

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
ST = ROOT + r"\STAGE_TRACKER.md"
RT = ROOT + r"\REPLY_TO_CTO.md"

t = open(TT, encoding="utf-8").read()

t = t.replace(
"| Suppressed checks | 9 (5 DRC + 4 ERC), none justified in writing, **unchanged for the whole session** (verified against every report in `_cto_extract\\`) | `.kicad_pro` |\n| DRC items the suppressions hide | **15** — 13 `track_not_centered_on_via`, 2 `missing_courtyard` (**U4**, **SW1**) | measured by re-enabling every check on a scratch copy, `_cto_extract\\drcprobe\\` |",
"| Suppressed checks | **0** — all nine re-enabled; nothing is set to `ignore` in DRC or ERC | `.kicad_pro` |\n| DRC items the suppressions hid | **0** — was 15 (13 `track_not_centered_on_via`, 2 `missing_courtyard`); all 15 fixed, none re-suppressed | `revC\\_drc_b3.json` |\n| `min_text_thickness` | **0.15 mm** (was 0.08, our own number); DRC still 0, so every text meets it | `.kicad_pro`, `revC\\_drc_b3.json` |")

t = t.replace(
'| D3 | P2 | 004 T9 | "ERC 0 errors, 0 warnings." | Partly | ERC is now **0/0**; **9 checks are still suppressed** (4 ERC + 5 DRC) with no written justification, which is the half of D3 that remains | `.kicad_pro` `rule_severities` | T-38 |',
'| D3 | P2 | 004 T9 | "ERC 0 errors, 0 warnings." | Done | ERC **0 errors, 0 warnings** with **no suppressed checks**: all nine were re-enabled, the 15 items they hid were fixed, and the count stayed 0 | `revC\\_erc_b3.json`, `revC\\_drc_b3.json`; `.kicad_pro` | — |')

t = t.replace(
"7. **Nine suppressed checks with no written justification.** DRC: `missing_courtyard`,\n   `track_not_centered_on_via`, `tuning_profile_track_geometries`,\n   `footprint_filters_mismatch`, `footprint_type_mismatch`. ERC: `single_global_label`,\n   `four_way_junction`, `simulation_model_issue`, `footprint_filter`. Two of the nine hide real\n   classes of fault: `missing_courtyard` is what C5 forbids downgrading, and\n   `footprint_type_mismatch` is likely hiding an SMD/through-hole mismatch on the sockets.",
"7. **Nine suppressed checks — closed this run.** All nine are now re-enabled and nothing is\n   set to `ignore`. What they hid: `missing_courtyard` 2 (U4 and SW1 had no courtyard at all),\n   `track_not_centered_on_via` 13. Both classes were fixed rather than re-suppressed, and the\n   remaining seven (`tuning_profile_track_geometries`, `footprint_filters_mismatch`,\n   `footprint_type_mismatch`; ERC `single_global_label`, `four_way_junction`,\n   `simulation_model_issue`, `footprint_filter`) report zero items on this board.")

t = t.replace(
"18. **Two footprints have no courtyard, and the suppressed check is exactly the one that would\n    report it.** `U4` (the watchdog) and `SW1` are drawn with no courtyard graphic on either side,\n    so no spacing rule can see them and nothing stops another part being placed over them. Found\n    by re-enabling every suppressed DRC check on a scratch copy: the suppressions hide **15 items\n    in total** — these 2 plus 13 `track_not_centered_on_via`. `missing_courtyard` must be turned\n    back on and justified, not left silent. Evidence: `_cto_extract\\drcprobe\\drc_undenied.json`.",
"18. **Two footprints had no courtyard — fixed this run.** `U4` (SOT-23-5) and `SW1` (6 × 6 tact\n    switch) were drawn with no courtyard on either side, so no spacing rule could see them.\n    Courtyards were added to the board **and** to the library footprints (`SOT-23-5_HS`,\n    `SW_6x6`) at the land extent plus 0.25 mm: U4 x ±2.70, y ±1.50; SW1 x ±4.25, y ±3.25.\n    With `missing_courtyard` re-enabled, both clear and **no courtyard overlaps a neighbour**.\n    Evidence: `revC\\_drc_b12.json` (13 items, courtyards absent) → `revC\\_drc_b3.json` (0).")

open(TT, "w", encoding="utf-8", newline="").write(t)

s = open(ST, encoding="utf-8").read()
s = s.replace("| Suppressed checks | 9 (5 DRC, 4 ERC), unchanged all session | `.kicad_pro`; compared across every report in `_cto_extract\\` |",
              "| Suppressed checks | **0** — all nine re-enabled, nothing ignored | `.kicad_pro` |")
s = s.replace("| **DRC items the nine suppressions hide** | **15** — 13 `track_not_centered_on_via` plus 2 `missing_courtyard` (**U4** and **SW1** have no courtyard at all) | all checks re-enabled on a scratch copy, `_cto_extract\\drcprobe\\drc_undenied.json` |",
              "| **DRC items the nine suppressions hid** | **0** — was 15; all fixed (courtyards added to U4 and SW1, 13 track ends centred) | `revC\\_drc_b3.json` |")
s = s.replace("| **ERC if the receiver's symbol library is the stale one** | **336 `lib_symbol_issues`** - measured by pointing `sym-lib-table` at `morishield\\...\\libraries\\MoriShield_Carrier.kicad_sym` (153,623 B) instead of the project's own (157,936 B). With the project's own library the count is 0 | `_cto_extract\\erc_x.py` |",
              "| **ERC against the release-layout library** | **0 `lib_symbol_issues`, 0 `footprint_link_issues`** - was 336 and 124. The stale 153,623 B library was refreshed to 157,936 B and the package tables now resolve `${KIPRJMOD}/libraries/...` | `revC\\_scratch\\libtest_after` |")
s = s.replace("| **Package build** | **blocked** - `revC\\ResponseSheet_RevC.csv` does not exist, so `revC\\pack.ps1` throws by design | `pack.ps1` gate 3 |",
              "| **Package build** | **blocked at GATE 4** - the response sheet now exists and `pack.ps1` stages the `.kicad_dru` and `.pretty`; it throws because the BOM and placement files are older than the board | `revC\\pack.ps1` |")
open(ST, "w", encoding="utf-8", newline="").write(s)

r = open(RT, encoding="utf-8").read()
r = r.replace("| D3 | ERC is now **0 errors, 0 warnings**; nine checks are still suppressed with no written justification | `revC\\erc_RevC.json`; `.kicad_pro` `rule_severities` | Partly — the suppressions remain |",
              "| D3 | ERC **0 errors, 0 warnings** with **no suppressed checks**: all nine re-enabled, the 15 items they hid fixed (two courtyards drawn, 13 track ends centred), nothing re-suppressed | `revC\\_erc_b3.json`, `revC\\_drc_b3.json` | Done |")
r = r.replace("| One \"Q1 buzzer\" label moved | F.SilkS, from (132.5, 188.5) to (130.0, 191.8) | It sat over R14 pad 1 once its text was raised to the 1.0 mm minimum | Done |",
"""| One "Q1 buzzer" label moved | F.SilkS, from (132.5, 188.5) to (130.0, 191.8) | It sat over R14 pad 1 once its text was raised to the 1.0 mm minimum | Done |
| Courtyards drawn for U4 and SW1, on the board and in the library footprints | `SOT-23-5_HS`, `SW_6x6`; land extent + 0.25 mm | Neither part had one, so no spacing rule could see them. Found by re-enabling the suppressed check | Done |
| Thirteen track ends snapped onto their via centres | 3V3_C, PE, /3V3_SENS_SW, /LED_DRV1/2, /+5V_SENS, /I2C0_MUX_SC0, /I2C0_SDA_CH4 | The suppressed `track_not_centered_on_via` check named them; largest move 0.283 mm | Done |
| `min_text_thickness` raised from 0.08 to 0.15 mm | `.kicad_pro` | 0.08 was our own number, not the fab's; DRC still 0, so every text already met 0.15 | Done |""")
open(RT, "w", encoding="utf-8", newline="").write(r)
print("trackers updated")
