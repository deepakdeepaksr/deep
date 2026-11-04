import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# ---- 1. mark questions 3 and 5 as answered by our own measurement ----
p = P + r'\REPLY_TO_CTO.md'
t = io.open(p, encoding='utf-8').read()
t = t.replace(
 '3. **microSD versus GPIO10/11 (A7, C2, C5, R11).**',
 '3. **microSD versus GPIO10/11 (A7, C2, C5, R11) - ANSWERED BY US 2026-11-02, kept for the '
 'record; see 8b for the correction we are asking you to make.**')
t = t.replace(
 '5. **The reed on GPIO41 (R11).**',
 '5. **The reed on GPIO41 (R11) - CLOSED BY US 2026-11-02, we are moving it to GPIO39.**')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('questions 3 and 5 annotated')

# ---- 2. show STAGE_TRACKER rows so the stale ones can be corrected ----
L = io.open(P + r'\STAGE_TRACKER.md', encoding='utf-8').read().split('\n')
print()
print('=== STAGE_TRACKER table rows ===')
for n, l in enumerate(L, 1):
    if l.startswith('|') and n < 60:
        print('%3d| %s' % (n, l[:150].encode('ascii', 'replace').decode()))
