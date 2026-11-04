import io, os, re

src = os.path.join(os.environ['TEMP'], 'e22_manual.txt')
t = io.open(src, encoding='utf-8', errors='ignore').read()
print('chars', len(t))

hits = [m.start() for m in re.finditer(r'M0\s*=\s*[01]', t)]
print('M0 = occurrences:', len(hits), hits[:12])
for h in hits[:8]:
    print('---', repr(t[h - 90:h + 120]))

print()
print('=== section headings containing "mode" ===')
for m in re.finditer(r'6\.\d[^\n]{0,60}', t):
    print('   ', repr(m.group(0)))
