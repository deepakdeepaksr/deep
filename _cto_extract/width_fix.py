import sys, collections
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
REQ = {'+5V_IN': 1.5, '+5V_F': 1.5, '/5V_PROT': 1.5, '+5V': 1.5,
       '/+5V_ESP': 0.8, '/+5V_SENS': 0.8, '/+5V_E22': 0.8, '/+5V_E22_IN': 0.8,
       '3V3_C': 0.5, '/3V3_SENS': 0.5, '/3V3_SENS_SW': 0.5, 'PE': 1.0}
RHO = {'outer': 0.505e-3, 'inner': 1.01e-3}

b = pcbnew.LoadBoard(base + r'\pcb\MoriShield_Carrier.kicad_pcb')
rows = []
for t in b.GetTracks():
    n = t.GetNetname()
    if n not in REQ or isinstance(t, pcbnew.PCB_VIA):
        continue
    a, c = t.GetStart(), t.GetEnd()
    L = (((c.x - a.x) ** 2 + (c.y - a.y) ** 2) ** 0.5) / 1e6
    w = t.GetWidth() / 1e6
    lay = b.GetLayerName(t.GetLayer())
    inner = lay.startswith('In')
    if w >= REQ[n] - 1e-6 or L < 3.0:
        continue
    r = L / max(w, 0.05) * RHO['inner' if inner else 'outer'] * 1e3
    rows.append((r, n, w, L, a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6, lay))

rows.sort(reverse=True)
print('=== segments >= 3 mm that are below the restored width, ranked by resistance ===')
print('%-8s %6s %6s  %-26s -> %-26s %-8s %7s' % ('net', 'width', 'len', 'from', 'to', 'layer', 'mOhm'))
tot = collections.defaultdict(float)
for r, n, w, L, x1, y1, x2, y2, lay in rows:
    tot[n] += r
    print('%-8s %5.2f  %5.1f  (%7.2f,%7.2f)      (%7.2f,%7.2f)      %-8s %6.1f'
          % (n, w, L, x1, y1, x2, y2, lay, r))
print('\n  %d segments' % len(rows))
print('\n=== summed resistance of the long under-width copper, per net ===')
for n, v in sorted(tot.items(), key=lambda kv: -kv[1]):
    print('   %-14s %6.1f mOhm' % (n, v))
