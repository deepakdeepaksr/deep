import sys, re
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')

print('=== J18 pads ===')
for fp in b.GetFootprints():
    if fp.GetReference() == 'J18':
        for pad in fp.Pads():
            p = pad.GetPosition()
            print('   pad %s net %-8s centre y %8.3f   pad spans y %.3f .. %.3f'
                  % (pad.GetNumber(), pad.GetNetname(), p.y / 1e6,
                     (p.y - pad.GetSize().y / 2) / 1e6, (p.y + pad.GetSize().y / 2) / 1e6))

print('\n=== the two marks, measured as rendered boxes ===')
for it in b.GetDrawings():
    if type(it).__name__ != 'PCB_TEXT':
        continue
    s = it.GetText().strip()
    if s not in ('5v +', '5v -'):
        continue
    a = it.GetPosition()
    bb = None
    for fn in ('GetBoundingBox', ):
        try:
            bb = getattr(it, fn)()
        except Exception:
            pass
    if bb is None:
        try:
            bb = it.Shape().Extents()
        except Exception:
            bb = None
    if bb is None:
        print('   %-6s anchor (%.3f, %.3f)   [box not readable]' % (s, a.x / 1e6, a.y / 1e6))
        continue
    print('   %-6s anchor (%.3f, %.3f)  rot %-4s  BOX x %.3f..%.3f  y %.3f..%.3f   centre (%.3f, %.3f)  w %.3f h %.3f'
          % (s, a.x / 1e6, a.y / 1e6, '?',
             bb.GetX() / 1e6, bb.GetRight() / 1e6, bb.GetY() / 1e6, bb.GetBottom() / 1e6,
             bb.GetX() / 1e6 + bb.GetWidth() / 2e6, bb.GetY() / 1e6 + bb.GetHeight() / 2e6,
             bb.GetWidth() / 1e6, bb.GetHeight() / 1e6))

print('\n=== J18 reference field position ===')
for fp in b.GetFootprints():
    if fp.GetReference() != 'J18':
        continue
    try:
        for gt in fp.Texts():
            print('   fp_text %r on %s at (%.3f, %.3f)'
                  % (gt.GetText(), gt.GetLayerName(), gt.GetPosition().x / 1e6, gt.GetPosition().y / 1e6))
    except Exception as e:
        print('   (text enumeration failed:', e, ')')

print('\n=== pcb\\work done : does the route C table exist? ===')
t = open(base + r'\pcb\work done', encoding='utf-8').read()
print('   chars', len(t))
for l in t.splitlines():
    s = l.strip()
    if re.match(r'^(work done )?[0-9]{1,2}[.)]\s', s) or s.lower().startswith('milestone') or s.startswith('§'):
        print('   HEAD:', s[:95])
for probe in ('40', '66', '31', 'mΩ', 'mOhm', 'mohm', 'Agreed before drawing', 'route C', 'TPS26630', 'stackup'):
    print('   %-22s %s' % (probe, t.count(probe)))
print('\n   --- last 1400 chars ---')
print(t[-1400:])
