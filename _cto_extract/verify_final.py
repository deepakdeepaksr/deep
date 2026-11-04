import json, collections, sys, re
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
d = json.load(open(base + r'\_cto_extract\drc_f.json', encoding='utf-8'))

print('=== ignored DRC checks (release gate D3 asks for each to be justified) ===')
print('  ', [i['key'] for i in d.get('ignored_checks', [])])

print('\n=== every ERROR-severity violation ===')
for v in d['violations']:
    if v['severity'] != 'error':
        continue
    its = v.get('items') or []
    pos = its[0].get('pos') if its and its[0].get('pos') else None
    loc = '(%.2f, %.2f)' % (pos['x'] / 1e6, pos['y'] / 1e6) if pos else ''
    desc = ' | '.join((i.get('description') or '')[:78] for i in its[:2])
    print('  %-22s %-16s %s' % (v['type'], loc, desc))

print('\n=== net classes: do they bind now? ===')
p = open(base + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
print('   (net_class blocks in board file:', p.count('(net_class'), ')')
for m in re.finditer(r'\(net_class "([^"]+)"', p):
    pass
names = re.findall(r'\(net_class "([^"]+)"', p)
print('   classes present:', names)

print('\n=== synthetic unconnected net names ===')
u = re.findall(r'\(net "unconnected-\(([^"]+?)-Pad(\d+)\)"', p)
print('   count:', len(u))
byref = collections.Counter(r for r, n in u)
print('   per ref:', dict(byref))

print('\n=== H1-H4 mounting holes ===')
b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')
for fp in b.GetFootprints():
    if fp.GetReference() in ('H1', 'H2', 'H3', 'H4'):
        pos = fp.GetPosition()
        print('   %-3s %-34s at %7.2f,%7.2f  pads %d'
              % (fp.GetReference(), str(fp.GetFPID().GetLibItemName())[:34],
                 pos.x / 1e6, pos.y / 1e6, len(list(fp.Pads()))))
s = open(base + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()
print('   "MountingHole" in schematic:', s.count('MountingHole'), '| H1..H4 refs:',
      len(re.findall(r'\(property "Reference" "H[1-4]"', s)))

print('\n=== gr_text escape integrity ===')
bad = re.findall(r'\\\\n', p)
print('   literal backslash-n sequences in board:', len(bad))
print('   gr_text count:', len(re.findall(r'\(gr_text ', p)),
      ' fp_text count:', len(re.findall(r'\(fp_text ', p)))

print('\n=== the PE corridor route near R47/R48 ===')
refs = {}
for fp in b.GetFootprints():
    if fp.GetReference() in ('R47', 'R48'):
        refs[fp.GetReference()] = fp
for r, fp in refs.items():
    pos = fp.GetPosition()
    print('   %-4s at %7.2f,%7.2f  pads: %s' % (r, pos.x / 1e6, pos.y / 1e6,
          ', '.join('%s@%.2f,%.2f w%.2f' % (pd.GetNumber(), pd.GetPosition().x / 1e6,
                                            pd.GetPosition().y / 1e6, pd.GetSize().x / 1e6)
                    for pd in fp.Pads())))
for t in b.GetTracks():
    if t.GetNetname() != 'PE' or isinstance(t, pcbnew.PCB_VIA):
        continue
    w = t.GetWidth() / 1e6
    if w < 1.0:
        a, c = t.GetStart(), t.GetEnd()
        L = ((c.x - a.x) ** 2 + (c.y - a.y) ** 2) ** 0.5 / 1e6
        if 140 < a.x / 1e6 < 175 and 100 < a.y / 1e6 < 130:
            print('   PE %.3f mm  %5.2f mm  (%.2f,%.2f)->(%.2f,%.2f) %s'
                  % (w, L, a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6, b.GetLayerName(t.GetLayer())))
