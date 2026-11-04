"""Scratch DRC for J26 candidates: footprint only, library noise filtered out."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
PRO = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pro")
DRU = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_dru")
CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
IGNORE = {"lib_footprint_issues", "footprint_link_issues", "lib_symbol_issues"}


def run(cx, cy, rot=0.0, tag="cand"):
    tmp = tempfile.mkdtemp(prefix="j26_%s_" % tag)
    b = pcbnew.LoadBoard(PCB)
    fp = b.FindFootprintByReference("J26")
    fp.SetPosition(pcbnew.VECTOR2I(int(round(cx * 1e6)), int(round(cy * 1e6))))
    if rot:
        fp.SetOrientationDegrees(rot)
    out = os.path.join(tmp, "MoriShield_Carrier.kicad_pcb")
    b.Save(out)
    shutil.copy(PRO, os.path.join(tmp, "MoriShield_Carrier.kicad_pro"))
    shutil.copy(DRU, os.path.join(tmp, "MoriShield_Carrier.kicad_dru"))
    rep = os.path.join(tmp, "drc.json")
    subprocess.run([CLI, "pcb", "drc", "--refill-zones", "--schematic-parity", "--severity-all",
                    "--all-track-errors", "--format", "json", "-o", rep, out],
                   check=False, capture_output=True)
    d = json.load(open(rep, encoding="utf-8"))
    viol = [v for v in d["violations"] if v["type"] not in IGNORE]
    print("=== J26 (%.2f,%.2f) rot %.0f : %d real violations, %d unconnected" %
          (cx, cy, rot, len(viol), len(d["unconnected_items"])))
    seen = {}
    for v in viol:
        items = " | ".join(i.get("description", "") for i in v.get("items", []))
        key = (v["type"], items)
        seen[key] = seen.get(key, 0) + 1
    for (t, items), n in seen.items():
        print("   %-22s x%-2d %s" % (t, n, items[:150]))
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    for (x, y, r, t) in [(205.0, 194.5, 0, "a"), (209.5, 195.0, 0, "b"), (221.0, 194.5, 0, "c"),
                         (133.0, 155.0, 90, "d"), (296.0, 194.5, 0, "e")]:
        run(x, y, r, t)
