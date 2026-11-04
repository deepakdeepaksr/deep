import io, os, json, shutil, subprocess, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
SRC = os.path.join(P, 'pcb')
CLI = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
SYMLIB_HERE = (SRC + '/MoriShield_Carrier.kicad_sym').replace('\\', '/')
SYMLIB_STALE = (P + '/morishield/morishield_hardware/libraries/MoriShield_Carrier.kicad_sym').replace('\\', '/')
FPLIB = (P + '/morishield/morishield_hardware/libraries/MoriShield_Carrier.pretty').replace('\\', '/')


def run(tag, sym_uri, fp_uri):
    DST = os.path.join(P, '_cto_extract', 'ercx_' + tag)
    shutil.rmtree(DST, ignore_errors=True)
    os.makedirs(DST)
    for f in ('MoriShield_Carrier.kicad_sch', 'MoriShield_Carrier.kicad_pro',
              'MoriShield_Carrier.kicad_sym'):
        shutil.copy2(os.path.join(SRC, f), os.path.join(DST, f))
    io.open(os.path.join(DST, 'sym-lib-table'), 'w', encoding='utf-8', newline='').write(
        '(sym_lib_table\n  (version 7)\n  (lib (name "MoriShield_Carrier")(type "KiCad")'
        '(uri "%s")(options "")(descr "project symbols"))\n)\n' % sym_uri)
    io.open(os.path.join(DST, 'fp-lib-table'), 'w', encoding='utf-8', newline='').write(
        '(fp_lib_table\n  (version 7)\n  (lib (name "MoriShield_Carrier")(type "KiCad")'
        '(uri "%s")(options "")(descr "project footprints"))\n)\n' % fp_uri)
    out = os.path.join(DST, 'erc.json')
    subprocess.run([CLI, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', out,
                    os.path.join(DST, 'MoriShield_Carrier.kicad_sch')],
                   capture_output=True, text=True, timeout=900)
    if not os.path.exists(out):
        print('%-12s no report' % tag)
        return
    e = json.load(open(out, encoding='utf-8'))
    ev = [v for s in e.get('sheets', []) for v in s.get('violations', [])]
    c = collections.Counter(v['type'] for v in ev)
    print('%-12s sym=%s   items %4d  %s' % (
        tag, 'own (157,936)' if 'pcb' in sym_uri else 'STALE (153,623)', len(ev), dict(c)))
    return ev, c


print('=== A. correct forward-slash absolute paths to the project own libraries ===')
run('ownlibs', SYMLIB_HERE, FPLIB)

print('=== B. same, but the symbol library is the release-layout copy ===')
run('stalelib', SYMLIB_STALE, FPLIB)
