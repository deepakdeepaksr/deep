import io, re, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

t = io.open(P + r'\TASK_TRACKER.md', encoding='utf-8').read()
L = t.splitlines()
i = next(n for n, l in enumerate(L) if l.startswith('## Part 2'))
j = next(n for n, l in enumerate(L) if l.startswith('## Part 3'))
states = {}
for l in L[i:j]:
    m = re.match(r'^\|\s*\*\*(C\d+)\*\*\s*\|(.*)\|\s*\*\*(Met|Not met|Partly)\*\*\s*\|', l)
    if m:
        states[m.group(1)] = m.group(3)
print('=== TASK_TRACKER Part 2, counted from the rows ===')
print('   rows found:', len(states))
print('   ', dict(collections.Counter(states.values())))
for k in sorted(states, key=lambda x: int(x[1:])):
    print('   %-5s %s' % (k, states[k]))
print()
print('   tally line in the file:',
      [l.strip()[:120] for l in L[i:j] if l.strip().startswith('**Gate tally')])
print()
for f in ('STAGE_TRACKER.md', 'PROJECT_CONTEXT_RevC.md'):
    tt = io.open(P + '\\' + f, encoding='utf-8').read()
    hits = [l.strip()[:150] for l in tt.splitlines() if 'of 13 met' in l or 'met (' in l and 'gate' in l.lower()]
    print('=== %s ===' % f)
    for h in hits[:3]:
        print('   ', h.encode('ascii', 'replace').decode())
