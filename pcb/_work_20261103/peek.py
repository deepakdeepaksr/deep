import json
import re

s = open(r'pcb/MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
i = s.find('(via')
print(repr(s[i:i + 260]))
j = s.find('(segment')
print(repr(s[j:j + 300]))
k = s.find('(footprint "JST_XH_4"')
print(repr(s[k:k + 900]))
