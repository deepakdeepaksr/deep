import sys, os
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
path = os.path.join(base, 'pcb', 'MoriShield_Carrier.kicad_pcb')
b = pcbnew.LoadBoard(path)

tr = list(b.GetTracks())
a = tr[0]
print('sample item type:', type(a).__name__, 'Type():', a.Type(),
      'PCB_TRACK_T =', pcbnew.PCB_TRACK_T, 'PCB_VIA_T =', pcbnew.PCB_VIA_T)
try:
    print('sample uuid str:', repr(str(a.GetUUID())), repr(a.GetUUID()))
except Exception as e:
    print('GetUUID failed:', e)
v = [t for t in tr if t.Type() == pcbnew.PCB_VIA_T][0]
print('via  uuid str:', repr(str(v.GetUUID())))
print('via  GetStart type:', type(v.GetStart()).__name__)
