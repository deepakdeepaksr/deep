import re, os

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\_cto_extract'
docs = ['MoriShield-Carrier-RevA-Review-v1.2.txt',
        'MoriShield-Carrier-ModuleFit-Review-v1.1.txt',
        'MoriShield-Carrier-FabReadiness-v1.0.txt',
        'MoriShield-Carrier-RevB-Review-v1.0.txt',
        'MoriShield-Carrier-ReleaseCheck-v1.0.txt']

PAT = re.compile(
    r'^\s*(?:'
    r'(\d{1,2}\.\d{1,2}?\s+[A-Z][^\n]{2,90})'      # 6.4 Heading
    r'|(\d{1,2}\.\s+[A-Z][^\n]{2,90})'              # 6. Heading
    r'|(Table\s+\d+[^\n]{0,80})'                     # Table N
    r'|(Appendix\s+[A-Z][^\n]{0,60})'
    r'|(C\d{1,2}\s*[—:\-][^\n]{0,90})'               # C1 criterion
    r'|([A-H]\d{1,2}\s*[—:\-|]\s*[^\n]{0,70})'       # A1 … H6 items
    r'|(R\d{1,2}\s*[—:\-|]\s*[^\n]{0,70})'           # R1 … R17
    r'|(G\d\s*[—:\-]\s*[^\n]{0,70})'                 # gates
    r')\s*$')

for f in docs:
    p = os.path.join(base, f)
    if not os.path.exists(p):
        print('!! missing', f)
        continue
    lines = open(p, encoding='utf-8').read().splitlines()
    print('\n' + '=' * 78)
    print(f, ' — ', len(lines), 'lines')
    print('=' * 78)
    seen = set()
    for ln in lines:
        m = PAT.match(ln)
        if not m:
            continue
        s = ' '.join(x for x in m.groups() if x).strip()
        key = s[:40].lower()
        if key in seen:
            continue
        seen.add(key)
        print('   ', s[:120])
