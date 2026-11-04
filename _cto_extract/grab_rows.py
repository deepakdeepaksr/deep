import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
L = io.open(P + r'\TASK_TRACKER.md', encoding='utf-8').read().splitlines()

print('=== FULL rows to correct ===')
for l in L:
    if re.match(r'^\|\s*(A7|C2|C5|R11)\s*\|\s*P', l):
        print(l)
        print('---')

i = next(n for n, l in enumerate(L) if l.startswith('## Part 6'))
j = next(n for n, l in enumerate(L) if l.startswith('## Part 7'))
print()
print('=== Part 6 finding numbers and first 90 chars ===')
for n in range(i, j):
    l = L[n]
    if re.match(r'^\d{1,2}\. ', l):
        print('%4d| %s' % (n + 1, l[:110]))
print()
print('=== any line containing mirror / J6 / E22 in Part 6 ===')
for n in range(i, j):
    if re.search(r'mirror|J6|E22|Ebyte|E22', L[n], re.I):
        print('%4d| %s' % (n + 1, L[n][:240]))
