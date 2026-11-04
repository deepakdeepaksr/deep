import io

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\REPLY_TO_CTO.md'
L = io.open(p, encoding='utf-8').read().split('\n')

i3 = next(n for n, l in enumerate(L) if l.startswith('## 3.'))
fixed = 0
for n in range(i3, len(L)):
    if L[n].startswith('| A7 | **Settled by measurement'):
        L[n] = '| A7 | Aswin is the single contact and signs the reply | 31 Oct | Signatory |'
        fixed += 1
        print('restored §3 A7 at line', n + 1)
io.open(p, 'w', encoding='utf-8', newline='').write('\n'.join(L))
print('restored rows:', fixed)

t = '\n'.join(L)
print()
print('=== question block order in section 4 ===')
i4 = t.find('## 4.')
seg = t[i4:t.find('## 5.')]
import re
for l in seg.split('\n'):
    if re.match(r'^\s*\d{1,2}[a-z]?\.\s+\*\*', l):
        print('   ', l[:96].encode('ascii', 'replace').decode())
