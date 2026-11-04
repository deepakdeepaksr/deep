import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\TASK_TRACKER.md'
L = io.open(p, encoding='utf-8').read().split('\n')
i = next(n for n, l in enumerate(L) if l.startswith('## Part 6'))
j = next(n for n, l in enumerate(L) if l.startswith('## Part 7'))
print('=== Part 6 findings 30 onward, in file order ===')
for n in range(i, j):
    m = re.match(r'^(\d{1,2})\. \*\*(.{0,80})', L[n])
    if m and int(m.group(1)) >= 30:
        print('%4d | %-3s %s' % (n + 1, m.group(1), m.group(2)))
