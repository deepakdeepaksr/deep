import re, sys

p = sys.argv[1]
t = open(p, encoding='utf-8', errors='replace').read()
vals = set()
for m in re.finditer(r'\((?:gr_text|fp_text) "([^"]{2,40})"', t):
    vals.add(m.group(1))
for v in sorted(vals):
    print(v)
