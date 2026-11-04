import io, os, re, shutil

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
src = os.path.join(os.environ['TEMP'], 'e22_manual.txt')
t = io.open(src, encoding='utf-8', errors='ignore').read()

# 1. put the manual IN THE WORKSPACE - it is a cited source and was only in TEMP
dst = P + r'\_cto_extract\E22-900T22D-UserManual.txt'
io.open(dst, 'w', encoding='utf-8').write(
    'Extracted text of the Ebyte E22-900T22D User Manual (26 pages).\n'
    'Source: https://www.cdebyte.com/pdf-down.aspx?id=1463\n'
    'Extracted with PyMuPDF; full-width punctuation preserved.\n'
    'This file is the citation source for revC\\FAB_NOTES.md and TASK_TRACKER.md.\n'
    + t)
print('manual saved to', os.path.relpath(dst, P), os.path.getsize(dst), 'bytes')

# 2. the mode section, verbatim, to a reviewable file
i = t.find('6.2 Normal')
if i < 0:
    i = min(m.start() for m in re.finditer(r'M0\s*=\s*[01]', t)) - 320
j = t.find('7 REGISTER', i)
if j < 0:
    j = i + 3200
seg = t[i:j]
out = P + r'\_cto_extract\e22_modes_raw.txt'
io.open(out, 'w', encoding='utf-8').write(seg)
print('mode section chars', len(seg), '->', os.path.basename(out))
