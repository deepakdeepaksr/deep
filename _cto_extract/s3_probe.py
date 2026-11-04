import io, re, csv, sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

r = list(csv.reader(io.open(P + r'\revC\decoupling_map.csv', encoding='utf-8-sig')))
print('=== decoupling map ===')
print('   rows (incl header):', len(r))
print('   header:', r[0])
for x in r[1:3]:
    print('   sample:', x)
if len(r) > 1:
    cols = r[0]
    for name in ('over limit', 'meets', 'distance_mm', 'status', 'limit_mm'):
        for i, c in enumerate(cols):
            if name in c.lower():
                vals = [row[i] for row in r[1:]]
                print('   col %-14s distinct: %s' % (c, sorted(set(vals))[:6]))

print()
print('=== module outlines: layer, kind, bbox ===')
import pcbnew
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')


def ln(i):
    try:
        return b.GetLayerName(i)
    except Exception:
        return str(i)


for it in b.GetDrawings():
    lay = ln(it.GetLayer())
    if lay not in ('Dwgs.User', 'F.Fab', 'CrtYd'):
        continue
    kind = type(it).__name__
    if kind == 'PCB_TEXT':
        print('   %-11s TEXT  %-28r at %.2f,%.2f' % (lay, it.GetText()[:28],
                                                    it.GetPosition().x / 1e6, it.GetPosition().y / 1e6))
    else:
        try:
            s, e = it.GetStart(), it.GetEnd()
            print('   %-11s %-10s (%.2f,%.2f)-(%.2f,%.2f)' % (lay, kind, s.x / 1e6, s.y / 1e6, e.x / 1e6, e.y / 1e6))
        except Exception:
            pass

print()
print('=== which footprints are the module sockets, and is anything named ESP/MODEM on them? ===')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}
for ref in ('J1', 'J2', 'J3', 'J4'):
    fp = d.get(ref)
    if fp:
        p = fp.GetPosition()
        print('   %-4s %-40s at %.2f,%.2f rot %.1f' % (ref, str(fp.GetFPID().GetLibItemName())[:40],
                                                       p.x / 1e6, p.y / 1e6, fp.GetOrientationDegrees()))
for ref, fp in sorted(d.items()):
    txt = (fp.GetValue() or '') + ' ' + str(fp.GetFPID().GetLibItemName())
    if re.search(r'ESP|WROOM|MODEM|A7672|LORA|E22', txt, re.I):
        p = fp.GetPosition()
        print('   module-ish: %-6s %-42s at %.2f,%.2f' % (ref, txt[:42], p.x / 1e6, p.y / 1e6))
