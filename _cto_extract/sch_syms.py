import re, sys

p = sys.argv[1]
t = open(p, encoding='utf-8', errors='replace').read()

# split into symbol instances blocks
i = 0
out = []
for m in re.finditer(r'\(symbol\b', t):
    start = m.start()
    depth = 0
    j = start
    in_str = False
    esc = False
    n = len(t)
    while j < n:
        c = t[j]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    break
        j += 1
    body = t[start:j+1]
    ref = re.search(r'\(property "Reference" "([^"]*)"', body)
    val = re.search(r'\(property "Value" "([^"]*)"', body)
    lib = re.search(r'\(lib_id "([^"]*)"', body)
    if ref and ref.group(1) not in ('#PWR', '#FLG'):
        out.append((ref.group(1), val.group(1) if val else '', lib.group(1) if lib else ''))
    i = j + 1

def key(r):
    m = re.match(r'([A-Za-z#]+)(\d+)', r[0])
    return (m.group(1), int(m.group(2))) if m else ('ZZ', 0)

for r in sorted(set(out), key=key):
    print('%-6s %-28s %s' % (r[0], r[1], r[2]))
