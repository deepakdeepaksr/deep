import sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}

print('=== J6 (the E22 LoRa socket) as the board actually has it ===')
fp = d.get('J6')
if fp:
    print('   J6', str(fp.GetFPID().GetLibItemName()), 'at %.2f,%.2f rot %.1f'
          % (fp.GetPosition().x / 1e6, fp.GetPosition().y / 1e6, fp.GetOrientationDegrees()))
    for p in sorted(fp.Pads(), key=lambda x: int(x.GetNumber())):
        pp = p.GetPosition()
        print('   pad %-3s name=%-6s net=%-16s at %.2f,%.2f'
              % (p.GetNumber(), p.GetName(), p.GetNetname() or '-', pp.x / 1e6, pp.y / 1e6))

print()
print('=== every E22 net and who is on it ===')
for n in ('/E22_M0', '/E22_M1', '/E22_AUX', '/E22_EN', '/E22_EN_G', '/E22_GATE',
          '/+5V_E22', '/+5V_E22_IN', '/UART1_LORA_TX', '/UART1_LORA_RX'):
    members = []
    for f in b.GetFootprints():
        for p in f.Pads():
            if p.GetNetname() == n:
                members.append('%s.%s' % (f.GetReference(), p.GetNumber()))
    print('   %-16s %s' % (n, ', '.join(members) or '(no pads on this net)'))

print()
print('=== ESP32 socket pins carrying GPIO10 / GPIO11 (the M1/M0 question) ===')
for ref, pads in (('J1', ('15', '16', '17', '18', '19', '20', '9', '12', '13', '14')),):
    for p in sorted(d[ref].Pads(), key=lambda x: int(x.GetNumber())):
        if p.GetNumber() in pads:
            print('   %s pad %-3s net=%s' % (ref, p.GetNumber(), p.GetNetname() or 'UNCONNECTED'))

print()
print('=== test points: net, position, purpose readable from the net name ===')
for ref in sorted([k for k in d if k.startswith('TP')], key=lambda x: int(x[2:])):
    fp = d[ref]
    p = list(fp.Pads())[0]
    print('   %-5s net=%-22s at %7.2f,%7.2f  excl_pos=%s'
          % (ref, p.GetNetname() or '-', fp.GetPosition().x / 1e6, fp.GetPosition().y / 1e6,
             fp.IsExcludedFromPosFiles()))

print()
print('=== E22 module outline vs the board edge (where the SMA points) ===')
for it in b.GetDrawings():
    if type(it).__name__ == 'PCB_TEXT':
        s = it.GetText()
        if 'E22' in s or 'SMA' in s or 'LoRa' in s or 'LORA' in s:
            print('   text %-34r at %.2f,%.2f' % (s, it.GetPosition().x / 1e6, it.GetPosition().y / 1e6))
