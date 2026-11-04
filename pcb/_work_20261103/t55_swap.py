"""Swap the net names on R56/R57 pads 1 and 2 so the board matches the schematic's pin order."""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")
text = io.open(PCB, encoding="utf-8").read()

for ref, strap in (("R56", "E22_M1_STRAP"), ("R57", "E22_M0_STRAP")):
    m = re.search(r'\(footprint "Resistor_SMD:R_0603_1608Metric"[\s\S]*?"%s"[\s\S]*?\n\t\)' % ref, text)
    if not m:
        # fall back: locate the block by reference property
        m = re.search(r'\(footprint "Resistor_SMD:R_0603_1608Metric"[\s\S]{0,4000}?\(property "Reference" "%s"' % ref, text)
        raise SystemExit("block match failed for %s" % ref)
    block = m.group(0)
    p1 = re.search(r'\(pad "1"[\s\S]*?\(net "[^"]*"\)', block).group(0)
    p2 = re.search(r'\(pad "2"[\s\S]*?\(net "[^"]*"\)', block).group(0)
    n1 = re.search(r'\(net "[^"]*"\)', p1).group(0)
    n2 = re.search(r'\(net "[^"]*"\)', p2).group(0)
    new_block = block.replace(p1, p1.replace(n1, n2), 1).replace(p2, p2.replace(n2, n1), 1)
    text = text[:m.start()] + new_block + text[m.end():]
    print("%s: pad1 %s, pad2 %s -> swapped" % (ref, n1, n2))

io.open(PCB, "w", encoding="utf-8", newline="").write(text)
print("written")
