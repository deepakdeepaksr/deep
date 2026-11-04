import sys, os
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
path = os.path.join(base, 'pcb', 'MoriShield_Carrier.kicad_pcb')
b = pcbnew.LoadBoard(path)
MM = pcbnew.FromMM


def ends(t):
    """Return ((x,y),(x,y)) in mm for a track, or ((x,y),(x,y)) doubled for a via."""
    if type(t).__name__ == 'PCB_VIA':
        p = t.GetPosition()
        return (p.x / 1e6, p.y / 1e6), (p.x / 1e6, p.y / 1e6), True
    a, c = t.GetStart(), t.GetEnd()
    return (a.x / 1e6, a.y / 1e6), (c.x / 1e6, c.y / 1e6), False


# ---- 1. U4 back into BOM and placement ----
for fp in b.GetFootprints():
    if fp.GetReference() == 'U4':
        fp.SetBoardOnly(False)
        fp.SetExcludedFromPosFiles(False)
        fp.SetExcludedFromBOM(False)
        print('U4 -> board_only=%s excl_POS=%s excl_BOM=%s'
              % (fp.IsBoardOnly(), fp.IsExcludedFromPosFiles(), fp.IsExcludedFromBOM()))

# ---- 2. the five dangling items, matched by net + exact geometry ----
WANT = [('3V3_C', False, (169.00, 129.25), (182.00, 129.25)),
        ('/EVENT_BTN', False, (170.55, 131.00), None),
        ('/PWR_EN', True, (256.899999, 170.1), None),
        ('/I2C0_SDA', True, (247.25, 172.0), None),
        ('/BUZZER_EN', True, (257.5, 167.5), None)]

removed = []
for net, is_via, p1, p2 in WANT:
    hit = None
    for t in list(b.GetTracks()):
        try:
            if t.GetNetname() != net:
                continue
            e1, e2, vi = ends(t)
            if vi != is_via:
                continue
            if (abs(e1[0] - p1[0]) < 0.02 and abs(e1[1] - p1[1]) < 0.02) or \
               (abs(e2[0] - p1[0]) < 0.02 and abs(e2[1] - p1[1]) < 0.02):
                if p2 is not None and not \
                   ((abs(e1[0] - p2[0]) < 0.02 and abs(e1[1] - p2[1]) < 0.02) or
                    (abs(e2[0] - p2[0]) < 0.02 and abs(e2[1] - p2[1]) < 0.02)):
                    continue
                hit = t
                break
        except Exception:
            continue
    if hit is None:
        print('  NOT FOUND: %s %s' % (net, p1))
        continue
    b.Remove(hit)
    removed.append(net)
    print('  removed %-12s %s at %.2f,%.2f' % (net, 'via' if is_via else 'track', p1[0], p1[1]))

if len(removed) != len(WANT):
    print('!! only %d of %d located - aborting before save' % (len(removed), len(WANT)))
    sys.exit(1)

# ---- 3. silkscreen the release check requires ----
bb = b.GetBoardEdgesBoundingBox()
L, B = bb.GetX() / 1e6, bb.GetBottom() / 1e6
print('outline left %.2f  bottom %.2f' % (L, B))


def silk_text(txt, x, y, h=1.0, w=0.15, rot=0):
    gt = pcbnew.PCB_TEXT(b)
    gt.SetText(txt)
    gt.SetLayer(pcbnew.F_Silkscreen)
    gt.SetPos(pcbnew.VECTOR2I(MM(x), MM(y)))
    gt.SetSize(pcbnew.VECTOR2I(MM(h), MM(h)))
    gt.SetLineWidth(MM(w))
    gt.SetOrient(rot)
    try:
        gt.SetFontId('')
    except Exception:
        pass
    gt.SetHorizJustify(pcbnew.GR_TEXT_HJUST_LEFT)
    gt.SetVertJustify(pcbnew.GR_TEXT_VJUST_CENTER)
    b.Add(gt)


def silk_rect(x0, y0, x1, y1, w=0.15):
    sh = pcbnew.PCB_SHAPE(b)
    sh.SetShape(pcbnew.SHAPE_T_RECT)
    sh.SetStart(pcbnew.VECTOR2I(MM(x0), MM(y0)))
    sh.SetEnd(pcbnew.VECTOR2I(MM(x1), MM(y1)))
    sh.SetLayer(pcbnew.F_Silkscreen)
    sh.SetWidth(MM(w))
    sh.SetFilled(False)
    b.Add(sh)


silk_text('MoriShield Carrier', L + 13.0, B - 3.0)
silk_text('Rev C', L + 13.0, B - 5.6)
silk_text('S/N', L + 24.0, B - 5.6)
silk_rect(L + 27.5, B - 6.8, L + 48.0, B - 4.4)
silk_text('1', 232.30, 113.56, h=1.4)          # J3 pin 1
silk_text('1', 272.30, 113.56, h=1.4)          # J4 pin 1
silk_text('MODEM THIS WAY UP', 240.0, 108.5, h=1.0)
print('silkscreen added: board id, revision, serial box, two PIN-1 marks, orientation note')

b.BuildConnectivity()
try:
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())
    print('zones refilled')
except Exception as e:
    print('zone refill failed:', e)
b.Save()
print('SAVED')

b2 = pcbnew.LoadBoard(path)
tr2 = list(b2.GetTracks())
print('\n=== post-save census (baseline 159 / 1175 / 233 / 5) ===')
print('   footprints %d  tracks %d  vias %d  zones %d'
      % (len(list(b2.GetFootprints())),
         len([t for t in tr2 if type(t).__name__ != 'PCB_VIA']),
         len([t for t in tr2 if type(t).__name__ == 'PCB_VIA']),
         len([z for z in b2.Zones() if not z.GetIsRuleArea()])))
