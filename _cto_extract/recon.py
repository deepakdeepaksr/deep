import sys, json, re, glob, os
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')

names = set()
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname():
            names.add(p.GetNetname())
for t in b.GetTracks():
    if t.GetNetname():
        names.add(t.GetNetname())
print('=== %d nets on the board ===' % len(names))
for n in sorted(names):
    print('   ', n)

print('\n=== does the board file itself carry net_class? ===')
p = open(base + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
print('   "net_class" occurrences:', p.count('net_class'))
m = re.search(r'\(net [^\n]*\n', p)
print('   sample net decl:', m.group(0).strip() if m else '-')

print('\n=== any non-empty netclass_patterns anywhere (schema reference) ===')
for f in glob.glob(base + r'\**\*.kicad_pro', recursive=True):
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception:
        continue
    pat = d.get('net_settings', {}).get('netclass_patterns')
    cls = [c.get('name') for c in d.get('net_settings', {}).get('classes', [])]
    if pat:
        print('   HIT', f.replace(base, '.'))
        print('        classes:', cls)
        print('        pattern[0]:', json.dumps(pat[0]))
        break
else:
    print('   none found - will use KiCad 8/9 schema {"netclass":..,"pattern":..}')

print('\n=== current classes entry, verbatim ===')
d = json.load(open(base + r'\pcb\MoriShield_Carrier.kicad_pro', encoding='utf-8'))
print(json.dumps(d['net_settings']['classes'], indent=1)[:900])
print('   rule_severities:', json.dumps(d['board']['design_settings'].get('rule_severities', {})))
