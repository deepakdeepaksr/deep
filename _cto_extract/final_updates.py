import io, re, os, subprocess, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# ---------------- STAGE_TRACKER ----------------
p = P + r'\STAGE_TRACKER.md'
t = io.open(p, encoding='utf-8').read()
t = t.replace('| **Date** | 2026-11-01 |', '| **Date** | 2026-11-02 (measured numbers refreshed 22:45) |')

anchor = '| Table 11 pre-send ticks | 2 of 16 | `TASK_TRACKER.md` Part 3 |'
extra = anchor + """
| **LoRa socket orientation** | J6 is numbered for a **180-degree insertion** and all seven nets line up that way - it is **not** mis-wired. But nothing marks it: no silk, pads named 1-7 only, header unkeyed | `pcb` J6 pad nets; Ebyte E22-900T22D manual section 3; Aswin's pin-1 reading 2026-11-02 |
| **microSD, measured** | slot owns **GPIO10, 11, 12, 13** (CS, MOSI, CLK, MISO). **GPIO9 and GPIO14 are not on the slot**, so `/I2C0_SCL` on GPIO9 is safe. CHK-001 C11 is right about 10-13, wrong to include 14 | Aswin's continuity test 2026-11-02 |
| **Open design changes not yet in the board** | T-55 strap E22 M0/M1 to GND through 0 ohm (frees the microSD); T-56 move the reed from GPIO41 to **GPIO39** (J2.9); T-57 print port labels on F.SilkS; T-58 keyed header | `TASK_TRACKER.md` Part 5 |
| **Port labels do not print** | 9 items on F.SilkS; every port name is on **F.Fab**, which is not in the Gerber set. J21 is the FDC1004 (channel 5); J17 and J20 have no identified sensor | text dump by layer 2026-11-02 |
| **ESP32 antenna** | identified as the **J1/J2 pin-1 end** (left row 3V3/3V3/RST, right row GND/TX/RX). The outline gives only 2.5 mm past that row where the board has about 11.6 mm, so the outline is short and the keep-out is not yet drawn. **Awaiting Aswin's tip-to-pin measurement** | vendor photo and board geometry 2026-11-02 |"""
t = t.replace(anchor, extra)

# S3 row: E1 is met, so it must not still be listed as a blocker
t = re.sub(r'E1 \(stitching fails the 10 mm rule\)', 'E1 met 2026-11-02 (143 links, max 10.00 mm)', t)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('STAGE_TRACKER updated; E1-as-blocker mentions left:', t.count('stitching fails'))

# ---------------- regenerate the response sheet ----------------
gen = os.path.join(P, 'pcb', '_make_response_sheet.py')
if os.path.exists(gen):
    r = subprocess.run(['python', gen], capture_output=True, text=True, cwd=P, timeout=600)
    print('CSV generator:', (r.stdout or r.stderr or '').strip().replace('\n', ' | ')[:300])
else:
    print('CSV generator NOT FOUND - ResponseSheet may now disagree with the reply')

# ---------------- verify ----------------
import csv
rows = list(csv.reader(io.open(P + r'\revC\ResponseSheet_RevC.csv', encoding='utf-8-sig')))
print('CSV rows:', len(rows) - 1)
for key in ('A7', 'C2', 'C5', 'R11', 'E5'):
    for rr in rows[1:]:
        if rr[0] == key:
            print('   %-4s %s' % (key, rr[4][:70]))
