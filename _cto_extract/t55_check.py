import io, re, sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
bt = io.open(P + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
st = io.open(P + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()

print('=== 1. strap net names: board vs schematic ===')
print('   board net declarations :', sorted(set(re.findall(r'\(net \d+ "([^"]*STRAP[^"]*)"', bt))))
print('   schematic label texts  :', sorted(set(re.findall(r'\(label "([^"]*STRAP[^"]*)"', st))))
print('   old nets still present :', bt.count('/E22_M1'), bt.count('/E22_M0'),
      '| board mentions of bare E22_M1_STRAP:', bt.count('E22_M1_STRAP'))
print('   how OTHER local-label nets are named on the board:',
      sorted(set(re.findall(r'\(net \d+ "(/E22_[A-Z]+)"', bt)))[:4])

print()
print('=== 2. R56 / R57 on the board: pads and nets ===')
for ref in ('R56', 'R57'):
    i = bt.find('(property "Reference" "%s"' % ref)
    if i < 0:
        print('   %s missing' % ref)
        continue
    s = bt.rfind('(footprint ', 0, i)
    blk = bt[s:s + 2200]
    at = re.search(r'\(footprint "[^"]*"\s*\(layer "([^"]+)"\)\s*\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)', blk)
    print('   %s lib=%s at %s' % (ref, re.search(r'\(footprint "([^"]+)"', blk).group(1), at.groups()[1:] if at else '?'))
    for m in re.finditer(r'\(pad "(\d)" smd roundrect\s*\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)\)\s*\(size ([\d.]+) ([\d.]+)\).*?\(net \d+ "([^"]*)"\)', blk, re.S):
        print('       pad %s offset (%s, %s) rot %s size %sx%s net=%s' % m.groups())

print()
print('=== 3. the two new GND vias ===')
for m in re.finditer(r'\(via \(at ([\d.\-]+) ([\d.\-]+)\)(.{0,300}?)\(net \d+ "([^"]*)"\)', bt, re.S):
    x, y = float(m.group(1)), float(m.group(2))
    if 266 < x < 270 and 160 < y < 167 and 'STRAP' in m.group(4) or ('GND' == m.group(4) and 266 < x < 270 and 160 < y < 167):
        print('   via (%.3f, %.3f) net=%s' % (x, y, m.group(4)))

print()
print('=== 4. T-56 reconnaissance: J2 instance and the REED label ===')
i = st.find('(property "Reference" "J2"')
s = st.rfind('(lib_id "', 0, i)
print('   J2 lib_id:', re.search(r'\(lib_id "([^"]+)"', st[s:s + 120]).group(1))
blk = st[s:s + 400]
print('   J2 instance at:', re.findall(r'\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)\)', blk)[:2])
for m in re.finditer(r'\(label "(REED_PULSE_F|STATUS_LED)"', st):
    seg = st[m.start():m.start() + 260]
    at = re.search(r'\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)', seg)
    print('   label %-14s at (%s, %s) rot %s' % (m.group(1), at.group(1), at.group(2), at.group(3)))
print('   J2 pin count in lib_symbols:',
      len(re.findall(r'\(pin "?\d+"? ', st[st.find('(symbol "MoriShield_Carrier:Sock_1x22_R"'):st.find('(symbol "MoriShield_Carrier:Sock_1x22_R"') + 9000])))
