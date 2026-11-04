import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\TASK_TRACKER.md'
L = io.open(p, encoding='utf-8').read().split('\n')

i = next(n for n, l in enumerate(L) if l.startswith('    21. **'))
n = i
while n < len(L) and (L[n].startswith('    ') or L[n].strip() == ''):
    if L[n].strip() == '' and n > i:
        break
    L[n] = L[n][4:] if L[n].startswith('    ') else L[n]
    n += 1
io.open(p, 'w', encoding='utf-8', newline='').write('\n'.join(L))
print('de-indented lines %d..%d' % (i + 1, n))

t = io.open(p, encoding='utf-8').read()
print('Part 6 finding numbers:', re.findall(r'^(\d{1,2})\. \*\*', t, re.M))
print('indented finding starts left:', len(re.findall(r'^\s+\d{1,2}\. \*\*', t, re.M)))
