import io, os, re, json, shutil, subprocess, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
SRC = os.path.join(P, 'pcb')
DST = os.path.join(P, '_cto_extract', 'drcprobe')
CLI = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

shutil.rmtree(DST, ignore_errors=True)
os.makedirs(DST)
for f in ('MoriShield_Carrier.kicad_pcb', 'MoriShield_Carrier.kicad_sch',
          'MoriShield_Carrier.kicad_pro', 'MoriShield_Carrier.kicad_sym',
          'MoriShield_Carrier.kicad_dru', 'fp-lib-table', 'sym-lib-table'):
    s = os.path.join(SRC, f)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(DST, f))

# point the lib tables at the real library dir using an absolute path
for f in ('fp-lib-table', 'sym-lib-table'):
    p = os.path.join(DST, f)
    t = io.open(p, encoding='utf-8').read()
    t = t.replace('${KIPRJMOD}', SRC.replace('\\', '/'))
    io.open(p, 'w', encoding='utf-8', newline='').write(t)

# re-enable every suppressed DRC check and every suppressed ERC check
pro = os.path.join(DST, 'MoriShield_Carrier.kicad_pro')
d = json.load(open(pro, encoding='utf-8'))
rs = d['board']['design_settings']['rule_severities']
IGN = [k for k, v in rs.items() if v == 'ignore']
for k in IGN:
    rs[k] = 'warning'
# ERC severities live in schema
es = d.get('schematic', {}).get('lib_symbols', None)
sch_sev = d.setdefault('schematic', {}).setdefault('breakdown', {})
drc_list = d['board']['design_settings']['rule_severities']
io.open(pro, 'w', encoding='utf-8').write(json.dumps(d, indent=2))
print('re-enabled DRC checks:', IGN)

r = subprocess.run([CLI, 'pcb', 'drc', '--refill-zones', '--schematic-parity', '--severity-all',
                    '--all-track-errors', '--format', 'json',
                    '-o', os.path.join(DST, 'drc_undenied.json'),
                    os.path.join(DST, 'MoriShield_Carrier.kicad_pcb')],
                   capture_output=True, text=True, timeout=1200)
out = os.path.join(DST, 'drc_undenied.json')
if not os.path.exists(out):
    print('DRC failed:', (r.stderr or r.stdout)[-400:])
else:
    dd = json.load(open(out, encoding='utf-8'))
    print('DRC with suppressions removed: %d items (the shipped file reports 0)' % len(dd['violations']))
    print('  ignored_checks now:', [i['key'] for i in dd.get('ignored_checks', [])])
    c = collections.Counter(v['type'] for v in dd['violations'])
    for k, n in c.most_common():
        print('   %-34s %4d' % (k, n))
    ex = collections.defaultdict(list)
    for v in dd['violations']:
        its = v.get('items') or []
        desc = ' | '.join((i.get('description') or '')[:70] for i in its[:1])
        if len(ex[v['type']]) < 4:
            ex[v['type']].append(desc)
    print()
    for k in c:
        print('==', k)
        for s in ex[k]:
            print('    ', s)
