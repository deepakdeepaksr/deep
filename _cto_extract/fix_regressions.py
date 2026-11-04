import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

OLD_E1 = 'max 10.00 mm, 0.0 % beyond 10 mm, 143 links'
NEW_E1 = 'max 11.16 mm, 0.1 % beyond 10 mm, 144 links'

# ---------------- TASK_TRACKER ----------------
p = P + r'\TASK_TRACKER.md'
t = io.open(p, encoding='utf-8').read()

t = t.replace('| GND plane distance to a ground link | **max 10.00 mm, 0.0 % beyond 10 mm, 143 links in both pours**',
              '| GND plane distance to a ground link | **REGRESSED 2026-11-03: max 11.16 mm, 0.1 % beyond 10 mm, '
              '144 links in both pours** (was 10.00 mm / 0.0 % / 143 before the J5, J26 and +5V copper moves)')
t = t.replace('| Vias inside SMD pads | **65 of 314**',
              '| Vias inside SMD pads | **67 of 314** - two new vias landed in pads during the 2026-11-03 '
              'placement work (was 65). `revC\\vias_in_pads.txt` and `revC\\FAB_NOTES.md` still say 65 and are stale')
t = t.replace('| E1 | P1 | 004 T9 | "Stitching plot: no point of either ground pour more than 10 mm from a ground link (antenna keep-out excepted)." | Done |',
              '| E1 | P1 | 004 T9 | "Stitching plot: no point of either ground pour more than 10 mm from a ground link (antenna keep-out excepted)." | **New** |')
t = t.replace('**65 of 314 vias sit inside an SMD pad**', '**67 of 314 vias sit inside an SMD pad**')
t = t.replace('65 vias in pads with no fab note agreed', '67 vias in pads; the fab note still quotes 65 and must be regenerated')
t = t.replace('silk 0; every footprint now has a courtyard', 'silk 0; every footprint has a courtyard')

L = t.split('\n')
for i, l in enumerate(L):
    if l.startswith('| E1 | P1 | 004 T9 |') and 'New** |' in l:
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) >= 7:
            c[5] = ('**Regressed 2026-11-03.** Re-measured after the J5, J26 and In2 +5V copper moves: '
                    '144 links, worst distance **11.16 mm**, **0.1 %** beyond 10 mm - the 10 mm acceptance is '
                    'broken again. Nobody re-ran the metric, so every document still said Done')
            c[6] = '`pcb\\_plot_stitching_final.py` re-run 2026-11-03; `revC\\E1_stitching_plot.png`'
            L[i] = '| ' + ' | '.join(c) + ' |'
t = '\n'.join(L)
t += """

**2026-11-03 late additions to Part 6.**

37. **E1 regressed and nobody noticed, because the metric is not part of DRC.**
    The stitching acceptance is a separate measurement, so a copper change that
    passes DRC 0 can silently break it. Re-measured after the placement work:
    144 links, worst **11.16 mm**, **0.1 %** beyond 10 mm. E1 was recorded as Done
    in all four documents. Standing rule: re-run `pcb\\_plot_stitching_final.py`
    after any copper or via change, before any document repeats the old number.

38. **Vias inside SMD pads went 65 to 67.** Two more were introduced by the
    2026-11-03 reroutes. `revC\\vias_in_pads.txt` and the fab note in
    `revC\\FAB_NOTES.md` still state 65 of 314, so check C5's evidence is now
    quoting a number the board does not match. Regenerate both before the package
    goes anywhere.
"""
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('TASK_TRACKER patched')

# ---------------- STAGE_TRACKER ----------------
p = P + r'\STAGE_TRACKER.md'
t = io.open(p, encoding='utf-8').read()
t = t.replace('| GND plane distance to a ground link | max 10.00 mm, 0.0 % beyond 10 mm, 143 links in both pours |',
              '| GND plane distance to a ground link | **REGRESSED: max 11.16 mm, 0.1 % beyond 10 mm, 144 links** |')
t = t.replace('| Vias in SMD pads | 65 of 314, fab note in place (check C5 met) |',
              '| Vias in SMD pads | **67 of 314** (was 65); the fab note still says 65 and must be regenerated |')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('STAGE_TRACKER patched')

# ---------------- REPLY_TO_CTO ----------------
p = P + r'\REPLY_TO_CTO.md'
t = io.open(p, encoding='utf-8').read()
L = t.split('\n')
for i, l in enumerate(L):
    if re.match(r'^\|\s*E1\s*\|', l):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) == 4:
            c[1] = ('**Regressed, and we caught it by re-measuring.** A GND pour was added on B.Cu with 85 '
                    'stitching vias, which took the worst distance to 10.00 mm and 0.0 % beyond. The placement '
                    'and reroute work of 2026-11-03 moved copper again, and re-measurement now gives **144 '
                    'links, worst 11.16 mm, 0.1 % beyond 10 mm** - outside your 10 mm acceptance. The stitching '
                    'metric is not a DRC check, so a clean DRC did not warn us; that is now a standing step '
                    'after any copper change')
            c[3] = 'Open - regressed, fix owed'
            L[i] = '| ' + ' | '.join(c) + ' |'
    if re.match(r'^\|\s*R16\s*\|', l):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) == 4:
            c[1] = c[1].replace('65 of 314', '67 of 314').replace('65 vias', '67 vias')
            c[1] += ' (count rose from 65 to 67 during the 2026-11-03 reroutes; the fab note is being regenerated to match)'
            L[i] = '| ' + ' | '.join(c) + ' |'
    if '7. **Vias in SMD pads (R16).**' in L[i]:
        L[i] = L[i].replace('7. **Vias in SMD pads (R16).**',
                            '7. **Vias in SMD pads (R16), now 67 of 314.**')
        print('  question 7 count updated')
t = '\n'.join(L)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('REPLY_TO_CTO patched')
