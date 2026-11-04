import io, re, sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()

print('=== sheets: is this one flat sheet? ===')
print('   (sheet (at  occurrences:', t.count('(sheet (at'))

print()
print('=== the four E22_M labels, with coordinates ===')
for m in re.finditer(r'\(label "(E22_M[01])"', t):
    seg = t[m.start():m.start() + 300]
    at = re.search(r'\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)', seg)
    uu = re.search(r'\(uuid "([^"]+)"', seg)
    print('   %-8s at (%9.2f, %9.2f) rot %-4s uuid %s' % (m.group(1), float(at.group(1)),
                                                          float(at.group(2)), at.group(3),
                                                          uu.group(1)[:8] if uu else '?'))

print()
print('=== J6 and J1 symbol instances: position, rotation, pin endpoints ===')
for ref, libname in (('J6', 'MoriShield_Carrier:Sock_1x07'), ('J1', 'MoriShield_Carrier:Sock_1x22_R')):
    i = t.find('(lib_id "%s")' % libname)
    if i < 0:
        print('   %s: lib_id %s not found' % (ref, libname))
        continue
    blk = t[i:i + 2600]
    at = re.search(r'\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)', blk)
    print('   %s at %s' % (ref, at.groups()))

print()
print('=== the MoriShield_Carrier:R symbol: pin offsets from its origin ===')
j = t.find('(symbol "MoriShield_Carrier:R"')
if j < 0:
    j = t.find('(symbol "R"')
blk = t[j:j + 4000]
for m in re.finditer(r'\(pin "(\d)"\s*line\s*\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)\)\s*\(length ([\d.]+)\)', blk):
    print('   pin %s at (%s, %s) rot %s length %s' % m.groups())

print()
print('=== board: J6 and J1 pad geometry, and every /E22_M track ===')
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
d = {f.GetReference(): f for f in b.GetFootprints()}
for ref in ('J6',):
    for p in sorted(d[ref].Pads(), key=lambda x: int(x.GetNumber())):
        q = p.GetPosition()
        print('   %s.%-3s (%.2f, %.2f) net=%s' % (ref, p.GetNumber(), q.x / 1e6, q.y / 1e6, p.GetNetname()))
for n in ('16', '17'):
    p = d['J1'].Pads()[n] if False else [x for x in d['J1'].Pads() if x.GetNumber() == n][0]
    q = p.GetPosition()
    print('   J1.%-3s (%.2f, %.2f) net=%s' % (n, q.x / 1e6, q.y / 1e6, p.GetNetname()))

print()
for net in ('/E22_M0', '/E22_M1'):
    segs = [x for x in b.GetTracks() if x.GetNetname() == net and type(x).__name__ != 'PCB_VIA']
    vs = [x for x in b.GetTracks() if x.GetNetname() == net and type(x).__name__ == 'PCB_VIA']
    print('   %s: %d segments, %d vias' % (net, len(segs), len(vs)))
    for s in segs:
        a, c = s.GetStart(), s.GetEnd()
        print('      (%.2f,%.2f)-(%.2f,%.2f) w %.2f layer %s'
              % (a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6, s.GetWidth() / 1e6, b.GetLayerName(s.GetLayer())))
    for v in vs:
        q = v.GetPosition()
        print('      via (%.2f,%.2f) layer %s' % (q.x / 1e6, q.y / 1e6, b.GetLayerName(v.GetStartLayer())))
