import re, sys, collections

PATH = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\TASK_TRACKER.md"
text = open(PATH, encoding="utf-8").read()

# Part 1 runs from its heading to the next "## Part 2"
start = text.index("## Part 1")
end = text.index("## Part 2")
part1 = text[start:end]

rows = []
for line in part1.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 7:
        continue
    if cells[0] in ("Item",) or set(cells[0]) <= set("- "):
        continue
    if re.fullmatch(r"[A-H]\d{1,2}|R\d{1,2}", cells[0]):
        rows.append(cells)

ids = [r[0] for r in rows]
expected = ([f"A{i}" for i in range(1, 13)] + [f"B{i}" for i in range(1, 13)] +
            [f"C{i}" for i in range(1, 14)] + [f"D{i}" for i in range(1, 4)] +
            [f"E{i}" for i in range(1, 8)] + [f"F{i}" for i in range(1, 3)] +
            [f"G{i}" for i in range(1, 5)] + [f"H{i}" for i in range(1, 7)] +
            [f"R{i}" for i in range(1, 18)])

dupes = [i for i, c in collections.Counter(ids).items() if c > 1]
missing = [i for i in expected if i not in ids]
extra = [i for i in ids if i not in expected]
status = collections.Counter(r[4] for r in rows)

print("Part 1 rows: %d" % len(rows))
groups = collections.Counter(re.match(r"[A-HR]", i).group(0) for i in ids)
print("A: %d  B: %d  C: %d  D: %d  E: %d  F: %d  G: %d  H: %d  R: %d" % (
    groups["A"], groups["B"], groups["C"], groups["D"], groups["E"],
    groups["F"], groups["G"], groups["H"], groups["R"]))
print("duplicates: %s" % (", ".join(dupes) if dupes else "none"))
print("missing: %s" % (", ".join(missing) if missing else "none"))
print("extra: %s" % (", ".join(extra) if extra else "none"))
print("status tally: %s" % dict(status))
print("expected total: %d" % len(expected))
