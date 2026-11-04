import re
s = open(r'pcb/MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
i = s.find('"MoriShield Carrier"')
j = s.rfind('(gr_text', 0, i)
print(repr(s[j:j + 400]))
i2 = s.find('"Rev C"')
j2 = s.rfind('(gr_text', 0, i2)
print(repr(s[j2:j2 + 300]))
