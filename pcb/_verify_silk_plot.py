"""Verify polarity marks on the PLOTTED F.SilkS Gerber, with measured offsets to the pad they label."""
import re, sys, math
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str
import pcbnew

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
GBR = ROOT + r"\revC\silk_check\MoriShield_Carrier-F_Silkscreen.gto"
PCB = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"

# ---- parse the plotted silk: every draw/flash coordinate ----
txt = open(GBR, encoding="utf-8", errors="ignore").read()
xs, ys = [], []
cur = None
for line in txt.splitlines():
    m = re.match(r"^(?:X(-?\d+))?(?:Y(-?\d+))?D0?([123])\*$", line.strip())
    if m:
        if m.group(1):
            cur = [int(m.group(1)) / 1e6, cur[1] if cur else 0.0]
        if m.group(2):
            cur = [cur[0] if cur else 0.0, int(m.group(2)) / 1e6]
        if cur:
            xs.append(cur[0]); ys.append(-cur[1])
print("plotted silk strokes: %d points, x %.2f..%.2f y %.2f..%.2f" % (len(xs), min(xs), max(xs), min(ys), max(ys)))

# ---- expected marks from the board ----
b = pcbnew.LoadBoard(PCB)
pads = {}
for f in b.GetFootprints():
    for p in f.Pads():
        pads[(f.GetReference(), p.GetNumber())] = (p.GetPosition().x / 1e6, p.GetPosition().y / 1e6,
                                                   p.GetSize().x / 1e6, p.GetSize().y / 1e6)

def near(px, py, r):
    return [(x, y) for (x, y) in zip(xs, ys) if abs(x - px) <= r and abs(y - py) <= r]

def bbox(pts):
    xs2 = [p[0] for p in pts]; ys2 = [p[1] for p in pts]
    return (min(xs2), min(ys2), max(xs2), max(ys2))

# board-level texts, from the file
text = open(PCB, encoding="utf-8").read()
root = parse(text)[0]
texts = []
for d in root.children:
    if isinstance(d, Node) and d.head == "gr_text" and d.value("layer") == "F.SilkS":
        a = d.atoms()
        at = d.find("at").atoms()
        texts.append((atom_str(a[0]), float(atom_str(at[0])), float(atom_str(at[1]))))
print("board silk texts on the board file:", [t[0] for t in texts])

rows = []
# 1. J18 polarity marks vs pads 1 and 2
for label, pad in (("5v +", ("J18", "1")), ("5v -", ("J18", "2"))):
    t = next((x for x in texts if x[0] == label), None)
    if not t:
        rows.append((label, "MISSING ON BOARD", "", "", "FAIL")); continue
    pts = near(t[1], t[2], 2.5)
    if not pts:
        rows.append((label, "NOT IN PLOT", "", "", "FAIL")); continue
    bb = bbox(pts)
    cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    px, py, w, h = pads[pad]
    rows.append((label, "%s.%s" % pad, "%.2f" % (cx - px), "%.2f" % (cy - py),
                 "OK" if abs(cx - px) <= 1.2 and abs(cy - py) <= 3.0 else "CHECK"))

# 2. board identity marks
for label in ("MoriShield Carrier", "Rev C", "S/N"):
    t = next((x for x in texts if x[0] == label), None)
    ok = bool(t) and bool(near(t[1], t[2], 6.0))
    rows.append((label, "board identity", "-", "-", "OK" if ok else "FAIL"))

# 3. footprint polarity marks: does plotted silk exist within the part's own outline?
for ref in ("D2", "D3", "D4", "D6", "D7", "ESD1", "ESD2", "ESD3", "ESD4", "ESD7", "ESD8", "ESD9",
            "ESD10", "ESD11", "ESD12", "ESD16", "ESD17", "ESD18", "ESD19", "ESD20",
            "U10", "C13", "C45", "C47", "J5", "J19", "J24", "J25", "Q9"):
    fp = None
    for f in b.GetFootprints():
        if f.GetReference() == ref:
            fp = f; break
    if fp is None:
        rows.append((ref, "no such part", "-", "-", "N/A")); continue
    cx, cy = fp.GetPosition().x / 1e6, fp.GetPosition().y / 1e6
    pts = near(cx, cy, 5.0)
    rows.append((ref, "silk near part centre", "%.2f" % (bbox(pts)[0] - cx) if pts else "-",
                 "%.2f" % (bbox(pts)[1] - cy) if pts else "-", "OK" if pts else "NO SILK"))

print()
print("%-22s %-24s %8s %8s  %s" % ("mark", "labels", "dx mm", "dy mm", "verdict"))
for r in rows:
    print("%-22s %-24s %8s %8s  %s" % r)
