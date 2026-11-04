import io, re, uuid as U

path = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb'
t = io.open(path, encoding='utf-8').read()
orig = t

# ---------- 1. U4 attributes ----------
i = t.find('(footprint ')
done = False
while i >= 0 and not done:
    j, depth = i, 0
    while j < len(t):
        if t[j] == '(':
            depth += 1
        elif t[j] == ')':
            depth -= 1
            if depth == 0:
                break
        j += 1
    blk = t[i:j]
    if '(property "Reference" "U4"' in blk:
        m = re.search(r'\n(\s*)\(attr ([^\n]*)\)', blk)
        print('U4 attr before:', m.group(2) if m else '(none found)')
        if m:
            DROP = {'board_only', 'exclude_from_pos_files', 'exclude_from_bom', 'virtual'}
            keep = [w for w in m.group(2).split() if w not in DROP]
            indent = m.group(1)
            if keep:
                repl = '\n%s(attr %s)' % (indent, ' '.join(keep))
            else:
                repl = ''                      # no attributes left: drop the line
            new = blk[:m.start()] + repl + blk[m.end():]
            t = t[:i] + new + t[j:]
            done = True
            print('U4 attr after: ', keep or '(line removed)')
        break
    i = t.find('(footprint ', j)
print('U4 attributes rewritten:', done)

# ---------- 2. silkscreen the release check requires ----------
def gtext(txt, x, y, size=1.0, th=0.15, rot=0, bold=False, justify='left bottom'):
    b = '\n\t\t\t\t(bold yes)' if bold else ''
    return ('\n\t(gr_text "%s"\n\t\t(at %g %g %g)\n\t\t(layer "F.SilkS")\n\t\t(uuid "%s")\n'
            '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size %g %g)\n\t\t\t\t(thickness %g)%s\n\t\t\t)\n'
            '\t\t\t(justify %s)\n\t\t)\n\t)' % (txt, x, y, rot, U.uuid4(), size, size, th, b, justify))


def grect(x0, y0, x1, y1, w=0.15):
    return ('\n\t(gr_rect\n\t\t(start %g %g)\n\t\t(end %g %g)\n\t\t(stroke\n\t\t\t(width %g)'
            '\n\t\t\t(type solid)\n\t\t)\n\t\t(fill no)\n\t\t(layer "F.SilkS")\n\t\t(uuid "%s")\n\t)'
            % (x0, y0, x1, y1, w, U.uuid4()))


add = (gtext('MoriShield Carrier', 139.5, 202.6, 1.0, 0.15, bold=True)
       + gtext('Rev C', 139.5, 200.2, 1.0, 0.15)
       + gtext('S/N', 150.0, 200.2, 1.0, 0.15)
       + grect(153.0, 199.2, 173.0, 201.4)
       + gtext('1', 232.20, 113.56, 1.4, 0.2, bold=True, justify='right center')
       + gtext('1', 272.40, 113.56, 1.4, 0.2, bold=True)
       + gtext('MODEM THIS WAY UP', 240.0, 108.6, 1.0, 0.15))

anchor = t.rfind('\t(embedded_fonts no)')
assert anchor > 0, 'anchor not found'
t = t[:anchor] + add + '\n' + t[anchor:]

print('silk blocks inserted: 4 text + 1 rect + 2 pin-1 marks + 1 orientation note')
print('chars %d -> %d' % (len(orig), len(t)))

io.open(path, 'w', encoding='utf-8', newline='').write(t)
print('WRITTEN')
