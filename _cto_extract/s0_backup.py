import os, sys, shutil, json, time, collections
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
src = os.path.join(base, 'pcb')
stamp = time.strftime('%Y%m%d_%H%M%S')
dst = os.path.join(src, '_snap', 'pre_S3run_' + stamp)
os.makedirs(dst, exist_ok=True)

for f in ('MoriShield_Carrier.kicad_pcb', 'MoriShield_Carrier.kicad_sch',
          'MoriShield_Carrier.kicad_pro', 'MoriShield_Carrier.kicad_sym',
          'fp-lib-table', 'sym-lib-table'):
    p = os.path.join(src, f)
    if os.path.exists(p):
        shutil.copy2(p, os.path.join(dst, f))
print('backup ->', dst)
print(' files:', sorted(os.listdir(dst)))


def census():
    b = pcbnew.LoadBoard(os.path.join(src, 'MoriShield_Carrier.kicad_pcb'))
    c = {}
    c['footprints'] = len(list(b.GetFootprints()))
    tr = list(b.GetTracks())
    c['tracks'] = len([t for t in tr if not isinstance(t, pcbnew.PCB_VIA)])
    c['vias'] = len([t for t in tr if isinstance(t, pcbnew.PCB_VIA)])
    c['zones'] = len([z for z in b.Zones() if not z.GetIsRuleArea()])
    c['nets'] = len({t.GetNetname() for t in tr if t.GetNetname()} |
                    {p.GetNetname() for fp in b.GetFootprints() for p in fp.Pads() if p.GetNetname()})
    c['refs'] = sorted(fp.GetReference() for fp in b.GetFootprints())
    c['padnets'] = {'%s.%s' % (fp.GetReference(), p.GetNumber()): p.GetNetname()
                    for fp in b.GetFootprints() for p in fp.Pads()}
    s = open(os.path.join(src, 'MoriShield_Carrier.kicad_sch'), encoding='utf-8').read()
    c['sch_instances'] = s.count('(property "Reference"')
    c['sch_noconnect'] = s.count('no_connect')
    c['sch_chars'] = len(s)
    c['sch_libsymbols'] = s.count('(lib_symbols')
    return c


c0 = census()
json.dump(c0, open(os.path.join(dst, 'census.json'), 'w', encoding='utf-8'), indent=1)
print('\n=== BASELINE CENSUS ===')
for k in ('footprints', 'tracks', 'vias', 'zones', 'nets', 'sch_instances', 'sch_noconnect', 'sch_chars'):
    print('   %-14s %s' % (k, c0[k]))
open(os.path.join(src, '_snap', 'LATEST_PRE_S3'), 'w').write(dst)
print('\ncensus saved. any later count that drops without an explanation is a defect.')
