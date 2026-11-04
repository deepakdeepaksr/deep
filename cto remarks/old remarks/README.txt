================================================================
MoriShield Carrier PCB — Review & Fabrication Package
Board: MoriShield_Carrier | KiCad 10.0.x | 2026-10-12
================================================================

This package contains everything needed to review and fabricate
the MoriShield carrier PCB.

CONTENTS
--------
design/
    MoriShield_Carrier.kicad_pro        KiCad project
    MoriShield_Carrier.kicad_sch        Schematic (ERC-clean)
    MoriShield_Carrier.kicad_pcb        Routed PCB (DRC-clean)
    MoriShield_Carrier.kicad_sym        Project symbol library
    MoriShield_Carrier.pretty/          Project footprint library
    fp-lib-table, sym-lib-table         Library tables (self-contained
                                        project — no external libs needed)

fabrication/
    Gerber set (RS-274X) + Excellon drill file — the exact files
    to send to the fab.

reports/
    MoriShield_Carrier-drc.rpt          0 violations / 0 unconnected
    MoriShield_Carrier-erc.rpt          0 errors / 7 intentional
                                        warnings (unconnected spare
                                        socket pins + PWR_FLAG notes)

MoriShield_Carrier_BOM.csv                Bill of materials
MoriShield_Carrier_positions.csv          Component placement
MoriShield_Carrier_schematic.pdf          Schematic print
renders/top.png, bottom.png               3D renders of routed board

FAB SPECIFICATION
-----------------
    Layers          2 (F.Cu + B.Cu)
    Board size      168 x 118 mm
    Thickness       1.6 mm
    Copper          1 oz (35 um) outer
    Min track       0.30 mm signal / up to 2.2 mm power
    Min clearance   0.18 mm (JLCPCB-compatible; DRC-verified)
    Min drill       0.45 mm via / 0.73 mm JST ZH / 0.95 mm sockets
                    / 3.2 mm mounting
    Surface finish  HASL lead-free (or ENIG — no BGA/fine-pitch)
    Solder mask     green (any)
    Silkscreen      white (top + bottom)
    Stencil         not required — hand-solder assembly
                    (0402/1206/SOT-89 footprints are handsolder-grade)

ASSEMBLY NOTES
--------------
- THT assembly except: C3/C4/C7-C10 (0402), R5/R6/R7 (1206),
  D2 (SMB), ESD1-4 (DFN1006-2), U1 (SOT-89) — all handsolder pads.
- Module sockets (J1-J9) take standard 2.54 mm female headers;
  plug-in modules: EdgeHax S3-PRO, Parry A7672S modem, buck
  converter, MPU6050, RTC, E22 LoRa.
- External sensors via JST (XH 2.5 mm / ZH 1.5 mm) at J11-J18.
- 5x20 mm fuse clip at F1 (5 A glass fuse).
- 4x M3 mounting holes (3.2 mm).

VALIDATION SUMMARY (all passed on this exact board)
---------------------------------------------------
    KiCad DRC          0 violations, 0 unconnected (severity-all,
                       zones refilled)
    KiCad ERC          0 errors, 7 intentional warnings
    Custom audit       33/33 checks (pad parity vs netlist,
                       connectivity union-find, geometry, stackup,
                       RF antenna keepout, per-net widths)
    Fab DFM presets    clean on JLCPCB standard+advanced,
                       PCBWay, OSH Park
    HQ DFM (offline)   0 errors (9 informational hole records)
    Power integrity    FEM DC solve (KiPIDA + padne):
                       +5 V at modem J5 = 4.85 V @ 2 A GSM burst,
                       +12 V chain drop <0.5 V, 3V3_C = 3.293 V,
                       GND bounce ~2 mV

POWER ARCHITECTURE
------------------
    12 V in (J18 screw term) -> F1 5 A -> D1 SB560 (rev-polarity)
    -> buck module (J9 socket) -> +5 V rail -> AMS1117 (U1)
    -> 3V3_C rail for sensor loads.
    GSM modem (J5) is on +5 V with 470 uF bulk at C5.
    12 V TVS SMBJ12CA (D2) on input.

ITEMS TO CONFIRM BEFORE MASS ORDER (physical, not software-checkable)
-------------------------------------------------------------------
1. Buck module pin order — board expects VO+/GND/IN+ single row + EN.
2. Parry A7672S modem footprint — 9-pin + 2-pin rows; board row
   gap is 33.56 mm (J3-J4). Verify against physical module.
3. EdgeHax S3-PRO pin map — GPIO21/22 = I2C-0, 47/48 = I2C-1, 18 = EN;
   board row gap is 26.0 mm (J1-J2). Verify against physical module.
4. GY-521 MPU6050 and E22 module pin orders/orientation.
5. Plug-in modules' own I2C pull-ups (they parallel with R1/R2 1k8,
   R3/R4 4k7 — check total sink current stays <3 mA/line).
6. Enclosure fit: 168 x 118 mm board + standoff clearance.

KNOWN/ACCEPTED LIMITATIONS
--------------------------
- +5 V at J5 ~4.85 V under sustained 2 A burst — within module
  tolerance; keep J5 cable short or add local bulk cap if margin
  is a concern.
- AMS1117 ~90 C at sustained 600 mA (fine for WiFi duty cycles).
- Schematic text lines beginning with "!padne" are power-solver
  annotations (source/load/regulator intent) — harmless, can be
  deleted if they clutter the review.

================================================================
