"""Build the E1 trial: copy the board, add a GND zone on B.Cu, raise PE priority."""
import sys, shutil, os, uuid, re, datetime
sys.path.insert(0, r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb")
from _sexp import parse, Node, atom_str

ROOT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb"
LIVE = ROOT + r"\pcb\MoriShield_Carrier.kicad_pcb"
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
TRIAL_DIR = ROOT + r"\pcb\_snap\E1_trial_" + stamp
os.makedirs(TRIAL_DIR, exist_ok=True)
TRIAL = TRIAL_DIR + r"\MoriShield_Carrier.kicad_pcb"
shutil.copy2(LIVE, TRIAL)
print("trial copy:", TRIAL)

text = open(TRIAL, encoding="utf-8").read()
root = parse(text)[0]

# --- the In1 GND zone: its polygon points, to reuse as the B.Cu outline ---
gnd = None
for z in root.children:
    if isinstance(z, Node) and z.head == "zone" and z.value("net") == "GND" and z.value("layer") == "In1.Cu":
        gnd = z
        break
assert gnd is not None
poly_node = gnd.find("polygon")
pts = poly_node.find_all("xy")
coords = [(float(atom_str(p.atoms()[0])), float(atom_str(p.atoms()[1]))) for p in pts]
print("In1 GND outline points:", len(coords))

# --- raise the PE zone to priority 1 so the new GND pour cannot starve it ---
edits = []
for z in root.children:
    if isinstance(z, Node) and z.head == "zone" and z.value("net") == "PE" and z.value("layer") == "B.Cu":
        pri = z.find("priority")
        if pri is None:
            # insert a priority node right after the (layer ...) line
            lay = z.find("layer")
            edits.append((lay.end, lay.end, "\n\t\t(priority 1)"))
        else:
            edits.append((pri.start, pri.end, "(priority 1)"))
print("PE priority edits:", len(edits))

# --- the new B.Cu GND zone ---
body = "".join("\n\t\t\t(xy %s %s)" % (x, y) for (x, y) in coords)
zone = (
    '\n\t(zone\n'
    '\t\t(net "GND")\n'
    '\t\t(layer "B.Cu")\n'
    '\t\t(uuid "%s")\n'
    '\t\t(hatch edge 0.5)\n'
    '\t\t(priority 0)\n'
    '\t\t(connect_pads\n'
    '\t\t\t(clearance 0.25)\n'
    '\t\t)\n'
    '\t\t(min_thickness 0.25)\n'
    '\t\t(fill yes\n'
    '\t\t\t(thermal_gap 0.5)\n'
    '\t\t\t(thermal_bridge_width 0.5)\n'
    '\t\t\t(island_removal_mode 0)\n'
    '\t\t)\n'
    '\t\t(polygon\n'
    '\t\t\t(pts%s\n\t\t\t)\n'
    '\t\t)\n'
    '\t)\n' % (uuid.uuid4(), body))

out = text
for (s, e, new) in sorted(edits, key=lambda x: -x[0]):
    out = out[:s] + new + out[e:]
idx = out.rstrip().rfind(")")
out = out[:idx] + zone + out[idx:]
open(TRIAL, "w", encoding="utf-8", newline="").write(out)
print("B.Cu GND zone written")
