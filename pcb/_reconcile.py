"""Compare TASK_TRACKER statuses with REPLY_TO_CTO statuses under the declared mapping."""
import re, csv, collections

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
RT = ROOT + r"\REPLY_TO_CTO.md"

# declared mapping: internal word -> the CTO's response-sheet vocabulary
MAP = {"Done": "Done", "Paper": "Partly", "Partly": "Partly",
       "New": "Open", "Open": "Open", "Superseded": "Superseded"}

def rows(path, start, end, n):
    t = open(path, encoding="utf-8").read()
    s = t.index(start); e = t.index(end, s)
    out = {}
    for line in t[s:e].splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= n and re.fullmatch(r"[A-H]\d{1,2}|R\d{1,2}", cells[0]):
            out[cells[0]] = cells
    return out

reg = rows(TT, "## Part 1", "## Part 2", 7)
r59 = rows(RT, "## 1. Response sheet", "## 2. Response sheet", 4)
r17 = rows(RT, "## 2. Response sheet", "## 3. Answers", 4)
reply = {**r59, **r17}

bad = []
for item in sorted(reg, key=lambda x: (x[0], int(x[1:]))):
    internal = reg[item][4]
    want = MAP.get(internal, "?")
    got = reply.get(item, ["", "", "", "MISSING"])[3].split(" ")[0].split("—")[0].strip()
    if want != got:
        bad.append((item, internal, want, reply.get(item, ["", "", "", "MISSING"])[3][:60]))

raw = [(i, reg[i][4], reply[i][3].split(" ")[0]) for i in reg
       if reply.get(i) and reg[i][4] != reply[i][3].split(" ")[0]]
print("raw word-for-word mismatches (no mapping):", len(raw))
print("items:", len(reg), "reply rows:", len(reply))
print("disagreements:", len(bad))
for b in bad:
    print("  %-4s register=%-10s mapped=%-10s reply=%s" % b)
