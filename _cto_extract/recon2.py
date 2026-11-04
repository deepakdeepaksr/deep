import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()

print('=== raw counts ===')
for tok in ('(wire ', '(label ', '(global_label ', '(hierarchical_label ', '(junction ', '(no_connect ', '(symbol "'):
    print('   %-24s %d' % (tok, t.count(tok)))

print()
print('=== every line mentioning E22_M ===')
for n, l in enumerate(t.splitlines(), 1):
    if 'E22_M' in l:
        print('   %5d| %s' % (n, l.strip()[:150]))

print()
print('=== the J6 instance block (from its lib_id to its closing) ===')
i = t.find('(reference "J6")')
print('   symbol_instances reference found at', i)
j = t.find('(lib_id "MoriShield_Carrier:Sock_1x07")')
print('   Sock_1x07 instance at', j)
if j > 0:
    blk = t[j:j + 3000]
    at = re.search(r'\(at ([\d.\-]+) ([\d.\-]+) ([\d.]+)', blk)
    print('   instance at:', at.groups() if at else '?')
    pins = re.findall(r'\(pin "(\d+)"', blk)
    print('   pins:', pins[:10])
    m = re.search(r'\(instances\)(.*?)\n\t\t\)', blk, re.S)
    print('   instances block:', (m.group(1).strip()[:200] if m else 'not in this window'))
