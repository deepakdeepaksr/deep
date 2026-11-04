import json, subprocess, collections, os

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
pro = base + r'\pcb\MoriShield_Carrier.kicad_pro'
cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

d = json.load(open(pro, encoding='utf-8'))
for c in d['net_settings']['classes']:
    if c['name'] == 'Power_5V_In':
        c['track_width'] = 3.0          # impossible on purpose
    if c['name'] == '3V3':
        c['track_width'] = 1.0
json.dump(d, open(pro, 'w', encoding='utf-8'), indent=2)
print('diagnostic widths written (Power_5V_In 3.0, 3V3 1.0)')

out = subprocess.run([cli, 'pcb', 'drc', '--refill-zones', '--severity-all', '--all-track-errors',
                      '--format', 'json', '-o', base + r'\_cto_extract\drc_diag.json',
                      base + r'\pcb\MoriShield_Carrier.kicad_pcb'],
                     capture_output=True, text=True)
r = json.load(open(base + r'\_cto_extract\drc_diag.json', encoding='utf-8'))
tw = [v for v in r['violations'] if v['type'] == 'track_width']
print('DRC total', len(r['violations']), ' track_width:', len(tw))
nets = collections.Counter()
for v in tw:
    for i in v.get('items', []):
        s = i.get('description') or ''
        if s.startswith('Track'):
            nets[s.split('[')[1].split(']')[0] if '[' in s else '?'] += 1
print('affected nets:', dict(nets))
for v in tw[:6]:
    its = v.get('items') or []
    print('   ', ' | '.join((i.get('description') or '')[:70] for i in its[:2]))
