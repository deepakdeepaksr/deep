import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()

print('=== every place the schematic names a sensor ===')
seen = set()
for m in re.finditer(r'(FDC1004|FDC|AS5600|WIND|REED|SOIL|MPU|GY521|DS3231)', t):
    s = t[max(0, m.start() - 70):m.start() + 110].replace('\n', ' ')
    key = s[:60]
    if key in seen:
        continue
    seen.add(key)
    print('   %r' % s[:170])

print()
print('=== symbol instance: pair each lib_id with the Reference that follows it ===')
ids = [(m.start(), m.group(1)) for m in re.finditer(r'\(lib_id "([^"]+)"', t)]
refs = [(m.start(), m.group(1)) for m in re.finditer(r'\(property "Reference" "([^"]+)"', t)]
pairs = {}
for rpos, ref in refs:
    cand = [i for i, p in ids if i < rpos]
    if cand:
        pairs[ref] = max(cand)  # nearest preceding lib_id
want = ('J6', 'J7', 'J8', 'J15', 'J16', 'J22', 'J23', 'J26', 'J11', 'J12', 'J13',
        'J14', 'J17', 'J20', 'J21', 'J24', 'J25')
for ref in want:
    pos = pairs.get(ref)
    if pos is None:
        print('   %-4s not found' % ref)
        continue
    lib = [g for i, g in ids if i == pos][0]
    seg = t[pos:pos + 1200]
    val = re.search(r'\(property "Value" "([^"]*)"', seg)
    print('   %-4s lib_id=%-34s Value=%s' % (ref, lib, (val.group(1) if val else '?')[:26]))

print()
print('=== pin names inside those symbol definitions (from the embedded cache) ===')
for sym in ('JST_XH_2', 'JST_XH_3', 'JST_XH_4', 'JST_XH_5', 'Conn_01x08', 'Conn_01x06', 'Conn_01x07'):
    j = t.find('(symbol "%s"' % sym)
    if j < 0:
        continue
    blk = t[j:j + 4000]
    pins = re.findall(r'\(name "([^"]*)"', blk)
    print('   %-12s %s' % (sym, [p for p in pins if p][:10]))
