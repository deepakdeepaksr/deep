import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
for f in ('TASK_TRACKER.md', 'REPLY_TO_CTO.md', 'STAGE_TRACKER.md', 'PROJECT_CONTEXT_RevC.md'):
    t = io.open(P + '\\' + f, encoding='utf-8').read()
    print('=== %s ===  mirror:%d  "not mis-wired":%d  180-degree:%d'
          % (f, t.lower().count('mirror'), t.lower().count('not mis-wired'), t.count('180-degree')))
    for l in t.splitlines():
        if 'mirror' in l.lower():
            print('    |', l[:170])
    print()

print('=== A7 / C2 / R11 rows in the reply now ===')
t = io.open(P + r'\REPLY_TO_CTO.md', encoding='utf-8').read()
for l in t.splitlines():
    if re.match(r'^\|\s*(A7|C2|R11|C5)\s*\|', l):
        print('   ', l[:180])
