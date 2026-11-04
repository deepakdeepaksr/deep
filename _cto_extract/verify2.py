import sys
sys.path.insert(0, r"C:\Program Files\KiCad\10.0\bin")
import pcbnew

b = pcbnew.LoadBoard(r"c:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\4L\MoriShield_Carrier.kicad_pcb")
fps = list(b.GetFootprints())
print("footprints:", len(fps), "nets:", b.GetNetCount())
bb = b.GetBoardEdgesBoundingBox()
print("board size mm: %.2f x %.2f" % (bb.GetWidth() / 1e6, bb.GetHeight() / 1e6))

d = {fp.GetReference(): fp for fp in fps}
for r in ("J1", "J2", "J3", "J4"):
    if r in d:
        p = d[r].GetPosition()
        print(r, "%.2f,%.2f" % (p.x / 1e6, p.y / 1e6), d[r].GetFPID().GetLibItemName())
if all(r in d for r in ("J1", "J2", "J3", "J4")):
    print("J1-J2 spacing %.2f" % ((d["J2"].GetPosition().x - d["J1"].GetPosition().x) / 1e6))
    print("J3-J4 spacing %.2f" % ((d["J4"].GetPosition().x - d["J3"].GetPosition().x) / 1e6))
    print("J1 y %.2f  J3 y %.2f" % (d["J1"].GetPosition().y / 1e6, d["J3"].GetPosition().y / 1e6))

print("mounting holes:", [fp.GetReference() for fp in fps if str(fp.GetFPID().GetLibItemName()).startswith("MountingHole")])
for r in ("TP1", "TP2", "TP3", "TP4", "TP5", "J24", "J25", "J20", "J13", "J6", "J21", "J16"):
    if r in d:
        p = d[r].GetPosition()
        print(r, "%.2f,%.2f" % (p.x / 1e6, p.y / 1e6), str(d[r].GetFPID().GetLibItemName()),
              [p.GetNetname() for p in d[r].Pads()][:6])

# U7/U8 i2c net check
for r in ("U7", "U8"):
    if r in d:
        for p in d[r].Pads():
            n = p.GetNetname()
            if "I2C" in n or "SDA" in n or "SCL" in n:
                print(r, "pad", p.GetNumber(), n)

# Q2/Q3 gate nets
for r in ("Q2", "Q3", "Q4", "Q1", "Q5", "Q6", "Q7"):
    if r in d:
        print(r, [p.GetNetname() for p in d[r].Pads()])
