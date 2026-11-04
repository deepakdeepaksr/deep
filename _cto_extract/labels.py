import io, re, sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')


def ln(i):
    try:
        return b.GetLayerName(i)
    except Exception:
        return str(i)


print('=== A. EVERY board-level graphic text, with its layer (only SilkS gets printed) ===')
for it in b.GetDrawings():
    if type(it).__name__ != 'PCB_TEXT':
        continue
    p = it.GetPosition()
    print('   %-9s %-30r (%7.2f,%7.2f)' % (ln(it.GetLayer()), it.GetText()[:30], p.x / 1e6, p.y / 1e6))

print()
print('=== B. per-connector silkscreen: what text lives inside each footprint, and on which layer ===')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}
for ref in ('J7', 'J8', 'J15', 'J16', 'J22', 'J23', 'J26', 'J11', 'J12', 'J13', 'J14',
            'J17', 'J20', 'J21', 'J24', 'J25', 'J6', 'J5'):
    fp = d.get(ref)
    if not fp:
        continue
    silk, fab, other = [], [], []
    for g in fp.Graphs() if hasattr(fp, 'Graphs') else []:
        pass
    for txt in fp.Strings():
        lay = ln(txt.GetLayer())
        t = txt.GetText()
        if 'Silk' in lay:
            silk.append(t)
        elif 'Fab' in lay:
            fab.append(t)
        else:
            other.append('%s@%s' % (t, lay))
    padnames = [p.GetName() for p in sorted(fp.Pads(), key=lambda x: int(x.GetNumber()) if x.GetNumber().isdigit() else 0)]
    print('   %-4s silk=%-38s fab=%-22s padnames=%s'
          % (ref, str(silk)[:38], str(fab)[:22], padnames))

print()
print('=== C. schematic: do the symbols for these ports carry pin function names? ===')
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_sch', encoding='utf-8').read()
for ref in ('J6', 'J7', 'J8', 'J15', 'J22', 'J26'):
    i = t.find('"(property \\"Reference\\" \\"%s\\"' % ref)
    i = t.find('(property "Reference" "%s"' % ref)
    if i < 0:
        print('   %s not found' % ref)
        continue
    seg = t[max(0, i - 1200):i + 200]
    lib = re.search(r'\(lib_id "([^"]+)"', seg[::-1])
    libid = lib.group(1)[::-1] if lib else '?'
    print('   %-4s lib_id=%s' % (ref, libid))
print()
print('   pin names inside the relevant symbol definitions:')
for sym in ('JST_XH_3', 'JST_XH_2', 'JST_XH_4', 'Conn_01x08', 'Conn_01x07', 'Conn_01x06'):
    j = t.find('(symbol "%s"' % sym)
    if j < 0:
        continue
    blk = t[j:j + 3000]
    pins = re.findall(r'\(name "([^"]*)"[^\n]*\)\s*\n?\s*\(number "(\d+)"', blk)
    print('     %-12s %s' % (sym, ', '.join('%s=pin%s' % (n or '(blank)', k) for n, k in pins[:9])))
