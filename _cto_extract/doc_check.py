import io, re, os, collections, datetime

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# ---------- stale check: derived files vs design files ----------
pcb_t = os.stat(P + r'\pcb\MoriShield_Carrier.kicad_pcb').st_mtime
sch_t = os.stat(P + r'\pcb\MoriShield_Carrier.kicad_sch').st_mtime
print('=== derived files older than the design they claim to describe ===')
for rel in (r'revC\MoriShield_Carrier_RevC_bom.csv', r'revC\MoriShield_Carrier_RevC_pos_front.csv',
             r'revC\MoriShield_Carrier_RevC_pos_back.csv', r'revC\FAB_NOTES.md',
             r'revC\decoupling_map.csv', r'revC\vias_in_pads.txt', r'revC\EVIDENCE_RevC.md',
             r'revC\render_top.png', r'revC\MoriShield_Carrier_RevC_schematic.pdf',
             r'revC\preview_do_not_ship\MoriShield_Carrier-F_Cu.gtl'):
    p = os.path.join(P, rel)
    if not os.path.exists(p):
        print('   %-56s ABSENT' % rel)
        continue
    m = os.stat(p).st_mtime
    d = (max(pcb_t, sch_t) - m) / 60.0
    print('   %-56s %s   %s' % (rel, datetime.datetime.fromtimestamp(m).strftime('%m-%d %H:%M'),
                                ('STALE by %.0f min' % d) if d > 0 else 'fresh'))

# ---------- document integrity ----------
print()
docs = ['STAGE_TRACKER.md', 'TASK_TRACKER.md', 'REPLY_TO_CTO.md']
exp = ([f'A{i}' for i in range(1, 13)] + [f'B{i}' for i in range(1, 13)] +
       [f'C{i}' for i in range(1, 14)] + [f'D{i}' for i in range(1, 4)] +
       [f'E{i}' for i in range(1, 8)] + [f'F{i}' for i in range(1, 3)] +
       [f'G{i}' for i in range(1, 5)] + [f'H{i}' for i in range(1, 7)] +
       [f'R{i}' for i in range(1, 18)])
for d in docs:
    p = os.path.join(P, d)
    if not os.path.exists(p):
        print('%s  ABSENT' % d)
        continue
    t = io.open(p, encoding='utf-8').read()
    L = t.splitlines()
    ids = [l.split('|')[1].strip() for l in L if re.match(r'^\|\s*(?:[A-H]\d{1,2}|R\d{1,2})\s*\|', l)]
    c = collections.Counter(ids)
    dup = sorted([k for k, v in c.items() if v > 1])
    missing = [x for x in exp if x not in c]
    print('=== %s ===  %d lines, %d KB' % (d, len(L), len(t) // 1024))
    print('   item rows: %d  unique: %d  duplicates: %s  missing of 76: %s' % (len(ids), len(c), dup, missing))
    print('   word "prototype":', len(re.findall(r'prototype', t, re.I)),
          '  "ready for fabrication":', len(re.findall(r'ready for fabrication', t, re.I)))
    st = collections.Counter()
    for l in L:
        m = re.search(r'\|\s*(Done|Paper|Partly|Open|New|Superseded|Deferred|Rejected|Agreed before drawing|Blocked|Met|Not met)\b', l)
        if m:
            st[m.group(1)] += 1
    print('   status words:', dict(st))
    print('   headings:', [l.strip() for l in L if l.startswith('## ')][:14])
