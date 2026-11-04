"""TASK 3: print port names on F.SilkS beside each connector, plus J6 pin functions."""
import pcbnew, uuid

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
b = pcbnew.LoadBoard(PCB)

NAMES = {
    "J7": "GY-521", "J8": "DS3231", "J11": "SGP41", "J12": "SHT45", "J13": "SPS30",
    "J14": "BME688", "J15": "SOIL", "J16": "FSR", "J22": "REED", "J26": "AS5600",
}
pos = {}
for f in b.GetFootprints():
    r = f.GetReference()
    if r in NAMES or r in ("J6", "J17", "J20"):
        pos[r] = (f.GetPosition().x / 1e6, f.GetPosition().y / 1e6)

def txt(s, x, y, size=1.0):
    return ('\t(gr_text "%s"\n\t\t(at %s %s 0)\n\t\t(layer "F.SilkS")\n\t\t(uuid "%s")\n\t\t(effects\n'
            '\t\t\t(font\n\t\t\t\t(size %s %s)\n\t\t\t\t(thickness 0.15)\n\t\t\t)\n\t\t)\n\t)\n'
            % (s, x, y, uuid.uuid4(), size, size))

blk = ""
placed = []
for ref, name in NAMES.items():
    if ref not in pos:
        continue
    x, y = pos[ref]
    # place the label above the connector, clear of its pads
    ty = round(y - 5.4, 2)
    blk += txt(name, round(x, 2), ty)
    placed.append((ref, name, round(x, 2), ty))

# J6: function labels at each pad end and an orientation note
if "J6" in pos:
    x, y = pos["J6"]
    blk += txt("E22 GND END", round(x + 6.2, 2), round(y + 2.4, 2))
    blk += txt("M0", round(x + 4.6, 2), 177.6)
    blk += txt("M1", round(x + 4.6, 2), 175.1)
    blk += txt("VCC", round(x + 4.6, 2), 172.6)

text = open(PCB, encoding="utf-8").read()
idx = text.rstrip().rfind(")")
open(PCB, "w", encoding="utf-8", newline="").write(text[:idx] + blk + text[idx:])
print("labels placed: %d port names + 4 J6 marks" % len(placed))
for p in placed:
    print("   %-4s %-8s at (%.2f, %.2f)" % p)
