import io, re, csv, sys, os, datetime
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# ---------- 1. decoupling map: recompute pass/fail from the numbers ----------
r = list(csv.reader(io.open(P + r'\revC\decoupling_map.csv', encoding='utf-8-sig')))
h, rows = r[0], r[1:]
iL, iM, iC, iB = h.index('limit_mm'), h.index('meets'), h.index('copper_mm'), h.index('basis')
withlim = [x for x in rows if x[iL].strip()]
blank = [x for x in rows if x[iL].strip() and not x[iM].strip()]
no = [x for x in rows if x[iM].strip().lower() == 'no']
print('=== decoupling map reconciliation ===')
print('   rows %d | with a limit %d | verdict "no" %d | limit present but verdict BLANK %d'
      % (len(rows), len(withlim), len(no), len(blank)))
calc_pass = [x for x in blank if float(x[iC]) <= float(x[iL]) + 1e-9]
calc_fail = [x for x in blank if float(x[iC]) > float(x[iL]) + 1e-9]
print('   of those blanks, recomputed from copper_mm vs limit_mm: %d would PASS, %d would FAIL'
      % (len(calc_pass), len(calc_fail)))
print('   -> so "0 of 27 meet" is only true if the 54 blank rows are unjudged, not passes.')
if calc_pass:
    print('   examples that pass but are blank:')
    for x in calc_pass[:5]:
        print('      %-14s %-6s pad %-3s cap %-6s %s mm vs limit %s'
              % (x[0], x[1], x[2], x[4], x[iC], x[iL]))
# by class
cls = {}
for x in rows:
    k = x[iB].split(':')[0]
    cls.setdefault(k, [0, 0, 0])
    if x[iL].strip():
        ok = float(x[iC]) <= float(x[iL]) + 1e-9
        cls[k][0] += 1
        cls[k][1 if ok else 2] += 1
print('   by class (with-limit, meet, fail):')
for k, v in sorted(cls.items()):
    print('      %-28s %3d %3d %3d' % (k, v[0], v[1], v[2]))

# ---------- 2. plot freshness vs design ----------
print()
print('=== is the C12 Gerber evidence current? ===')
pcb_t = os.stat(P + r'\pcb\MoriShield_Carrier.kicad_pcb').st_mtime
g = os.stat(P + r'\revC\silk_check\MoriShield_Carrier-F_Silkscreen.gto').st_mtime
print('   board saved  %s' % datetime.datetime.fromtimestamp(pcb_t).strftime('%m-%d %H:%M:%S'))
print('   plot made    %s' % datetime.datetime.fromtimestamp(g).strftime('%m-%d %H:%M:%S'))
print('   verdict:', 'PLOT IS OLDER THAN THE BOARD - stale' if g < pcb_t else 'plot post-dates the board')

# ---------- 3. does the modem outline really cover J5 and test points? ----------
import pcbnew
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}


def rect_from_drawings(needle):
    for it in b.GetDrawings():
        if type(it).__name__ == 'PCB_TEXT' and needle in it.GetText():
            return it.GetPosition()
    return None


print()
print('=== "nothing reachable sits under a module" - measured ===')
# modem outline: find F.Fab rect near J3/J4
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
    cands.append((lay, min(s.x / 1e6, e.x / 1e6), min(s.y / 1e6, e.y / 1e6),
                  max(s.x / 1e6, e.x / 1e6), max(s.y / 1e6, e.y / 1e6)))
print('   outline rectangles on F.Fab/Dwgs.User: %d' % len(cands))
for c in cands:
    print('      %-9s (%7.2f,%7.2f)-(7.2f%7.2f)  %5.1f x %5.1f mm'
          % (c[0], c[1], c[2], c[3], c[4], c[3] - c[1], c[4] - c[2]))

# which outlines contain J5 / TP2..TP5
pts = {}
for ref in ('J5', 'TP2', 'TP3', 'TP4', 'TP5', 'J18', 'J19', 'SW1'):
    if ref in d:
        p = d[ref].GetPosition()
        pts[ref] = (p.x / 1e6, p.y / 1e6)
for ref, (x, y) in sorted(pts.items()):
    inside = [c for c in cands if c[1] <= x <= c[3] and c[2] <= y <= c[4]]
    print('   %-5s at (%7.2f,%7.2f)  inside %d outline(s): %s'
          % (ref, x, y, len(inside), ['%.1fx%.1f@%s' % (c[3] - c[1], c[4] - c[2], c[0]) for c in inside]))

# ---------- 4. the two B.Cu tracks that block the E22 keep-out ----------
print()
print('=== B.Cu segments crossing the proposed E22 keep-out (x 296-304.57, y 163-177) ===')
try:
    BCU = pcbnew.LayerNameToId('B.Cu')
except Exception:
    BCU = None
if BCU is None:
    import re as _re
    txt = io.open(P + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
    print('   (LayerNameToId unavailable; parsing text)')
for t in b.GetTracks():
    if type(t).__name__ == 'PCB_VIA':
        continue
    if b.GetLayerName(t.GetLayer()) != 'B.Cu':
        continue
    a, c = t.GetStart(), t.GetEnd()
    ax, ay, cx, cy = a.x / 1e6, a.y / 1e6, c.x / 1e6, c.y / 1e6
    if max(min(ax, cx), 296.0) <= min(max(ax, cx), 304.57) and \
       max(min(ay, cy), 163.0) <= min(max(ay, cy), 177.0):
        L = ((cx - ax) ** 2 + (cy - ay) ** 2) ** 0.5
        print('   %-18s (%7.2f,%7.2f)-(%7.2f,%7.2f)  len %.2f mm  w %.2f'
              % (t.GetNetname(), ax, ay, cx, cy, L, t.GetWidth() / 1e6))
