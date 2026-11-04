import io, re, os, shutil, subprocess, json

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
PCB = os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_pcb')
SCH = os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_sch')
CLI = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
OUT = os.path.join(P, 'revC')
os.makedirs(OUT, exist_ok=True)

# ---------- 1. the 1.0 mm 3V3_C stub left behind by the via removal ----------
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
        if 'fd70c941-4c0f-4077-9d4d-9dbbedff1d3a' in '\n'.join(lines[i:j + 1]):
            print('removing stub:', ' '.join(lines[i:j + 1])[:110])
            cut += 1
            i = j + 1
            continue
        out.extend(lines[i:j + 1]); i = j + 1; continue
    out.append(lines[i]); i += 1
assert cut == 1, 'stub found %d times' % cut
io.open(PCB, 'w', encoding='utf-8', newline='').write('\n'.join(out))
print('stub removed')

# ---------- 2. deliverables that can be generated from the CLI ----------
runs = [
    ([CLI, 'sch', 'export', 'pdf', '-o', os.path.join(OUT, 'MoriShield_Carrier_RevC_schematic.pdf'), SCH],
     'schematic PDF'),
    ([CLI, 'sch', 'export', 'bom', '--format', 'csv', '-o', os.path.join(OUT, 'MoriShield_Carrier_RevC_bom.csv'), SCH],
     'BOM (values/footprints only - fields still missing)'),
    ([CLI, 'pcb', 'export', 'pos', '--output', os.path.join(OUT, 'MoriShield_Carrier_RevC_pos.top.pos'),
     '--side', 'top', PCB], 'placement, top'),
    ([CLI, 'pcb', 'export', 'pos', '--output', os.path.join(OUT, 'MoriShield_Carrier_RevC_pos.bottom.pos'),
     '--side', 'bottom', PCB], 'placement, bottom'),
    ([CLI, 'pcb', 'export', 'drill', '--format', 'excellon', '--units', 'mm',
     '--output', os.path.join(OUT, 'preview_do_not_ship'), PCB], 'drill (preview only - board is not final)'),
]
for cmd, what in runs:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        ok = r.returncode == 0
        print('  %-52s %s' % (what, 'OK' if ok else 'FAILED: ' + (r.stderr or '')[:120]))
    except Exception as e:
        print('  %-52s ERROR %s' % (what, e))

for a, b in ((r'_cto_extract\erc_b2.json', 'erc_RevC.json'), (r'_cto_extract\drc_b2.json', 'drc_RevC.json')):
    pass

print('\nfiles in revC\\:')
for f in sorted(os.listdir(OUT)):
    print('   %-46s %8d bytes' % (f, os.path.getsize(os.path.join(OUT, f))))
