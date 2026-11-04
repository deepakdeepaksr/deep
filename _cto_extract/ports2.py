import sys, re
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}

print('=== J2 pad names (the GPIO is inside the pad name) and their nets ===')
for p in sorted(d['J2'].Pads(), key=lambda x: int(x.GetNumber())):
    print('   J2.%-3s name=%-16s net=%s' % (p.GetNumber(), p.GetName(), p.GetNetname() or 'none'))

print()
print('=== J1 pad names for the pins carrying signals ===')
for p in sorted(d['J1'].Pads(), key=lambda x: int(x.GetNumber())):
    n = p.GetNetname() or 'none'
    if not n.startswith('unconnected'):
        print('   J1.%-3s name=%-14s net=%s' % (p.GetNumber(), p.GetName(), n))

print()
print('=== connectors J19 to J26 ===')
for ref in ('J19', 'J20', 'J21', 'J22', 'J23', 'J24', 'J25', 'J26'):
    fp = d.get(ref)
    if not fp:
        print('   %s ABSENT' % ref)
        continue
    p = fp.GetPosition()
    pads = sorted(fp.Pads(), key=lambda x: int(x.GetNumber()) if x.GetNumber().isdigit() else 0)
    print('   %-4s %-42s (%7.2f,%7.2f)' % (ref, str(fp.GetFPID().GetLibItemName())[:42], p.x / 1e6, p.y / 1e6))
    print('        %s' % ', '.join('%s:%s(%s)' % (x.GetNumber(), x.GetName(), x.GetNetname() or 'none') for x in pads))

print()
print('=== ESP32-S3 ADC channel map applied to what we use ===')
adc1 = set(range(1, 11))
adc2 = set(range(11, 21))
used = {}
for ref in ('J1', 'J2'):
    for p in d[ref].Pads():
        nm = p.GetName() or ''
        m = re.search(r'IO(\d+)', nm)
        net = p.GetNetname() or ''
        if m and net and not net.startswith('unconnected'):
            used[int(m.group(1))] = (ref + '.' + p.GetNumber(), net)
for g in sorted(used):
    tag = 'ADC1 (works with Wi-Fi)' if g in adc1 else ('ADC2 (UNUSABLE with Wi-Fi on)' if g in adc2 else '')
    if 'ADC' in used[g][1].upper() or tag:
        print('   GPIO%-3s %-10s %-18s %s' % (g, used[g][0], used[g][1], tag))
