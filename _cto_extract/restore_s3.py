import io, re, glob, os

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
cur = io.open(P + r'\REPLY_TO_CTO.md', encoding='utf-8').read().split('\n')
bak = sorted(glob.glob(P + r'\_cto_extract\REPLY.bak2-*'))[-1]
old = io.open(bak, encoding='utf-8').read().split('\n')
print('using backup', os.path.basename(bak))

i3 = next(n for n, l in enumerate(cur) if l.startswith('## 3.'))
i4 = next(n for n, l in enumerate(cur) if l.startswith('## 4.'))

# rebuild the §3 table from the backup: match rows by their id
old3 = {}
j3 = next(n for n, l in enumerate(old) if l.startswith('## 3.'))
j4 = next(n for n, l in enumerate(old) if l.startswith('## 4.'))
for l in old[j3:j4]:
    m = re.match(r'^\|\s*([A-Z]\w*)\s*\|', l)
    if m:
        old3[m.group(1)] = l

restored = []
for n in range(i3, i4):
    m = re.match(r'^\|\s*([A-Z]\w*)\s*\|', cur[n])
    if not m:
        continue
    key = m.group(1)
    if key in old3 and cur[n] != old3[key]:
        print('  §3 %s was overwritten with response-sheet text -> restored' % key)
        print('     now : %s' % cur[n][:110])
        cur[n] = old3[key]
        restored.append(key)

# align the C5 status word with the register (Partly, not Open)
for n, l in enumerate(cur):
    if l.startswith('| C5 | M0 and M1 are on separate pins') and l.rstrip().endswith('not yet in the files |'):
        cur[n] = l.replace('| Open - fix not yet in the files |',
                           '| Partly - separate-pin half is in the file, the strap is not |')
        print('  C5 status aligned to Partly')

io.open(P + r'\REPLY_TO_CTO.md', 'w', encoding='utf-8', newline='').write('\n'.join(cur))
print('restored rows:', restored)
