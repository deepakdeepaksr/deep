import re

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
RT = ROOT + r"\REPLY_TO_CTO.md"


def replace_row(path, item, new_line):
    lines = open(path, encoding="utf-8").read().split("\n")
    n = 0
    for i, line in enumerate(lines):
        if line.startswith("| %s |" % item):
            lines[i] = new_line
            n += 1
    assert n == 1, "expected exactly one row for %s, found %d" % (item, n)
    open(path, "w", encoding="utf-8", newline="").write("\n".join(lines))
    return n


# ---------------- REPLY ----------------
replace_row(RT, "D3",
    "| D3 | ERC **0 errors, 0 warnings** and **no suppressed checks at all**: all nine re-enabled. "
    "What they hid is fixed, not re-suppressed: courtyards drawn for U4 and SW1 (board and library), "
    "13 track ends centred on their vias. DRC stayed 0 with every check live | "
    "`revC\\erc_RevC.json`, `revC\\drc_RevC.json`; `.kicad_pro` `rule_severities` (no `ignore` entries) | Done |")

replace_row(RT, "C5",
    "| C5 | M0 and M1 are on separate pins as the item requires, but both still sit in the GPIO10/11 "
    "group that CHK-001 C11 calls the microSD | pad nets; `revC\\drc_RevC.json` | "
    "Partly — the separate-pin half is in place; the microSD conflict is question 3 |")

r = open(RT, encoding="utf-8").read()
old_hdr = r[r.index("Status words: **Done**"):r.index("| Item | What changed and where | Evidence | Status |")]
new_hdr = """Status words used here are the response-sheet vocabulary of MS-CAR-CHK-001 §7:
**Done** · **Partly** (what is missing is named) · **Deferred** (only with Serigreen's message
and date, which we do not yet hold) · **Rejected** (reason) · **Agreed before drawing** ·
**Superseded**. One word is added because that vocabulary has no "not started" term:
**Open — answer requested** means nothing has been done and a question is attached.

Our internal register in `TASK_TRACKER.md` uses six words. The mapping is declared here so that
nothing is silently upgraded or downgraded:

| Register word | Meaning in the register | Status written here |
|---|---|---|
| Done | designed in and evidenced | **Done** |
| Paper | design complete, bench or measurement result owed | **Partly** (bench result owed) |
| Partly | some of it is in the files | **Partly** |
| New | regressed or newly understood, nothing in place | **Open — answer requested** |
| Open | not started, or started and reverted | **Open — answer requested** |
| Superseded | the design change removed the item | **Superseded** |

The same table governs §2.

"""
assert old_hdr in r
r = r.replace(old_hdr, new_hdr)
open(RT, "w", encoding="utf-8", newline="").write(r)

# ---------------- TASK_TRACKER ----------------
lines = open(TT, encoding="utf-8").read().split("\n")
for i, line in enumerate(lines):
    if line.startswith("| **C5** Footprints and assembly |"):
        lines[i] = ('| **C5** Footprints and assembly | "No footprint mismatch, no courtyard overlap, no silk '
                    'over pads, no via in a pad without a fab note, constraints met." | **Partly** | '
                    '0 footprint mismatch; **silk 0**; **every footprint now has a courtyard** (U4 and SW1 drawn '
                    'this run) and `missing_courtyard` is enabled with **0 items and no overlap**; the only '
                    'remaining gap is **65 vias in SMD pads with no agreed fab note** |')
open(TT, "w", encoding="utf-8", newline="").write("\n".join(lines))

replace_row(TT, "R15",
    "| R15 | P2 | 001 T13 | \"Files.\" | Partly | The rule-file half is done: `MoriShield_Carrier.kicad_dru` "
    "exists and names only nets on this board. The text half is not: stale descriptions, F.Fab labels, "
    "J24 symbol pin names and the `!padne` directives still describe the old design | "
    "`pcb\\MoriShield_Carrier.kicad_dru`; `.kicad_sch` directives | T-37 |")

replace_row(TT, "C5",
    "| C5 | P1 | 004 T9 | \"Firmware reads back channel, address, power and key.\" | Partly | M0 and M1 are on "
    "separate pins as the item requires; both still sit in the GPIO10/11 group that CHK-001 C11 calls the "
    "microSD (see A7/C2), so the firmware read-back is not yet a clean claim | pad nets | T-23 |")
print("block 0 edits applied")
