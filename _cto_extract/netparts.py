import re, sys

p = sys.argv[1]
t = open(p, encoding='utf-8', errors='replace').read()
nets = set(sys.argv[2].split(','))

i = 0
n = len(t)
pat = re.compile(r'\(footprint "')
while True:
    m = pat.search(t, i)
    if not m:
        break
    start = m.start()
    depth = 0
    j = start
    in_str = False
    esc = False
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
    i = j + 1
    ref = re.search(r'\(property "Reference" "([^"]*)"', body)
    val = re.search(r'\(property "Value" "([^"]*)"', body)
    ref = ref.group(1) if ref else '?'
    val = val.group(1) if val else ''
    hits = []
    for pm in re.finditer(r'\(pad "([^"]*)"[\s\S]*?\(net "([^"]*)"\)', body):
        if pm.group(2) in nets:
            hits.append('pad %s -> %s' % (pm.group(1), pm.group(2)))
    if hits:
        print('%-6s %-14s %s' % (ref, val, ' | '.join(hits)))
