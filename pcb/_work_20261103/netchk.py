import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
s = io.open(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"), encoding="utf-8").read()
for n in ("E22_M1_STRAP", "E22_M0_STRAP", "unconnected-(J1-IO10-Pad16)", "/E22_M1", "/E22_M0"):
    print("%-32s %d" % (n, s.count('"%s"' % n)))
print("--- shallowest (net \"...\") lines:")
shown = 0
for l in s.split("\n"):
    t = l.lstrip("\t")
    if t.startswith('(net "') and l.count("\t") <= 1:
        print("tabs=%d %r" % (l.count("\t"), l.strip()[:60]))
        shown += 1
        if shown >= 3:
            break
