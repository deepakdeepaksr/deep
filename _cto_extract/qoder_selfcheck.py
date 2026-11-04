import io, re, os

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
t = io.open(P + r'\QODER.md', encoding='utf-8').read()

print('lines %d | KB %d' % (len(t.splitlines()), len(t) // 1024))
print('banned-word count:', len(re.findall(r'prototyp', t, re.I)))
print('"ready for fabrication" claims:', len(re.findall(r'ready for fabrication', t, re.I)))
print('sections:', [l[:44] for l in t.splitlines() if l.startswith('## ')])

print()
print('=== referenced workspace paths that do not exist ===')
refs = set(re.findall(r'[A-Za-z0-9_\-\.\\/]*\.(?:py|ps1|md|csv|json|txt|pdf|kicad_pcb|kicad_sch|kicad_pro|kicad_sym|kicad_dru)', t))
bad = []
for r in sorted(refs):
    if r.startswith('.') or len(r) < 5:
        continue
    cands = [os.path.join(P, r.replace('\\', os.sep)),
             os.path.join(P, 'pcb', r.replace('\\', os.sep))]
    if not any(os.path.exists(c) for c in cands):
        bad.append(r)
print('   ', bad or 'NONE')

print()
print('=== the commands in section 2 actually run? ===')
for s in [r'pcb\_census.py', r'pcb\_plot_stitching_final.py', r'_cto_extract\trace2.py',
          r'_cto_extract\gate_truth.py', r'_cto_extract\final_verify.py',
          r'_cto_extract\E22-900T22D-UserManual.txt', r'me.md', 'work done',
          r'pcb\MoriShield_Carrier.kicad_dru',
          r'morishield\morishield_hardware\libraries\MoriShield_Carrier.pretty']:
    print('   %-56s %s' % (s, os.path.exists(P + '\\' + s)))
