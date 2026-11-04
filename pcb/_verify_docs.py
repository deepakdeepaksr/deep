import re, collections, sys

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
TT = ROOT + r"\TASK_TRACKER.md"
RT = ROOT + r"\REPLY_TO_CTO.md"
IR = ROOT + r"\_archive\INPUT_REGISTER_RevC.md"

def ids_in_section(text, start_marker, end_marker, pattern):
    s = text.index(start_marker)
    e = text.index(end_marker, s)
    sec = text[s:e]
    out = []
    for line in sec.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and re.fullmatch(pattern, cells[0]):
                out.append(cells[0])
    return out

tt = open(TT, encoding="utf-8").read()
rt = open(RT, encoding="utf-8").read()
ir = open(IR, encoding="utf-8").read()

expected = ([f"A{i}" for i in range(1, 13)] + [f"B{i}" for i in range(1, 13)] +
            [f"C{i}" for i in range(1, 14)] + [f"D{i}" for i in range(1, 4)] +
            [f"E{i}" for i in range(1, 8)] + [f"F{i}" for i in range(1, 3)] +
            [f"G{i}" for i in range(1, 5)] + [f"H{i}" for i in range(1, 7)] +
            [f"R{i}" for i in range(1, 18)])

tt_ids = ids_in_section(tt, "## Part 1", "## Part 2", r"[A-H]\d{1,2}|R\d{1,2}")
print("TASK_TRACKER Part 1 rows: %d" % len(tt_ids))
print("  duplicates:", [k for k, v in collections.Counter(tt_ids).items() if v > 1] or "none")
print("  missing:", [i for i in expected if i not in tt_ids] or "none")
print("  extra:", [i for i in tt_ids if i not in expected] or "none")

rt59 = ids_in_section(rt, "## 1. Response sheet", "## 2. Response sheet", r"[A-H]\d{1,2}")
rt17 = ids_in_section(rt, "## 2. Response sheet", "## 3. Answers", r"R\d{1,2}")
print("REPLY_TO_CTO 59 rows: %d" % len(rt59))
print("  missing:", [i for i in expected[:59] if i not in rt59] or "none")
print("  extra:", [i for i in rt59 if i not in expected[:59]] or "none")
print("REPLY_TO_CTO 17 rows: %d" % len(rt17))
print("  missing:", [i for i in expected[59:] if i not in rt17] or "none")
print("  extra:", [i for i in rt17 if i not in expected[59:]] or "none")

# every question id that appears in the input register (sections A-L only: O.1 lists connectors)
ir_q = ir[:ir.index("## M.")]
qids = []
for line in ir_q.splitlines():
    if line.startswith("|"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"[A-J]\d{1,2}", cells[0]):
            qids.append(cells[0])
qids = list(dict.fromkeys(qids))
print("input-register question ids found: %d" % len(qids))

# coverage in the reply: section 3 answers table + section 4 questions list
s3 = rt[rt.index("## 3. Answers"):rt.index("## 4. Questions")]
s4 = rt[rt.index("## 4. Questions"):rt.index("## 5. Changes")]
covered = set()
for sec in (s3, s4):
    for line in sec.splitlines():
        m = re.match(r"\|\s*([A-J]\d{1,2})\s*\|", line)
        if m:
            covered.add(m.group(1))
        m2 = re.match(r"\d+\.\s*([A-J]\d{1,2})\b", line.strip())
        if m2:
            covered.add(m2.group(1))
missing = [q for q in qids if q not in covered]
print("question ids not mentioned in REPLY_TO_CTO: %s" % (", ".join(missing) if missing else "none"))

# forbidden words
for name, txt in (("TASK_TRACKER", tt), ("REPLY_TO_CTO", rt), ("STAGE_TRACKER", open(ROOT + r"\STAGE_TRACKER.md", encoding="utf-8").read())):
    bad = []
    for w in ("prototype", "ready for fabrication", "fabrication-ready", "manufacturing-ready", "release candidate"):
        if w in txt.lower():
            bad.append(w)
    print("%s forbidden phrases: %s" % (name, bad or "none"))
