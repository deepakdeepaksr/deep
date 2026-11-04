import json, subprocess, re

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
pro = base + r'\pcb\MoriShield_Carrier.kicad_pro'
cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

d = json.load(open(pro, encoding='utf-8'))
for c in d['net_settings']['classes']:
    c['track_width'] = 3.0          # every class impossible, Default included
json.dump(d, open(pro, 'w', encoding='utf-8'), indent=2)
print('all classes set to 3.0 mm track')

subprocess.run([cli, 'pcb', 'drc', '--refill-zones', '--severity-all', '--all-track-errors',
                '--format', 'json', '-o', base + r'\_cto_extract\drc_diag2.json',
                base + r'\pcb\MoriShield_Carrier.kicad_pcb'], capture_output=True, text=True)
r = json.load(open(base + r'\_cto_extract\drc_diag2.json', encoding='utf-8'))
tw = [v for v in r['violations'] if v['type'] == 'track_width']
print('DRC total', len(r['violations']), '  track_width:', len(tw))
print('=> classes', 'ARE' if tw else 'are NOT', 'being applied by kicad-cli')

p = open(base + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
print('\n=== board file structure around (layers ===')
i = p.find('(layers')
print(p[i - 200:i + 700])
print('=== count of top-level (net N "x") decls ===')
print(len(re.findall(r'\n\s+\(net \d+ "', p)))
