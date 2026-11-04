import io, re, csv, collections, os, datetime

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
DOCS = ['PROJECT_CONTEXT_RevC.md', 'TASK_TRACKER.md', 'REPLY_TO_CTO.md', 'STAGE_TRACKER.md']

exp = ([f'A{i}' for i in range(1, 13)] + [f'B{i}' for i in range(1, 13)] +
       [f'C{i}' for i in range(1, 14)] + [f'D{i}' for i in range(1, 4)] +
       [f'E{i}' for i in range(1, 8)] + [f'F{i}' for i in range(1, 3)] +
       [f'G{i}' for i in range(1, 5)] + [f'H{i}' for i in range(1, 7)] +
       [f'R{i}' for i in range(1, 18)])

print('=== document integrity ===')
for d in DOCS:
    t = io.open(P + '\\' + d, encoding='utf-8').read()
    L = t.split('\n')
    ids = [l.split('|')[1].strip() for l in L
           if re.match(r'^\|\s*(?:[A-H]\d{1,2}|R\d{1,2})\s*\|\s*P', l)]
    c = collections.Counter(ids)
    print('%-26s %4d lines  %5d KB  prototype=%d  ready-for-fab=%d'
          % (d, len(L), len(t) // 1024,
             len(re.findall('prototype', t, re.I)),
             len(re.findall('ready for fabrication', t, re.I))))
    if d == 'TASK_TRACKER.md':
        print('     item rows %d, unique %d, missing %s, dupes %s'
              % (len(ids), len(c), [x for x in exp if x not in c],
                 [k for k, v in c.items() if v > 1]))
        f = re.findall(r'^(\d{1,2})\. \*\*', t, re.M)
        print('     Part 6 findings %s..%s  duplicates: %s'
              % (f[0], f[-1], sorted({x for x in f if f.count(x) > 1}) or 'none'))
        print('     tasks T-55..T-58 present:', all(x in t for x in ('T-55', 'T-56', 'T-57', 'T-58')))
    if d == 'REPLY_TO_CTO.md':
        print('     item rows %d, missing %s' % (len(ids), [x for x in exp if x not in c]))
        print('     questions 8b-8f present:', all(('8%s.' % k) in t for k in 'bcdef'))
        print('     §3 A7 signatory row intact:',
              bool(re.search(r'\| A7 \| Aswin is the single contact', t)))

print()
print('=== design files untouched by this document pass ===')
for f in (r'pcb\MoriShield_Carrier.kicad_pcb', r'pcb\MoriShield_Carrier.kicad_sch',
          r'pcb\MoriShield_Carrier.kicad_pro'):
    st = os.stat(P + '\\' + f)
    print('   %-42s %s' % (f, datetime.datetime.fromtimestamp(st.st_mtime).strftime('%m-%d %H:%M:%S')))

print()
print('=== CSV agrees with the reply ===')
rows = list(csv.reader(io.open(P + r'\revC\ResponseSheet_RevC.csv', encoding='utf-8-sig')))
print('   rows %d, header %s' % (len(rows) - 1, rows[0]))
print('   ids unique:', len({r[0] for r in rows[1:]}) == 76)

print()
print('=== files a new machine must carry ===')
need = ['PROJECT_CONTEXT_RevC.md', 'TASK_TRACKER.md', 'REPLY_TO_CTO.md', 'STAGE_TRACKER.md',
        r'pcb\MoriShield_Carrier.kicad_pcb', r'pcb\MoriShield_Carrier.kicad_sch',
        r'pcb\MoriShield_Carrier.kicad_pro', r'pcb\MoriShield_Carrier.kicad_sym',
        r'pcb\MoriShield_Carrier.kicad_dru', r'pcb\fp-lib-table', r'pcb\sym-lib-table',
        r'revC\pack.ps1', r'revC\ResponseSheet_RevC.csv', r'revC\FAB_NOTES.md',
        r'revC\BUCK_AUDIT_XL4015_20261101.md', r'revC\decoupling_map.csv',
        r'revC\erc_RevC.json', r'revC\drc_RevC.json',
        r'morishield\morishield_hardware\libraries\MoriShield_Carrier.kicad_sym',
        r'morishield\morishield_hardware\libraries\MoriShield_Carrier.pretty',
        r'_cto_extract\MoriShield-Carrier-RevB-Review-v1.0.txt',
        r'_cto_extract\MoriShield-Carrier-ReleaseCheck-v1.0.txt',
        r'_cto_extract\MoriShield-Carrier-FabReadiness-v1.0.txt']
miss = [n for n in need if not os.path.exists(P + '\\' + n)]
print('   %d required, missing: %s' % (len(need), miss or 'NONE'))
