import io, re, csv, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# TASK_TRACKER Part 1 statuses (the authoritative register)
tt = io.open(P + r'\TASK_TRACKER.md', encoding='utf-8').read().splitlines()
a = next(n for n, l in enumerate(tt) if l.startswith('## Part 1'))
b = next(n for n, l in enumerate(tt) if l.startswith('## Part 2'))
reg = {}
for l in tt[a:b]:
    m = re.match(r'^\|\s*([A-H]\d{1,2}|R\d{1,2})\s*\|', l)
    if m:
        c = [x.strip() for x in l.split('|')][1:]
        if len(c) >= 5:
            reg[m.group(1)] = (c[1], c[4])      # prio, status

# REPLY_TO_CTO §1/§2 statuses
rp = io.open(P + r'\REPLY_TO_CTO.md', encoding='utf-8').read().splitlines()
i1 = next(n for n, l in enumerate(rp) if l.startswith('## 1.'))
i2 = next(n for n, l in enumerate(rp) if l.startswith('## 3.'))
reply = {}
for l in rp[i1:i2]:
    m = re.match(r'^\|\s*([A-H]\d{1,2}|R\d{1,2})\s*\|', l)
    if m:
        c = [x.strip() for x in l.split('|')][1:]
        if len(c) >= 3:
            reply[m.group(1)] = c[-1]

# CSV
rows = list(csv.reader(io.open(P + r'\revC\ResponseSheet_RevC.csv', encoding='utf-8-sig')))
cs = {r[0]: (r[1], r[4]) for r in rows[1:]}


def base(s):
    s = (s or '').strip()
    for k in ('Done', 'Partly', 'Open', 'New', 'Paper', 'Superseded', 'Deferred', 'Rejected'):
        if s.startswith(k):
            return k
    return s[:24]


print('register rows: %d   reply rows: %d   csv rows: %d' % (len(reg), len(reply), len(cs)))
print()
print('=== ids missing from reply or csv ===')
print('  reply missing:', sorted(set(reg) - set(reply)))
print('  csv   missing:', sorted(set(reg) - set(cs)))
print('  extra in reply:', sorted(set(reply) - set(reg)))
print()
print('=== status disagreement: TASK_TRACKER vs REPLY_TO_CTO vs CSV ===')
n = 0
for k in sorted(reg):
    r1 = base(reg[k][1])
    r2 = base(reply.get(k, ''))
    r3 = base(cs.get(k, ('', ''))[1])
    if len({r1, r2, r3}) > 1:
        n += 1
        print('  %-4s  tracker=%-11s reply=%-11s csv=%-11s' % (k, r1, r2, r3))
print('  total disagreements:', n)
print()
print('=== priority consistency tracker vs csv ===')
bad = [(k, reg[k][0], cs[k][0]) for k in reg if k in cs and reg[k][0] != cs[k][0]]
print('  mismatches:', bad or 'none')
print()
print('=== register status tally ===')
print('  ', dict(collections.Counter(base(v[1]) for v in reg.values())))
