import sys, json
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')

segs = [t for t in b.GetTracks() if type(t).__name__ != 'PCB_VIA']
vias = [t for t in b.GetTracks() if type(t).__name__ == 'PCB_VIA']
pads = [(fp.GetReference(), p.GetNumber(), p.GetNetname(), p.GetPosition())
        for fp in b.GetFootprints() for p in fp.Pads()]

print('=== everything within 6 mm of (167.45, 129.80) ===')
cx, cy = 167.45, 129.80
for ref, num, net, pos in pads:
    x, y = pos.x / 1e6, pos.y / 1e6
    if abs(x - cx) < 6 and abs(y - cy) < 6:
        print('   pad   %-6s %-3s %-10s (%.2f, %.2f)' % (ref, num, net or '-', x, y))
for t in segs:
    a, c = t.GetStart(), t.GetEnd()
    for q in (a, c):
        if abs(q.x / 1e6 - cx) < 6 and abs(q.y / 1e6 - cy) < 6:
            L = ((c.x - a.x) ** 2 + (c.y - a.y) ** 2) ** 0.5 / 1e6
            print('   trk   %-12s %.3f mm  (%.2f,%.2f)->(%.2f,%.2f) %-8s %s'
                  % (t.GetNetname(), L, a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6,
                     b.GetLayerName(t.GetLayer()), str(t.GetUUID())[:8]))
            break
for v in vias:
    q = v.GetPosition()
    if abs(q.x / 1e6 - cx) < 6 and abs(q.y / 1e6 - cy) < 6:
        print('   via   %-12s (%.2f, %.2f)' % (v.GetNetname(), q.x / 1e6, q.y / 1e6))

print('\n=== is the 0.7778 mm stub attached to anything live? ===')
target = None
for t in segs:
    if str(t.GetUUID()) == 'a8d45380-c35a-468e-a3e8-032be5d19b87':
        target = t
if target is None:
    print('   stub not found')
else:
    a, c = target.GetStart(), target.GetEnd()
    for name, q in (('start', a), ('end', c)):
        onpad = [p for p in pads if abs(p[3].x - q.x) < 300 and abs(p[3].y - q.y) < 300]
        nbr = [o for o in segs if o is not target and o.GetNetname() == target.GetNetname()
               and any(abs(o.GetStart().x - q.x) < 300 and abs(o.GetStart().y - q.y) < 300 or
                       abs(o.GetEnd().x - q.x) < 300 and abs(o.GetEnd().y - q.y) < 300 for _ in [0])]
        nv = [v for v in vias if v.GetNetname() == target.GetNetname()
              and abs(v.GetPosition().x - q.x) < 300 and abs(v.GetPosition().y - q.y) < 300]
        print('   %-5s (%.2f,%.2f)  pads=%s  same-net tracks=%d  vias=%d'
              % (name, q.x / 1e6, q.y / 1e6,
                 ['%s.%s:%s' % (r, n, t2 or '-') for r, n, t2, _ in onpad] or 'none',
                 len(nbr), len(nv)))
