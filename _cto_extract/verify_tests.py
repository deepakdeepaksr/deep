import sys, io, re
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}

print('=== A. if the E22 is inserted REVERSED (module pin 1 -> J6 pad 7), does everything line up? ===')
j6 = {p.GetNumber(): p.GetNetname() for p in d['J6'].Pads()}
mod = {1: 'M0', 2: 'M1', 3: 'RXD', 4: 'TXD', 5: 'AUX', 6: 'VCC', 7: 'GND'}
expect_rev = {7: 'M0', 6: 'M1', 5: 'RXD', 4: 'TXD', 3: 'AUX', 2: 'VCC', 1: 'GND'}
expect_std = {1: 'M0', 2: 'M1', 3: 'RXD', 4: 'TXD', 5: 'AUX', 6: 'VCC', 7: 'GND'}
want = {'M0': 'GND-or-M0-net', 'M1': '', 'RXD': '/UART1_LORA_TX', 'TXD': '/UART1_LORA_RX',
        'AUX': '/E22_AUX', 'VCC': '/+5V_E22', 'GND': 'GND'}
for pad in sorted(j6, key=int):
    mpin = 8 - int(pad)          # reversed insertion: module pin N lands on pad 8-N
    print('   pad %s = %-18s | normal insertion -> module pin %s | reversed insertion -> module pin %s (%s)'
          % (pad, j6[pad], pad, mpin, mod[mpin]))

print()
print('=== B. J1 / J2 pin-1 ends (where is the ESP32 antenna end on the carrier?) ===')
for ref in ('J1', 'J2'):
    fp = d[ref]
    pads = {p.GetNumber(): p.GetPosition() for p in fp.Pads()}
    nets = {p.GetNumber(): p.GetNetname() for p in fp.Pads()}
    p1, p22 = pads['1'], pads['22']
    print('   %s pin 1 at (%.2f, %.2f)  pin 22 at (%.2f, %.2f)' % (ref, p1.x / 1e6, p1.y / 1e6, p22.x / 1e6, p22.y / 1e6))
    print('        pin1=%s  pin2=%s  pin3=%s   ...  pin20=%s pin21=%s pin22=%s'
          % (nets['1'], nets['2'], nets['3'], nets['20'], nets['21'], nets['22']))
print('   ESP32 outline: x 180.50-212.50, y 91.50-156.50')
print('   vendor: antenna end has left row 3V3,3V3,RST and right row GND,TX,RX')

print()
print('=== C. what sits UNDER the modem outline (x 228.50-271.50, y 90.50-150.50)? ===')
inside = []
for ref, fp in d.items():
    p = fp.GetPosition()
    x, y = p.x / 1e6, p.y / 1e6
    if 228.50 <= x <= 271.50 and 90.50 <= y <= 150.50:
        h = 0
        try:
            for pad in fp.Pads():
                pass
        except Exception:
            pass
        inside.append((ref, str(fp.GetFPID().GetLibItemName())[:34], fp.GetValue()[:18], x, y))
for t in sorted(inside, key=lambda z: z[0]):
    print('   %-6s %-34s %-18s (%.2f, %.2f)' % t)
print('   count: %d' % len(inside))

print()
print('=== D. I2C channels: which connector is on CH3 and CH6, and are all six real ports? ===')
names = set()
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname():
            names.add(p.GetNetname())
for ch in range(0, 7):
    for kind in ('SDA', 'SCL'):
        net = '/I2C0_%s_CH%d' % (kind, ch)
        members = []
        for fp in b.GetFootprints():
            for p in fp.Pads():
                if p.GetNetname() == net:
                    members.append('%s.%s' % (fp.GetReference(), p.GetNumber()))
        print('   %-18s %s' % (net, ', '.join(members) or '(none)'))
