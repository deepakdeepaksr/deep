import re

s = open(r'pcb/MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
for m in re.finditer(r'\(footprint "([^"]+)"', s):
    if 'XH_4' in m.group(1):
        print(m.start(), m.group(1))
i = s.find('J26')
print(repr(s[i - 400:i + 500]))
