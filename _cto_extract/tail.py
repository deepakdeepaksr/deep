import re

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

print('--- raw text items near J18 ---')
p = open(base + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
for m in re.finditer(r'\((gr_text|fp_text)\s+"?([^"\s)]*)"?\s+\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', p):
    x, y = float(m.group(3)), float(m.group(4))
    if 120 < x < 142 and 94 < y < 115:
        seg = p[m.start():m.start() + 620]
        lay = re.search(r'\(layer "([^"]+)"', seg)
        ren = re.search(r'\(render "([^"]+)"', seg)
        sz = re.search(r'\(size ([-\d.]+) ([-\d.]+)', seg)
        th = re.search(r'\(thickness ([-\d.]+)', seg)
        print('  %-8s %-9s at %8.3f %8.3f rot %-6s layer=%-18s render=%-7s size=%s thick=%s'
              % (m.group(1), repr(m.group(2)), x, y, m.group(5),
                 lay.group(1) if lay else '?', ren.group(1) if ren else 'stroke',
                 sz.groups() if sz else '?', th.group(1) if th else '?'))

print('\n--- work done ---')
t = open(base + r'\work done', encoding='utf-8').read()
print('  chars', len(t))
for l in t.splitlines():
    s = l.strip()
    if s.lower().startswith('milestone') or re.match(r'^[0-9]{1,2}[.)]\s+\S', s):
        print('  HEAD:', s[:95])
print('  contains "40":', '40 m' in t, '| "66":', '66 m' in t, '| mohm tokens:', len(re.findall(r'm\W{0,2}hm|mOhm|mΩ', t, re.I)))
print('\n  --- last 1100 chars ---')
print(t[-1100:])
