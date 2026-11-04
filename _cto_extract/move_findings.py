import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\TASK_TRACKER.md'
t = io.open(p, encoding='utf-8').read()

marker = '**2026-11-03 late additions to Part 6.**'
k = t.find(marker)
assert k > 0, 'appended block not found'
tail = t[k:]
t = t[:k].rstrip() + '\n'
print('removed stray tail of %d chars' % len(tail))

# the two findings, re-stripped of their wrong numbers
blocks = re.split(r'\n(?=3[78]\. )', tail.replace(marker, '').strip())
blocks = [b for b in blocks if re.match(r'^3[78]\. ', b)]
print('findings recovered:', len(blocks))
fixed = []
for b in blocks:
    b = re.sub(r'^3[78]\. ', '', b)
    fixed.append(b.strip())

L = t.splitlines()
j = next(n for n, l in enumerate(L) if l.startswith('## Part 7'))
# number them 41 and 42, keeping their own bold headings
newlines = ['']
for off, body in enumerate(fixed):
    newlines.append('%d. %s' % (41 + off, body))
L[j:j] = newlines
t = '\n'.join(L) + '\n'

# renumber the whole of Part 6 in file order so nothing can collide again
L = t.splitlines()
i = next(n for n, l in enumerate(L) if l.startswith('## Part 6'))
j = next(n for n, l in enumerate(L) if l.startswith('## Part 7'))
n = 0
for k2 in range(i, j):
    m = re.match(r'^(\d{1,2})\. ', L[k2])
    if m:
        n += 1
        L[k2] = re.sub(r'^\d{1,2}\. ', '%d. ' % n, L[k2], count=1)
t = '\n'.join(L)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('Part 6 findings now 1..%d' % n)

f = re.findall(r'^(\d{1,2})\. \*\*', t, re.M)
print('duplicates:', sorted({x for x in f if f.count(x) > 1}) or 'none')
print('ascending:', [int(x) for x in f] == sorted(int(x) for x in f))
print('ends with Part 7 intact:', '## Part 7' in t)
