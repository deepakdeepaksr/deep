import io, re, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\TASK_TRACKER.md'
t = io.open(p, encoding='utf-8').read()
L = t.split('\n')

# findings 18-21 were pushed to a 4-space indent, which makes them read as a
# continuation of finding 17 instead of numbered items. De-indent only those.
start = None
for i, l in enumerate(L):
    if l.startswith('    18. '):
        start = i
        break
end = None
if start is not None:
    for i in range(start, len(L)):
        if L[i].startswith('    21. '):
            end = i
        if end is not None and L[i].strip() == '' and i > end:
            break
        if end is not None and L[i].startswith('---'):
            end = i
            break
print('block found:', start, 'to', end)

if start is not None:
    for i in range(start, (end or len(L))):
        if L[i].startswith('    '):
            L[i] = L[i][4:]
        elif L[i].strip() == '':
            L[i] = ''
    io.open(p, 'w', encoding='utf-8', newline='').write('\n'.join(L))
    print('de-indented %d lines' % ((end or len(L)) - start))

# re-verify the document
t = io.open(p, encoding='utf-8').read()
L = t.splitlines()
ids = [l.split('|')[1].strip() for l in L if re.match(r'^\|\s*(?:[A-H]\d{1,2}|R\d{1,2})\s*\|', l)]
exp = ([f'A{i}' for i in range(1, 13)] + [f'B{i}' for i in range(1, 13)] +
       [f'C{i}' for i in range(1, 14)] + [f'D{i}' for i in range(1, 4)] +
       [f'E{i}' for i in range(1, 8)] + [f'F{i}' for i in range(1, 3)] +
       [f'G{i}' for i in range(1, 5)] + [f'H{i}' for i in range(1, 7)] +
       [f'R{i}' for i in range(1, 18)])
c = collections.Counter(ids)
print('76 ids present:', all(x in c for x in exp), ' unique:', len(c))
print('word prototype:', len(re.findall(r'prototype', t, re.I)))
print('numbered findings in Part 6:', re.findall(r'^(\d{1,2})\. \*\*', t, re.M))
print('stale phrases left:', t.count('124 silk items remain'), t.count('about 110 mΩ'), t.count('0 errors, 1 warning'))
