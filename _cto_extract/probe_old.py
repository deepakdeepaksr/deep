import sys
sys.path.insert(0, r"C:\Program Files\KiCad\10.0\bin")
import pcbnew, collections

p = r"c:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\cto remarks\old remarks\design\MoriShield_Carrier.kicad_pcb"
b = pcbnew.LoadBoard(p)
print("file:", p)
print("size mm: %.2f x %.2f" % (b.GetBoardEdgesBoundingBox().GetWidth() / 1e6,
                                b.GetBoardEdgesBoundingBox().GetHeight() / 1e6))
print("footprints:", len(list(b.GetFootprints())), "nets:", b.GetNetCount())
print("copper layers:", b.GetCopperLayerCount())
fps = {fp.GetReference(): fp for fp in b.GetFootprints()}
for r in ("U1", "J9", "D1", "J18", "J5", "U4", "U7", "U8", "Q9", "F1", "J19"):
    if r in fps:
        fp = fps[r]
        print(f"  {r}: {str(fp.GetFPID().GetLibItemName())} at {fp.GetPosition().x/1e6:.1f},{fp.GetPosition().y/1e6:.1f}")
    else:
        print(f"  {r}: absent")
nets = [b.GetNetname(n) for n in range(b.GetNetCount())]
rs = sorted(n for n in set(nets) if n and ("RS485" in n or n in ("+12V", "+5V", "SDA0", "SCL0")))
print("selected nets:", rs)
