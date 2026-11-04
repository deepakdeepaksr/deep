import sys, re, io
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')

print('=== footprints that could be RF / antenna connectors ===')
KEY = ('SMA', 'U.FL', 'UFL', 'IPEX', 'IPX', 'RF', 'ANT', 'COAX', 'MMCX', 'H.SERIES', 'CONNECT')
for fp in b.GetFootprints():
    name = str(fp.GetFPID().GetLibItemName())
    val = fp.GetValue() or ''
    ref = fp.GetReference()
    nets = [p.GetNetname() for p in fp.Pads() if p.GetNetname()]
    if any(k in (name + ' ' + val).upper() for k in KEY) or any('ANT' in (n or '').upper() for n in nets):
        pos = fp.GetPosition()
        print('   %-6s %-46s %-24s at %7.2f,%7.2f  nets=%s'
              % (ref, name[:46], val[:24], pos.x / 1e6, pos.y / 1e6, nets))

print()
print('=== nets containing ANT / RF / LoRa / WIFI ===')
names = set()
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname():
            names.add(p.GetNetname())
for t in b.GetTracks():
    if t.GetNetname():
        names.add(t.GetNetname())
for n in sorted(names):
    if re.search(r'ANT|RF|LORA|E22|WIFI|2G4|SUBG', n, re.I):
        print('   ', n)

print()
print('=== board outline and the three radio areas ===')
bb = b.GetBoardEdgesBoundingBox()
print('   board %.2f x %.2f mm  at (%.2f, %.2f)'
      % (bb.GetWidth() / 1e6, bb.GetHeight() / 1e6, bb.GetX() / 1e6, bb.GetY() / 1e6))
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
for m in re.finditer(r'\(gr_text "([^"]{3,40})"', t):
    s = t[m.start():m.start() + 300]
    at = re.search(r'\(at ([\d.]+) ([\d.]+)', s)
    if at and re.search(r'ANT|SMA|RF|50', m.group(1), re.I):
        print('   text %-28r at %s,%s' % (m.group(1), at.group(1), at.group(2)))
