# DEVIN.md — MoriShield Carrier Rev C handoff

Read this file top to bottom before touching anything. It is the working brief for a fresh Devin
Desktop session on another machine. Everything below was measured, not remembered.

All project paths are **relative to the repository root**. Only the KiCad tool paths are absolute,
because they are machine-specific — see §2 and fix them if they differ on your PC.

---

## 1. What this project is, and where it stands

Rev C of a 4-layer carrier board (178.15 × 118.15 mm) for an ESP32-S3-WROOM N16R8, an A7672S 4G modem,
an E22-900T22D LoRa module, an I2C mux and a set of field sensor ports. It is **not released for
fabrication** and S3 is **not** complete. Nothing here authorises a build.

**Verified state (2026-11-04, after the restore in §8):**

| Measure | Value |
|---|---|
| ERC | 0 violations, `ignored_checks []` |
| DRC | 0 violations, 0 unconnected, 0 parity, `ignored_checks []` |
| Census | 161 footprints · 1150 segments · 319 vias · 6 zones · 136 nets |
| Copper length | **5142.324 mm** (the real guard — see §4 rule 12) |
| Vias inside SMD pads | **67 of 319** |
| E1 stitching | **148 links, worst 10.00 mm, 0.0 % beyond 10 mm** |
| Gate tally | **4 met (C1, C2, C5, C12), 1 partly (C9), 8 not met** |
| `pack.ps1` | stops at **GATE 5 PRODUCTION** |
| Traceability | `trace2.py` 76/76/76, 0 status disagreements, 0 priority mismatches |

**Done and proven, do not revisit:** T-55 (E22 mode straps) and T-56 (reed move). Details in §5.

---

## 2. Environment

| Tool | Path (machine-specific) | Used for |
|---|---|---|
| `kicad-cli` | `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` | DRC, ERC, Gerbers, drill, POS |
| Python **with** `pcbnew` | `C:\Program Files\KiCad\10.0\bin\python.exe` | anything that loads the board |
| System Python 3.10 | `python` on PATH | text/s-expression scripts only — **no `pcbnew`** |

The board is KiCad 10 format (`(version 20260206)`). The project library is
`morishield/morishield_hardware/libraries/MoriShield_Carrier.pretty`, reached through
`pcb/fp-lib-table` with forward slashes and `${KIPRJMOD}`.

**Trap:** `pcb/_census.py` imports `pcbnew`, so it must be run with the **KiCad** Python. Running it with
the system Python fails with `ModuleNotFoundError: pcbnew`.

---

## 3. The files that matter

| Path | What it is |
|---|---|
| `pcb/MoriShield_Carrier.kicad_pcb` | the board |
| `pcb/MoriShield_Carrier.kicad_sch` | the schematic |
| `pcb/MoriShield_Carrier.kicad_dru` | custom width/clearance rules — DRC reads these |
| `pcb/_census.py` | seven-number census incl. copper length and vias-in-pads |
| `pcb/_plot_stitching_final.py` | E1 stitching metric; writes `revC/E1_stitching_plot.png` |
| `pcb/_regen_vias_in_pads.py` | regenerates `revC/vias_in_pads.txt` |
| `pcb/_make_response_sheet.py` | regenerates `revC/ResponseSheet_RevC.csv` |
| `revC/decoupling_map.csv` | the C9 map; every row must carry `verdict` + `verdict_reason` |
| `revC/FAB_NOTES.md` | the fab note quoted to Serigreen |
| `revC/pack.ps1` | five gates; must stop at GATE 5 |
| `_cto_extract/gate_truth.py` | recomputes the gate tally from the rows — **never type a tally** |
| `_cto_extract/trace2.py` | traceability, must print 0 and 0 |
| `_cto_extract/final_verify.py` | document integrity |
| `pcb/_snap/` | snapshots, one per edit, each with a census |
| `pcb/_work_20261103/` | all the working scripts from the last sessions |

**Documents to keep in step:** `TASK_TRACKER.md`, `STAGE_TRACKER.md`, `REPLY_TO_CTO.md`,
`PROJECT_CONTEXT_RevC.md`, and the root file `work done` (session reports).

