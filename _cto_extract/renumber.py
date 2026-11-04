import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\TASK_TRACKER.md'
L = io.open(p, encoding='utf-8').read().split('\n')

i = next(n for n, l in enumerate(L) if l.startswith('## Part 6'))
j = next(n for n, l in enumerate(L) if l.startswith('## Part 7'))

n = 0
changed = []
for k in range(i, j):
    m = re.match(r'^(\d{1,2})\. ', L[k])
    if m:
        n += 1
        if m.group(1) != str(n):
            changed.append((k + 1, m.group(1), n))
            L[k] = re.sub(r'^\d{1,2}\. ', '%d. ' % n, L[k], count=1)
print('renumbered %d findings, total %d' % (len(changed), n))
for c in changed:
    print('   line %-4d %s -> %d' % c)

t = '\n'.join(L)

# the superseded finding must not cite a number that has now moved
t = t.replace('SUPERSEDED - J6 is NOT mis-wired.** Finding 23 of this run read - measured 2026-11-02.**',
              'SUPERSEDED - J6 is NOT mis-wired.** This finding was first written as '
              '"the J6 rewire is a reroute, not a net rename" - measured 2026-11-02.**')
t = t.replace('SUPERSEDED - J6 is NOT mis-wired.** Finding 23 of this run read',
              'SUPERSEDED - J6 is NOT mis-wired.** This finding was first written as '
              '"the J6 rewire is a reroute, not a net rename"')
t = t.replace('Part 6 of this register had two findings numbered 22, 23, 24 and 25.** The\n'
              '    2026-11-02 run appended its own set without checking the existing numbers. Fixed\n'
              '    by renumbering the later set to 26-29. A register that cites "finding 23" is\n'
              '    ambiguous until this is clean.',
              'Part 6 of this register had duplicate finding numbers.** The 2026-11-02 run\n'
              '    appended its own set without checking the existing numbers, so 22 to 27 each\n'
              '    appeared twice. Fixed by renumbering every finding in file order. The lesson is\n'
              '    recorded because a register that cites "finding 23" is ambiguous until it is not.')

io.open(p, 'w', encoding='utf-8', newline='').write(t)

f = re.findall(r'^(\d{1,2})\. \*\*', t, re.M)
print('final finding numbers:', f)
print('duplicates:', sorted({x for x in f if f.count(x) > 1}) or 'none')
print('ascending order:', [int(x) for x in f] == sorted(int(x) for x in f))
