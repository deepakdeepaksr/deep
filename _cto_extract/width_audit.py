import sys, json, collections
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

CLASS = {
    'Power_5V_In':    (['+5V_IN', '+5V_F', '/5V_PROT'], 1.50, 0.25),
    'Power_5V_Modem': (['+5V'],                         1.50, 0.25),
    'Power_5V_Sens':  (['/+5V_ESP', '/+5V_SENS', '/+5V_E22', '/+5V_E22_IN', 'LED5V_A'], 0.80, 0.20),
    '3V3':            (['3V3_C', '/3V3_SENS', '/3V3_SENS_SW', 'LED33_A'], 0.50, 0.20),
    'GND':            (['GND'],                         0.30, 0.20),
    'PE':             (['PE'],                          1.00, 0.30),
}
lookup = {}
for cn, (nets, w, c) in CLASS.items():
    for n in nets:
        lookup[n] = (cn, w, c)

b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')
FCU = pcbnew.F_Cu

print('=== copper width audit, measured directly (DRC cannot check this) ===')
tot_bad = 0
for net, (cn, req, _c) in sorted(lookup.items(), key=lambda kv: -kv[1][1]):
    segs = [t for t in b.GetTracks() if t.GetNetname() == net and not isinstance(t, pcbnew.PCB_VIA)]
    vias = [t for t in b.GetTracks() if t.GetNetname() == net and isinstance(t, pcbnew.PCB_VIA)]
    bad = [t for t in segs if t.GetWidth() / 1e6 < req - 1e-6]
    vbad = [v for v in vias if v.GetWidth(FCU) / 1e6 < (1.0 if req >= 1.5 else 0.8) - 1e-6]
    tot_bad += len(bad) + len(vbad)
    have = sorted({round(t.GetWidth() / 1e6, 3) for t in segs})
    print('\n  %-16s class %-15s needs >= %.2f mm   segments %d, widths present %s'
          % (net, cn, req, len(segs), have))
    if bad:
        agg = collections.Counter()
        for t in bad:
            agg[round(t.GetWidth() / 1e6, 3)] += 1
        print('     %d UNDER-WIDTH segments: %s' % (len(bad), dict(agg)))
        for t in sorted(bad, key=lambda x: x.GetWidth())[:14]:
            a, c = t.GetStart(), t.GetEnd()
            L = ((c.x - a.x) ** 2 + (c.y - a.y) ** 2) ** 0.5 / 1e6
            print('       %.3f mm  %6.2f mm long  (%.2f,%.2f)->(%.2f,%.2f)  %s'
                  % (t.GetWidth() / 1e6, L, a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6,
                     b.GetLayerName(t.GetLayer())))
        if len(bad) > 14:
            print('       ... %d more' % (len(bad) - 14))
    if vbad:
        print('     %d vias below the class via rule: diameters %s'
              % (len(vbad), sorted({round(v.GetWidth(FCU) / 1e6, 2) for v in vbad})))

print('\n  TOTAL items below the restored rule set: %d' % tot_bad)

print('\n=== estimated resistance of each 5 V segment group (1 oz outer / 0.5 oz inner) ===')
RHO_SQ = {True: 0.505e-3, False: 1.01e-3}     # ohm per square, outer / inner
for net in ('+5V_IN', '+5V_F', '+5V', '/+5V_ESP', '/+5V_SENS'):
    outer = inner = 0.0
    for t in b.GetTracks():
        if t.GetNetname() != net or isinstance(t, pcbnew.PCB_VIA):
            continue
        a, c = t.GetStart(), t.GetEnd()
        L = ((c.x - a.x) ** 2 + (c.y - a.y) ** 2) ** 0.5 / 1e6
        w = max(t.GetWidth() / 1e6, 0.05)
        lay = b.GetLayerName(t.GetLayer())
        if lay.endswith('.Cu') and lay.startswith('In'):
            inner += L / w * RHO_SQ[False]
        else:
            outer += L / w * RHO_SQ[True]
    print('   %-12s series path ~ %6.1f mOhm   (outer %.1f + inner %.1f)'
          % (net, (outer + inner) * 1e3, outer * 1e3, inner * 1e3))
