import collections
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pcb"))
from _sexp import parse, Node, atom_str  # noqa: E402

text = io.open(os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb"), encoding="utf-8").read()
root = parse(text)[0]
print("root head:", root.head)
print("child heads:", collections.Counter(c.head for c in root.children if isinstance(c, Node)).most_common(12))
for c in root.children:
    if isinstance(c, Node) and c.head == "net":
        print("net node at", c.start, repr(text[c.start:c.end])[:60])
        break
# find any node with head net, anywhere
hits = [n for n in root.find_all("net")][:3]
for n in hits:
    print("nested net:", repr(text[n.start:n.end])[:80])
