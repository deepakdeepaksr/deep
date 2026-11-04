# QODER.md — Continuation Context for Qoder

> **Purpose.** Drop this one file into a fresh Qoder session on another machine and the assistant can resume planning, status tracking, documentation integrity and Devin-prompt generation without re-deriving anything. It is the *index and rulebook*, not the archive — the detail lives in the files it points at.

| | |
|---|---|
| **Project** | MoriShield Carrier, **Rev C** (internal v3), 4-layer only |
| **Role of Qoder here** | Planning, requirement tracing, document integrity, verification of Devin's claims, prompt generation. **Not** board editing |
| **Role of Devin Desktop** | Implementation: KiCad CLI, scripts, board and schematic edits |
| **Human** | Aswin — sole contact with Serigreen and sole signatory. Deepak does hardware, intermittently |
| **This file written** | 2026-11-04, after an independent verification pass |
| **Board status** | **Not released for fabrication.** Release is Serigreen's, in writing, naming files by checksum |

---

## 1. Read order on a new machine

1. **This file** — rules, state, what's open.
2. `PROJECT_CONTEXT_RevC.md` §8 and §9 — the full technical handoff, including the two reversals this project has had.
3. `TASK_TRACKER.md` Part 0 (measured numbers), Part 1 (the 76 items), Part 2 (the 13 release checks), Part 5 (tasks T-01…T-59), Part 6 (findings 1–46).
4. `STAGE_TRACKER.md` — stage gates S1…S5 with verbatim CTO wording.
5. `REPLY_TO_CTO.md` — the only outbound document.
6. `work done` (root, no extension) — the latest session report. `pcb\work done` is the older milestone log.

**Authority chain:** tool output → `TASK_TRACKER.md` → `STAGE_TRACKER.md` → `REPLY_TO_CTO.md` → `revC\ResponseSheet_RevC.csv` (generated). Never the reverse. The CSV is never hand-edited.

---

## 2. Verified state — re-run these to confirm before trusting anything below

```powershell
$kc = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
& $kc sch erc --severity-all --format json -o _cto_extract\erc_now.json pcb\MoriShield_Carrier.kicad_sch
& $kc pcb drc --refill-zones --schematic-parity --severity-all --all-track-errors `
      --format json -o _cto_extract\drc_now.json pcb\MoriShield_Carrier.kicad_pcb
