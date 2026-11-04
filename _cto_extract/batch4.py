import os, subprocess, json, collections, shutil

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
PCB = os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_pcb')
SCH = os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_sch')
CLI = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
OUT = os.path.join(P, 'revC')
PREV = os.path.join(OUT, 'preview_do_not_ship')
os.makedirs(PREV, exist_ok=True)


def run(cmd, what):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        msg = (r.stderr or r.stdout or '').strip().replace('\n', ' ')[:130]
        print('  %-46s %s' % (what, 'OK' if r.returncode == 0 else 'FAILED  ' + msg))
        return r.returncode == 0
    except Exception as e:
        print('  %-46s ERROR %s' % (what, e))
        return False


print('=== exports ===')
run([CLI, 'sch', 'export', 'bom', '-o', os.path.join(OUT, 'MoriShield_Carrier_RevC_bom.csv'),
     '--group-by', 'Value,Footprint', '--fields',
     'Item,Reference,Value,Footprint,DNP,Manufacturer,MPN,Rating,Temp,Variant',
     '--labels', 'Item,Refs,Value,Footprint,DNP,Manufacturer,MPN,Rating,Temp,Variant', SCH],
    'BOM (empty MPN/Rating columns show the C6 gap)')
run([CLI, 'pcb', 'export', 'pos', '-o', os.path.join(OUT, 'MoriShield_Carrier_RevC_pos.cfg'),
     '--format', 'gerber', '--side', 'both', PCB], 'placement (gerber format, both sides)')
run([CLI, 'pcb', 'export', 'pos', '-o', os.path.join(OUT, 'MoriShield_Carrier_RevC_pos_front.csv'),
     '--format', 'csv', '--units', 'mm', '--side', 'front', PCB], 'placement front csv')
run([CLI, 'pcb', 'export', 'pos', '-o', os.path.join(OUT, 'MoriShield_Carrier_RevC_pos_back.csv'),
     '--format', 'csv', '--units', 'mm', '--side', 'back', PCB], 'placement back csv')
run([CLI, 'pcb', 'export', 'drill', '-o', PREV, '--format', 'excellon',
     '--excellon-units', 'mm', '--generate-map', '--map-format', 'gerber', PCB],
    'drill (preview only)')
run([CLI, 'pcb', 'export', 'gerbers', '-o', PREV, '--plot-all', '--preserve-pad-vectors',
     '--crossout-vias-outside-board', PCB], 'gerbers (preview only)')

print('\n=== renders for the evidence pack ===')
for side, name in (('a', 'render_top'), ('b', 'render_bottom')):
    run([CLI, 'pcb', 'render', '-o', os.path.join(OUT, name + '.png'),
         '--quality', 'high', '--rotate', '270' if side == 'a' else '90',
         '--perspective', '--background', 'White', PCB], name)
run([CLI, 'pcb', 'render', '-o', os.path.join(OUT, 'render_iso.png'),
     '--quality', 'high', '--rotate', '45', '--tilt', '60', '--perspective',
     '--background', 'White', PCB], 'render_iso')

print('\n=== verification: ERC and DRC on the saved files ===')
run([CLI, 'sch', 'erc', '--severity-all', '--format', 'json',
     '-o', os.path.join(OUT, 'erc_RevC.json'), SCH], 'ERC')
run([CLI, 'pcb', 'drc', '--refill-zones', '--schematic-parity', '--severity-all',
     '--all-track-errors', '--format', 'json', '-o', os.path.join(OUT, 'drc_RevC.json'), PCB], 'DRC')

try:
    e = json.load(open(os.path.join(OUT, 'erc_RevC.json'), encoding='utf-8'))
    ev = [v for s in e.get('sheets', []) for v in s.get('violations', [])]
    print('\n  ERC   errors %d   warnings %d   %s'
          % (len([v for v in ev if v['severity'] == 'error']),
             len([v for v in ev if v['severity'] == 'warning']),
             dict(collections.Counter(v['type'] for v in ev))))
    print('  ERC   ignored checks:', [i['key'] for i in e.get('ignored_checks', [])])
except Exception as ex:
    print('  ERC read failed', ex)
try:
    d = json.load(open(os.path.join(OUT, 'drc_RevC.json'), encoding='utf-8'))
    print('  DRC   %d items  %s' % (len(d['violations']),
          dict(collections.Counter(v['severity'] for v in d['violations']))))
    print('        ', dict(collections.Counter(v['type'] for v in d['violations'])))
    print('  DRC   unconnected %d   parity %d'
          % (len(d.get('unconnected_items', [])), len(d.get('schematic_parity', []))))
    print('  DRC   ignored checks:', [i['key'] for i in d.get('ignored_checks', [])])
except Exception as ex:
    print('  DRC read failed', ex)

print('\n=== revC\\ contents ===')
for root, dirs, files in os.walk(OUT):
    for f in sorted(files):
        fp = os.path.join(root, f)
        print('   %-62s %9d' % (fp.replace(P + os.sep, ''), os.path.getsize(fp)))
