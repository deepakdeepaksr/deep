import sys, re
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')

ds = b.GetDesignSettings()
try:
    ncs = ds.m_NetClasses
    print('netclasses seen by the BOARD:', ncs.GetCount())
    for i in range(ncs.GetCount()):
        c = ncs.Item(i)
        print('   %-16s track %.3f clr %.3f via %.2f/%.2f  nets assigned: %d'
              % (c.GetName(), c.GetTrackWidth() / 1e6, c.GetClearance() / 1e6,
                 c.GetViaDiameter() / 1e6, c.GetViaDrill() / 1e6, c.GetAssignNum()))
except Exception as e:
    print('board netclass enumeration failed:', e)

print('\n=== which class does each power net resolve to? ===')
try:
    ncs = ds.m_NetClasses
    for n in ('+5V_IN', '+5V_F', '+5V', '/+5V_SENS', '/+5V_ESP', '3V3_C', 'GND', 'PE', '/MODEM_RST', 'I2C1_SDA'):
        c = ncs.GetNetClass(n)
        print('   %-12s -> %-16s (min track %.3f)'
              % (n, c.GetName() if c else 'NONE', (c.GetTrackWidth() / 1e6) if c else -1))
except Exception as e:
    print('lookup failed:', e)

print('\n=== top-level (net ...) declarations in the board file ===')
p = open(base + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
m = re.search(r'\n\s*\(net \d+ "GND".{0,160}', p, re.S)
print('  ', repr(m.group(0)) if m else 'no top-level net decl found')
print('   "netclass" token count:', p.count('netclass'))
print('   "net_class" token count:', p.count('net_class'))
