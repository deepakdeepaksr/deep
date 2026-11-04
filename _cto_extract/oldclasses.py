import json

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
d = json.load(open(base + r'\backup\MoriShield_Carrier.kicad_pro', encoding='utf-8'))
ns = d['net_settings']
print('=== backup project: net classes ===')
for c in ns['classes']:
    print('  %-16s track %.3f  clearance %.3f  via %.2f/%.2f  micro %.2f/%.2f'
          % (c['name'], c['track_width'], c['clearance'], c['via_diameter'], c['via_drill'],
             c['microvia_diameter'], c['microvia_drill']))
print('=== patterns ===')
for p in ns['netclass_patterns']:
    print('  %-18s <- %s' % (p['netclass'], p['pattern']))
print('=== rules ===')
print(' ', json.dumps(d['board']['design_settings']['rules'], indent=1))
print('=== net class defaults present? ===')
print(' ', [k for k in d['board']['design_settings'].keys()])
