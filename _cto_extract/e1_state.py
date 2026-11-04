import sys, io, re, math, collections
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')


def layer(idv):
    try:
        return b.GetLayerName(idv)
    except Exception:
        return str(idv)


print('=== 1. every zone: net, layer, rule-area, fill state ===')
for z in b.Zones():
    print('   %-12s %-10s rule_area=%-5s filled=%-5s priority=%s outline_pts=%s'
          % (z.GetNetname() or '-', layer(z.GetLayer()), z.GetIsRuleArea(), z.IsFilled(),
             z.GetLocalClearance() if False else z.m_Priority if hasattr(z, 'm_Priority') else '?',
             'n/a'))

print()
print('=== 2. GND copper by layer (tracks+vias+pads) ===')
cnt = collections.Counter()
for t in b.GetTracks():
    if t.GetNetname() == 'GND':
        if type(t).__name__ == 'PCB_VIA':
            cnt['via'] += 1
        else:
            cnt[layer(t.GetLayer())] += 1
print('   GND tracks per layer + via count:', dict(cnt))
smd_gnd = th_gnd = 0
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname() != 'GND':
            continue
        if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
            smd_gnd += 1
        else:
            th_gnd += 1
print('   GND pads: SMD %d (touch only their own layer)  through-hole %d (span all layers)'
      % (smd_gnd, th_gnd))

print()
print('=== 3. silkscreen items that an outer-layer pour would put copper under ===')
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
silk_front = len(re.findall(r'\(layer "F\.SilkS"', t))
silk_back = len(re.findall(r'\(layer "B\.SilkS"', t))
print('   F.SilkS graphics/texts: %d   B.SilkS: %d' % (silk_front, silk_back))
print('   min_silk_clearance is 0.0, so copper under ANY of these flags silk_over_copper')

print()
print('=== 4. courtyards now present? ===')
blocks = re.split(r'\n\t\(footprint ', t)
no_c = []
per = {}
for blk in blocks[1:]:
    ref = re.search(r'\(property "Reference" "([^"]*)"', blk)
    if not ref:
        continue
    n = len(re.findall(r'CrtYd', blk))
    per[ref.group(1)] = n
    if n == 0:
        no_c.append(ref.group(1))
print('   footprints parsed %d, with no courtyard: %s' % (len(per), no_c or 'NONE'))
print('   U4 courtyard graphics: %s   SW1: %s' % (per.get('U4'), per.get('SW1')))

print()
print('=== 5. /+5V_SENS widths now ===')
w = collections.defaultdict(collections.Counter)
for tr in b.GetTracks():
    if tr.GetNetname() == '/+5V_SENS' and type(tr).__name__ != 'PCB_VIA':
        w[layer(tr.GetLayer())][round(tr.GetWidth() / 1e6, 2)] += 1
for k, v in w.items():
    print('   %-9s %s' % (k, dict(v)))

print()
print('=== 6. vias still inside SMD pads ===')
vias = [x for x in b.GetTracks() if type(x).__name__ == 'PCB_VIA']
n = 0
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
            continue
        for v in vias:
            if p.HitTest(v.GetPosition()):
                n += 1
print('   count: %d   (total vias %d)' % (n, len(vias)))
