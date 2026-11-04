import re, sys

path = sys.argv[1]
txt = open(path, encoding='utf-8', errors='replace').read()

def blocks(txt, tag):
    out = []
    i = 0
    n = len(txt)
    pat = re.compile(r'\(' + tag + r' "')
    while True:
        m = pat.search(txt, i)
        if not m:
            break
        start = m.start()
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
        out.append(txt[start:j+1])
        i = j + 1
    return out

want = set(sys.argv[2].split(','))
for body in blocks(txt, 'footprint'):
    refm = re.search(r'\(property "Reference" "([^"]*)"', body)
    ref = refm.group(1) if refm else '?'
    if ref not in want:
        continue
    val = re.search(r'\(property "Value" "([^"]*)"', body)
    print('==', ref, val.group(1) if val else '')
    for m in re.finditer(r'\(pad "([^"]*)"[\s\S]*?\(net "([^"]*)"\)', body):
        print('   pad %-4s %s' % (m.group(1), m.group(2)))
