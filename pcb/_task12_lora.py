"""TASK 1+2: correct the J6 LoRa socket mapping, strap M0/M1 to GND, free GPIO10/11."""
import sys, uuid
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
SCH = ROOT + r"\pcb\MoriShield_Carrier.kicad_sch"

# ---- board: J6 pads and J1.16/17 ----
J6 = {"1": "GND", "2": "GND", "3": "/UART1_LORA_TX", "4": "/UART1_LORA_RX",
      "5": "/E22_AUX", "6": "/+5V_E22", "7": "GND"}
J1 = {"16": "unconnected-(J1-IO10-Pad16)", "17": "unconnected-(J1-IO11-Pad17)"}

text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]
edits = []
for fp in root.children:
    if not (isinstance(fp, Node) and fp.head == "footprint"):
        continue
    ref = None
    for p in fp.children:
        if isinstance(p, Node) and p.head == "property":
            a = p.atoms()
            if len(a) >= 2 and atom_str(a[0]) == "Reference":
                ref = atom_str(a[1])
    want = J6 if ref == "J6" else (J1 if ref == "J1" else None)
    if not want:
        continue
    for p in fp.children:
        if isinstance(p, Node) and p.head == "pad":
            num = atom_str(p.atoms()[0])
            if num in want:
                n = p.find("net")
                edits.append((n.start, n.end, '(net "%s")' % want[num]))
out = text
for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]

# ---- board: orientation silk at J6 pin 1 ----
silk = ('\t(gr_text "PIN 1 = M0"\n\t\t(at 268.5 180.6 0)\n\t\t(layer "F.SilkS")\n\t\t(uuid "%s")\n'
        '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1 1)\n\t\t\t\t(thickness 0.15)\n\t\t\t)\n\t\t)\n\t)\n'
        '\t(gr_circle\n\t\t(center 265.6 177.62)\n\t\t(end 266.2 177.62)\n\t\t(stroke\n\t\t\t(width 0.15)\n\t\t\t(type default)\n\t\t)\n'
        '\t\t(fill solid)\n\t\t(layer "F.SilkS")\n\t\t(uuid "%s")\n\t)\n') % (uuid.uuid4(), uuid.uuid4())
idx = out.rstrip().rfind(")")
out = out[:idx] + silk + out[idx:]
open(PCB, "w", encoding="utf-8", newline="").write(out)
print("board: %d pad nets rewritten, silk added" % len(edits))

# ---- schematic: relabel J6 pins by position, free J1.16/17 ----
st = open(SCH, encoding="utf-8").read()
sroot = parse(st)[0]

def at(n):
    a = n.atoms()
    return (round(float(atom_str(a[0])), 2), round(float(atom_str(a[1])), 2))

RENAME = {(482.6, 304.8): "GND", (482.6, 307.34): "UART1_LORA_TX",
          (482.6, 312.42): "E22_AUX", (482.6, 314.96): "+5V_E22", (482.6, 317.5): "GND"}
DROP = {(113.03, 327.66), (113.03, 330.2)}

sedits, dropped = [], []
for c in sroot.children:
    if isinstance(c, Node) and c.head in ("label", "global_label"):
        pos = at(c.find("at"))
        if pos in RENAME:
            a = c.atoms()[0]
            sedits.append((a[0], a[1] if isinstance(a, tuple) else a))
            # replace the first atom (the name)
            first = c.children[0]
            s = c.start
            # locate the name token inside the node
            txt = st[c.start:c.end]
            name_old = atom_str(c.atoms()[0])
            sedits[-1] = (s, s + len('(label "%s"' % name_old), '(label "%s"' % RENAME[pos])
        elif pos in DROP:
            s0 = c.start
            while s0 > 0 and st[s0 - 1] in " \t":
                s0 -= 1
            if s0 > 0 and st[s0 - 1] == "\n":
                s0 -= 1
            sedits.append((s0, c.end, ""))
            dropped.append(pos)
out2 = st
for (s, e, new) in sorted(sedits, key=lambda x: -x[0]):
    out2 = out2[:s] + new + out2[e:]
# add no_connects at the two freed pins
nc = "".join('\t(no_connect\n\t\t(at 115.57 %s)\n\t\t(uuid "%s")\n\t)\n' % (y, uuid.uuid4()) for y in (327.66, 330.2))
idx = out2.rstrip().rfind(")")
out2 = out2[:idx] + nc + out2[idx:]
open(SCH, "w", encoding="utf-8", newline="").write(out2)
print("schematic: %d labels renamed, %d dropped, 2 no_connects added" % (len(RENAME), len(dropped)))
