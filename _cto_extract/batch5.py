import io, re, os, subprocess, json, collections

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
PCB = os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_pcb')
SCH = os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_sch')
CLI = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
OUT = os.path.join(P, 'revC')
PREV = os.path.join(OUT, 'preview_do_not_ship')
os.makedirs(PREV, exist_ok=True)

# ---------- 1. last dead stub (floats 0.3 mm below R10.1's pad) ----------
t = io.open(PCB, encoding='utf-8').read()
lines, out, i, cut = t.split('\n'), [], 0, 0
while i < len(lines):
    if re.match(r'^\s*\(segment\b', lines[i]):
        j, depth = i, 0
        while j < len(lines):
            depth += lines[j].count('(') - lines[j].count(')')
            if depth == 0:
                break
            j += 1
        if 'a8d45380-c35a-468e-a3e8-032be5d19b87' in '\n'.join(lines[i:j + 1]):
            cut += 1
            i = j + 1
            continue
        out.extend(lines[i:j + 1]); i = j + 1; continue
    out.append(lines[i]); i += 1
assert cut == 1, 'stub count %d' % cut
io.open(PCB, 'w', encoding='utf-8', newline='').write('\n'.join(out))
print('1. last dead 3V3_C stub removed')


def run(cmd, what):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
        ok = r.returncode == 0
        print('   %-40s %s' % (what, 'OK' if ok else 'FAILED ' + (r.stderr or r.stdout or '').strip().replace('\n', ' ')[:110]))
        return ok
    except Exception as e:
        print('   %-40s ERROR %s' % (what, e)); return False


print('2. renders')
run([CLI, 'pcb', 'render', '-o', os.path.join(OUT, 'render_top.png'), '--side', 'front',
     '--quality', 'high', '--background', 'transparent', '--width', '1800', '--height', '1000', PCB], 'render top')
run([CLI, 'pcb', 'render', '-o', os.path.join(OUT, 'render_bottom.png'), '--side', 'back',
     '--quality', 'high', '--background', 'transparent', '--width', '1800', '--height', '1000', PCB], 'render bottom')
run([CLI, 'pcb', 'render', '-o', os.path.join(OUT, 'render_iso.png'), '--quality', 'high',
     '--rotate', '-45,0,45', '--perspective', '--floor', '--background', 'transparent',
     '--width', '1800', '--height', '1000', PCB], 'render isometric')

print('3. preview production files (NOT for release - board is mid-S3)')
LAYERS = ('F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Mask,B.Mask,'
          'F_Silkscreen,B_Silkscreen,F_Courtyard,B_Courtyard,F_Fab,B_Fab,Edge_Cuts')
run([CLI, 'pcb', 'export', 'gerbers', '-o', PREV, '-l', LAYERS, '--check-zones', PCB], 'gerbers')
run([CLI, 'pcb', 'export', 'drill', '-o', PREV, '--format', 'excellon', '--excellon-units', 'mm', PCB], 'drill')

print('4. final verification on the saved files')
run([CLI, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', os.path.join(OUT, 'erc_RevC.json'), SCH], 'ERC')
run([CLI, 'pcb', 'drc', '--refill-zones', '--schematic-parity', '--severity-all',
     '--all-track-errors', '--format', 'json', '-o', os.path.join(OUT, 'drc_RevC.json'), PCB], 'DRC')

e = json.load(open(os.path.join(OUT, 'erc_RevC.json'), encoding='utf-8'))
ev = [v for s in e.get('sheets', []) for v in s.get('violations', [])]
print('\n   ERC  errors %d  warnings %d  %s'
      % (len([v for v in ev if v['severity'] == 'error']), len([v for v in ev if v['severity'] == 'warning']),
         dict(collections.Counter(v['type'] for v in ev))))
d = json.load(open(os.path.join(OUT, 'drc_RevC.json'), encoding='utf-8'))
ty = collections.Counter(v['type'] for v in d['violations'])
sv = collections.Counter(v['severity'] for v in d['violations'])
print('   DRC  %d items  %s' % (len(d['violations']), dict(sv)))
print('        %s' % dict(ty))
print('        unconnected %d   parity %d' % (len(d.get('unconnected_items', [])), len(d.get('schematic_parity', []))))

print('\n   revC\\')
for root, dirs, files in os.walk(OUT):
    for f in sorted(files):
        fp = os.path.join(root, f)
        print('      %-58s %9d' % (fp.replace(P + os.sep, ''), os.path.getsize(fp)))
