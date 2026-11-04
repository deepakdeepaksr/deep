import io, re, subprocess

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# 1. status cell must be the plain vocabulary word, not bold
p = P + r'\TASK_TRACKER.md'
t = io.open(p, encoding='utf-8').read()
t = t.replace('(antenna keep-out excepted)." | **New** |', '(antenna keep-out excepted)." | New |')
# 2. "unchanged from Rev B" is no longer true at 67
t = t.replace('**67 of 314 vias sit inside an SMD pad** - re-measured today, unchanged from Rev B.',
              '**67 of 314 vias sit inside an SMD pad** - Rev B quoted 65; the 2026-11-03 reroutes added two more.')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('TASK_TRACKER: status word cleaned:', '(antenna keep-out excepted)." | New |' in t)

p = P + r'\REPLY_TO_CTO.md'
t = io.open(p, encoding='utf-8').read()
t = t.replace('**67 of 314 vias sit inside an SMD pad** - re-measured this round, unchanged from Rev B.',
              '**67 of 314 vias sit inside an SMD pad** - Rev B quoted 65; two more were introduced by the '
              '2026-11-03 reroutes, so the count is rising, not static.')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('REPLY: R16 sentence corrected:', 'unchanged from Rev B' not in t)

# 3. regenerate the CSV and re-verify
r = subprocess.run(['python', P + r'\pcb\_make_response_sheet.py'], capture_output=True, text=True, cwd=P)
print('CSV:', (r.stdout or r.stderr).strip().replace('\n', ' | ')[:160])
r2 = subprocess.run(['python', P + r'\_cto_extract\trace2.py'], capture_output=True, text=True, cwd=P)
for l in r2.stdout.split('\n')[:6]:
    print('  ', l)
