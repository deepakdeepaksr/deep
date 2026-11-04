import io, re, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'


def count(path):
    L = io.open(path, encoding='utf-8').read().splitlines()
    i = next(n for n, l in enumerate(L) if l.startswith('## Part 2'))
    j = next(n for n, l in enumerate(L) if l.startswith('## Part 3'))
    rows = {}
    for l in L[i:j]:
        s = l.strip()
        if not (s.startswith('|') and '**C' in s[:12]):
            continue
        c = [x.strip() for x in s.strip('|').split('|')]
        m = re.match(r'^\*\*(C\d+)\*\*', c[0])
        if not m:
            continue
        st = [x for x in c if x.strip('* ').lower() in ('met', 'not met', 'partly')]
        rows[m.group(1)] = st[0].strip('* ') if st else None
    return rows


rows = count(P + r'\TASK_TRACKER.md')
cnt = collections.Counter(rows.values())
met = sorted([k for k, v in rows.items() if v == 'Met'], key=lambda x: int(x[1:]))
par = sorted([k for k, v in rows.items() if v == 'Partly'], key=lambda x: int(x[1:]))
notmet = sorted([k for k, v in rows.items() if v == 'Not met'], key=lambda x: int(x[1:]))
print('rows counted: %d (expect 13)' % len(rows))
print('MET     %d  %s' % (len(met), ', '.join(met)))
print('PARTLY  %d  %s' % (len(par), ', '.join(par)))
print('NOT MET %d  %s' % (len(notmet), ', '.join(notmet)))
print()
print('Tally line to paste:')
print('  **Gate tally, counted from the rows above: %d met (%s), %d partly (%s), '
      '%d not met (%s).**' % (len(met), ', '.join(met), len(par), ', '.join(par) or '-',
                              len(notmet), ', '.join(notmet)))
missing = [k for k in rows if rows[k] is None]
print('rows with no recognised status:', missing or 'none')
