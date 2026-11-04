"""Refill zones in memory and save (rule 5: ZONE_FILLER, never edit a zone via the API)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCB = os.path.join(ROOT, "pcb", "MoriShield_Carrier.kicad_pcb")

b = pcbnew.LoadBoard(PCB)
filler = pcbnew.ZONE_FILLER(b)
filler.Fill(b.Zones())
b.Save(PCB)
print("refilled %d zones and saved" % b.GetAreaCount())
