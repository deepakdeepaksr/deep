"""Add limit_mm / meets / basis to the decoupling map, using the CTO's own wording."""
import csv, collections

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
P = ROOT + r"\revC\decoupling_map.csv"

# Limits quoted from the CTO documents:
#  CHK C9: "for each supply pin, the nearest 100 nF within 5 mm along the copper
#          (3 mm for an IC's own pin), and the bulk capacitor (10 uF or more) within 10 mm"
#  B7:     output capacitor within 5 mm of the regulator's output, 10 uF within 5 mm of its input
#  B12:    100 nF within 10 mm of each named port
IC = ("U", "Q", "D")
PORT = ("J",)

rows = list(csv.DictReader(open(P, encoding="utf-8")))
out = []
for r in rows:
    ref = r["load_ref"]
    is_ic = ref.startswith(IC)
    is_port = ref.startswith(PORT)
    is_tp = ref.startswith("TP")
    cap = r["cap_value"] or ""
    bulk = any(k in cap for k in ("uF",)) and not cap.startswith("0.")
    if is_tp:
        limit, basis = "", "test point, not a load - excluded"
    elif is_ic:
        limit, basis = 3.0, "IC supply pin: 100 nF within 3 mm (CHK C9)"
    elif is_port:
        limit, basis = 5.0, "port supply pin: 100 nF within 5 mm (CHK C9)"
    else:
        limit, basis = 10.0, "passive/other: bulk within 10 mm (B12)"
    try:
        d = float(r["copper_mm"])
    except Exception:
        d = None
    meets = "" if (limit == "" or d is None) else ("yes" if d <= limit else "no")
    r2 = dict(r)
    r2["limit_mm"] = "" if limit == "" else ("%g" % limit)
    r2["meets"] = meets
    r2["basis"] = basis
    out.append(r2)

cols = ["net", "load_ref", "load_pad", "nearest_cap", "cap_value", "copper_mm", "straight_mm",
        "method", "limit_mm", "meets", "basis"]
with open(P, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    w.writerows(out)

tested = [r for r in out if r["meets"] in ("yes", "no")]
ok = [r for r in tested if r["meets"] == "yes"]
bad = [r for r in tested if r["meets"] == "no"]
tp = [r for r in out if r["limit_mm"] == ""]
print("rows %d | tested %d | meet %d | fail %d | excluded %d" % (len(out), len(tested), len(ok), len(bad), len(tp)))
print("failures by load:")
for r in sorted(bad, key=lambda r: -(float(r["copper_mm"]) if r["copper_mm"] else 0)):
    print("  %-14s %-5s.%-3s %-8s %8s mm  limit %-3s  via %s" % (
        r["net"], r["load_ref"], r["load_pad"], r["cap_value"], r["copper_mm"], r["limit_mm"], r["method"]))
