import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\REPLY_TO_CTO.md'
t = io.open(p, encoding='utf-8').read()

# ---------- 1. rewrite the five affected response-sheet rows ----------
rows = {
 'A7': '| A7 | **Settled by measurement, and the fix is scheduled.** We metered the microSD slot on '
        'the EdgeHax board: slot pin 2 to **GPIO10**, pin 3 to **GPIO11**, pin 5 to **GPIO12**, pin 7 to '
        '**GPIO13**, pin 4 to 3V3, pin 6 to GND, and **nothing on GPIO9**. CHK-001 C11 is therefore right '
        'about GPIO10-13 and wrong to include GPIO14. The violation was real - `/E22_M1` sat on GPIO10 '
        '(the card\'s CS) and `/E22_M0` on GPIO11 (its MOSI). Both mode pins are being strapped to ground '
        'through 0 ohm resistors, which frees the card and matches the configuration we already ran over '
        'the air | continuity measurement, Aswin 2026-11-02; Ebyte E22-900T22D manual section 3; '
        '`TASK_TRACKER.md` Part 6 findings 32-33 | Partly - conflict removed by T-55, firmware map still '
        'to be signed |',
 'C2': '| C2 | The microSD conflict is resolved as per A7, so the slot is usable. **No 24-hour run and no '
        '20-power-cut cycle has been performed**, and we are not claiming either | '
        '`TASK_TRACKER.md` Part 1; bench plan owed | Partly - bench result owed |',
 'C5': '| C5 | M0 and M1 stay on separate pins as the item requires, and both move to a grounded 0 ohm '
        'strap, off the microSD pins. **Recorded honestly: strapping them removes in-circuit hardware mode '
        'control.** Configuration mode is then reached by lifting one strap, which is possible because the '
        'module is socketed and the strap resistors are reachable with it removed. If you want mode control '
        'from firmware instead, say so before we place the straps | pad nets; Ebyte manual sections 6.2-6.5; '
        '`TASK_TRACKER.md` T-55 | Partly - read-back over UART unaffected, strap decision requested (8c) |',
 'R11': '| R11 | **Closed by us, not waiting on you.** We accept C11: GPIO40-42 are the board\'s LEDs and are '
        'outputs only. The reed moves from GPIO41 to **GPIO39 (J2 pin 9)**, which is the only free usable input '
        'in that block - GPIO35-38 are the octal-PSRAM group the N16R8 module owns and GPIO40 is LED-only. '
        'Bench counts against a reference at 1, 10 and 50 Hz are still owed | pad nets; continuity and pin-name '
        'reading 2026-11-02; CHK-001 C11 | Partly - pin moved by T-56, bench counts owed |',
 'E5': '| E5 | J18 legend correct and verified on the plotted Gerber (0.05 mm from pad centres); board name, '
        '`Rev C` and S/N box printed. **New finding:** every port name on this board (`J15 SOIL`, `J11 SGP41`, '
        '`J12 SHT45`, `J13 SPS30`, `J14 BME688`, `GY-521`, `DS3231 RTC`, `J5 MODEM 5V`) is drawn on **F.Fab, '
        'which is not in the Gerber set** - only nine items are on F.SilkS, so a builder sees no port labels at '
        'all. Being fixed by T-57 | F.SilkS and F.Fab text dump 2026-11-02; `revC\\silk_check\\` | Partly - '
        'labels to be moved to a printed layer |',
}
n = 0
L = t.split('\n')
for i, l in enumerate(L):
    m = re.match(r'^\|\s*(A7|C2|C5|R11|E5)\s*\|', l)
    if m and '**Settled by measurement' not in l and 'New finding' not in l:
        # only the §1/§2 response-sheet rows have 4 columns and no date column
        cols = [c.strip() for c in l.strip().strip('|').split('|')]
        if len(cols) == 4:
            L[i] = rows[m.group(1)]
            n += 1
t = '\n'.join(L)
print('response rows replaced:', n)

# ---------- 2. add the new Serigreen questions after the whole 8a paragraph ----------
Lq = t.split('\n')
start = next(n for n, l in enumerate(Lq) if l.startswith('8a. '))
end = start + 1
while end < len(Lq) and not re.match(r'^\s*\d{1,2}[a-z]?\.\s', Lq[end]) and not Lq[end].startswith('**'):
    end += 1
print('8a paragraph spans lines %d..%d' % (start + 1, end))
NEW_Q_LIST = [q for q in """8b. **A correction to CHK-001 C11, with the measurement behind it.** C11 states "GPIO10 to 14 are the
board's own microSD". Our continuity test on the board you supply gives **GPIO10, 11, 12 and 13** - the
card's CS, MOSI, CLK and MISO - and **GPIO14 is not connected to the slot**, nor is GPIO9. That matters
because `/I2C0_SCL` sits on GPIO9 and is safe, and because a rule that bans GPIO14 costs us a pin we do
not need to ban. Please confirm or correct.

8c. **E22 mode pins - one decision we would like from you before we place parts.** We intend to strap M0
and M1 to ground through 0 ohm resistors, which is what the module's manual permits and what we ran over
the air. The trade is that hardware mode control is then only available by lifting a strap with the module
removed from its socket. If you want mode control from firmware instead, we will move M0 and M1 to two
spare pins on the I/O expander - say so now, because it changes the parts we order.

8d. **E22 supply rail.** The board feeds the LoRa module from 5 V. Its TXD and AUX outputs are TTL and
follow the supply, and the ESP32-S3 is not 5 V tolerant, so we propose moving the module to the 3.3 V
rail - which is also how we tested it. Confirm you have no objection, or tell us to keep 5 V and add the
manual's 4-10 k pull-ups instead.

8e. **Two ports we cannot identify.** J17 (channel 4) and J20 (channel 6) are fully wired 4-pin I2C ports
with ESD arrays and pull-ups, and nothing in 003, 004, the schematic or our notes says which sensor goes
in them. J20 is one of the two runs blocking the LoRa antenna keep-out, so if it is spare we can free the
corridor; if it is not, we reroute. Which is it?

8f. **Keyed headers.** J6, J3 and J4 are unkeyed, so a module can be inserted rotated 180 degrees. We are
adding silkscreen so it is obvious, but only a key makes it impossible. Do you want a shrouded or keyed
header specified, and at what cost limit?""".split('\n')]

Lq[end:end] = NEW_Q_LIST
t = '\n'.join(Lq)
print('questions 8b-8f inserted at line', end + 1)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('REPLY_TO_CTO written, lines', len(t.split('\n')))
