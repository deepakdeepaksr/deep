import re, os, time

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = open(base + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()

print('=== every text item mentioning 5v / + / - / J18 anywhere in the board ===')
hits = 0
for m in re.finditer(r'\((gr_text|fp_text)\b', p):
    seg = p[m.start():m.start() + 900]
    tm = re.match(r'\((gr_text|fp_text)\s+"?((?:[^"\\]|\\.)*)"?', seg)
    if not tm:
        continue
    kind, txt = tm.group(1), tm.group(2)
    if not re.search(r'5v|5V|\+|\u2212|J18|^\s*-\s*$', txt, re.I):
        continue
    at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', seg)
    lay = re.search(r'\(layer "([^"]+)"', seg)
    ren = re.search(r'\(render "([^"]+)"', seg)
    sz = re.search(r'\(size\s+([-\d.]+)\s+([-\d.]+)\)', seg)
    th = re.search(r'\(thickness\s+([-\d.]+)\)', seg)
    hits += 1
    print('  %-8s text=%-10r at=%s rot=%s layer=%-20s render=%-8s size=%s thick=%s'
          % (kind, txt, at.groups()[:2] if at else '?', at.group(3) if at else '-',
             lay.group(1) if lay else '?', ren.group(1) if ren else 'stroke(default)',
             sz.groups() if sz else '?', th.group(1) if th else '?'))
print('  total', hits)

print('\n=== J18 footprint block: its own fp_text fields ===')
i = p.find('(fp_reference "J18"') if '(fp_reference "J18"' in p else -1
for m in re.finditer(r'\(footprint "([^"]*)"[^\n]*\n(?:.*?\n){0,3}?.*?\(property "Reference" "J18"', p):
    print('  footprint header:', m.group(1))
blk = re.search(r'\(footprint .*?\(property "Reference" "J18".*?\n  \)\n', p, re.S)
if blk:
    s = blk.group(0)
    for mm in re.finditer(r'\((fp_text|gr_text)\s+"?([^"\s)]*)"?\s+\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)([^\n]*)', s):
        print('   ', mm.group(1), repr(mm.group(2)), mm.group(3), mm.group(4), mm.group(5))
    for mm in re.finditer(r'\(at\s+([-\d.]+)\s+([-\d.]+)\)', s[:400]):
        print('    footprint origin:', mm.group(1), mm.group(2))
        break

print('\n=== notes files, newest first ===')
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d not in ('.history', '__pycache__', 'venv_fab', '_qa', '6L')]
    for f in files:
        if f.lower().endswith(('.md', '.txt')) or f == 'work done':
            fp = os.path.join(root, f)
            mt = time.localtime(os.path.getmtime(fp))
            if mt.tm_mday == 1 and mt.tm_mon == 11:
                print('  %02d:%02d:%02d  %8d  %s' % (mt.tm_hour, mt.tm_min, mt.tm_sec,
                                                     os.path.getsize(fp), fp.replace(base, '.')))
