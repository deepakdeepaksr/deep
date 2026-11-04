import io, re, os, json, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'

print('=== what lives on Dwgs.User (module outlines / enclosure?) ===')
t = io.open(P + r'\pcb\MoriShield_Carrier.kicad_pcb', encoding='utf-8').read()
for m in re.finditer(r'\(gr_(rect|line|arc|text)\b(.*?)\n\t\t\)', t, re.S):
    body = m.group(2)
    if 'Dwgs.User' not in body:
        continue
    st = re.search(r'\(start ([\d.]+) ([\d.]+)\)', body)
    en = re.search(r'\(end ([\d.]+) ([\d.]+)\)', body)
    uuid = re.search(r'\(uuid ([^)]+)\)', body)
    print('   gr_%s  start %s  end %s' % (m.group(1),
                                          st.groups() if st else '-',
                                          en.groups() if en else '-'))

print()
print('=== revC folder: what a package would actually contain ===')
root = os.path.join(P, 'revC')
rows = []
for dirpath, dirs, files in os.walk(root):
    for f in files:
        p = os.path.join(dirpath, f)
        st = os.stat(p)
        rows.append((st.st_mtime, os.path.relpath(p, root), st.st_size))
import datetime
for m, rel, sz in sorted(rows):
    print('   %s  %8.1f KB  %s' % (datetime.datetime.fromtimestamp(m).strftime('%m-%d %H:%M'), sz / 1024, rel))

pcb_t = os.stat(os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_pcb')).st_mtime
sch_t = os.stat(os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_sch')).st_mtime
print()
print('design files: pcb %s   sch %s' % (
    datetime.datetime.fromtimestamp(pcb_t).strftime('%m-%d %H:%M:%S'),
    datetime.datetime.fromtimestamp(sch_t).strftime('%m-%d %H:%M:%S')))
for f in ('MoriShield_Carrier_RevC_schematic.pdf', 'drc_RevC.json', 'erc_RevC.json'):
    p = os.path.join(root, f)
    if os.path.exists(p):
        age = os.stat(p).st_mtime
        print('   %-42s %s   %s' % (f, datetime.datetime.fromtimestamp(age).strftime('%m-%d %H:%M:%S'),
                                    'NEWER than design - ok' if age >= max(pcb_t, sch_t) else 'STALE - older than design!'))
print()
print('=== gerbers present? ===')
for pat in ('*.gbr', '*.gtl', '*.gbl', '*.drl', '*.gbrjob', '*.zip'):
    hits = [os.path.relpath(os.path.join(dp, f), root) for dp, dn, fn in os.walk(root) for f in fn if re.match(pat.replace('.', r'\.'), f)]
    print('   %-10s %d  %s' % (pat, len(hits), hits[:6]))