---

## 4. Rules — these exist because each one was learned the hard way

1. **Snapshot before every edit**, to `pcb/_snap/<purpose>_<stamp>/`, with a census. Copy the board,
   the schematic, the project and the `.kicad_dru`.
2. **DRC always** with all four flags:
   `kicad-cli pcb drc --refill-zones --schematic-parity --severity-all --all-track-errors`.
   **ERC always** with `--severity-all`. Report violations, unconnected, parity and `ignored_checks`.
3. **Parity 0 is not evidence.** Prove parity 0 *and* unconnected 0 *and* DRC 0 *and* ERC 0 *and* a
   connectivity read-back from the saved file.
4. **Copper deletion is text surgery** on the balanced `(segment ...)` / `(via ...)` block whose UUID the
   DRC report gives. Never `board.Remove()`.
5. **Zones:** fill in memory with `ZONE_FILLER`; never create or edit a zone through the API.
6. **Library paths:** forward slashes only; any path change gets an unmodified control.
7. **Silk:** stroke font, 1.0 mm height, 0.15 mm stroke, no silk over copper or silk. Move things, never
   lower the rule.
8. **Never invent** part numbers, module heights or measurements. Generic values with a footprint are
   fine; MPN stays TBC.
9. **J6 is NOT mis-wired.** It is numbered for a 180° insertion and all seven nets line up that way.
   Never write "mirror image" about it. The defect was that nothing marked or keyed it.
10. After every task, update `TASK_TRACKER.md` and `STAGE_TRACKER.md` from tool output, then regenerate
    `revC/ResponseSheet_RevC.csv` with `pcb/_make_response_sheet.py`; `trace2.py` must report 0 and 0.
11. **A local label `X` produces the net `/X`.** A board net without the leading slash raises
    `net_conflict` on the label side **only**. The tell: only one side of a two-pin part conflicts; a
    pin-order error conflicts on both. This cost a day on 2026-11-04.
12. **A `pcbnew` Save re-issues every UUID and merges collinear/corner segments**, so a segment count can
    fall with no copper lost. Therefore: (a) re-run DRC immediately before any text surgery to get
    current UUIDs, and (b) record **total copper length** at every checkpoint — counts alone are not the
    guard. Proof from 2026-11-04: 1178 segments / 5306.342 mm → 1166 segments / 5306.609 mm with no edit
    in between.

---

## 5. What is finished

**T-55 — E22 M0/M1 strapped to GND. Done 2026-11-04.**
- Schematic: local labels `E22_M1_STRAP` / `E22_M0_STRAP`; **R56, R57** = 0 Ω, `Resistor_SMD:R_0603_1608Metric`,
  each with a `GND` power symbol on pin 2; no-connect flags on J1 pins 16 and 17 at **(115.57, 327.66)**
  and **(115.57, 330.20)**.
- Board: `/E22_M0` and `/E22_M1` deleted as nets; J1.16 → `unconnected-(J1-IO10-Pad16)`, J1.17 →
  `unconnected-(J1-IO11-Pad17)`; J6.6 on `/E22_M1_STRAP`, J6.7 on `/E22_M0_STRAP`; R56/R57 at
  (267.50, 164.92) and (267.50, 162.38) rot 0; strap runs on **B.Cu** because `/PWR_EN` is a wall at
  x 264.75; each resistor's GND pad has **its own via** at (269.40, 164.92) / (269.40, 162.38).
- GPIO10 and GPIO11 are free for the microSD.

**T-56 — reed moved from GPIO41 to GPIO39. Done 2026-11-04.**
- Schematic: `REED_PULSE_F` label moved to J2 pin 9's endpoint **(152.40, 309.88)**; its old wire and the
  pre-existing no-connect on pin 9 deleted; no-connect placed on pin 7 at **(152.40, 304.80)**.
