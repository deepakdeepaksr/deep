import io, subprocess

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
REPL = [
    ('re-measured today, unchanged from Rev B.',
     're-measured 2026-11-03: Rev B quoted 65, and two more appeared in the reroutes.'),
    ('re-measured this round, unchanged from Rev B.',
     're-measured 2026-11-03: Rev B quoted 65, and two more appeared in the reroutes.'),
    ('rather than 65 routing changes', 'rather than 67 routing changes'),
]
for f in ('TASK_TRACKER.md', 'REPLY_TO_CTO.md'):
    p = P + '\\' + f
    t = io.open(p, encoding='utf-8').read()
    n = 0
    for a, b in REPL:
        if a in t:
            t = t.replace(a, b)
            n += 1
    io.open(p, 'w', encoding='utf-8', newline='').write(t)
    print('%-20s replacements: %d   "unchanged from Rev B" left: %d'
          % (f, n, t.count('unchanged from Rev B')))

r = subprocess.run(['python', P + r'\pcb\_make_response_sheet.py'], capture_output=True, text=True, cwd=P)
print('CSV:', (r.stdout or r.stderr).strip().replace('\n', ' | ')[:120])
r2 = subprocess.run(['python', P + r'\_cto_extract\trace2.py'], capture_output=True, text=True, cwd=P)
print(r2.stdout[:260])
r3 = subprocess.run(['python', P + r'\_cto_extract\final_verify.py'], capture_output=True, text=True, cwd=P)
for l in r3.stdout.split('\n'):
    if any(k in l for k in ('prototype', 'item rows', 'Part 6 findings', 'missing', 'ids unique', 'required')):
        print('  ', l.strip()[:120])
