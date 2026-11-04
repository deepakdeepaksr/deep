import io, re, subprocess

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

for f in ('TASK_TRACKER.md', 'REPLY_TO_CTO.md'):
    t = io.open(P + '\\' + f, encoding='utf-8').read()
    print('--', f)
    print('   "unchanged from Rev B" left :', t.count('unchanged from Rev B'))
    print('   bold "**New**" status left  :', t.count('| **New** |'))
    for l in t.splitlines():
        if re.match(r'^\|\s*E1\s*\|', l) and '004 T9' in l:
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            print('   E1 status cell:', repr(c[4]) if len(c) > 4 else '?')
        if re.match(r'^\|\s*E1\s*\|', l) and '004 T9' not in l and len(l) < 400:
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if len(c) == 4:
                print('   E1 reply status:', repr(c[3])[:60])

r = subprocess.run(['python', P + r'\_cto_extract\trace2.py'], capture_output=True, text=True, cwd=P)
print()
for l in r.stdout.split('\n')[:7]:
    print('  ', l)
