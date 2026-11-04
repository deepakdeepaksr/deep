import io, re, json, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
d = json.load(open(P + r'\pcb\MoriShield_Carrier.kicad_pro', encoding='utf-8'))
erc = d['erc']
print('=== erc section keys ===')
print(sorted(erc.keys()))
sev = erc.get('severities', {})
print('\n=== ERC severities set to "ignore" or unusual ===')
for k, v in sorted(sev.items()) if isinstance(sev, dict) else []:
    if v not in (0, 'error', 'warning'):
        print('   %-40s %s' % (k, v))
print('   raw:', json.dumps(sev)[:900])
print('\n=== erc exclusions / unconnected ===')
for k in erc:
    v = erc[k]
    if isinstance(v, list):
        print('   %-30s list len %d  %s' % (k, len(v), json.dumps(v)[:200]))

t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()
print('\n=== schematic suppression markers ===')
print('   (ignore ...) tokens :', len(re.findall(r'\(ignore ', t)))
print('   Counter             :', dict(collections.Counter(re.findall(r'\(ignore ([a-z_]+)', t))))
print('   no_connect          :', len(re.findall(r'no_connect', t)))
print('   unconnected type    :', len(re.findall(r'\(type\s+"unconnected"', t)))
print('   global labels       :', len(re.findall(r'\(global_label', t)))
print('   hierarchical labels :', len(re.findall(r'\(hierarchical_label', t)))