- Board: J2.7 → `unconnected-(J2-IO41-Pad7)`, J2.9 → `/REED_PULSE_F`, rerouted
  (183.50,133.68)→(182.25,134.93)→(182.25,137.50). R50, C40, ESD17 and J22 stay on `/REED_PULSE`.

**E1 — stitching. Met.** Two GND vias at (277.00, 90.00) and (164.00, 186.00) restored it from 144 links /
11.16 mm to 148 / 10.00 mm / 0.0 %.

**Via-in-pad evidence. Current.** `revC/vias_in_pads.txt` = 67 rows of 319, with reference, pad, net,
position, via size and drill.

---

## 6. What is next: T-59, the 13 ADD decoupling pins

`revC/decoupling_map.csv` carries `verdict` = MOVE 3 / ADD 13 / NONE 20, with a `verdict_reason` on every
row. The 13 ADD are **four net problems**, not thirteen pin jobs. Work them as batches and verify **once
per batch**:

| batch | net | pins | why they are ADD |
|---|---|---|---|
| 1 | `3V3_C` | J1.1, J4.3, J7.2, J7.8, J8.5, J26.1 | **the rail has no 10 µF capacitor at all** — every cap on it is 100 nF |
| 2 | `/3V3_SENS_SW` | J11.1, J12.1, J15.1, J16.1, J17.1 | one bulk (C51 at 186,173), 22.8–89.2 mm from these pins |
| 3 | `/+5V_ESP` | D7.1 | no 100 nF on the net at all (C28 is 10 µF) |
| 4 | `+5V` | J24.1 | the 100 nF site will not fit beside the bulk |

**Measured legal sites** (bare footprint, checked for copper, hole-to-hole, courtyards and module
outlines — a connecting track and a GND via still have to be routed):

| pin | net | value | site |
|---|---|---|---|
| J1.1 | 3V3_C | 100 nF | (210.50, 157.75) rot 0 |
| J4.3 | 3V3_C | 100 nF | (273.50, 117.39) rot 0 |
| J7.2 | 3V3_C | 100 nF | (215.65, 163.00) rot 0 |
| J7.8 | 3V3_C | 100 nF | (229.14, 169.00) rot 0 |
| J8.5 | 3V3_C | 100 nF | (166.06, 157.25) rot 90 |
| J26.1 | 3V3_C | 100 nF | (129.75, 152.50) rot 90 |
| J11.1 | /3V3_SENS_SW | 100 nF | (171.75, 195.00) rot 90 |
| J12.1 | /3V3_SENS_SW | 100 nF | (187.75, 193.50) rot 90 |
| J15.1 | /3V3_SENS_SW | 100 nF | (146.13, 193.50) rot 90 |
| J16.1 | /3V3_SENS_SW | 100 nF | (163.94, 189.50) rot 90 |
| J17.1 | /3V3_SENS_SW | 100 nF | (266.75, 194.25) rot 90 |
| J24.1 | +5V | 100 nF | (138.97, 147.25) rot 0 |
| D7.1 | /+5V_ESP | 100 nF | (215.60, 97.50) rot 90 |

**You must decide the capacitor count per net and justify it.** A bulk cap only helps a pin within 10 mm
along the copper, so one cap cannot serve pins scattered across the board. State, per pin, which new part
satisfies it. Do not add one cap and claim six pins are fixed. Values: 10 µF for the bulk half, 100 nF for
the local half; reuse a footprint already on the board; MPN/rating/temperature stay TBC.

**Batch 3 is the one to start with** — a single part, so it can be finished rather than half-done. It was
attempted twice on 2026-11-04 and both attempts were restored. Read §7 before you retry it.

---

## 7. Traps that have already cost days

- **Never regex a board footprint's `(at ...)`.** KiCad omits the rotation field when it is 0, and
  `(at ...)` appears in every property, so a text pattern silently matches the wrong node. Take the `at`
  child of the footprint node from the s-expression parser. This is exactly why batch 3 failed twice: the
  cloned C52 stayed on top of C41 and shorted to it.
- **Rotating a placed footprint raises `lib_footprint_mismatch`.** The library copy is the reference, so a
  placed part may not be turned without editing the library. New parts can be placed at any rotation; an
  existing one cannot be re-oriented.
