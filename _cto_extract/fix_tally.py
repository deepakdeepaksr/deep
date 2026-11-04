import io, re, subprocess

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# TASK_TRACKER: its own tally line contradicts its own rows
p = P + r'\TASK_TRACKER.md'
t = io.open(p, encoding='utf-8').read()
old = '**Gate tally: 4 met (C1, C2, C5, C12), 2 partly (C9, C10), 7 not met.**'
new = ('**Gate tally, counted from the rows above: 4 met (C1, C2, C5, C12), '
       '1 partly (C9), 8 not met (C3, C4, C6, C7, C8, C10, C11, C13).**')
print('tally line found:', old in t)
t = t.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(t)

# PROJECT_CONTEXT section 9.3
p2 = P + r'\PROJECT_CONTEXT_RevC.md'
t2 = io.open(p2, encoding='utf-8').read()
old2 = '| Gate | **4 met** (C1, C2, C5, C12), 2 partly, 7 not met. **C9 and C10 not met** |'
new2 = ('| Gate | **4 met** (C1, C2, C5, C12), **1 partly** (C9), **8 not met** — counted from '
        'the Part 2 rows. **C9 and C10 are the two S3 checks still open** |')
print('9.3 gate row found:', old2 in t2)
t2 = t2.replace(old2, new2)

t2 += """
### 9.7 Gate tally correction, and one more standing rule

`TASK_TRACKER.md` Part 2's own summary line said "2 partly (C9, C10), 7 not met" while its
rows say **C9 Partly and C10 Not met** - 4 met, 1 partly, 8 not met. Corrected in place.
The same wrong tally had propagated into `PROJECT_CONTEXT_RevC.md` and the 2026-11-03
session report.

**Standing rule added: a summary count must be derived from the rows, never typed.**
`python _cto_extract\\gate_truth.py` now recomputes it from Part 2 and prints the three
numbers; run it with every wrap-up and copy its output into the tally line.
"""
io.open(p2, 'w', encoding='utf-8', newline='').write(t2)
print('PROJECT_CONTEXT updated')

# verify all three now agree
for f in ('TASK_TRACKER.md', 'STAGE_TRACKER.md', 'PROJECT_CONTEXT_RevC.md'):
    tt = io.open(P + '\\' + f, encoding='utf-8').read()
    hits = [l.strip()[:130] for l in tt.splitlines() if re.search(r'(4 met|4 of 13 met)', l)]
    print('--', f)
    for h in hits[:3]:
        print('    ', h.encode('ascii', 'replace').decode())

r = subprocess.run(['python', P + r'\_cto_extract\trace2.py'], capture_output=True, text=True, cwd=P)
print()
print(r.stdout[:200])
