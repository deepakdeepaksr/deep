import sys, io, re, json, collections
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
MM = 1e6


def lname(i):
    try:
        return b.GetLayerName(i)
    except Exception:
        return str(i)


tr = list(b.GetTracks())
segs = [t for t in tr if type(t).__name__ != 'PCB_VIA']
vias = [t for t in tr if type(t).__name__ == 'PCB_VIA']
zones = [z for z in b.Zones() if not z.GetIsRuleArea()]
names = set()
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname():
            names.add(p.GetNetname())
for t in tr:
    if t.GetNetname():
        names.add(t.GetNetname())
print('1. CENSUS  footprints %d  segments %d  vias %d  zones %d  net names %d'
      % (len(list(b.GetFootprints())), len(segs), len(vias), len(zones), len(names)))

print('\n2. ZONES')
for z in zones:
    print('   %-14s %-8s filled=%s  net=%s' % (z.GetNetname() or '-', lname(z.GetLayer()),
                                               z.IsFilled(), z.GetNetname()))

print('\n3. the new B.Cu GND zone: thermal + clearance settings')
for z in zones:
    if z.GetNetname() == 'GND':
        try:
            ta = z.GetThermalReliefAdj()
            gap = z.GetThermalReliefGap() / MM
            bridge = z.GetThermalReliefCopperBridge() / MM
            print('   layer=%-8s thermal_adj=%s  gap=%.3f mm  bridge=%.3f mm  clear=%.3f'
                  % (lname(z.GetLayer()), ta, gap, bridge, z.GetClearance() / MM))
        except Exception as e:
            print('   (could not read zone settings: %s)' % e)

print('\n4. GND stitching vias: count of GND vias, and their drill/size')
gv = [v for v in vias if v.GetNetname() == 'GND']
print('   GND vias total %d' % len(gv))
print('   size/drill histogram:', dict(collections.Counter(
    (round(v.GetWidth(0) / MM, 2)) for v in gv)))

print('\n5. vias still inside SMD pads (must stay 65 unless new vias were dropped on pads)')
n = 0
hits = []
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
            continue
        for v in vias:
            if p.HitTest(v.GetPosition()):
                n += 1
                hits.append('%s.%s' % (fp.GetReference(), p.GetNumber()))
print('   count %d' % n)
print('   sample', hits[:8])

print('\n6. does any of the 85 new stitching vias sit in an SMD pad?')
plan = P + r'\revC\_e1_trial_plan.json'
if os_ok := __import__('os').path.exists(plan):
    d = json.load(open(plan, encoding='utf-8'))
    pts = d.get('vias') or d.get('positions') or d
    print('   plan file keys:', list(d)[:6] if isinstance(d, dict) else 'list')
else:
    print('   plan file absent')

print('\n7. /+5V_SENS widths (0.60 cap claim)')
w = collections.defaultdict(collections.Counter)
for t in segs:
    if t.GetNetname() == '/+5V_SENS':
        w[lname(t.GetLayer())][round(t.GetWidth() / MM, 2)] += 1
for k, v in w.items():
    print('   %-9s %s' % (k, dict(v)))

print('\n8. silkscreen on back (the reason a B.Cu pour is silk-safe)')
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
print('   F.SilkS refs %d   B.SilkS refs %d' % (len(re.findall(r'\(layer "F\.SilkS"', t)),
                                                len(re.findall(r'\(layer "B\.SilkS"', t))))
print('   (zone blocks in file: %d)' % len(re.findall(r'\(zone ', t)))
