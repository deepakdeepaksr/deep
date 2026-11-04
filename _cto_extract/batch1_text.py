import re, io, os, sys

path = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb'
t = io.open(path, encoding='utf-8').read()

UUIDS = {
    '195ff0ab-7ba1-40c9-8384-2f4ce3e9fab0': 'track 3V3_C 13.0mm',
    'a872d970-ab82-4fe9-b6e2-873436224da0': 'via /PWR_EN',
    '75133ec4-ff1a-4f0a-85da-0df0d6da4120': 'via /I2C0_SDA',
    'e54073cd-5da7-46a9-bcb2-993543087529': 'track /EVENT_BTN 1.05mm',
    '496bf122-792d-4b7b-93ab-91957d8f81af': 'via /BUZZER_EN',
}

print('before:  (segment %d   (via %d   chars %d'
      % (len(re.findall(r'\n\s*\(segment\b', t)), len(re.findall(r'\n\s*\(via\b', t)), len(t)))

for u, what in UUIDS.items():
    if u not in t:
        print('  MISSING from file:', u, what)
        continue

# remove each (track ...) / (via ...) block that carries one of these uuids,
# walking the s-expression by balanced parentheses
lines = t.split('\n')
out, i, removed = [], 0, []
while i < len(lines):
    ln = lines[i]
    if re.match(r'^\s*\((segment|via)\b', ln):
        j, depth = i, 0
        while j < len(lines):
            depth += lines[j].count('(') - lines[j].count(')')
            if depth == 0:
                break
            j += 1
        block = '\n'.join(lines[i:j + 1])
        hit = [u for u in UUIDS if u in block]
        if hit:
            removed.append((hit[0], UUIDS[hit[0]], block.split('\n')[0].strip()[:60]))
            i = j + 1
            continue
        out.extend(lines[i:j + 1])
        i = j + 1
        continue
    out.append(ln)
    i += 1

print('\nblocks removed: %d' % len(removed))
for u, what, head in removed:
    print('   %-28s %s   %s' % (what, u[:8], head))

if len(removed) != 5:
    print('\n!! expected 5, got %d - file NOT written' % len(removed))
    sys.exit(1)

new = '\n'.join(out)
print('\nafter:   (track %d   (via %d   chars %d'
      % (len(re.findall(r'\n\s*\(track\b', new)), len(re.findall(r'\n\s*\(via\b', new)), len(new)))

io.open(path, 'w', encoding='utf-8', newline='').write(new)
print('WRITTEN')
