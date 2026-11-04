import sys, os, json
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
path = os.path.join(base, 'pcb', 'MoriShield_Carrier.kicad_pcb')
b = pcbnew.LoadBoard(path)
MM = pcbnew.FromMM

# ---------- 1. U4 back into the BOM and the placement file ----------
for fp in b.GetFootprints():
    if fp.GetReference() == 'U4':
        before = fp.GetAttributes()
        fp.SetBoardOnly(False)
        fp.SetExcludedFromPosFiles(False)
        fp.SetExcludedFromBOM(False)
        print('U4 attributes %d -> %d   board_only=%s excl_POS=%s excl_BOM=%s'
              % (before, fp.GetAttributes(), fp.IsBoardOnly(),
                 fp.IsExcludedFromPosFiles(), fp.IsExcludedFromBOM()))

# ---------- 2. the five dangling items DRC names, deleted by UUID ----------
TARGETS = {
    '195ff0ab-7ba1-40c9-8384-2f4ce3e9fab0': ('3V3_C', 'track'),
    'a872d970-ab82-4fe9-b6e2-873436224da0': ('/PWR_EN', 'via'),
    '75133ec4-ff1a-4f0a-85da-0df0d6da4120': ('/I2C0_SDA', 'via'),
    'e54073cd-5da7-46a9-bcb2-993543087529': ('/EVENT_BTN', 'track'),
    '496bf122-792d-4b7b-93ab-91957d8f81af': ('/BUZZER_EN', 'via'),
}
removed = 0
got_uuid = True
for t in list(b.GetTracks()):
    try:
        u = str(t.GetUUID())
    except Exception:
        got_uuid = False
        break
    if u in TARGETS:
        want_net, kind = TARGETS[u]
        if t.GetNetname() != want_net:
            print('   SKIP %s: net is %s not %s' % (u, t.GetNetname(), want_net))
            continue
        is_via = isinstance(t, pcbnew.PCB_VIA)
        if (is_via and kind != 'via') or (not is_via and kind != 'track'):
            print('   SKIP %s: kind mismatch' % u)
            continue
        b.Remove(t)
        removed += 1
        print('   removed %-11s %-6s %s' % (want_net, kind, u[:8]))
print('dangling items removed:', removed, 'of', len(TARGETS))

if not got_uuid or removed < len(TARGETS):
    # fall back to net + geometry, which is unambiguous for these five
    GEOM = [('3V3_C', 'track', 169.0, 129.25, 13.0), ('/EVENT_BTN', 'track', 170.55, 131.0, 1.05),
            ('/PWR_EN', 'via', 256.899999, 170.1, 0), ('/I2C0_SDA', 'via', 247.25, 172.0, 0),
            ('/BUZZER_EN', 'via', 257.5, 167.5, 0)]
    for net, kind, x, y, ln in GEOM:
        for t in list(b.GetTracks()):
            if t.GetNetname() != net:
                continue
            is_via = isinstance(t, pcbnew.PCB_VIA)
            if (kind == 'via') != is_via:
                continue
            a = t.GetPosition() if is_via else t.GetStart()
            c = t.GetPosition() if is_via else t.GetEnd()
            near = lambda p: abs(p.x / 1e6 - x) < 0.02 and abs(p.y / 1e6 - y) < 0.02
            L2 = ((c.x - a.x) ** 2 + (c.y - a.y) ** 2) ** 0.5 / 1e6
            if (near(a) or near(c)) and (ln == 0 or abs(L2 - ln) < 0.02):
                b.Remove(t)
                removed += 1
                print('   removed by geometry: %-12s %s' % (net, kind))
                break
    print('total removed after geometry pass:', removed)

if removed < len(TARGETS):
    print('!! could not locate all five dangling items - aborting without saving')
    sys.exit(1)

# ---------- 3. silkscreen the CTO asks for and the board does not have ----------
bb = b.GetBoardEdgesBoundingBox()
L, T = bb.GetX() / 1e6, bb.GetY() / 1e6
R, B = bb.GetRight() / 1e6, bb.GetBottom() / 1e6
print('board outline %.2f,%.2f -> %.2f,%.2f' % (L, T, R, B))


def silk_text(txt, x, y, h=1.0, w=0.15, rot=0):
    gt = pcbnew.PCB_TEXT(b)
    gt.SetText(txt)
    gt.SetLayer(pcbnew.F_Silkscreen)
    gt.SetPos(pcbnew.VECTOR2I(MM(x), MM(y)))
    gt.SetSize(pcbnew.VECTOR2I(MM(h), MM(h)))
    gt.SetLineWidth(MM(w))
    gt.SetOrient(rot)
    try:
        gt.SetFontId('')          # empty = KiCad stroke font, not TrueType
    except Exception:
        pass
    gt.SetHorizJustify(pcbnew.GR_TEXT_HJUST_LEFT)
    gt.SetVertJustify(pcbnew.GR_TEXT_VJUST_CENTER)
    gt.SetVisible(True)
    b.Add(gt)
    return gt


def silk_rect(x0, y0, x1, y1, w=0.15):
    sh = pcbnew.PCB_SHAPE(b)
    sh.SetShape(pcbnew.SHAPE_T_RECT)
    sh.SetStart(pcbnew.VECTOR2I(MM(x0), MM(y0)))
    sh.SetEnd(pcbnew.VECTOR2I(MM(x1), MM(y1)))
    sh.SetLayer(pcbnew.F_Silkscreen)
    sh.SetWidth(MM(w))
    sh.SetFilled(False)
    b.Add(sh)


added = []
try:
    added.append(silk_text('MoriShield Carrier', L + 14.0, B - 2.6).__class__.__name__)
    silk_text('Rev C  2026-11-01', L + 14.0, B - 5.2)
    silk_text('S/N ____________', L + 40.0, B - 5.2)
    silk_rect(L + 39.4, B - 6.4, L + 62.0, B - 4.0)
    # orientation marks: PIN 1 at the top of each modem socket row
    silk_text('1', 232.6, 113.56, h=1.2)
    silk_text('1', 272.0, 113.56, h=1.2)
    silk_text('MODEM UP', 244.0, 110.4, h=1.0)
    print('silkscreen added')
except Exception as e:
    print('silkscreen failed:', e)

b.BuildConnectivity()
try:
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())
except Exception as e:
    print('zone refill skipped:', e)
b.Save()
print('saved.')

b2 = pcbnew.LoadBoard(path)
tr = list(b2.GetTracks())
print('\n=== post-save census ===')
print('   footprints %d  tracks %d  vias %d  zones %d'
      % (len(list(b2.GetFootprints())),
         len([t for t in tr if not isinstance(t, pcbnew.PCB_VIA)]),
         len([t for t in tr if isinstance(t, pcbnew.PCB_VIA)]),
         len([z for z in b2.Zones() if not z.GetIsRuleArea()])))
print('   silk text items:', len([d for d in b2.GetDrawings()
                                  if type(d).__name__ == 'PCB_TEXT' and 'Silkscreen' in d.GetLayerName()]))