- **Pad geometry:** the 0805 footprints on this board have pads at **±1.0375 mm**; the 0603 at **±0.825 mm**.
  Do not assume ±0.9375.
- **Board net declarations are nested, not top-level.** Renaming by name (`"X"` → `"/X"`) works; looking
  for a top-level `(net ...)` list does not.
- **A via inside an SMD pad must not be left silently.** The count is quoted to Serigreen in
  `revC/FAB_NOTES.md` and `revC/vias_in_pads.txt`. It is 67 and must stay 67 unless a fab note is agreed.
  Place the via clear and connect it with a short track.
- **`/PWR_EN` is a vertical wall at x 264.75 on F.Cu**, between J6 and the area to its right. Anything
  crossing it must go on B.Cu.
- **J5 serviceability:** courtyard 217.65–226.54 × 87.86–99.44, **0.36 mm** from the top board edge. The
  wire entry is along ±x: **5.1 mm** clear to the left (toward the ESP32), **1.91 mm** to the right (toward
  the modem). A bend on the modem side does not fit. The MX126 datasheet is not in the workspace, so the
  entry side is **not verified**.
- **`lib_footprint_mismatch`** also fires if you hand-build a footprint that differs from the library copy.
  Convert library `.kicad_mod` files rather than writing footprints from scratch.

---

## 8. Where the last session stopped

`T-59` batch 3 was attempted twice and **restored both times**. The board and schematic are byte-identical
to the entry state and verified clean (`pcb/_work_20261103/B3_restored.json`: 0/0/0, census identical in
all seven numbers). Nothing is half-applied.

Rollback snapshots, newest first:
`pcb/_snap/T59_5VESP_20261104_090758` (both files at entry to the T-59 attempt),
`T56_board_20261104_084453`, `T56_reedmove_20261104_084415`,
`T55_vias_20261104_083749`, `T55_rename_20261104_083700`,
`T55_pcb_20261104_075500`, `T1_E1_20261103_204817`.

---

## 9. The verification chain — run it after every change

```
kicad-cli pcb drc --refill-zones --schematic-parity --severity-all --all-track-errors \
    --format json -o revC/drc_RevC.json pcb/MoriShield_Carrier.kicad_pcb
kicad-cli sch erc --severity-all --format json -o revC/erc_RevC.json pcb/MoriShield_Carrier.kicad_sch
<kicad-python> pcb/_census.py                 # seven numbers, incl. copper length
<kicad-python> pcb/_plot_stitching_final.py   # after ANY copper or via change
<kicad-python> pcb/_regen_vias_in_pads.py     # must be 67 rows
<kicad-python> pcb/_make_response_sheet.py
python _cto_extract/gate_truth.py             # the tally, never typed
python _cto_extract/trace2.py                 # must print 0 and 0
python _cto_extract/final_verify.py
powershell -File revC/pack.ps1                # must stop at GATE 5
```

A clean checkpoint is: **ERC 0, DRC 0/0/0, vias-in-pads 67, a copper length you can account for, and
stitching ≤ 10.00 mm / 0.0 %.** If any is not clean, restore the snapshot and report what blocked — do
not carry a change forward dirty.

---

## 10. Out of scope unless the user says otherwise

The converter decision and R4/U10; stack-up; BOM MPNs; In2.Cu clearing (all seven remaining nets have
negative outer corridors, −0.30 to −0.60 mm, so it is a reroute-and-replace job, not a corridor search);
E7 series resistors; C8 ESD array moves; the remaining schematic surgeries; release Gerbers; the zip. Do
not draw a keep-out without the antenna measurements. **Do not declare S3 complete.**

**Owed by Aswin:** the ESP32 antenna tab length (tip to nearest header pin, mm); what J17 and J20 are for;
GY-521 and DS3231 heights; the MX126 wire-entry side. **Owed by Serigreen:** the questions in
`REPLY_TO_CTO.md`, including written agreement on plug/fill/cap for the 67 vias in pads.
