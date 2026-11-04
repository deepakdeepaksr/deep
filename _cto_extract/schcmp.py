import re

for f in (r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\4L\MoriShield_Carrier.kicad_sch',
          r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_sch'):
    t = open(f, encoding='utf-8').read()
    fp = re.findall(r'\(property "Footprint" "([^"]*)"', t)
    nonempty = [x for x in fp if x.strip()]
    print(f.rsplit('\\', 2)[-2])
    print('   bytes              :', len(t))
    print('   Footprint props    :', len(fp), ' non-empty:', len(nonempty), ' empty:', len(fp) - len(nonempty))
    print('   lib_symbols cache  :', len(re.findall(r'^\t\(lib_symbols', t, re.M)),
          ' symbol defs:', len(re.findall(r'^\t\t\(symbol "', t, re.M)))
    print('   instances          :', len(re.findall(r'\(property "Reference"', t)))
    print('   uuid / at lines    :', len(re.findall(r'\(uuid ', t)))
    print('   no_connect         :', len(re.findall(r'no_connect', t)))
    print('   MoriShield_Carrier lib ids:', len(re.findall(r'MoriShield_Carrier:', t)))
