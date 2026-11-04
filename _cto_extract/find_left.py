import io, re, subprocess

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

for f in ('TASK_TRACKER.md', 'REPLY_TO_CTO.md'):
    p = P + '\\' + f
    t = io.open(p, encoding='utf-8').read()
    L = t.split('\n')
    for n, l in enumerate(L):
        if 'unchanged from Rev B' in l:
            print('%s line %d: %s' % (f, n + 1, l[:300]))
        if '| **New** |' in l:
            print('%s line %d BOLD-NEW: %s' % (f, n + 1, l[:200]))
    print()
