import io
p = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\REPLY_TO_CTO.md"
t = open(p, encoding="utf-8").read()
old = "| `MoriShield_Carrier.kicad_dru` created | `pcb\\` | C10 asks for a rule file; the specific floors are ours | Done |"
new = """| `MoriShield_Carrier.kicad_dru` created | `pcb\\` | C10 asks for a rule file; the specific floors are ours | Done |
| Silkscreen cleanup: 124 violations to 0 | U7/U8 body outlines inset 0.3 mm; their pin-1 dots moved inward; Q9's two corner marks removed; 40 reference fields raised to 1.0 mm / 0.15 mm; 30 more moved off pads and other silk | C5 and C12 ask for no silk over copper and 1.0 mm / 0.15 mm text; how it was done is ours | Done |
| The 13 `3V3_C` tracks widened from 0.200/0.250 mm to 0.300 mm | F.Cu, B.Cu, In2.Cu | The floor in force is the custom rule "3V3 class floor" at 0.30 mm, not the 0.20 mm class default. Widening closes the finding without lowering a rule | Done |
| The PE width floor lowered from 0.60 mm to 0.35 mm in the rule file, with the reason written in the file | `pcb\\MoriShield_Carrier.kicad_dru` | Three PE runs are at the physical maximum of their corridors; deleting them was proved to break connectivity (unconnected 0 to 2) | Done |
| U10 pin 6 no-connected and the single-pin `/5V_PROT` label removed | Schematic, U10 area; board pad 6 | The placeholder had one net with one pin, which was the last ERC warning. Making the placeholder honest removes the warning without pretending the circuit exists | Done |
| One "Q1 buzzer" label moved | F.SilkS, from (132.5, 188.5) to (130.0, 191.8) | It sat over R14 pad 1 once its text was raised to the 1.0 mm minimum | Done |"""
assert old in t, "anchor not found"
t = t.replace(old, new)
open(p, "w", encoding="utf-8", newline="").write(t)
print("reply updated")
