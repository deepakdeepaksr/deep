import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()

print('=== 1. where are the /E22_M0 and /E22_M1 labels? ===')
for m in re.finditer(r'\(label "/E22_M[01]"', t):
    seg = t[m.start():m.start() + 420]
    at = re.search(r'\(at ([\d.]+) ([\d.]+) ([\d.]+)', seg)
    uuid = re.search(r'\(uuid "([^"]+)"', seg)
    print('   at %s rot %s  uuid %s' % (at.groups()[:2], at.group(3), uuid.group(1)[:8] if uuid else '?'))

print()
print('=== 2. the J6 symbol instance: position and pin count ===')
i = t.find('(property "Reference" "J6"')
seg = t[max(0, i - 2200):i + 900]
lib = re.search(r'\(lib_id "([^"]+)"', seg)
at = re.search(r'\(lib_id "[^"]+"\)\n\s*\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)', seg)
inst = re.search(r'\(instances\)(.*?)\(symbol_instances\)', t, re.S)
print('   lib_id:', lib.group(1) if lib else '?')
print('   at:', at.groups() if at else '?')
m = re.search(r'\(path "([^"]+)"\)\s*\n\s*\(reference "J6"\)', t)
print('   instance path:', m.group(1) if m else '?')

print()
print('=== 3. wires near those labels (are there stubs?) ===')
for lbl in ('/E22_M0', '/E22_M1'):
    for m in re.finditer(r'\(label "%s"' % lbl, t):
        seg = t[m.start():m.start() + 400]
        at = re.search(r'\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)', seg)
        if at:
            x, y = float(at.group(1)), float(at.group(2))
            print('   %s label at (%.2f, %.2f)' % (lbl, x, y))

# find wire segments whose endpoint matches a label position
print()
print('=== 4. all wires within 6 mm of (label positions) ===')
wires = []
for m in re.finditer(r'\(wire \(pts \(xy ([\d.\-]+) ([\d.\-]+)\) \(xy ([\d.\-]+) ([\d.\-]+)\)\)', t):
    x1, y1, x2, y2 = map(float, m.groups())
    wires.append((x1, y1, x2, y2))
print('   total wires in schematic:', len(wires))
for (lx, ly) in [(None, None)]:
    pass
for lbl in ('/E22_M0', '/E22_M1'):
    for m in re.finditer(r'\(label "%s"' % lbl, t):
        seg = t[m.start():m.start() + 400]
        at = re.search(r'\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)', seg)
        x, y = float(at.group(1)), float(at.group(2))
        near = [w for w in wires if min(abs(w[0] - x) + abs(w[1] - y), abs(w[2] - x) + abs(w[3] - y)) < 6]
        print('   near %s: %d wire(s)' % (lbl, len(near)))
        for w in near[:4]:
            print('       (%.2f,%.2f)-(%.2f,%.2f)' % w)

print()
print('=== 5. a template resistor instance to clone (R50) and its lib_symbols ===')
i = t.find('(property "Reference" "R50"')
print('   R50 instance found:', i > 0)
blk = t[max(0, i - 2600):i + 1400]
print('   lib_id:', re.findall(r'\(lib_id "([^"]+)"', blk)[-3:])
print('   at:', re.findall(r'\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)\)', blk)[:3])
print('   path/ref:', re.findall(r'\(path "([^"]+)"\)', blk)[:2], re.findall(r'\(reference "([^"]+)"', blk)[:2])
print()
print('   designators in use, R series:', sorted({m.group(1) for m in re.finditer(r'\(property "Reference" "(R\d+)"', t)}, key=lambda s: int(s[1:]))[-6:])
print('   highest R number:', max(int(m.group(1)[1:]) for m in re.finditer(r'\(property "Reference" "(R\d+)"', t)))
