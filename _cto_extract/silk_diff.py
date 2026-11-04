import io, os, re, glob

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'


def silk_items(fp):
    t = io.open(fp, encoding='utf-8', errors='ignore').read()
    out = []
    for m in re.finditer(r'\((?:gr_text|fp_text)\s+"?((?:[^"\n\\]|\\.){0,30})"?', t):
        seg = t[m.start():m.start() + 460]
        lay = re.search(r'\(layer "([^"]+)"', seg)
        if lay and 'Silk' in lay.group(1):
            out.append((lay.group(1), m.group(1)))
    return out


cur = silk_items(os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_pcb'))
print('current silkscreen text items:', len(cur))
snaps = sorted(glob.glob(os.path.join(P, 'pcb', '_snap', '*', 'MoriShield_Carrier.kicad_pcb')))
print('snapshots holding a board file:', len(snaps))
for s in snaps[-6:]:
    v = silk_items(s)
    tag = os.path.basename(os.path.dirname(s))
    print('   %-42s silk %4d  %s' % (tag, len(v),
                                     'IDENTICAL to current' if sorted(v) == sorted(cur)
                                     else 'DIFFERENT (%+d)' % (len(v) - len(cur))))

print()
print('=== do F.Fab / Dwgs.User appear in the plotted layer set? ===')
gdir = os.path.join(P, 'revC', 'silk_check')
for f in sorted(os.listdir(gdir)):
    print('   ', f)
job = os.path.join(gdir, 'MoriShield_Carrier-job.gbrjob')
if os.path.exists(job):
    t = io.open(job, encoding='utf-8', errors='ignore').read()
    print('   job file layers:', re.findall(r'<GerberJobFile[^>]*>|<LayerID>([^<]+)</LayerID>', t)[:20])
