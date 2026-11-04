import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()

print('=== sensor words present anywhere in the schematic ===')
for w in ('REED', 'AS5600', 'MPU', 'GY-521', 'SOIL', 'FDC', 'CAPACIT', 'WIND',
          'DS3231', 'BME', 'SGP', 'SHT', 'SPS30', 'BUZZER', 'LED'):
    print('   %-10s %d' % (w, len(re.findall(re.escape(w), t, re.I))))

print()
print('=== each port: Reference / Value / lib_id / pin names ===')
blocks = re.split(r'\n\t\t\(symbol ', t)
for ref in ('J6', 'J7', 'J8', 'J15', 'J16', 'J22', 'J23', 'J26', 'J11', 'J14', 'J20'):
    hit = None
    for bl in blocks:
        if re.search(r'\(property "Reference" "%s"' % ref, bl):
            hit = bl
            break
    if hit is None:
        print('   %-4s NOT FOUND as a symbol instance' % ref)
        continue
    lib = re.search(r'\(lib_id "([^"]+)"', hit)
    val = re.search(r'\(property "Value" "([^"]*)"', hit)
    pins = re.findall(r'\(name "([^"]*)"[^)]*\)\s*\(number "(\d+)"', hit)
    if not pins:
        pins = re.findall(r'\(name "([^"]*)"', hit)
    print('   %-4s lib_id=%-26s Value=%-18s' % (ref, (lib.group(1) if lib else '?')[:26],
                                                (val.group(1) if val else '?')[:18]))
    print('        pin names: %s' % str(pins[:10])[:150])
