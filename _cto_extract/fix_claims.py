import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

# ---------------- REPLY_TO_CTO: the prose must match the file ----------------
p = P + r'\REPLY_TO_CTO.md'
t = io.open(p, encoding='utf-8').read()

new = {
 'A7': '| A7 | **Not closed - the measurement is settled, the fix is not in the board.** '
        'Measured: the microSD slot owns GPIO10, 11, 12 and 13 (CS, MOSI, CLK, MISO); GPIO9 and GPIO14 '
        'are not on the slot. So `/E22_M1` on GPIO10 and `/E22_M0` on GPIO11 do conflict with the card, '
        'and `/I2C0_SCL` on GPIO9 is safe. We attempted the strap on 2026-11-03, it did not reach a '
        'clean board, and it was **reverted - the nets are still as they were**. Nothing in this '
        'package claims otherwise | continuity measurement 2026-11-02; `TASK_TRACKER.md` Part 6 '
        'findings 32 and 33; `pcb\\_snap\\T56_reed_20261103_181533\\` | Open - fix not yet in the '
        'files |',
 'C2': '| C2 | The microSD conflict is real and **not yet fixed in the board** (see A7). No 24-hour '
        'run and no 20-power-cut cycle has been performed, and we are not claiming either | '
        '`TASK_TRACKER.md` Part 1 | Open - fix and bench result both owed |',
 'C5': '| C5 | M0 and M1 are on separate pins as the item requires, and both still sit on the '
        'microSD\'s GPIO10 and GPIO11 - **the strap was attempted on 2026-11-03 and reverted, so the '
        'conflict stands in the file**. When it lands: strapping removes in-circuit hardware mode '
        'control, and configuration mode is then reached by lifting one 0 ohm strap with the module out '
        'of its socket. If you want firmware mode control instead, say so before we place parts | pad '
        'nets read from the saved file; Ebyte manual sections 6.2-6.5 | Open - fix not yet in the files |',
 'R11': '| R11 | **Not closed.** We accept C11 - GPIO40 to 42 are the board\'s LEDs and are outputs '
        'only - and the reed is still on GPIO41 in the saved file. The intended destination is GPIO39 '
        '(J2 pin 9), the only free usable input in that block, because GPIO35 to 38 are the octal-PSRAM '
        'group the N16R8 owns. We attempted the move on 2026-11-03; it left ERC and parity non-zero, so '
        'it was reverted. Bench counts at 1, 10 and 50 Hz are also still owed | J2 pad nets read from '
        'the saved file; `pcb\\_snap\\T56_reed_20261103_181533\\` | Open - fix and bench result both owed |',
 'E5': '| E5 | J18 legend correct and verified on the plotted Gerber (0.05 mm from pad centres); board '
        'name, `Rev C` and S/N box printed. **Unchanged finding:** every port name is on F.Fab, which is '
        'not in the Gerber set, so the physical board still carries no port labels. Ten labels were '
        'attempted on 2026-11-03 at 1.0 mm / 0.15 mm and produced 15 silk violations; two repositioning '
        'passes did not clear them, so the attempt was reverted. The blocker is that the bottom silk '
        'band is already occupied by reference fields, which must move first | F.SilkS and F.Fab text '
        'dump; `pcb\\_snap\\T57_silk_20261103_181704\\` | Partly - labels still not printed |',
}
L = t.split('\n')
n = 0
for i, l in enumerate(L):
    m = re.match(r'^\|\s*(A7|C2|C5|R11|E5)\s*\|', l)
    if not m:
        continue
    cols = [c.strip() for c in l.strip().strip('|').split('|')]
    if len(cols) != 4:
        continue                       # leave the §3 answers table alone
    L[i] = new[m.group(1)]
    n += 1
io.open(p, 'w', encoding='utf-8', newline='').write('\n'.join(L))
print('REPLY rows rewritten:', n)

# ---------------- TASK_TRACKER: kill the self-contradiction about J6 ----------------
p2 = P + r'\TASK_TRACKER.md'
t2 = io.open(p2, encoding='utf-8').read()
t2 = t2.replace('remains in mirror image. This is a blocked gate, not a design decision.',
                'remains as designed. **This finding is superseded by finding 32: J6 is NOT '
                'mis-wired** - it is numbered for a 180-degree insertion and all seven nets line up '
                'that way. What was blocked was the physical pin-1 confirmation, which Aswin gave on '
                '2026-11-02.')
# the register rows must not imply the fix landed
t2 = t2.replace('T-55 straps both mode pins to ground and frees them',
                'T-55 straps both mode pins to ground and frees them. **Attempted 2026-11-03 and '
                'reverted - not in the file**')
t2 = t2.replace('T-55 removes that; the 24-hour run is still not planned',
                'T-55 would remove that, but the attempt on 2026-11-03 was reverted; the 24-hour run '
                'is still not planned')
t2 = t2.replace('T-56 moves `/REED_PULSE_F` from J2.7 to J2.9',
                'T-56 moves `/REED_PULSE_F` from J2.7 to J2.9 - **attempted 2026-11-03, reverted, the '
                'reed is still on GPIO41**')
io.open(p2, 'w', encoding='utf-8', newline='').write(t2)
print('TASK_TRACKER contradictions patched; "remains in mirror image" left:',
      t2.count('remains in mirror image'))
