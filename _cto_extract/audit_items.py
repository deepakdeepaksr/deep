import sys, collections
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}

print('=== A7: "nothing on J1 pins 16 to 20" ===')
for n in ('16', '17', '18', '19', '20'):
    p = d['J1'].Pads()[n] if False else None
for p in sorted(d['J1'].Pads(), key=lambda x: int(x.GetNumber())):
    if p.GetNumber() in ('16', '17', '18', '19', '20'):
        print('   J1.%-3s %s' % (p.GetNumber(), p.GetNetname() or '<none>'))

print('\n=== R8 / C11: the watchdog chain end to end ===')
for ref in ('U4',):
    fp = d.get(ref)
    if fp:
        print('  %s %s' % (ref, str(fp.GetFPID().GetLibItemName())))
        for p in sorted(fp.Pads(), key=lambda x: int(x.GetNumber()) if x.GetNumber().isdigit() else 0):
            print('    pad %-3s name %-10s net %s' % (p.GetNumber(), p.GetName(), p.GetNetname() or '<none>'))
for net in ('/WDT_MR', '/WDT_WDI', '/RST_ESP', '/I2C_SW_RST'):
    holders = ['%s.%s' % (fp.GetReference(), p.GetNumber())
               for fp in b.GetFootprints() for p in fp.Pads() if p.GetNetname() == net]
    print('   net %-12s -> %s' % (net, ', '.join(holders) or 'NOTHING'))

print('\n=== R17: which bus is the mux / expander on ===')
for ref in ('U7', 'U8'):
    fp = d.get(ref)
    if not fp:
        continue
    nets = sorted({p.GetNetname() for p in fp.Pads() if p.GetNetname()})
    print('  %s %-30s nets: %s' % (ref, str(fp.GetFPID().GetLibItemName())[:30], ', '.join(nets)))

print('\n=== E7: series resistance on the cabled I2C lines ===')
ch = [n for n in {p.GetNetname() for fp in b.GetFootprints() for p in fp.Pads() if p.GetNetname()}
      if '_CH' in n and 'I2C0' in n]
print('   cabled I2C nets: %d' % len(ch))
for n in sorted(ch):
    segs = [t for t in b.GetTracks() if t.GetNetname() == n and not isinstance(t, pcbnew.PCB_VIA)]
    rs = []
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.GetNetname() == n and fp.GetReference().startswith('R'):
                rs.append(fp.GetReference() + '=' + fp.GetValue())
    print('   %-22s tracks %2d  resistors on net: %s' % (n, len(segs), ', '.join(rs) or 'NONE'))

print('\n=== R12: what is on the inner copper layers ===')
cnt = collections.Counter()
for t in b.GetTracks():
    lay = b.GetLayerName(t.GetLayer())
    if lay.startswith('In'):
        cnt[(lay, t.GetNetname())] += 1
tot = collections.Counter()
for (lay, net), n in cnt.items():
    tot[lay] += n
print('   items per inner layer:', dict(tot))
top = sorted(cnt.items(), key=lambda kv: -kv[1])[:12]
for (lay, net), n in top:
    print('     %-9s %-18s %3d' % (lay, net, n))

print('\n=== C6 / Table 14 row 3: parts excluded from BOM or placement ===')
for fp in b.GetFootprints():
    eb = fp.GetAttributes()
    flags = []
    if eb & pcbnew.FP_BOARD_ONLY:
        flags.append('board_only')
    if eb & pcbnew.FP_EXCLUDE_FROM_BOM:
        flags.append('excl_BOM')
    if eb & pcbnew.FP_EXCLUDE_FROM_POS_FILES:
        flags.append('excl_POS')
    if eb & pcbnew.FP_VIRTUAL:
        flags.append('virtual')
    if flags:
        print('   %-6s %-30s %s' % (fp.GetReference(), str(fp.GetFPID().GetLibItemName())[:30], ', '.join(flags)))

print('\n=== C8: ESD parts within 5 mm of every connector pin that leaves the box ===')
conn = [fp for fp in b.GetFootprints() if fp.GetReference().startswith('J')]
esds = [fp for fp in b.GetFootprints() if fp.GetReference().startswith('ESD')]
for fp in conn:
    pins = [p for p in fp.Pads() if p.GetNetname() and not p.GetNetname().startswith('unconnected')]
    worst = None
    for p in pins:
        near = min((((q.GetPosition().x - p.GetPosition().x) ** 2 +
                     (q.GetPosition().y - p.GetPosition().y) ** 2) ** 0.5 / 1e6
                    for e in esds for q in e.Pads() if q.GetNetname() == p.GetNetname()), default=None)
        if near is not None and (worst is None or near > worst):
            worst = near
    sig = [p for p in pins if p.GetNetname() not in ('GND', '+5V', '3V3_C', 'PE', '/+5V_SENS', '/3V3_SENS_SW')]
    if sig and worst is not None and worst > 5.0:
        print('   %-5s nearest ESD on a protected net: %.1f mm  (worst)' % (fp.GetReference(), worst))
    elif sig and worst is None:
        print('   %-5s signal pins present, NO ESD part on any of them' % fp.GetReference())
