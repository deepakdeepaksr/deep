"""Generate revC\\ResponseSheet_RevC.csv from REPLY_TO_CTO.md sections 1 and 2.

Columns: Item, Prio, What changed and where, Evidence, Status.
Priority is looked up from TASK_TRACKER.md Part 1. Nothing is paraphrased: every
cell is copied from the markdown, and the script then re-reads the CSV and
compares it cell by cell with the source tables.
"""
import csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPLY = os.path.join(ROOT, "REPLY_TO_CTO.md")
TASK = os.path.join(ROOT, "TASK_TRACKER.md")
OUT = os.path.join(ROOT, "revC", "ResponseSheet_RevC.csv")


def table_rows(text, start, end):
    s = text.index(start)
    e = text.index(end, s)
    rows = []
    for line in text[s:e].splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            continue
        if cells[0] in ("Item", "") or set(cells[0]) <= set("- "):
            continue
        rows.append(cells)
    return rows


reply = open(REPLY, encoding="utf-8").read()
task = open(TASK, encoding="utf-8").read()

prio = {}
p1 = task[task.index("## Part 1"):task.index("## Part 2")]
for line in p1.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) >= 3 and re.fullmatch(r"[A-H]\d{1,2}|R\d{1,2}", cells[0]):
        prio[cells[0]] = cells[1]

r59 = table_rows(reply, "## 1. Response sheet", "## 2. Response sheet")
r17 = table_rows(reply, "## 2. Response sheet", "## 3. Answers")
rows = r59 + r17
assert len(r59) == 59, "expected 59 rows, got %d" % len(r59)
assert len(r17) == 17, "expected 17 rows, got %d" % len(r17)

out = []
for item, changed, evidence, status in rows:
    out.append({"Item": item, "Prio": prio.get(item, ""),
                "What changed and where": changed, "Evidence": evidence, "Status": status})

with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["Item", "Prio", "What changed and where", "Evidence", "Status"],
                       quoting=csv.QUOTE_ALL)
    w.writeheader()
    w.writerows(out)

# ---- round-trip check ----
back = list(csv.DictReader(open(OUT, encoding="utf-8")))
assert len(back) == 76, "round trip read %d rows" % len(back)
bad = 0
for src, dst in zip(rows, back):
    if (src[0], src[1], src[2], src[3]) != (dst["Item"], dst["What changed and where"],
                                            dst["Evidence"], dst["Status"]):
        bad += 1
        print("MISMATCH:", src[0])
    if not dst["Prio"]:
        bad += 1
        print("NO PRIORITY:", src[0])
print("rows=%d mismatches=%d" % (len(back), bad))
print("first file:", back[0]["Item"], "|", back[0]["Status"])
print("last file :", back[-1]["Item"], "|", back[-1]["Status"])
