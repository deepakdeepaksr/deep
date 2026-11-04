import csv, io, sys
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(P + r'\pcb\MoriShield_Carrier.kicad_pcb')
fps = {fp.GetReference() for fp in b.GetFootprints()}
pos = {r[0] for r in list(csv.reader(io.open(P + r'\revC\MoriShield_Carrier_RevC_pos_front.csv',
                                             encoding='utf-8-sig')))[1:] if r}
miss = sorted(fps - pos, key=lambda x: (len(x), x))
print('footprints %d   in placement %d   absent from placement %d'
      % (len(fps), len(pos), len(miss)))
print('in placement but not on board:', sorted(pos - fps) or 'none')
d = {fp.GetReference(): fp for fp in b.GetFootprints()}
for r in miss:
    fp = d[r]
    print('   %-6s %-44s pads=%-3d excl_pos=%-5s board_only=%-5s layer=%s'
          % (r, str(fp.GetFPID().GetLibItemName())[:44], len(list(fp.Pads())),
             fp.IsExcludedFromPosFiles(), fp.IsBoardOnly(), b.GetLayerName(fp.GetLayer())))
