import io, re, os

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
t = io.open(P + r'\PROJECT_CONTEXT_RevC.md', encoding='utf-8').read()

print('=== wording checks ===')
print('  "prototype"      :', len(re.findall(r'prototype', t, re.I)))
print('  "ready for fab"  :', len(re.findall(r'ready for fabrication', t, re.I)))
print('  lines            :', len(t.splitlines()))

refs = sorted(set(re.findall(r'[A-Za-z0-9_\-\.\\/]*\.(?:py|ps1|md|csv|json|png|txt|pdf|kicad_pcb|kicad_sch|kicad_pro|kicad_sym|kicad_dru)', t)))
print('\n=== referenced paths that do not exist ===')
missing = []
for r in refs:
    cand = [os.path.join(P, r.replace('\\', os.sep)), os.path.join(P, 'pcb', r.replace('\\', os.sep))]
    if not any(os.path.exists(c) for c in cand):
        missing.append(r)
for m in missing:
    print('   ', m)
print('   total missing:', len(missing), 'of', len(refs), 'referenced')
