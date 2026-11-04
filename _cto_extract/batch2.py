import io, re, json, os

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
PCB = os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_pcb')
SCH = os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_sch')
PRO = os.path.join(P, 'pcb', 'MoriShield_Carrier.kicad_pro')

# ---------- A. the orphan via my own track deletion created ----------
t = io.open(PCB, encoding='utf-8').read()
lines, out, i, cut = t.split('\n'), [], 0, 0
while i < len(lines):
    if re.match(r'^\s*\(via\b', lines[i]):
        j, depth = i, 0
        while j < len(lines):
            depth += lines[j].count('(') - lines[j].count(')')
            if depth == 0:
                break
            j += 1
        if '4550b204-6490-49b5-944f-1254fe1ff4c6' in '\n'.join(lines[i:j + 1]):
            cut += 1
            i = j + 1
            continue
        out.extend(lines[i:j + 1])
        i = j + 1
        continue
    out.append(lines[i].replace('(start 153 199.2)', '(start 156.5 199.2)'))
    i += 1
assert cut == 1, 'orphan via not found exactly once (%d)' % cut
io.open(PCB, 'w', encoding='utf-8', newline='').write('\n'.join(out))
print('A. orphan 3V3_C via removed (1), serial box moved clear of the S/N label')

# ---------- B. title block, in the format the file actually uses ----------
s = io.open(SCH, encoding='utf-8').read()
NOTE = ('Rev C: watchdog input routed; J18 polarity corrected and input copper widened; '
        'modem RESET connected; AS5600 wind-vane header J26 added; net classes restored. '
        'RS485 removed for off-board USB testing - deferral to be confirmed by Serigreen.')
reps = [
    ('(rev "Proto-Simple Rev 0.2 (Post-RS485 Stripped)")', '(rev "Rev C")'),
    ('(date "2026-10-22")', '(date "2026-11-01")'),
    ('(comment 1 "Added DIY Wind Sensor (AS5600 + Reed), RS485 removed for off-board USB testing.")',
     '(comment 1 "%s")' % NOTE),
]
for a, bb in reps:
    n = s.count(a)
    print('   %-22s %d occurrence(s)' % (a[:20], n))
    assert n == 1, 'expected exactly 1'
    s = s.replace(a, bb)
io.open(SCH, 'w', encoding='utf-8', newline='').write(s)
print('B. schematic title block rewritten')

# ---------- C. mirror it in the project file ----------
d = json.load(open(PRO, encoding='utf-8'))
sh = d.get('sheets', [])
fixed = 0
for row in sh:
    if isinstance(row, dict) and 'title_block' in row:
        pass
if 'sheets' in d and isinstance(d['sheets'], dict):
    print('   sheets is a dict')
# the project stores the sheet tree under "sheets"; the netlist export showed the
# same rev/date strings there, so patch by text on the serialised form instead.
raw = json.dumps(d)
c1 = raw.count('Proto-Simple Rev 0.2 (Post-RS485 Stripped)')
raw = raw.replace('Proto-Simple Rev 0.2 (Post-RS485 Stripped)', 'Rev C')
c2 = raw.count('2026-10-22')
raw = raw.replace('2026-10-22', '2026-11-01')
print('C. project: rev strings %d, date strings %d' % (c1, c2))

# ---------- D. 3V3 class floor, with the reason recorded ----------
d = json.loads(raw)
for c in d['net_settings']['classes']:
    if c['name'] == '3V3':
        print('D. 3V3 class track %.2f -> 0.20' % c['track_width'])
        c['track_width'] = 0.20
d['net_settings']['class_notes'] = (
    '3V3 floor 0.20 mm: the rail carries the MPU-6050 socket, the DS3231 socket, the I2C '
    'pull-ups and the modem VDD_UART level-translator reference - worst case under 50 mA. '
    'The two long In2 runs are widened on shape, not on current.')
json.dump(d, io.open(PRO, 'w', encoding='utf-8'), indent=2)
print('   project written')
