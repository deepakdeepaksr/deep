import sys, re
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')

# 1. every net that mentions the sensors he asked about
print('=== nets mentioning the sensors in question ===')
names = {}
for fp in b.GetFootprints():
    for p in fp.Pads():
        n = p.GetNetname()
        if n:
            names.setdefault(n, []).append('%s.%s' % (fp.GetReference(), p.GetNumber()))
for t in b.GetTracks():
    n = t.GetNetname()
    if n:
        names.setdefault(n, [])
KEY = ('REED', 'WIND', 'FDC', 'SOIL', 'MPU', 'GY', '5600', 'ADC', 'AIN', 'I2C1', 'HUM', 'TEMP')
for n in sorted(names):
    if any(k in n.upper() for k in KEY):
        print('   %-22s %s' % (n, ', '.join(sorted(set(names[n]))) or '(no pads)'))

# 2. every connector, its pads and nets
print()
print('=== every connector on the board, with its nets ===')
for fp in sorted(b.GetFootprints(), key=lambda f: (f.GetReference()[0],
                                                   int(re.sub(r'\D', '', f.GetReference()) or 0))):
    ref = fp.GetReference()
    if not ref.startswith('J'):
        continue
    lib = str(fp.GetFPID().GetLibItemName())
    p = fp.GetPosition()
    pads = sorted(fp.Pads(), key=lambda x: int(x.GetNumber()) if x.GetNumber().isdigit() else 0)
    nets = [x.GetNetname() or '-' for x in pads]
    uniq = [x for i, x in enumerate(nets) if x not in nets[:i]]
    print('   %-4s %-40s (%7.2f,%7.2f) %d pads' % (ref, lib[:40], p.x / 1e6, p.y / 1e6, len(pads)))
    print('        %s' % ', '.join('%s:%s' % (x.GetNumber(), x.GetNetname() or 'none') for x in pads)[:230])

# 3. the board's own port labels (F.Fab / silk text) - which sensor each port is for
print()
print('=== port labels drawn on the board ===')
for it in b.GetDrawings():
    if type(it).__name__ == 'PCB_TEXT':
        s = it.GetText().strip()
        if re.match(r'^J\d', s) or 'SOIL' in s.upper() or 'SPS' in s.upper() or 'SGP' in s.upper():
            pp = it.GetPosition()
            print('   %-26r at (%.2f, %.2f)  layer=%s' % (s, pp.x / 1e6, pp.y / 1e6, b.GetLayerName(it.GetLayer())))
