import json, sys, collections
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
d = json.load(open(P + r'\_cto_extract\drc_b2.json', encoding='utf-8'))

print('=== the 16 track_width violations, with real widths ===')
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
byloc = {}
for t in b.GetTracks():
    if isinstance(t, pcbnew.PCB_VIA):
        continue
    a, c = t.GetStart(), t.GetEnd()
    byloc[(round(a.x / 1e6, 2), round(a.y / 1e6, 2))] = t
    byloc[(round(c.x / 1e6, 2), round(c.y / 1e6, 2))] = t

for v in d['violations']:
    if v['type'] != 'track_width':
        continue
    its = v.get('items') or []
    pos = its[0].get('pos') or {}
    x, y = round(pos.get('x', 0), 2), round(pos.get('y', 0), 2)   # DRC pos is already mm
    t = byloc.get((x, y))
    w = t.GetWidth() / 1e6 if t else None
    lay = b.GetLayerName(t.GetLayer()) if t else '?'
    print('   %-10s (%7.2f,%7.2f)  width %s  %s   %s'
          % (its[0].get('description', '').split('[')[1].split(']')[0] if '[' in its[0].get('description', '') else '?',
             x, y, ('%.3f' % w) if w else 'not-found', lay,
             (its[1].get('description') if len(its) > 1 else '')[:60]))

print('\n=== current class floors as the project holds them ===')
pr = json.load(open(P + r'\pcb\MoriShield_Carrier.kicad_pro', encoding='utf-8'))
for c in pr['net_settings']['classes']:
    print('   %-16s track %.2f  clr %.2f  via %.2f/%.2f'
          % (c['name'], c['track_width'], c['clearance'], c['via_diameter'], c['via_drill']))
print('   min_track_width rule:', pr['board']['design_settings']['rules']['min_track_width'])

print('\n=== the new track_dangling ===')
for v in d['violations']:
    if v['type'] == 'track_dangling':
        print('   ', json.dumps(v['items'])[:300])
