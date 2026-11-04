import io, re, sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
out = io.open(P + r'\_cto_extract\t55_templates.txt', 'w', encoding='utf-8')
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()

out.write('=== A. MoriShield_Carrier:R symbol definition (pin geometry) ===\n')
j = t.find('(symbol "MoriShield_Carrier:R"')
out.write(t[j:j + 2600] + '\n')

out.write('\n=== B. a full resistor INSTANCE block: R50 ===\n')
i = t.find('(lib_id "MoriShield_Carrier:R")')
while i > 0:
    blk = t[i - 40:i + 3200]
    if '(property "Reference" "R50"' in blk:
        out.write(blk[:3200] + '\n')
        break
    i = t.find('(lib_id "MoriShield_Carrier:R")', i + 10)

out.write('\n=== C. a GND power symbol instance block (nearest one to R50) ===\n')
k = t.find('(lib_id "MoriShield_Carrier:GND")')
blk = t[k - 40:k + 2200]
out.write(blk[:2200] + '\n')

out.write('\n=== D. /E22_M1 copper on the board ===\n')
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
for net in ('/E22_M1',):
    for x in b.GetTracks():
        if x.GetNetname() != net:
            continue
        a, c = x.GetStart(), x.GetEnd()
        if type(x).__name__ == 'PCB_VIA':
            out.write('   VIA (%.2f,%.2f)\n' % (a.x / 1e6, a.y / 1e6))
        else:
            try:
                uu = str(x.GetUuid())
            except Exception:
                try:
                    uu = str(x.m_Uuid)
                except Exception:
                    uu = '?'
            out.write('   SEG (%.2f,%.2f)-(%.2f,%.2f) w %.2f %s uuid %s\n'
                      % (a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6, x.GetWidth() / 1e6,
                         b.GetLayerName(x.GetLayer()), uu))

out.write('\n=== E. an 0603 resistor footprint block to clone (R50) ===\n')
bt = io.open(P + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
i = bt.find('(property "Reference" "R50"')
s = bt.rfind('(footprint ', 0, i)
out.write(bt[s:s + 3000] + '\n')

out.write('\n=== F. how a label attaches: the E22_M1 label block at J6 ===\n')
m = t.find('(label "E22_M1"')
out.write(t[m:m + 700] + '\n')

out.close()
print('written _cto_extract\\t55_templates.txt')
import os
print('size', os.path.getsize(P + r'\_cto_extract\t55_templates.txt'))
