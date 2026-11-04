import sys, os
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
path = os.path.join(base, 'pcb', 'MoriShield_Carrier.kicad_pcb')
b = pcbnew.LoadBoard(path)
MM = pcbnew.FromMM

tr = list(b.GetTracks())
print('loads OK. segments %d  vias %d  footprints %d'
      % (len([t for t in tr if type(t).__name__ != 'PCB_VIA']),
         len([t for t in tr if type(t).__name__ == 'PCB_VIA']),
         len(list(b.GetFootprints()))))

for fp in b.GetFootprints():
    if fp.GetReference() == 'U4':
        fp.SetBoardOnly(False)
        fp.SetExcludedFromPosFiles(False)
        fp.SetExcludedFromBOM(False)
        print('U4 -> board_only=%s excl_POS=%s excl_BOM=%s'
              % (fp.IsBoardOnly(), fp.IsExcludedFromPosFiles(), fp.IsExcludedFromBOM()))

bb = b.GetBoardEdgesBoundingBox()
L, B = bb.GetX() / 1e6, bb.GetBottom() / 1e6
print('outline left %.2f  bottom %.2f' % (L, B))

SILK = pcbnew.LayerNameToId('F.Silkscreen')
print('F.Silkscreen layer id =', SILK, pcbnew.GetLayerName(SILK) if hasattr(pcbnew, 'GetLayerName') else '')
HJ = getattr(pcbnew, 'GR_TEXT_HJUST_LEFT', 0)
VJ = getattr(pcbnew, 'GR_TEXT_VJUST_CENTER', 0)
RECT = getattr(pcbnew, 'SHAPE_T_RECT', 1)


def silk_text(txt, x, y, h=1.0, w=0.15, rot=0):
    gt = pcbnew.PCB_TEXT(b)
    gt.SetText(txt)
    gt.SetLayer(SILK)
    gt.SetPos(pcbnew.VECTOR2I(MM(x), MM(y)))
    gt.SetSize(pcbnew.VECTOR2I(MM(h), MM(h)))
    gt.SetLineWidth(MM(w))
    gt.SetOrient(rot)
    try:
        gt.SetFontId('')
    except Exception:
        pass
    gt.SetHorizJustify(HJ)
    gt.SetVertJustify(VJ)
    b.Add(gt)


def silk_rect(x0, y0, x1, y1, w=0.15):
    sh = pcbnew.PCB_SHAPE(b)
    sh.SetShape(RECT)
    sh.SetStart(pcbnew.VECTOR2I(MM(x0), MM(y0)))
    sh.SetEnd(pcbnew.VECTOR2I(MM(x1), MM(y1)))
    sh.SetLayer(SILK)
    sh.SetWidth(MM(w))
    sh.SetFilled(False)
    b.Add(sh)


silk_text('MoriShield Carrier', L + 13.0, B - 3.0)
silk_text('Rev C', L + 13.0, B - 5.6)
silk_text('S/N', L + 24.0, B - 5.6)
silk_rect(L + 27.5, B - 6.8, L + 48.0, B - 4.4)
silk_text('1', 232.30, 113.56, h=1.4)
silk_text('1', 272.30, 113.56, h=1.4)
silk_text('MODEM THIS WAY UP', 240.0, 108.5, h=1.0)
print('silkscreen added')

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
print('\npost-save: segments %d  vias %d  footprints %d  zones %d'
      % (len([t for t in tr2 if type(t).__name__ != 'PCB_VIA']),
         len([t for t in tr2 if type(t).__name__ == 'PCB_VIA']),
         len(list(b2.GetFootprints())),
         len([z for z in b2.Zones() if not z.GetIsRuleArea()])))
