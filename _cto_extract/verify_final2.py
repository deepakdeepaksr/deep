import json, sys, re, collections
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}

print('=== 1. E22 control lines vs the ESP32 board microSD pins ===')
for ref, pads in (('J1', ('9', '10', '11', '16', '17', '8', '6')), ('J2', ('6', '7', '8', '9', '16', '17'))):
    for p in sorted(d[ref].Pads(), key=lambda x: int(x.GetNumber())):
        if p.GetNumber() in pads:
            print('   %s pad %-3s  %-18s' % (ref, p.GetNumber(), p.GetNetname() or '<none>'))
print('   ESP32-S3 header map: J1.16=GPIO10  J1.17=GPIO11  J1.8=GPIO15  J2.8=GPIO40  J2.7=GPIO41')

print('\n=== 2. which 3 footprints now fail lib_footprint_mismatch ===')
r = json.load(open(base + r'\_cto_extract\drc_f.json', encoding='utf-8'))
for v in r['violations']:
    if v['type'] in ('lib_footprint_mismatch', 'annular_width', 'via_diameter'):
        its = v.get('items') or []
        print('   %-22s %s' % (v['type'], ' | '.join((i.get('description') or '')[:60] for i in its[:2])))

print('\n=== 3. the /I2C0_MUX_SC0 via ===')
for t in b.GetTracks():
    if t.GetNetname() == '/I2C0_MUX_SC0' and isinstance(t, pcbnew.PCB_VIA):
        sz = t.GetSize() if hasattr(t, 'GetSize') else None
        w = t.GetWidth(pcbnew.F_Cu) / 1e6
        try:
            dr = t.GetDrillSize().x / 1e6
        except Exception:
            dr = -1
        p = t.GetPosition()
        print('   via at %.2f,%.2f  copper %.3f mm  drill %.3f mm  annular %.3f mm'
              % (p.x / 1e6, p.y / 1e6, w, dr, (w - dr) / 2))

print('\n=== 4. PE copper inside the R47/R48 corridor ===')
for r_ in ('R47', 'R48'):
    fp = d[r_]
    for p in fp.Pads():
        print('   %s pad %s at %.2f,%.2f  w %.2f  net %s'
              % (r_, p.GetNumber(), p.GetPosition().x / 1e6, p.GetPosition().y / 1e6,
                 p.GetSize().x / 1e6, p.GetNetname() or '<none>'))
for t in b.GetTracks():
    if t.GetNetname() != 'PE':
        continue
    a, c = t.GetStart(), t.GetEnd()
    if isinstance(t, pcbnew.PCB_VIA):
        if 290 < a.x / 1e6 < 297 and 132 < a.y / 1e6 < 139:
            print('   PE via %.2f,%.2f copper %.3f' % (a.x / 1e6, a.y / 1e6, t.GetWidth(pcbnew.F_Cu) / 1e6))
    else:
        if 290 < a.x / 1e6 < 297 and 132 < a.y / 1e6 < 139:
            print('   PE track %.3f mm (%.2f,%.2f)->(%.2f,%.2f) %s'
                  % (t.GetWidth() / 1e6, a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6, b.GetLayerName(t.GetLayer())))

print('\n=== 5. net class values currently in the project ===')
pr = json.load(open(base + r'\pcb\MoriShield_Carrier.kicad_pro', encoding='utf-8'))
for c in pr['net_settings']['classes']:
    print('   %-16s track %.2f  clr %.2f  via %.2f/%.2f'
          % (c['name'], c['track_width'], c['clearance'], c['via_diameter'], c['via_drill']))
print('   patterns:', len(pr['net_settings']['netclass_patterns']))

print('\n=== 6. clearance violations: which pairs, measured ===')
for v in r['violations']:
    if v['type'] != 'clearance':
        continue
    its = v.get('items') or []
    pos = its[0].get('pos') if its else None
    loc = '(%.2f, %.2f)' % (pos['x'] / 1e6, pos['y'] / 1e6) if pos else ''
    print('   %-24s %s' % (loc, ' | '.join((i.get('description') or '')[:56] for i in its[:2])))
