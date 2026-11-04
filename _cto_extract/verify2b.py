import re, json, collections, sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

print('=== A. schematic instances and Footprint fields ===')
t = open(base + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()
for k in ('J26', 'U10', 'MODEM_RST', '5V_PROT', 'AS5600', 'WDT_WDI', 'no_connect'):
    print('   %-11s %d' % (k, len(re.findall(re.escape(k), t))))
syms = re.findall(r'\(symbol "(.*?)"\n\s+\(lib_id "([^"]*)"\)(.*?\n\t\t\))', t, re.S)
print('   lib_id symbol blocks:', len(syms))
empty = [s[0] for s in syms if not re.search(r'\(property "Footprint" "(.+?)"', s[2])]
print('   instances with EMPTY Footprint field: %d of %d' % (len(empty), len(syms)))
print('   e.g.', empty[:12])
j26 = [s for s in syms if s[0] in ('J26', 'U10')]
for s in j26:
    fp = re.search(r'\(property "Footprint" "([^"]*)"', s[2])
    print('   %-5s lib_id=%-34s footprint=%r' % (s[0], s[1], fp.group(1) if fp else None))

print('\n=== B. project: net classes and rules ===')
d = json.load(open(base + r'\pcb\MoriShield_Carrier.kicad_pro', encoding='utf-8'))
ns = d.get('net_settings', {})
print('   net_settings keys:', sorted(ns.keys()))
nc = ns.get('classes', [])
print('   net class count:', len(nc), [c.get('name') for c in nc])
for v in nc:
    print('     %-14s clearance %.3f  track %.3f  via %.2f/%.2f'
          % (v.get('name'), v.get('clearance', 0), v.get('track_width', 0),
             v.get('via_diameter', 0), v.get('via_drill', 0)))
print('   netclass_patterns:', json.dumps(ns.get('netclass_patterns', []))[:300])
fp = re.findall(r'\(property "Footprint" "([^"]*)"', t)
print('   Footprint props %d  non-empty %d  EMPTY %d' % (len(fp), len([x for x in fp if x.strip()]), len([x for x in fp if not x.strip()])))
ds = d.get('board', {}).get('design_settings', {})
print('   design_settings keys:', sorted(ds.keys()))
print('   rules:', json.dumps(ds.get('rules', {}))[:400])
print('   stackup present:', 'stackup' in ds)

print('\n=== C. J18 graphic text in the board file ===')
p = open(base + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
for m in re.finditer(r'\(gr_text "([^"]*)" \(at ([\d.\-]+) ([\d.\-]+)(?: ([\d.\-]+))?\)(.*?)\n\s*\)', p, re.S):
    txt, x, y = m.group(1), float(m.group(2)), float(m.group(3))
    rest = m.group(5)
    if 118 < x < 145 and 92 < y < 118:
        layer = re.search(r'\(layer "([^"]+)"\)', rest)
        render = re.search(r'\(render "([^"]+)"\)', rest)
        size = re.search(r'\(effects \(font \(size ([\d.]+) ([\d.]+))', rest)
        thick = re.search(r'\(thickness ([\d.]+)\)', rest)
        print('   "%-6s" %-16s at %8.3f,%8.3f  render=%-8s size=%s stroke=%s'
              % (txt, layer.group(1) if layer else '?', x, y,
                 render.group(1) if render else 'stroke(default)',
                 size.groups() if size else '?', thick.group(1) if thick else '?'))

print('\n=== D. net_conflict 58 -> 61: the three new ones ===')
def nc_set(f):
    dd = json.load(open(base + r'\_cto_extract' + '\\' + f, encoding='utf-8'))
    out = collections.Counter()
    for it in dd.get('schematic_parity', []):
        if it.get('type') == 'net_conflict':
            its = it.get('items') or []
            out[' ; '.join((i.get('description') or '')[:60] for i in its)] += 1
    return out
old, new = nc_set('drc_pcb3.json'), nc_set('drc_v.json')
print('   old total', sum(old.values()), ' new total', sum(new.values()))
for k in new:
    if new[k] > old.get(k, 0):
        print('   NEW x%d: %s' % (new[k] - old.get(k, 0), k))
for k in old:
    if old[k] > new.get(k, 0):
        print('   GONE x%d: %s' % (old[k] - new.get(k, 0), k))

print('\n=== E. J5 feed copper now ===')
import pcbnew
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')
for t_ in b.GetTracks():
    if t_.GetNetname() in ('+5V', '+5V_F', '+5V_IN') and not isinstance(t_, pcbnew.PCB_VIA):
        a, c = t_.GetStart(), t_.GetEnd()
        if t_.GetWidth() / 1e6 < 1.0:
            print('   %-8s %.3f mm  (%.2f,%.2f)->(%.2f,%.2f)  %s'
                  % (t_.GetNetname(), t_.GetWidth() / 1e6, a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6,
                     b.GetLayerName(t_.GetLayer())))
