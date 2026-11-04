import json, shutil, os, time

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
pro = base + r'\pcb\MoriShield_Carrier.kicad_pro'
snap = base + r'\pcb\_snap'
os.makedirs(snap, exist_ok=True)

stamp = time.strftime('%Y%m%d_%H%M%S')
shutil.copy2(pro, os.path.join(snap, 'MoriShield_Carrier.kicad_pro.pre-netclass-' + stamp))
print('backup ->', os.path.join(snap, 'MoriShield_Carrier.kicad_pro.pre-netclass-' + stamp))

d = json.load(open(pro, encoding='utf-8'))


def cls(name, track, clr, vd, vs, prio):
    return {"bus_width": 12, "clearance": clr, "diff_pair_gap": 0.25,
            "diff_pair_via_gap": 0.25, "diff_pair_width": 0.2, "line_style": 0,
            "microvia_diameter": 0.3, "microvia_drill": 0.1, "name": name,
            "pcb_color": "rgba(0, 0, 0, 0.000)", "priority": prio,
            "schematic_color": "rgba(0, 0, 0, 0.000)", "track_width": track,
            "tuning_profile": "", "via_diameter": vd, "via_drill": vs, "wire_width": 6}


# Rev A widths restored, adapted to the 5 V-only architecture.
# Via stack stays 0.6/0.3 (4L density); only the heavy paths get larger vias.
d['net_settings']['classes'] = [
    cls('Default',          0.20, 0.20, 0.60, 0.30, 2147483647),
    cls('Signal',           0.20, 0.20, 0.60, 0.30, 2147483646),
    cls('GND',              0.30, 0.20, 0.60, 0.30, 100),
    cls('3V3',              0.50, 0.20, 0.60, 0.30, 110),
    cls('PE',               1.00, 0.30, 1.00, 0.50, 120),
    cls('Power_5V_Sens',    0.80, 0.20, 0.80, 0.40, 130),
    cls('Power_5V_Modem',   1.50, 0.25, 1.00, 0.50, 140),
    cls('Power_5V_In',      1.50, 0.25, 1.00, 0.50, 150),
]

d['net_settings']['netclass_patterns'] = [
    {"netclass": "Power_5V_In",    "pattern": "+5V_IN"},
    {"netclass": "Power_5V_In",    "pattern": "+5V_F"},
    {"netclass": "Power_5V_In",    "pattern": "/5V_PROT"},
    {"netclass": "Power_5V_Modem", "pattern": "+5V"},
    {"netclass": "Power_5V_Sens",  "pattern": "/+5V_ESP"},
    {"netclass": "Power_5V_Sens",  "pattern": "/+5V_SENS"},
    {"netclass": "Power_5V_Sens",  "pattern": "/+5V_E22"},
    {"netclass": "Power_5V_Sens",  "pattern": "/+5V_E22_IN"},
    {"netclass": "Power_5V_Sens",  "pattern": "LED5V_A"},
    {"netclass": "3V3",            "pattern": "3V3_C"},
    {"netclass": "3V3",            "pattern": "/3V3_SENS"},
    {"netclass": "3V3",            "pattern": "/3V3_SENS_SW"},
    {"netclass": "3V3",            "pattern": "LED33_A"},
    {"netclass": "GND",            "pattern": "GND"},
    {"netclass": "PE",             "pattern": "PE"},
    {"netclass": "Signal",         "pattern": "*"},
]

r = d['board']['design_settings']['rules']
r['min_track_width'] = 0.20
r['min_via_diameter'] = 0.60
r['min_via_annular_width'] = 0.15
r['min_clearance'] = 0.20
r['min_through_hole_diameter'] = 0.30

json.dump(d, open(pro, 'w', encoding='utf-8'), indent=2)
print('written. classes now:', [c['name'] for c in d['net_settings']['classes']])
print('patterns:', len(d['net_settings']['netclass_patterns']))
