import io, re, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()

print('=== A. every silk text in the file, with its real size and thickness ===')
bad = []
kinds = collections.Counter()
# board-level gr_text and footprint-level fp_text both carry (layer "F.SilkS") etc.
for m in re.finditer(r'\((?:gr_text|fp_text)\s+"?((?:[^"\\\n]|\\.)*)"?\s*(.*?)\n\s*\)', t, re.S):
    txt, body = m.group(1), m.group(2)
    lay = re.search(r'\(layer "([^"]+)"', body)
    if not lay or 'Silk' not in lay.group(1):
        continue
    sz = re.search(r'\(size\s+([\d.]+)\s+([\d.]+)\)', body)
    th = re.search(r'\(thickness\s+([\d.]+)\)', body)
    rend = re.search(r'\(render "([^"]+)"', body)
    w, h = (float(sz.group(1)), float(sz.group(2))) if sz else (None, None)
    tk = float(th.group(1)) if th else None
    kinds[(lay.group(1), round(h, 2) if h else None, round(tk, 2) if tk else None,
           rend.group(1) if rend else 'stroke')] += 1
    if h is not None and h < 1.0:
        bad.append(('height %.2f' % h, txt[:22], lay.group(1)))
    if tk is not None and tk < 0.15:
        bad.append(('thickness %.3f' % tk, txt[:22], lay.group(1)))

for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
    print('   layer=%-8s h=%-5s thick=%-6s render=%-8s x %d' % (k[0], k[1], k[2], k[3], v))
print('   TEXTS BELOW LEGAL SILK (1.0 mm / 0.15 mm):', len(bad))
for b in bad[:12]:
    print('     ', b)

print()
print('=== B. courtyards -- missing_courtyard is set to "ignore", so DRC cannot report it ===')
fps = re.findall(r'\(footprint "([^"]*)"(.*?)\n\t\t\)', t, re.S)
blocks = re.split(r'\n\t\(footprint ', t)
no_c = []
for blk in blocks[1:]:
    ref = re.search(r'\(property "Reference" "([^"]*)"', blk)
    if not ref:
        continue
    if 'CrtYd' not in blk:
        no_c.append(ref.group(1))
print('   footprints parsed:', len(blocks) - 1)
print('   footprints with NO courtyard graphic:', len(no_c))
print('   refs:', no_c[:24])

print()
print('=== C. module outlines: R14/A4 require both module bodies drawn ===')
for tok in ('Edge.Cuts', 'Dwgs.User', 'F.Fab'):
    n = len(re.findall(r'\(layer "%s"' % re.escape(tok), t))
    print('   layer %s references: %d' % (tok, n))

print()
print('=== D. rule-area / keep-out presence (E3 antenna keep-out) ===')
print('   (rule_area blocks:', t.count('(rule_area'), ')   zone with (fill allow_soldermask_bridges etc.)')
print('   total (zone blocks:', len(re.findall(r'\n\t\t\(zone ', t)) + len(re.findall(r'\n\t\(zone ', t)), ')')
