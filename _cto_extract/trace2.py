import io, re, csv, collections, os

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'


def cells(l):
    return [x.strip() for x in l.strip().strip('|').split('|')]


MAP = {'New': 'Open', 'Paper': 'Partly'}


def base(s):
    s = (s or '').strip()
    for k in ('Done', 'Partly', 'Open', 'New', 'Paper', 'Superseded', 'Deferred', 'Rejected'):
        if s.startswith(k):
            return MAP.get(k, k)
    return s[:26] or 'EMPTY'


tt = io.open(P + r'\TASK_TRACKER.md', encoding='utf-8').read().splitlines()
a = next(n for n, l in enumerate(tt) if l.startswith('## Part 1'))
b = next(n for n, l in enumerate(tt) if l.startswith('## Part 2'))
reg = {}
for l in tt[a:b]:
    m = re.match(r'^\s*\|\s*([A-H][0-9]{1,2}|R[0-9]{1,2})\s*\|', l)
    if m:
        c = cells(l)
        if len(c) >= 5:
            reg[m.group(1)] = (c[1], c[4])
rp = io.open(P + r'\REPLY_TO_CTO.md', encoding='utf-8').read().splitlines()
i1 = next(n for n, l in enumerate(rp) if l.startswith('## 1.'))
i2 = next(n for n, l in enumerate(rp) if l.startswith('## 3.'))
reply = {}
for l in rp[i1:i2]:
    m = re.match(r'^\s*\|\s*([A-H][0-9]{1,2}|R[0-9]{1,2})\s*\|', l)
    if m:
        c = cells(l)
        if len(c) >= 3:
            reply[m.group(1)] = c[-1]
cs = {r[0]: (r[1], r[4]) for r in list(csv.reader(io.open(P + r'\revC\ResponseSheet_RevC.csv',
                                                           encoding='utf-8-sig')))[1:]}

print('register %d   reply %d   csv %d' % (len(reg), len(reply), len(cs)))
print('ids only in one place:', sorted(set(reg) ^ set(reply)), sorted(set(reg) ^ set(cs)))
bad = []
for k in sorted(reg):
    v = {base(reg[k][1]), base(reply.get(k, '')), base(cs.get(k, ('', ''))[1])}
    if len(v) > 1:
        bad.append((k, base(reg[k][1]), base(reply.get(k, '')), base(cs.get(k, ('', ''))[1])))
print('status disagreements after mapping: %d' % len(bad))
for x in bad:
    print('   %-4s tracker=%-10s reply=%-10s csv=%-10s' % x)
prio = [(k, reg[k][0], cs[k][0]) for k in reg if k in cs and reg[k][0] != cs[k][0]]
print('priority mismatches tracker vs csv:', prio or 'none')
print('register tally:', dict(collections.Counter(base(v[1]) for v in reg.values())))
print('raw vocabulary kept in register:',
      dict(collections.Counter(re.match(r'^\w+', base('')) and '' or
                               (v[1].split('—')[0].strip().split()[0] if v[1] else '')
                               for v in reg.values())))

print()
print('=== gate tally + Part 4 conditions as they now read ===')
for l in tt:
    if l.strip().startswith('**Gate tally') or l.strip().startswith('**Table 11'):
        print('  ', l.strip()[:200])
i = next(n for n, l in enumerate(tt) if l.startswith('## Part 4'))
j = next(n for n, l in enumerate(tt) if l.startswith('## Part 5'))
for l in tt[i + 4:i + 14]:
    print('  ', l[:190])
