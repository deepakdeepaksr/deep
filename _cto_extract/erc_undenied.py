import io, os, json, shutil, subprocess, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
SRC = os.path.join(P, 'pcb')
DST = os.path.join(P, '_cto_extract', 'ercprobe_dir')
CLI = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

shutil.rmtree(DST, ignore_errors=True)
os.makedirs(DST)
for f in ('MoriShield_Carrier.kicad_sch', 'MoriShield_Carrier.kicad_pro',
          'MoriShield_Carrier.kicad_sym', 'sym-lib-table', 'fp-lib-table'):
    s = os.path.join(SRC, f)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(DST, f))
for f in ('sym-lib-table', 'fp-lib-table'):
    p = os.path.join(DST, f)
    if os.path.exists(p):
        io.open(p, 'w', encoding='utf-8', newline='').write(
            io.open(p, encoding='utf-8').read().replace('${KIPRJMOD}', SRC.replace('\\', '/')))

pro = os.path.join(DST, 'MoriShield_Carrier.kicad_pro')
d = json.load(open(pro, encoding='utf-8'))
KEYS = ['single_global_label', 'four_way_junction', 'simulation_model_issue', 'footprint_filter']
d.setdefault('erc', {}).setdefault('rule_severities', {})
for k in KEYS:
    d['erc']['rule_severities'][k] = 'warning'
io.open(pro, 'w', encoding='utf-8').write(json.dumps(d, indent=2))
print('forced ERC severities to warning:', KEYS)

out = os.path.join(DST, 'erc_undenied.json')
r = subprocess.run([CLI, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', out,
                    os.path.join(DST, 'MoriShield_Carrier.kicad_sch')],
                   capture_output=True, text=True, timeout=900)
if not os.path.exists(out):
    print('ERC run failed:', (r.stderr or r.stdout)[-400:])
else:
    e = json.load(open(out, encoding='utf-8'))
    ev = [v for s in e.get('sheets', []) for v in s.get('violations', [])]
    print('ERC with the four checks re-enabled: %d items (shipped file reports 0)' % len(ev))
    print('  ignored now:', [i['key'] for i in e.get('ignored_checks', [])])
    c = collections.Counter((v['severity'], v['type']) for v in ev)
    for k, n in c.most_common():
        print('   %-14s %-26s %4d' % (k[0], k[1], n))
    seen = collections.defaultdict(list)
    for v in ev:
        its = v.get('items') or []
        seen[v['type']].append(' | '.join((i.get('description') or '')[:78] for i in its[:2]))
    for t, lst in seen.items():
        print('==', t, len(lst))
        for s in lst[:8]:
            print('    ', s)
