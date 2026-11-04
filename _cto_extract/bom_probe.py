import re, sys, json, os

path = sys.argv[1]
txt = open(path, encoding='utf-8', errors='replace').read()

# Find top-level footprint blocks by scanning for "(footprint \"" and tracking paren depth
blocks = []
i = 0
n = len(txt)
while True:
    m = re.compile(r'\(footprint "([^"]+)"').search(txt, i)
    if not m:
        break
    start = m.start()
    # walk forward to matching paren
    depth = 0
    j = start
    in_str = False
    esc = False
    while j < n:
        c = txt[j]
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
    blocks.append((m.group(1), txt[start:j+1]))
    i = j + 1

rows = []
for fp, body in blocks:
    ref = re.search(r'\(property "Reference" "([^"]*)"', body)
    val = re.search(r'\(property "Value" "([^"]*)"', body)
    mpn = re.search(r'\(property "MPN" "([^"]*)"', body)
    foot = re.search(r'\(property "Footprint" "([^"]*)"', body)
    rows.append((ref.group(1) if ref else '?', fp, val.group(1) if val else '', mpn.group(1) if mpn else ''))

def key(r):
    m = re.match(r'([A-Za-z]+)(\d+)', r[0])
    return (m.group(1), int(m.group(2))) if m else ('ZZZ', 0)

rows.sort(key=key)
for r in rows:
    print('%-6s | %-70s | %s' % (r[0], r[1], r[2]))
print('TOTAL', len(rows))
