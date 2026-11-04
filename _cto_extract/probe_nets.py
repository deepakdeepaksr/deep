import re

path = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\_cto_extract\net_now.net'
lines = open(path, encoding='utf-8').read().splitlines()

nets = []
cur = None
pending = None
depth = 0
for ln in lines:
    s = ln.strip()
    if s == '(net':
        cur = ['?', []]
        nets.append(cur)
        depth = 0
        pending = None
        continue
    if cur is None:
        continue
    m = re.match(r'^\(name "(.+)"\)$', s)
    if m and cur[0] == '?':
        cur[0] = m.group(1)
        continue
    m = re.match(r'^\(ref "(.+)"\)$', s)
    if m:
        pending = m.group(1)
        continue
    m = re.match(r'^\(pin "(.+)"\)$', s)
    if m and pending:
        cur[1].append((pending, m.group(1)))
        pending = None
        continue

named = [n for n in nets if n[0] != '?']
print('nets:', len(named), 'unnamed:', len(nets) - len(named))


def show(sub):
    hit = False
    for name, nodes in named:
        if sub.upper() in name.upper():
            print('  %-22s %s' % (name, ', '.join('%s.%s' % n for n in nodes)))
            hit = True
    if not hit:
        print('  (none)')


for key in ('I2C1_SDA', 'I2C1_SCL', 'REED', 'PWR_KEY', 'PWR_EN', 'ADC_F', 'STATUS', 'WDT'):
    print('==', key)
    show(key)

print('\n--- every net that touches a connector ---')
for name, nodes in named:
    js = [n for n in nodes if re.match(r'^J\d+$', n[0])]
    if js:
        print('%-24s %s' % (name, ', '.join('%s.%s' % n for n in js)))
