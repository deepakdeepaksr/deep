import io, os, json, shutil, subprocess, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
SRC = os.path.join(P, 'pcb')
CLI = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

# CONTROL: identical copy, project file untouched (no severity edits)
DST = os.path.join(P, '_cto_extract', 'erc_control')
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

out = os.path.join(DST, 'erc_control.json')
subprocess.run([CLI, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', out,
                os.path.join(DST, 'MoriShield_Carrier.kicad_sch')],
               capture_output=True, text=True, timeout=900)
e = json.load(open(out, encoding='utf-8'))
ev = [v for s in e.get('sheets', []) for v in s.get('violations', [])]
print('CONTROL copy, severities untouched : %d ERC items   ignored=%s'
      % (len(ev), [i['key'] for i in e.get('ignored_checks', [])]))
print('  ', dict(collections.Counter(v['type'] for v in ev)))

# and the original in place, for the record
out2 = os.path.join(P, '_cto_extract', 'erc_orig_again.json')
subprocess.run([CLI, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', out2,
                os.path.join(SRC, 'MoriShield_Carrier.kicad_sch')],
               capture_output=True, text=True, timeout=900)
e2 = json.load(open(out2, encoding='utf-8'))
ev2 = [v for s in e2.get('sheets', []) for v in s.get('violations', [])]
print('ORIGINAL in place                  : %d ERC items   ignored=%s'
      % (len(ev2), [i['key'] for i in e2.get('ignored_checks', [])]))
print('  ', dict(collections.Counter(v['type'] for v in ev2)))
