import sys, os
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
path = os.path.join(base, 'pcb', 'MoriShield_Carrier.kicad_pcb')
b = pcbnew.LoadBoard(path)

print('=== 1. FOOTPRINT attribute API on this build ===')
fp = [f for f in b.GetFootprints() if f.GetReference() == 'U4'][0]
meth = [m for m in dir(fp) if 'ttrib' in m or 'Exclude' in m or 'BoardOnly' in m or 'InBom' in m or 'OnBoard' in m]
print('   ', meth)
print('   U4 attributes int =', fp.GetAttributes())
consts = [n for n in dir(pcbnew) if n.startswith('FP_')]
print('   pcbnew FP_* constants:', consts)

print('\n=== 2. dangling copper, found geometrically ===')
segs = [t for t in b.GetTracks() if not isinstance(t, pcbnew.PCB_VIA)]
vias = [t for t in b.GetTracks() if isinstance(t, pcbnew.PCB_VIA)]
pads = [(p.GetPosition(), p.GetNetname()) for f in b.GetFootprints() for p in f.Pads()]


def endpoints(t):
    return t.GetStart(), t.GetEnd()


def supported(pt, net, tol=200, skip=None):
    """True if the point lands on a pad, a via of the same net, or another track end."""
    for q, n in pads:
        if abs(q.x - pt.x) <= tol and abs(q.y - pt.y) <= tol and (n == net or n is None):
            return 'pad'
    for v in vias:
        if v is skip:
            continue
        q = v.GetPosition()
        if abs(q.x - pt.x) <= tol and abs(q.y - pt.y) <= tol and v.GetNetname() == net:
            return 'via'
    for o in segs:
        if o is skip:
            continue
        if o.GetNetname() != net:
            continue
        for q in endpoints(o):
            if abs(q.x - pt.x) <= tol and abs(q.y - pt.y) <= tol:
                return 'track'
    return None


dangling = []
for t in segs:
    a, c = endpoints(t)
    sa = supported(a, t.GetNetname(), skip=t)
    sc = supported(c, t.GetNetname(), skip=t)
    if not sa or not sc:
        L = ((c.x - a.x) ** 2 + (c.y - a.y) ** 2) ** 0.5 / 1e6
        dangling.append((L, t, sa, sc))
dangling.sort(key=lambda x: -x[0])
print('   %d track segments have an unsupported end:' % len(dangling))
for L, t, sa, sc in dangling[:20]:
    a, c = endpoints(t)
    print('     net %-12s %.3f mm  %-7s a=%s b=%s  (%.2f,%.2f)->(%.2f,%.2f)'
          % (t.GetNetname(), L, b.GetLayerName(t.GetLayer()), sa or 'FREE', sc or 'FREE',
             a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6))

print('\n   vias with no track of the same net touching them:')
orph = []
for v in vias:
    q = v.GetPosition()
    hit = any(o.GetNetname() == v.GetNetname() and
              (abs(endpoints(o)[0].x - q.x) <= 200 and abs(endpoints(o)[0].y - q.y) <= 200 or
               abs(endpoints(o)[1].x - q.x) <= 200 and abs(endpoints(o)[1].y - q.y) <= 200)
              for o in segs)
    onpad = any(abs(p[0].x - q.x) <= 200 and abs(p[0].y - q.y) <= 200 for p in pads)
    if not hit:
        orph.append((v, onpad))
print('   %d' % len(orph))
for v, onpad in orph[:12]:
    q = v.GetPosition()
    print('     net %-14s at %.2f,%.2f  dia %.2f  on a pad: %s'
          % (v.GetNetname(), q.x / 1e6, q.y / 1e6, v.GetWidth(pcbnew.F_Cu) / 1e6, onpad))

print('\n(nothing deleted or saved in this pass)')
