import sys, json, collections
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')
FCU = pcbnew.F_Cu


def dia(t):
    return round(t.GetWidth(FCU) / 1e6, 2)


print('=== copper on the input path, end to end (R5) ===')
for net in ('+5V_IN', '+5V_F', '+5V', '/+5V_ESP', '/+5V_SENS', '/+5V_E22', '3V3_C'):
    tr = [t for t in b.GetTracks() if t.GetNetname() == net]
    if not tr:
        continue
    seg = [t for t in tr if not isinstance(t, pcbnew.PCB_VIA)]
    vias = [t for t in tr if isinstance(t, pcbnew.PCB_VIA)]
    w = collections.Counter(round(t.GetWidth() / 1e6, 3) for t in seg)
    v = collections.Counter(dia(t) for t in vias)
    print('  %-11s tracks %s | vias(dia mm) %s' % (net, dict(w), dict(v)))

print('\n=== narrowest copper per net on the 5 V path ===')
for net in ('+5V_IN', '+5V_F', '+5V'):
    seg = [t for t in b.GetTracks() if t.GetNetname() == net and not isinstance(t, pcbnew.PCB_VIA)]
    for t in sorted(seg, key=lambda x: x.GetWidth()):
        a, c = t.GetStart(), t.GetEnd()
        print('  %-8s %.3f mm   (%.2f,%.2f) -> (%.2f,%.2f)  %s'
              % (net, t.GetWidth() / 1e6, a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6, b.GetLayerName(t.GetLayer())))

print('\n=== J18 pads and silkscreen (R3) ===')
for fp in b.GetFootprints():
    if fp.GetReference() != 'J18':
        continue
    for pad in fp.Pads():
        pp = pad.GetPosition()
        print('  pad %s net %-8s at %.2f,%.2f  size %.2f x %.2f'
              % (pad.GetNumber(), pad.GetNetname(), pp.x / 1e6, pp.y / 1e6,
                 pad.GetSize().x / 1e6, pad.GetSize().y / 1e6))
for txt in b.GetDrawings():
    if type(txt).__name__ != 'PCB_TEXT':
        continue
    ln = txt.GetLayerName()
    if 'Silkscreen' not in ln:
        continue
    s = txt.GetText().strip()
    p = txt.GetPosition()
    if p.x / 1e6 < 150 and 90 < p.y / 1e6 < 120:
        try:
            sw = txt.GetStroke().m_Width / 1e6
        except Exception:
            sw = -1
        print('  silk "%s" %-16s at %.2f,%.2f stroke %.3f mm' % (s, ln, p.x / 1e6, p.y / 1e6, sw))

print('\n=== dangling copper ===')
d = json.load(open(base + r'\_cto_extract\drc_pcb.json', encoding='utf-8'))
for v in d['violations']:
    if 'dangling' in v.get('type', ''):
        its = v.get('items') or []
        pos = its[0].get('pos') if its else None
        loc = '%.2f,%.2f' % (pos['x'] / 1e6, pos['y'] / 1e6) if pos else '?'
        print('  %-15s %-14s %s' % (v['type'], loc, (its[-1].get('description') if its else '')[:70]))

print('\n=== /MODEM_RST route ===')
for t in b.GetTracks():
    if t.GetNetname() != '/MODEM_RST':
        continue
    if isinstance(t, pcbnew.PCB_VIA):
        p = t.GetPosition()
        print('  via  %.2f,%.2f dia %.2f' % (p.x / 1e6, p.y / 1e6, dia(t)))
    else:
        a, c = t.GetStart(), t.GetEnd()
        print('  trk  (%.2f,%.2f)->(%.2f,%.2f) %.3f mm %s'
              % (a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6, t.GetWidth() / 1e6, b.GetLayerName(t.GetLayer())))

print('\n=== /WDT_WDI route (the fix) ===')
for t in b.GetTracks():
    if t.GetNetname() != '/WDT_WDI':
        continue
    if isinstance(t, pcbnew.PCB_VIA):
        p = t.GetPosition()
        print('  via  %.2f,%.2f dia %.2f' % (p.x / 1e6, p.y / 1e6, dia(t)))
    else:
        a, c = t.GetStart(), t.GetEnd()
        print('  trk  (%.2f,%.2f)->(%.2f,%.2f) %.3f mm %s'
              % (a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6, t.GetWidth() / 1e6, b.GetLayerName(t.GetLayer())))

