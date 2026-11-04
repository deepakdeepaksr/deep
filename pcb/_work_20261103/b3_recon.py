"""Batch 3 recon: capacitor symbol pin offsets, highest C reference, D7.1 spot check."""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node  # noqa: E402


def av(v):
    return v[1] if isinstance(v, tuple) else v


root = parse(io.open(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_sch"), encoding="utf-8").read())[0]
refs = []
for s in root.find_all("symbol"):
    props = {av(p.atoms()[0]): av(p.atoms()[1]) for p in s.children
             if isinstance(p, Node) and p.head == "property" and len(p.atoms()) >= 2}
    r = props.get("Reference", "")
    if r.startswith("C") and r[1:].isdigit():
        refs.append(int(r[1:]))
print("highest C reference:", max(refs))
for s in root.find("lib_symbols").children:
    if isinstance(s, Node) and s.head == "symbol" and av(s.atoms()[0]) == "MoriShield_Carrier:C":
        for p in s.find_all("pin"):
            a = p.find("at").atoms()
            print("  C lib pin", av(p.find("number").atoms()[0]), "local",
                  [av(x) for x in a], "len", av(p.find("length").atoms()[0]))
        break
# an existing C instance to clone
for s in root.find_all("symbol"):
    props = {av(p.atoms()[0]): av(p.atoms()[1]) for p in s.children
             if isinstance(p, Node) and p.head == "property" and len(p.atoms()) >= 2}
    if props.get("Reference") == "C41":
        a = s.find("at").atoms()
        print("C41 instance at", [av(x) for x in a], "value", props.get("Value"),
              "fp", props.get("Footprint"))
        break
