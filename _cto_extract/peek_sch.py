import io, re

s = io.open(r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_sch',
            encoding='utf-8').read()
i = s.find('(title_block')
print('--- first title_block ---')
print(s[i:i + 800])
print('--- counts ---')
print('  title_block occurrences :', s.count('(title_block'))
print('  Proto-Simple            :', s.count('Proto-Simple'))
print('  2026-10-22              :', s.count('2026-10-22'))
print('  (company)               :', s.count('(company)'))
print('  paper values            :', set(re.findall(r'\(paper "([^"]+)"\)', s)))
print('  sheets                  :', s.count('(sheet (at'))
