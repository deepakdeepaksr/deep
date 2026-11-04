"""Scratch DRC for a candidate footprint move (library noise filtered)."""
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


def run(ref, cx, cy, rot=None, tag="cand", extra=None):
    tmp = tempfile.mkdtemp(prefix="mv_%s_" % tag)
    b = pcbnew.LoadBoard(PCB)
    fp = b.FindFootprintByReference(ref)
    fp.SetPosition(pcbnew.VECTOR2I(int(round(cx * 1e6)), int(round(cy * 1e6))))
    if rot is not None:
        fp.SetOrientationDegrees(rot)
    if extra:
        extra(b)
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
    print("=== %s -> (%.2f,%.2f) rot %s : %d real violations, %d unconnected" %
          (ref, cx, cy, rot, len(viol), len(d["unconnected_items"])))
    seen = {}
    for v in viol:
        items = " | ".join(i.get("description", "") for i in v.get("items", []))
        seen[(v["type"], items)] = seen.get((v["type"], items), 0) + 1
    for (t, items), n in seen.items():
        print("   %-24s x%-2d %s" % (t, n, items[:150]))
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    run("J5", 224.0, 93.0, 90.0, "a")
    run("J5", 278.0, 146.0, 0.0, "b")
