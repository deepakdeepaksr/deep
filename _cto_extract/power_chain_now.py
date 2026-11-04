"""Dump current pad nets for the J18 power-input chain (Rev C board, 4-layer).

Writes evidence to pcb\\_evidence\\power_chain_pads.json and prints a table.
Uses the minimal KiCad s-expression reader in _audit6l\\sexpr.py.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.join("_audit6l"))
from sexpr import parse  # noqa: E402

BOARD = os.path.join("pcb", "MoriShield_Carrier.kicad_pcb")
OUT = os.path.join("pcb", "_evidence", "power_chain_pads.json")
WANT = ["J18", "F1", "U10", "Q9", "D2", "C13", "C31", "ESD16", "D7", "J5", "TP2"]


def prop(block, name):
    for it in block:
        if isinstance(it, list) and len(it) >= 2 and it[0] == "property" and it[1] == name:
            return it[2]
    return None


def pads(block):
    out = []
    for it in block:
        if isinstance(it, list) and it and it[0] == "pad":
            net = None
            for sub in it:
                if isinstance(sub, list) and sub and sub[0] == "net":
                    # KiCad 10 writes (net "NAME"); older writes (num "NAME")
                    for tok in sub[1:]:
                        if isinstance(tok, str):
                            net = tok
                            break
            out.append({"pad": it[1], "type": it[2] if len(it) > 2 else None,
                        "net": net})
    return out


root = parse(io.open(BOARD, encoding="utf-8").read())
result = {}
for it in root:
    if isinstance(it, list) and it and it[0] == "footprint":
        ref = prop(it, "Reference")
        if ref in WANT:
            result[ref] = {
                "value": prop(it, "Value"),
                "library_id": it[1] if len(it) > 1 else None,
                "pads": pads(it),
            }

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8").write(json.dumps(result, indent=1))

for ref in WANT:
    d = result.get(ref)
    if not d:
        print("%-5s MISSING" % ref)
        continue
    nets = ["%s:%s" % (p["pad"], p["net"] or "-") for p in d["pads"]]
    print("%-5s %-14s %-46s %s" % (ref, d["value"], (d["library_id"] or "").split(":")[-1],
                                   "  ".join(nets)))
print("\nwrote", OUT)
