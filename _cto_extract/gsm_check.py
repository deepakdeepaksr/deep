import sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}

print('=== GSM: carrier socket vs the Parry guide ===')
G_J3 = ['PWR_EN', 'MIC_N', 'MIC_P', 'EAR_N', 'EAR_P', 'GND', 'SDA_1V8', 'SCL_1V8',
        'GND', 'GPIO2_1V8', 'ADC', 'GND']
G_J4 = ['PWR_KEY', 'GND', 'VDD_IN_UART', 'A7672_TXD', 'A7672_RXD', 'GND', 'VDD_1V8',
        'A7672_RESET', 'GPIO1_1V8', 'UART_LOG_RX', 'UART_LOG_TX', 'GND']
for ref, guide in (('J3', G_J3), ('J4', G_J4)):
    fp = d[ref]
    print('\n  carrier %s  (%s)' % (ref, str(fp.GetFPID().GetLibItemName())))
    for p in sorted(fp.Pads(), key=lambda x: int(x.GetNumber())):
        i = int(p.GetNumber()) - 1
        nm = p.GetNetname() or '<none>'
        print('    pad %-3s carrier-net %-30s   guide says: %s' % (p.GetNumber(), nm, guide[i]))

print('\n=== who drives the control pins ===')
for net in ('/PWR_EN', '/PWR_KEY', '/MODEM_RST', '/UART2_MOD_RX', '/UART2_MOD_TX'):
    holders = []
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.GetNetname() == net:
                holders.append('%s.%s(%s)' % (fp.GetReference(), p.GetNumber(),
                                              str(fp.GetFPID().GetLibItemName())[:16]))
    print('  %-16s %s' % (net, ', '.join(holders)))
for r in ('R16', 'R15'):
    fp = d.get(r)
    if fp:
        print('  %-4s value %-6s pads: %s' % (r, fp.GetValue(),
              ', '.join('%s=%s' % (p.GetNumber(), p.GetNetname() or '<none>') for p in fp.Pads())))

print('\n=== ESP32 socket, current state ===')
L = ['3V3', '3V3', 'RST', 'IO4', 'IO5', 'IO6', 'IO7', 'IO15', 'IO16', 'IO17', 'IO18',
     'IO8', 'IO3', 'IO46', 'IO9', 'IO10', 'IO11', 'IO12', 'IO13', 'IO14', '5V', 'GND']
R = ['GND', 'IO43', 'IO44', 'IO1', 'IO2', 'IO42', 'IO41', 'IO40', 'IO39', 'IO38', 'IO37',
     'IO36', 'IO35', 'IO0', 'IO45', 'IO48', 'IO47', 'IO21', 'IO20', 'IO19', 'GND', 'GND']
for ref, doc in (('J1', L), ('J2', R)):
    print('\n  %s' % ref)
    for p in sorted(d[ref].Pads(), key=lambda x: int(x.GetNumber())):
        i = int(p.GetNumber()) - 1
        print('    pad %-3s %-8s  %s' % (p.GetNumber(), doc[i], p.GetNetname() or '<none>'))

print('\n=== E22 LoRa header J6 ===')
fp = d.get('J6')
if fp:
    print('  %s' % str(fp.GetFPID().GetLibItemName()))
    for p in sorted(fp.Pads(), key=lambda x: int(x.GetNumber())):
        print('    pad %-3s %s' % (p.GetNumber(), p.GetNetname() or '<none>'))
