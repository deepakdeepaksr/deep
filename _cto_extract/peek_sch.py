import io, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCH = os.path.join(ROOT, 'pcb', 'MoriShield_Carrier.kicad_sch')
s = io.open(SCH, encoding='utf-8').read()

print('=== Find symbols in entire schematic with Reference ===')
for m in re.finditer(r'\(property "Reference" "([^"]+)"\s+\(at ([\d\.]+) ([\d\.]+) [^\)]+\)', s):
    ref, x, y = m.group(1), float(m.group(2)), float(m.group(3))
    if 890 <= x <= 960 and 270 <= y <= 320:
        print(f'{ref} at ({x}, {y})')















