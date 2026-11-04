import sys, io, os
sys.path.insert(0, r'C:\Program Files\KiCad\10.0\bin')
import pcbnew

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
b = pcbnew.LoadBoard(os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_pcb'))

rows = []
for fp in b.GetFootprints():
    for p in fp.Pads():
        if p.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
            continue
        for t in b.GetTracks():
            if type(t).__name__ == 'PCB_VIA' and p.HitTest(t.GetPosition()):
                rows.append((fp.GetReference(), p.GetNumber(), p.GetNetname() or '-',
                             str(fp.GetFPID().GetLibItemName())[:34],
                             t.GetNetname(),
                             round(t.GetPosition().x / 1e6, 2), round(t.GetPosition().y / 1e6, 2),
                             round(t.GetWidth(pcbnew.F_Cu) / 1e6, 2)))

out = io.open(os.path.join(P, 'revC', 'vias_in_pads.txt'), 'w', encoding='utf-8')
out.write('Vias inside SMD pads - MoriShield Carrier Rev C\n')
out.write('source: every via centre tested against every SMD pad on the board\n')
out.write('count:  %d\n\n' % len(rows))
out.write('%-8s %-4s %-16s %-34s %-16s %8s %8s %6s\n'
          % ('ref', 'pad', 'pad net', 'footprint', 'via net', 'x mm', 'y mm', 'via dia'))
for r in sorted(rows):
    out.write('%-8s %-4s %-16s %-34s %-16s %8.2f %8.2f %6.2f\n' % r)
out.write('\nFix: specify plug/fill/cap per IPC-4761 Class B or C on the fab drawing\n')
out.write('(see FAB_NOTES.md). Re-count after any layout change.\n')
out.close()
print('revC\\vias_in_pads.txt written:', len(rows), 'vias')

byfoot = {}
for r in rows:
    byfoot[r[3]] = byfoot.get(r[3], 0) + 1
print('\nby footprint family:')
for k, v in sorted(byfoot.items(), key=lambda x: -x[1]):
    print('   %-36s %3d' % (k, v))
