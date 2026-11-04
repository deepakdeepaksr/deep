import sys, re, json
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

print('=== U4 symbol pin map (what pad N actually is) ===')
for f in (r'pcb\MoriShield_Carrier.kicad_sym', r'pcb\MoriShield_Carrier.kicad_sch'):
    t = open(base + '\\' + f, encoding='utf-8').read()
    i = t.find('"TPS3823"')
    if i < 0:
        i = t.find('TPS3823')
    if i < 0:
        print('  ', f, '- TPS3823 not found'); continue
    blk = t[i:i + 2600]
    pins = re.findall(r'\(symbol "TPS3823_\d+_\d+".*?\)', blk, re.S)
    for p in re.finditer(r'\(pin \w+ \(at ([-\d.]+) ([-\d.]+)[^)]*\).*?\(name "([^"]*)"[^)]*\).*?\(number "([^"]*)"', blk, re.S):
        print('   pad %-3s name %-12s at (%s, %s)' % (p.group(4), p.group(3), p.group(1), p.group(2)))
    print('   [from', f, ']')
    break

print('\n=== footprint attribute flags ===')
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')
CHECKS = [('board_only', 'IsBoardOnly'), ('excl_BOM', 'IsExcludedFromBom'),
          ('excl_POS', 'IsExcludedFromPosFiles'), ('not_in_sch', 'IsNotInSchematic'),
          ('in_bom', 'IsInBom'), ('on_board', 'IsOnBoard')]
avail = [(n, m) for n, m in CHECKS if hasattr(pcbnew.FOOTPRINT, m)]
print('   readable flags:', [n for n, _ in avail])
for fp in b.GetFootprints():
    hits = [n for n, m in avail if getattr(fp, m)()]
    odd = [h for h in hits if h in ('board_only', 'excl_BOM', 'excl_POS', 'not_in_sch')]
    if odd:
        print('   %-6s %-30s %s' % (fp.GetReference(), str(fp.GetFPID().GetLibItemName())[:30], ', '.join(hits)))

print('\n=== C8: ESD distance, every connector with signal pins ===')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}
esd_pads = {}
for fp in b.GetFootprints():
    if fp.GetReference().startswith('ESD'):
        for p in fp.Pads():
            if p.GetNetname():
                esd_pads.setdefault(p.GetNetname(), []).append(p.GetPosition())
for ref in sorted([k for k in d if k.startswith('J')], key=lambda x: (len(x), x)):
    fp = d[ref]
    bad, ok, noesd = [], [], []
    for p in fp.Pads():
        n = p.GetNetname()
        if not n or n.startswith('unconnected') or n in ('GND', 'PE', '+5V', '3V3_C',
                                                        '/+5V_SENS', '/3V3_SENS_SW', '+5V_IN', '/+5V_ESP'):
            continue
        cand = esd_pads.get(n)
        if not cand:
            noesd.append(n)
            continue
        m = min((((q.x - p.GetPosition().x) ** 2 + (q.y - p.GetPosition().y) ** 2) ** 0.5 / 1e6
                 for q in cand))
        (ok if m <= 5.0 else bad).append('%s %.1fmm' % (n, m))
    if bad or noesd:
        print('   %-5s over5mm: %-34s no-ESD-part: %s' % (ref, ', '.join(bad) or '-', ', '.join(sorted(set(noesd))) or '-'))
