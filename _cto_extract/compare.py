import json, collections, os, sys, re
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'


def counts(path):
    d = json.load(open(os.path.join(base, '_cto_extract', path), encoding='utf-8'))
    out = {}
    if 'sheets' in d:
        out['erc'] = collections.Counter(v.get('type') for s in d['sheets'] for v in s.get('violations', []))
    if 'violations' in d:
        out['drc'] = collections.Counter(v.get('type') for v in d['violations'])
        out['unc'] = len(d.get('unconnected_items', []))
        out['par'] = collections.Counter(p.get('type') for p in d.get('schematic_parity', []))
    return out


old_e, new_e = counts('erc_now.json'), counts('erc_pcb.json')
old_d, new_d = counts('drc_now.json'), counts('drc_pcb.json')

print('=== ERC   4L baseline  ->  pcb folder ===')
for k in sorted(set(old_e.get('erc', {})) | set(new_e.get('erc', {}))):
    a, b = old_e.get('erc', {}).get(k, 0), new_e.get('erc', {}).get(k, 0)
    print('  %-34s %5d -> %5d   %s' % (k, a, b, 'REGRESSION' if b > a else ''))

print('=== DRC   4L baseline  ->  pcb folder ===')
for k in sorted(set(old_d.get('drc', {})) | set(new_d.get('drc', {}))):
    a, b = old_d.get('drc', {}).get(k, 0), new_d.get('drc', {}).get(k, 0)
    tag = 'NEW/WORSE' if b > a else ('fixed' if a > b else '')
    print('  %-34s %5d -> %5d   %s' % (k, a, b, tag))
print('  %-34s %5d -> %5d' % ('unconnected', old_d.get('unc', 0), new_d.get('unc', 0)))
print('=== parity 4L baseline -> pcb folder ===')
for k in sorted(set(old_d.get('par', {})) | set(new_d.get('par', {}))):
    a, b = old_d.get('par', {}).get(k, 0), new_d.get('par', {}).get(k, 0)
    print('  %-34s %5d -> %5d   %s' % (k, a, b, 'NEW/WORSE' if b > a else ''))

print('\n=== board diff ===')
b4 = pcbnew.LoadBoard(os.path.join(base, r'4L\MoriShield_Carrier.kicad_pcb'))
bp = pcbnew.LoadBoard(os.path.join(base, r'pcb\MoriShield_Carrier.kicad_pcb'))
f4 = {fp.GetReference() for fp in b4.GetFootprints()}
fp_ = {fp.GetReference() for fp in bp.GetFootprints()}
print('  footprints  %d -> %d   added: %s   removed: %s'
      % (len(f4), len(fp_), sorted(fp_ - f4), sorted(f4 - fp_)))
def netnames(b):
    s = set()
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.GetNetname():
                s.add(p.GetNetname())
    for t in b.GetTracks():
        if t.GetNetname():
            s.add(t.GetNetname())
    return s


n4, np_ = netnames(b4), netnames(bp)
print('  net names   %d -> %d   added: %s   removed: %s'
      % (len(n4), len(np_), sorted(np_ - n4), sorted(n4 - np_)))
t4 = list(b4.GetTracks()); tp = list(bp.GetTracks())
print('  tracks+vias   %d -> %d   (vias %d -> %d)'
      % (len(t4), len(tp), sum(isinstance(t, pcbnew.PCB_VIA) for t in t4),
         sum(isinstance(t, pcbnew.PCB_VIA) for t in tp)))

d = {fp.GetReference(): fp for fp in bp.GetFootprints()}
print('\n=== the three new areas ===')
for ref in ('U8', 'J26', 'U10', 'J1', 'J4', 'J18', 'F1'):
    f = d.get(ref)
    if not f:
        print('  %-5s ABSENT' % ref)
        continue
    p = f.GetPosition()
    print('  %-5s %-34s at %8.2f,%8.2f' % (ref, str(f.GetFPID().GetLibItemName())[:34], p.x / 1e6, p.y / 1e6))
    if ref in ('U8', 'J26', 'U10', 'J1', 'J4'):
        for pad in sorted(f.Pads(), key=lambda x: int(x.GetNumber()) if x.GetNumber().isdigit() else 0):
            if ref in ('U8',) and pad.GetNumber() not in ('11', '17'):
                continue
            if ref in ('J1',) and pad.GetNumber() != '6':
                continue
            if ref in ('J4',) and pad.GetNumber() != '8':
                continue
            pp = pad.GetPosition()
            print('        pad %-3s %-16s %8.2f,%8.2f' % (pad.GetNumber(), pad.GetNetname() or '<none>',
                                                          pp.x / 1e6, pp.y / 1e6))

print('\n=== schematic text checks ===')
sp = os.path.join(base, r'pcb\MoriShield_Carrier.kicad_sch')
t = open(sp, encoding='utf-8').read()
for pat in ('J26', 'U10', 'MODEM_RST', '5V_PROT', 'WDT_WDI', 'eFuse', 'AS5600', 'no_connect'):
    print('  %-12s %4d occurrences' % (pat, len(re.findall(re.escape(pat), t))))
s4 = open(os.path.join(base, r'4L\MoriShield_Carrier.kicad_sch'), encoding='utf-8').read()
print('  instances   %d -> %d' % (len(re.findall(r'\(property "Reference"', s4)),
                                  len(re.findall(r'\(property "Reference"', t))))
print('  lib_symbols %d -> %d' % (len(re.findall(r'^\t\(symbol "', s4, re.M)), len(re.findall(r'^\t\(symbol "', t, re.M))))

print('\n=== library files present ===')
for folder in ('4L', 'pcb'):
    files = os.listdir(os.path.join(base, folder))
    print('  %-4s sym-lib-table:%-5s fp-lib-table:%-5s .kicad_sym:%s'
          % (folder, 'sym-lib-table' in files, 'fp-lib-table' in files,
             [f for f in files if f.endswith('.kicad_sym')]))
