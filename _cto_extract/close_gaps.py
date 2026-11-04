import io, re, os, subprocess

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# ---------- 1. FAB_NOTES: quote the manual verbatim ----------
modes = io.open(P + r'\_cto_extract\e22_modes_raw.txt', encoding='utf-8').read()
lines = modes.splitlines()
take = lines[0:40]
verbatim = '\n'.join(l for l in take if l.strip() and not l.startswith('==='))

p = P + r'\revC\FAB_NOTES.md'
t = io.open(p, encoding='utf-8').read()
block = """

## E22 mode selection - quoted verbatim from the manufacturer manual

Source: `_cto_extract\\E22-900T22D-UserManual.txt` (Ebyte E22-900T22D User Manual,
26 pages, from cdebyte.com). Copied into the workspace on 2026-11-04 so this is
checkable without the internet. Previously the note cited sections 6.2-6.5 without
quoting them because the manual was not in the repo - that gap is closed.

| Mode | M0 | M1 | What the manual says |
|---|---|---|---|
| 6.2 Normal (Mode 0) | 0 | 0 | "Users can input data through the serial port and the module will start wireless transmission." Receiving on, output on TXD. |
| 6.3 WOR (Mode 1) | 1 | 0 | Transmitter adds a preamble automatically; receiving "the same as mode 0". |
| 6.4 Configuration (Mode 2) | 0 | 1 | "Wireless transmitting off / Wireless receiving off / Users can access the registers to configure the module's operation state." |
| 6.5 Deep sleep (Mode 3) | 1 | 1 | "Unable to transmit wireless data / Unable to receive wireless data". |

Verbatim extract, sections 6.2 to 6.5:

```
%s
```

### What this means for the straps on this board

- R56 and R57 hold M0 and M1 low, so the module powers into **Mode 0, normal
  transmission** - the configuration Aswin proved over the air.
- **Configuration mode is M0 = 0, M1 = 1.** So removing **R56** (the M1 strap) and
  leaving R57 fitted gives Mode 2, which is the only way to change channel, speed,
  power or address. Both straps fitted is Mode 0; removing R57 alone gives Mode 1
  (WOR), not configuration.
- Section 7.1 adds a constraint for whoever configures a unit: in Mode 2 the module
  supports **9600 8N1 only**, and the register command format is
  `C0 + start address + length + parameters`.
- Note in 6.5: leaving sleep mode re-reads the parameters and holds AUX low during
  that window - relevant to how firmware uses AUX.
""" % verbatim

if 'E22 mode selection - quoted verbatim' not in t:
    t = t.rstrip() + block + '\n'
    io.open(p, 'w', encoding='utf-8', newline='').write(t)
    print('FAB_NOTES.md: verbatim section appended, %d chars' % len(block))
else:
    print('FAB_NOTES.md: section already present')

# ---------- 2. census with copper length and vias-in-pads ----------
census = '''import sys, os
sys.path.insert(0, r"C:\\Program Files\\KiCad\\10.0\\bin")
import pcbnew

"""Census guard - counts, total copper length, and vias inside SMD pads.

A pcbnew Save re-issues every UUID and merges collinear/corner segments, so the
segment count alone can fall with no copper lost. Total copper length is the real
guard. Run before and after every board edit and compare all five numbers.
"""

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "MoriShield_Carrier.kicad_pcb")
b = pcbnew.LoadBoard(path)
tr = list(b.GetTracks())
segs = [t for t in tr if type(t).__name__ != "PCB_VIA"]
vias = [t for t in tr if type(t).__name__ == "PCB_VIA"]
zones = [z for z in b.Zones() if not z.GetIsRuleArea()]
length = sum(((t.GetEnd().x - t.GetStart().x) ** 2 +
              (t.GetEnd().y - t.GetStart().y) ** 2) ** 0.5 for t in segs) / 1e6
inpad = 0
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
            continue
        for v in vias:
            if p.HitTest(v.GetPosition()):
                inpad += 1
nets = set()
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname():
            nets.add(p.GetNetname())
for t in tr:
    if t.GetNetname():
        nets.add(t.GetNetname())
print("footprints %d | segments %d | vias %d | zones %d | nets %d"
      % (len(list(b.GetFootprints())), len(segs), len(vias), len(zones), len(nets)))
print("copper length %.3f mm | vias inside SMD pads %d" % (length, inpad))
'''
p2 = P + r'\pcb\_census.py'
io.open(p2, 'w', encoding='utf-8', newline='').write(census)
print('pcb\\_census.py written')

r = subprocess.run([r'C:\Program Files\KiCad\10.0\bin\python.exe', p2],
                   capture_output=True, text=True, cwd=P)
print(r.stdout.strip() or (r.stderr or '')[:200])