& 'C:\Program Files\KiCad\10.0\bin\python.exe' pcb\_census.py
& 'C:\Program Files\KiCad\10.0\bin\python.exe' pcb\_plot_stitching_final.py
python _cto_extract\trace2.py
python _cto_extract\gate_truth.py
python _cto_extract\final_verify.py
```

Expected as of 2026-11-04 09:15:

| Measure | Value |
|---|---|
| ERC | 0 violations, `ignored_checks []` |
| DRC | **0 violations, 0 unconnected, 0 parity**, `ignored_checks []` |
| Census | 161 footprints · 1150 segments · 319 vias · 6 zones · 136 nets |
| Total copper length | **5142.324 mm** |
| Vias inside SMD pads | **67** |
| E1 ground stitching | **148 links, worst 10.00 mm, 0.0 % beyond 10 mm** |
| Release gate | **4 met** (C1, C2, C5, C12) · **1 partly** (C9) · **8 not met** |
| S3 gate | C2 ✅ C5 ✅ C12 ✅ · **C9 ❌ C10 ❌** |
| Traceability | 76 ids in register/reply/CSV, **0 status disagreements, 0 priority mismatches** |
| `revC\pack.ps1` | passes Gates 1–4, stops at **GATE 5 PRODUCTION** (no release Gerbers) |
| Decoupling | 36 supply pins: **1 meets both, 3 meet local, 33 fail** — verdicts MOVE 3 / ADD 13 / NONE 20 |

**Latest design file:** `pcb\MoriShield_Carrier.kicad_pcb`. Everything else (`4L\`, `6L\`, `backup\`, `pcb\_snap\`, `.history\`, `_cto_extract\V5_*`, `revC\_work\scratch\`) is history or a test copy. Never open one of those and save.

---

## 3. What this project is, in one paragraph

A 178.15 × 118.15 mm 4-layer carrier in a 200 × 155 × 80 mm enclosure, feeding **5 V at J18 from an external buck converter that Serigreen supplies and mounts in the box**. Two socketed modules — **ESP32-S3 (EdgeHax/Keyestudio S3-PRO, WROOM-1 N16R8)** on J1/J2 and **Parry A7672S LTE** on J3/J4 — plus an **E22-900T22D LoRa** on J6, an E22-class satellite radio, and sensors: FDC1004 capacitance (J21 = I2C channel 5), SPS30 particulate (J13), SGP41 (J11), SHT45 (J12), BME688 (J14), MPU-6050 (J7), DS3231 RTC (J8), AS5600 wind direction (J26), reed wind speed (J22), two analog soil/FSR inputs (J15, J16), panel LEDs (J24), buzzer (J25), event button (J23). **RS485 was removed** — wind is now reed + AS5600, and the soil probe is read on demand by laptop through a USB-RS485 adapter. The 12 V rail is gone; the board is 5 V throughout.

**Requirement universe:** 76 items (A1–H6 from MS-CAR-REV-A-004 Table 9 = "the 59 items", plus R1–R17 from MS-CAR-REV-B-001 Table 13), 13 release checks (CHK-001 §4), 16 pre-send ticks (CHK Table 11), 6 conditions on the 5 V input (§6.4), 8 package rows (CHK Table 2). Source text is in `_cto_extract\*.txt` — **quote from those, never from memory.**

---

## 4. Standing rules — every one of these exists because of a mistake already made

### 4.1 Verification rules

1. **DRC must always carry all four flags.** Without `--schematic-parity` the parity section is silently empty and reads 0. This produced false "clean" results twice.
2. **Parity 0 is not evidence.** A net rename on 2026-11-02 kept parity at 0 and broke the copper. Prove: parity 0 **and** unconnected 0 **and** DRC 0 **and** ERC 0 **and** a per-pad connectivity read-back.
3. **`pcbnew` Save re-issues every UUID and merges collinear segments.** The segment count can fall with no copper lost. Therefore: always re-run DRC immediately before text surgery to get current UUIDs, and guard with **total copper length**, not counts. (`pcb\_census.py` prints both.)
4. **A KiCad local label named `X` produces the net `/X`.** A board net written without the leading slash produces `net_conflict` on the label side only — which looks like a pin-order bug and is not. This cost a day on 2026-11-04.
5. **Cloning a board footprint by regex on `(at …)` is unsafe.** KiCad omits the rotation field when it is `0`, and `(at …)` also appears in every property line. Take the footprint's own `at` from the s-expression parser as the child of the footprint node. This is why T-59 batch 3 failed twice on 2026-11-04.
6. **The stitching metric is not a DRC check.** A copper change can silently break E1 while DRC stays 0. Re-run `pcb\_plot_stitching_final.py` after **any** copper, via or zone change, before any document repeats a number.
7. **Never type a summary count.** Recompute the gate tally with `_cto_extract\gate_truth.py`. A typed tally was wrong in two documents on 2026-11-03.
8. **Timestamps are evidence.** `pack.ps1` gates 1 and 4 exist because Rev B shipped Gerbers older than the board (finding R1). If a derived file predates the design, it is wrong regardless of content.

### 4.2 Honesty rules

9. **Never describe this board as a non-production build** — not even inside a denial or a rule that bans it. Automated scans count occurrences, so the banned term must not appear anywhere in any project document.
10. **Never claim fabrication readiness.** Never mark an item Done unless a tool or measurement proves it.
11. **Never invent** MPNs, ratings, temperatures, module heights, dielectric data, fab capabilities or measurements. Write `TBC` and raise a question. Generic passive values plus a footprint are allowed; MPN stays `TBC`.
12. **A reverted attempt must be visible.** If work was rolled back, the outbound reply must not still describe it as landed. This happened on 2026-11-03 — prose said "resolved" while status said "Open".
13. **Own your own errors.** Qoder has been wrong three times in this project (the "mirror-image" claim, the 460-item phantom, a typed tally). Say so plainly and show the control that disproved it.

### 4.3 Process rules

14. **Qoder never edits design files.** Board and schematic belong to Devin. Documents and the reply belong to Qoder. Not both tools in one pass on one file.
15. **Aswin must not open the board or schematic in KiCad while Devin works** — his save silently overwrites, no merge.
16. **Snapshot before every edit** to `pcb\_snap\<purpose>_<stamp>\`, and report rollback paths in every session report.
17. **Relative paths in every prompt and script.** 95 files still embed the old absolute workspace path — treat that as migration debt.

---

## 5. Open work

### 5.1 Devin — next, in order

| # | Work | Why it's next | Scope |
|---|---|---|---|
| 1 | **T-59 batch 3** — one 100 nF on `/+5V_ESP` for D7.1 | Smallest possible batch; the plan is already written and correct, only the footprint-placement parse was wrong. Fix rule 5 first, then it should land first try | S |
| 2 | **T-59 batch 1** — `3V3_C` has **no bulk capacitor at all**, 6 pins (J1.1, J4.3, J7.2, J7.8, J8.5, J26.1) | A power-integrity fact, not a paperwork item | M |
| 3 | **T-59 batch 2** — `/3V3_SENS_SW` has one bulk (C51) 22.8–89.2 mm from 5 pins | Same class | M |
| 4 | **T-59 batch 4** — `+5V` J24.1, 100 nF site won't fit beside the movable bulk | May end as NONE with a reason | S |
| 5 | **The wrap** — regenerate BOM/POS/vias list/FAB_NOTES/plot/reports, update the three documents, CSV, `trace2`, `gate_truth`, `pack.ps1`, session report | Only after a batch actually lands | S |

**Batching insight:** the 13 ADD pins are **4 net-level problems**, not 13 pin jobs. Verify once per net, not once per pin — that is what made it look like 40 cycles and impossible.

### 5.2 Blocked, and on whom

| Blocked item | Waiting on |
|---|---|
| **R4 / U10 protection**, condition 2, gate C8 | Serigreen's route-C deviation signature |
| **Converter**, condition 1, B1, B2, B10, gate C7 | Serigreen — they supply it. Our audit says **No-Go** on the XL4015 (8–36 V operating, 40 V absolute max) |
| **E3 antenna keep-outs** | Aswin: ESP32 antenna tab length, modem U.FL position |
| **R12 / In2 clearing** (61 segments, 431.40 mm, 7 nets) | All seven corridors measured **negative** (−0.30 to −0.60 mm) → needs rerouting, not corridor-hunting |
| **C8 ESD within 5 mm** (11.3–27.6 mm at J11–J23; none at J24/J25/J26) | Placement + reroute; new arrays need MPNs |
| **E7** 47 Ω on 10 cabled I2C lines | Schematic surgery; only attempted with parity provable |
| **Stack-up, S4 package, zip** | Fab capability sheet; Serigreen's written release |
| **B10, C2 24-hour, R11 counts, A2 registration** | **First boards — the carrier is not manufactured** |
| **J17 / J20 identity** | Aswin or Serigreen; J20 blocks the LoRa keep-out corridor |

### 5.3 Aswin — the physical list

Calipers and a camera, ~20 minutes: ESP32 antenna tab tip → nearest header hole; modem U.FL position and height; **female-header plastic height and pin protrusion** (the number that decides everything under a module); GY-521 and DS3231 heights and battery diameter; MX126 terminal height and wire-entry side. Plus: send the Serigreen questions, tell firmware that **E22 configuration mode is 9600 8N1 only**, and decide whether the microSD slot must work. The full step-by-step is in `me.md` (root) and `PROJECT_CONTEXT_RevC.md` §9.

---

## 6. Facts that took real effort to establish — do not re-derive them

| Fact | Status |
|---|---|
| **J6 is NOT mis-wired.** It is numbered for a **180° insertion**; all seven nets line up that way. The real defect was that nothing marked or keyed the orientation (item A3) | Settled 2026-11-03. Never write "mirror image" about J6 again |
| **microSD owns GPIO10, 11, 12, 13** (CS, MOSI, CLK, MISO). **GPIO9 and GPIO14 are not on the slot** — so `/I2C0_SCL` on GPIO9 is safe, and CHK-001 C11 is wrong to include GPIO14 | Measured by Aswin's multimeter |
| **GPIO35–38 are the octal-PSRAM group** on the N16R8 and unusable. **GPIO39 (J2.9) is the only free usable input** in that block — now carries the reed | Settled |
| **E22 mode table, verbatim:** Normal M0=0/M1=0 · WOR M0=1/M1=0 · **Configuration M0=0/M1=1** · Deep sleep 1/1. Configuration is **9600 8N1 only** | `_cto_extract\E22-900T22D-UserManual.txt` §6.2–6.5, §7.1 |
| **Strapping M0/M1 to GND was chosen over driving them from expander U8** — a hard strap is deterministic and does not put radio mode behind a muxed, cabled I2C bus that R17 already says is unreliable | Decision, in `TASK_TRACKER.md` |
| **E1 was closed by a GND pour on B.Cu, not F.Cu** — F.SilkS has 1575 graphics, B.SilkS has **zero**. A front pour would flag copper under every label | Settled 2026-11-02 |
| **A 92 mm whip will not stand inside an 80 mm box** → two sealed SMA bulkheads in the lid; a drilled hole is not IP65 | Settled |
| **The FDC1004 is on J21 = channel 5.** J15 is a separate *analog* soil input on GPIO2 = ADC1_CH1. Both analog inputs are on **ADC1**, which keeps working with Wi-Fi on | Settled |
| **`3V3_C` has no bulk capacitor anywhere on the rail** | Current finding, drives T-59 batch 1 |
| **A 5 V E22 presents ~5 V on TXD/AUX; the ESP32-S3 is not 5 V tolerant** → propose 3V3 for that module (open question 7) | Open |

---

## 7. How to write a Devin prompt that works

Structure every prompt the same way — this format has converged where free-form instructions didn't:

1. **Title** naming the tasks and the rule that changed since last time.
2. **Paths** — relative to the workspace root, and an explicit "do not hard-code absolute paths".
3. **Read first** — the specific files and sections.
4. **State on entry** — the numbers, with "re-confirm; stop and report any difference".
5. **Rules** — only the ones that bind this run, plus the standing verification rules.
6. **Tasks** — each with exact coordinates, net names **with their leading slash**, and a per-task verification gate.
7. **Stop conditions** — "if parity is not 0, restore and report the exact object and coordinate. Two failed attempts means stop."
8. **DO NOT** list — what's blocked and why, so it isn't rediscovered.
9. **REPORT BACK** — a numbered contract: the four numbers per task, census incl. copper length, stitching after any copper change, pad-net read-backs, recomputed gate tally, rollback paths, and "write *not verified* where you could not verify".

**Always put the newest trap at the top of the rules block.** That is the only reason rule 5 above will save the next run a day.

---

## 8. Machine migration checklist

- [ ] Copy the **whole** `new pcb` folder. Let OneDrive finish first.
- [ ] Must travel together: `pcb\` **including `pcb\_snap\`**, `morishield\morishield_hardware\libraries\` (**without the `.pretty`, ERC reports 124 phantom errors**), `revC\`, `_cto_extract\`, the four root documents, `QODER.md`, `me.md`, `work done`, the two vendor pinout `.md` files.
- [ ] Install **KiCad 10.0** at `C:\Program Files\KiCad\10.0`. Scripts hard-code it. Use `bin\python.exe` for anything importing `pcbnew` — plain `python` has no `pcbnew`.
- [ ] 95 files embed `C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb`. Either recreate that path exactly, or do one replacement pass over `revC\*.ps1` and `pcb\*.py`.
- [ ] Run the §2 command block. If all seven numbers match, the machine is at the same state as this one.
- [ ] PowerShell: avoid multi-line inline `python -c` — quoting breaks it. Write a script file into `_cto_extract\` and run that.
- [ ] Never edit `sym-lib-table` / `fp-lib-table` with backslash paths — they are eaten as escapes, resolution fails silently, and ERC invents hundreds of `lib_symbol_issues`.

---

## 9. Definition of done for the next milestones

**S3 complete** = C2, C5, C9, C10 and C12 all met. Today three are met. **C9 needs T-59 finished plus the 3D check with real heights; C10 needs the In2 clearing, the antenna rule areas, and power copper meeting C7 — and that last clause is gated on Serigreen.** S3 is therefore not reachable without external answers, and no prompt should imply otherwise.

**S4 (fabrication release)** additionally needs: release Gerbers and drill plotted *after* a clean DRC, an **IPC-D-356 netlist (none exists in `revC\` today)**, a job file with the real stack, a fab drawing, BOM lines with manufacturer/MPN/rating/temperature, and the three timestamps recorded in the response sheet.

**Nothing in this project authorises fabrication.** Release is Serigreen's, in writing, naming the exact file set by checksum.
