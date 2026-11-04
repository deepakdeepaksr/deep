import re

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
RT = ROOT + r"\REPLY_TO_CTO.md"

# ---------------- REPLY: D3 -> Done ----------------
r = open(RT, encoding="utf-8").read()
old_d3 = "| D3 | ERC is now **0 errors, 0 warnings**; nine checks are still suppressed with no written justification. We measured what they hide: re-enabling all nine on a copy adds **15 DRC items** - 13 `track_not_centered_on_via` and 2 `missing_courtyard`, which are `U4` and `SW1`, the two footprints drawn with no courtyard at all | `revC\\erc_RevC.json`; `.kicad_pro` `rule_severities`; the lifted-suppression run in `_cto_extract\\drcprobe\\` | Partly - the suppressions remain and 15 items are behind them |"
new_d3 = "| D3 | ERC **0 errors, 0 warnings** and **no suppressed checks at all**: all nine re-enabled. What they hid is fixed, not re-suppressed: courtyards drawn for U4 and SW1 (board and library), 13 track ends centred on their vias. DRC stayed 0 with every check live | `revC\\erc_RevC.json`, `revC\\drc_RevC.json`; `.kicad_pro` `rule_severities` (no `ignore` entries) | Done |"
assert old_d3 in r, "D3 anchor not found"
r = r.replace(old_d3, new_d3)

# ---------------- REPLY: C5 -> Partly (separate pins done, SD conflict open) ----------------
old_c5 = "| C5 | M0/M1 on separate pins but both in the microSD group | pad nets | Open — answer requested (question 3) |"
new_c5 = "| C5 | M0 and M1 are on separate pins as the item requires, but both still sit in the GPIO10/11 group that CHK-001 C11 calls the microSD | pad nets; `revC\\drc_RevC.json` | Partly — the separate-pin half is in place; the microSD conflict is question 3 |"
assert old_c5 in r, "C5 anchor not found"
r = r.replace(old_c5, new_c5)

# ---------------- REPLY: declare the status mapping ----------------
old_hdr = """Status words: **Done** · **Partly** (what is missing is named) · **Deferred** (only with
Serigreen's message and date, which we do not yet hold) · **Rejected** (reason) ·
**Agreed before drawing** · **Superseded** · **Open — answer requested**."""
new_hdr = """Status words used here are the response-sheet vocabulary of MS-CAR-CHK-001 §7:
**Done** · **Partly** (what is missing is named) · **Deferred** (only with Serigreen's message
and date, which we do not yet hold) · **Rejected** (reason) · **Agreed before drawing** ·
**Superseded**. One word is added because the vocabulary has no "not started" term:
**Open — answer requested** means nothing has been done and a question is attached.

Our internal register in `TASK_TRACKER.md` uses six words. The mapping is declared here so that
nothing is silently upgraded or downgraded:

| Register word | Meaning in the register | Status written here |
|---|---|---|
| Done | designed in and evidenced | **Done** |
| Paper | design complete, bench or measurement result owed | **Partly** (bench result owed) |
| Partly | some of it is in the files | **Partly** |
| New | regressed or newly understood; nothing in place | **Open — answer requested** |
| Open | not started, or started and reverted | **Open — answer requested** |
| Superseded | the design change removed the item | **Superseded** |

The same table appears at the head of §2 and applies to both."""
assert old_hdr in r, "header anchor not found"
r = r.replace(old_hdr, new_hdr)
open(RT, "w", encoding="utf-8", newline="").write(r)

# ---------------- TASK_TRACKER: C5 gate row, R15, C5 item ----------------
t = open(TT, encoding="utf-8").read()
old_gate = '| **C5** Footprints and assembly | "No footprint mismatch, no courtyard overlap, no silk over pads, no via in a pad without a fab note, constraints met." | **Partly** | 0 footprint mismatch (Q9, U7, U8 cleared); **silk 0**; **U4 and SW1 have no courtyard at all** and `missing_courtyard` is suppressed, so overlap cannot be assessed for them; **65 vias in pads** with no fab note agreed |'
new_gate = '| **C5** Footprints and assembly | "No footprint mismatch, no courtyard overlap, no silk over pads, no via in a pad without a fab note, constraints met." | **Partly** | 0 footprint mismatch; **silk 0**; **every footprint now has a courtyard** (U4 and SW1 drawn this run) and `missing_courtyard` is enabled with **0 items and no overlap**; the only remaining gap is **65 vias in SMD pads with no agreed fab note** |'
assert old_gate in t, "C5 gate anchor not found"
t = t.replace(old_gate, new_gate)

old_r15 = '| R15 | P2 | 001 T13 | "Files." | Open | Stale descriptions, F.Fab labels, J24 symbol pin names and `!padne` directives; the `.kicad_dru` now exists and names nets on this board | `pcb\\MoriShield_Carrier.kicad_dru` | T-37 |'
new_r15 = '| R15 | P2 | 001 T13 | "Files." | Partly | The rule file half is done: `MoriShield_Carrier.kicad_dru` exists and names only nets on this board. The text half is not: stale descriptions, F.Fab labels, J24 symbol pin names and the `!padne` directives still describe the old design | `pcb\\MoriShield_Carrier.kicad_dru`; `.kicad_sch` directives | T-37 |'
assert old_r15 in t, "R15 anchor not found"
t = t.replace(old_r15, new_r15)

old_c5item = '| C5 | P1 | 004 T9 | "Firmware reads back channel, address, power and key." | New | M0/M1 are on separate pins but both on the microSD group (see A7/C2) | pad nets | T-23 |'
new_c5item = '| C5 | P1 | 004 T9 | "Firmware reads back channel, address, power and key." | Partly | M0 and M1 are on separate pins as the item requires; both still sit in the GPIO10/11 group that CHK-001 C11 calls the microSD (see A7/C2), so the firmware read-back is not yet a clean claim | pad nets | T-23 |'
assert old_c5item in t, "C5 item anchor not found"
t = t.replace(old_c5item, new_c5item)
open(TT, "w", encoding="utf-8", newline="").write(t)
print("block 0 edits applied")
