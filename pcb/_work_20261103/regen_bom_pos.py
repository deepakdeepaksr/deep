"""Regenerate the BOM and both placement files from the saved board, in the formats
pack.ps1 already expects."""
import collections
import csv
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
OUT = os.path.join(ROOT, "revC")
CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"


def ref_key(r):
    m = re.match(r"([A-Za-z]+)(\d+)", r)
    return (m.group(1), int(m.group(2))) if m else (r, 0)


def merge(refs):
    refs = sorted(set(refs), key=ref_key)
    out = []
    i = 0
    while i < len(refs):
        pre, num = ref_key(refs[i])
        j = i
        while (j + 1 < len(refs) and ref_key(refs[j + 1])[0] == pre
               and ref_key(refs[j + 1])[1] == ref_key(refs[j])[1] + 1):
            j += 1
        if j - i >= 2:
            out.append("%s%d-%s%d" % (pre, num, pre, ref_key(refs[j])[1]))
        else:
            out.extend(refs[i:j + 1])
        i = j + 1
    return ",".join(out)


b = pcbnew.LoadBoard(PCB)
groups = collections.defaultdict(list)
for f in b.GetFootprints():
    fp = "%s:%s" % (str(f.GetFPID().GetLibNickname()), str(f.GetFPID().GetLibItemName()))
    groups[(f.GetValue(), fp)].append(f.GetReference())

rows = []
for (val, fp), refs in sorted(groups.items(), key=lambda kv: ref_key(sorted(kv[1])[0])):
    rows.append([merge(refs), val, fp, str(len(refs)), "", "", "", "", "", ""])
with open(os.path.join(OUT, "MoriShield_Carrier_RevC_bom.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, quoting=csv.QUOTE_ALL)
    w.writerow(["Refs", "Value", "Footprint", "Qty", "DNP", "Manufacturer", "MPN", "Rating", "Temp", "Variant"])
    w.writerows(rows)
print("BOM rows", len(rows))

for side in ("front", "back"):
    dst = os.path.join(OUT, "MoriShield_Carrier_RevC_pos_%s.csv" % side)
    subprocess.run([CLI, "pcb", "export", "pos", "--format", "csv", "--units", "mm",
                    "--side", side, "-o", dst, PCB], check=False, capture_output=True)
    print("POS", side, "written")
