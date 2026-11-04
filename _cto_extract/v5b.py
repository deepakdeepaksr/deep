import io, re, csv, sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# ---- A. IC and port supply pin rows, sorted worst first ----
r = list(csv.reader(io.open(P + r'\revC\decoupling_map.csv', encoding='utf-8-sig')))
h, rows = r[0], r[1:]
iL, iM, iC, iB = h.index('limit_mm'), h.index('meets'), h.index('copper_mm'), h.index('basis')
sup = [x for x in rows if x[iB].startswith(('IC supply', 'port supply')) and x[iL].strip()]
print('=== supply-pin rows: %d (IC %d, port %d) ===' % (
    len(sup), len([x for x in sup if x[iB].startswith('IC')]),
    len([x for x in sup if x[iB].startswith('port')])))
bad = [x for x in sup if float(x[iC]) > float(x[iL])]
print('   exceed their limit: %d ; verdict "no" recorded: %d'
      % (len(bad), len([x for x in sup if x[iM].strip() == 'no'])))
for x in sorted(sup, key=lambda y: -float(y[iC]))[:14]:
    print('   %-14s %-5s pad %-3s  cap %-6s %-7s  %6s mm  limit %-5s  verdict=%r'
          % (x[0], x[1], x[2], x[4], x[5], x[iC], x[iL], x[iM]))

# ---- B. what does the CTO actually require? ----
print()
print('=== source wording for the decoupling distance ===')
for f in ('MoriShield-Carrier-ReleaseCheck-v1.0.txt', 'MoriShield-Carrier-FabReadiness-v1.0.txt'):
    t = io.open(P + r'\_cto_extract' + '\\' + f, encoding='utf-8', errors='ignore').read()
    for m in re.finditer(r'(?i)(decoupl\w+|within \d+\s*mm|local capacit\w+)', t):
        s = t[max(0, m.start() - 200):m.start() + 320].replace('\n', ' ')
        if re.search(r'(?i)mm|capacit', s):
            open(P + r'\_cto_extract\c9_wording.txt', 'a', encoding='utf-8').write(
                '\n### %s @%d\n%s\n' % (f, m.start(), s))
print('   hits written to _cto_extract\c9_wording.txt')

# ---- C. outlines vs reachable parts ----
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}
cands = []
for it in b.GetDrawings():
    if type(it).__name__ != 'PCB_SHAPE':
        continue
    lay = b.GetLayerName(it.GetLayer())
    if lay not in ('F.Fab', 'Dwgs.User'):
        continue
    try:
        s, e = it.GetStart(), it.GetEnd()
    except Exception:
        continue
    x0, x1 = sorted((s.x / 1e6, e.x / 1e6))
    y0, y1 = sorted((s.y / 1e6, e.y / 1e6))
    cands.append((lay, x0, y0, x1, y1))
print()
print('=== module outlines now in the file ===')
for c in cands:
    print('   %-9s (%7.2f,%7.2f)-(%7.2f,%7.2f)   %5.1f x %5.1f mm' % (c[0], c[1], c[2], c[3], c[4], c[3] - c[1], c[4] - c[2]))

print()
print('=== is anything reachable under a module? ===')
for ref in ('J5', 'J18', 'J19', 'TP2', 'TP3', 'TP4', 'TP5', 'SW1', 'J24', 'J25', 'J26'):
    fp = d.get(ref)
    if not fp:
        continue
    p = fp.GetPosition()
    x, y = p.x / 1e6, p.y / 1e6
    ins = [c for c in cands if c[1] <= x <= c[3] and c[2] <= y <= c[4]]
    tag = 'UNDER ' + str([c[0] + ' %.1fx%.1f' % (c[3] - c[1], c[4] - c[2]) for c in ins]) if ins else 'clear'
    print('   %-5s (%7.2f,%7.2f)  %s' % (ref, x, y, tag))

# ---- D. B.Cu segments crossing the E22 keep-out ----
print()
print('=== B.Cu segments crossing x 296-304.57, y 163-177 ===')
for t in b.GetTracks():
    if type(t).__name__ == 'PCB_VIA' or b.GetLayerName(t.GetLayer()) != 'B.Cu':
        continue
    a, c = t.GetStart(), t.GetEnd()
    ax, ay, cx, cy = a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6
    if max(min(ax, cx), 296.0) <= min(max(ax, cx), 304.57) and max(min(ay, cy), 163.0) <= min(max(ay, cy), 177.0):
        L = ((cx - ax) ** 2 + (cy - ay) ** 2) ** 0.5
        print('   %-18s (%7.2f,%7.2f)-(%7.2f,%7.2f) len %.2f mm w %.2f' % (t.GetNetname(), ax, ay, cx, cy, L, t.GetWidth() / 1e6))
