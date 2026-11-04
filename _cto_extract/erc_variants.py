import io, os, json, shutil, subprocess, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
SRC = os.path.join(P, 'pcb')
CLI = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

VARIANTS = {
    'V2_verbatim_tables': False,   # copy, tables left as ${KIPRJMOD}
    'V3_no_fp_table': 'nofp',
    'V4_no_sym_table': 'nosym',
    'V5_with_pcb_present': 'pcb',
}

for name, mode in VARIANTS.items():
    DST = os.path.join(P, '_cto_extract', name)
    shutil.rmtree(DST, ignore_errors=True)
    os.makedirs(DST)
    files = ['MoriShield_Carrier.kicad_sch', 'MoriShield_Carrier.kicad_pro',
             'MoriShield_Carrier.kicad_sym', 'sym-lib-table', 'fp-lib-table']
    if mode == 'pcb':
        files += ['MoriShield_Carrier.kicad_pcb', 'MoriShield_Carrier.kicad_prl',
                  'MoriShield_Carrier.kicad_dru']
    for f in files:
        s = os.path.join(SRC, f)
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(DST, f))
    if mode in ('nofp', 'nosym'):
        drop = 'fp-lib-table' if mode == 'nofp' else 'sym-lib-table'
        os.remove(os.path.join(DST, drop))
    if mode is False:
        pass  # verbatim ${KIPRJMOD}
    else:
        for f in ('sym-lib-table', 'fp-lib-table'):
            p = os.path.join(DST, f)
            if os.path.exists(p):
                io.open(p, 'w', encoding='utf-8', newline='').write(
                    io.open(p, encoding='utf-8').read().replace('${KIPRJMOD}', SRC.replace('\\', '/')))

    out = os.path.join(DST, 'erc.json')
    subprocess.run([CLI, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', out,
                    os.path.join(DST, 'MoriShield_Carrier.kicad_sch')],
                   capture_output=True, text=True, timeout=900)
    if not os.path.exists(out):
        print('%-22s  ERC did not produce a report' % name)
        continue
    e = json.load(open(out, encoding='utf-8'))
    ev = [v for s in e.get('sheets', []) for v in s.get('violations', [])]
    print('%-22s  items %4d   %s' % (name, len(ev), dict(collections.Counter(v['type'] for v in ev))))
