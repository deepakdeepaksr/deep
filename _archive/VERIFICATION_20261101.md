# Verification — `pcb\` package, 1 November 2026

| | |
|---|---|
| **Files tested** | `pcb\MoriShield_Carrier.kicad_pcb` (saved 11-01 00:16), `pcb\MoriShield_Carrier.kicad_sch` (10-31 23:40) |
| **Against** | `4L\` baseline, re-run on the same machine state so the comparison is honest |
| **Tool** | KiCad 10.0.6 `kicad-cli`, `--refill-zones --schematic-parity --severity-all --all-track-errors` |
| **Reports** | `_cto_extract\erc_pcb4.json`, `_cto_extract\drc_pcb3.json` |

## 1. Verdict

**The board work is real and it is good. The package is not sendable yet** — one silkscreen marking will mis-wire a board, the 4 A path is still 0.3 mm where it matters most, and the schematic does not know about any of the new hardware.

## 2. Confirmed fixed — independently verified, not taken on trust

| Claim | Evidence | Verdict |
|---|---|---|
| Watchdog net connected | `unconnected 1 → 0`. U8 pad 11 = `/WDT_WDI`, pad 17 = no net. Route traced segment by segment: U8.11 (249.90,169.93) → F.Cu → via (250.45,169.90) → B.Cu → (249.50,170.90) → (248.00,170.30) → (244.50,173.50) → … → U4 | ✅ **R2 (P0) closed, and without a 0 Ω jumper** |
| No 0 Ω needed | No new footprint of that kind; 224 → 233 vias, 1368 → 1405 tracks | ✅ |
| Nothing damaged | footprints 157 → 159 (**added J26, U10; removed none**), nets 71 → 73 (**added `/MODEM_RST`, `/5V_PROT`; removed none**) | ✅ |
| No shorts or clearance errors | DRC has **zero** `clearance`, `shorting_items`, `tracks_same_net` or `track_crossing` entries | ✅ |
| Dangling copper improved | `via_dangling 5 → 3` | ✅ −2 |
| J26 as proposed | 4-pin JST-XH at (162.45, 181.35): pad 1 `3V3_C`, 2 `GND`, 3 `/I2C1_SCL`, 4 `/I2C1_SDA` | ✅ |
| `/MODEM_RST` endpoints | J1 pad 6 (209.50,141.30) → J4 pad 8 (269.50,131.34), 0.25 mm, 4 vias | ✅ endpoints, ⚠ angle — §5.5 |
| Input run widened | `+5V_IN` J18→F1 now **1.5 mm × 3 segments** (was 0.5 mm) | ✅ that leg only — §5.2 |

## 3. A folder defect, now fixed — and a correction to my own first reading

`pcb\` was **missing `sym-lib-table`, `fp-lib-table` and `MoriShield_Carrier.kicad_sym`**. First ERC run returned **441 warnings** (328 `lib_symbol_issues` + 113 `footprint_link_issues`) where 4L had returned none.

I also found that the inherited `fp-lib-table` points at `${KIPRJMOD}/../../MORISHIELD/source/MoriShield_Carrier.pretty` — **that path does not exist on this machine.** The real library is at `morishield\morishield_hardware\libraries\MoriShield_Carrier.pretty`.

**What I changed in `pcb\`** (nothing in the design itself):

| File | Now points at | Effect |
|---|---|---|
| `fp-lib-table` | `${KIPRJMOD}/../morishield/morishield_hardware/libraries/MoriShield_Carrier.pretty` | DRC `lib_footprint_issues` **32 → 0**; ERC `footprint_link_issues` **113 → 0** |
| `sym-lib-table` | `${KIPRJMOD}/MoriShield_Carrier.kicad_sym` | ERC `lib_symbol_issues` **328 → 0** |
| `MoriShield_Carrier.kicad_sym` | copied from `4L\` | the symbol library the schematic actually matches |

**Result: ERC is now 0 errors, 0 warnings.** DRC is **165 → 132**, all below the 4L baseline.

**Correction:** my first pass reported the 113 `footprint_link_issues` as a regression from this work. Re-running 4L on the same state shows 113 there too — it was the broken footprint path, present in `4L\` as well. Not their doing.

⚠ **Release trap:** `morishield\morishield_hardware\libraries\MoriShield_Carrier.kicad_sym` is **stale** — pointing `sym-lib-table` at it produces 328 mismatches. The release layout uses `../libraries/` for both tables, so shipping that way would hand the CTO a schematic whose symbols do not match. Either refresh that copy or ship the `.kicad_sym` beside the project.

## 4. What remains, ranked

| # | Item | Severity |
|---|---|---|
| 5.1 | J18 silkscreen `+`/`−` are **swapped** | **P0 — will mis-wire a board** |
| 5.2 | 4 A path still 0.3 mm after the fuse, including the modem's own feed | **P0 — R5, condition 5, B10** |
| 5.3 | Schematic has no J26, no U10, no `/MODEM_RST`, no `/5V_PROT` | **P0 for a sendable package — D1** |
| 5.4 | U10 is a position, not a circuit (5 of 6 pads netless) | P1 — R4 |
| 5.5 | `/MODEM_RST` has a 19.8° segment and runs under the modem | P1 |
| 5.6 | 5 dangling items, Q9 mismatch, 124 silk items | P2 |

## 5. Detail

### 5.1 J18 — the markings are on the wrong pads

| | X | Y | |
|---|---|---|---|
| Pad 1, net `+5V_IN` | 134.47 | **107.25** | the 5 V terminal |
| Pad 2, net `GND` | 134.47 | **102.25** | the ground terminal |
| Silk **`"5v +"`** | 128.00 | **100.50** | ← beside **GND** |
| Silk **`"5v −"`** | 128.00 | **107.00** | ← beside **+5 V** |

An installer who reads the silkscreen connects supply-positive to GND and supply-negative to +5 V. With no reverse protection fitted yet, that goes straight into the board. This is R3, and it is worse than "ambiguous": there are now two confident, wrong labels. The two `text_thickness` DRC warnings are these same texts — the stroke is below the fab minimum, so both need rewriting anyway.

### 5.2 The widened run stops at the fuse

| Net | Where | Width | Carries |
|---|---|---|---|
| `+5V_IN` | J18.1 → F1.1 | **1.5 mm** ✅ | full input |
| `+5V_IN` | (151.50,96.00) → (146.50,96.00) | **0.5 mm** ⚠ | full input |
| `+5V_F` | (161.50,96.00) → (166.50,96.00) | **0.3 mm** ⚠ | full board current, post-fuse |
| `+5V_F` | (166.50,96.00) → (162.94,99.56) → (162.94,103.05) | 0.5 mm ⚠ | full board current |
| `+5V` | **(239.51,95.83) → (232.92,95.83) → (225.50,103.25) on In2.Cu** | **0.3 mm** ⚠ | **the modem's entire 5 V feed — up to 2 A** |
| `/+5V_SENS` | 14 segments | 0.2 mm ⚠ | sensor rail |

(239.51, 95.83) is **J5 pad 1** — the modem's supply. A 0.3 mm inner-layer track is the weakest copper on the board sitting in the highest-current path; inner layers are half-etched, so 0.3 mm there is worse than 0.3 mm external. Roughly: 1.5 mm external ≈ 3 A, 0.5 mm ≈ 1 A, 0.3 mm internal ≪ 1 A.

R5's finding was "0.5 mm input copper behind a 4 A fuse, one 0.3 mm via carries the board". One leg is fixed. The rest is unchanged, so **R5, condition 5 and B10 stay open.**

### 5.3 The schematic does not know any of this

| String | Occurrences in `pcb\…kicad_sch` |
|---|---|
| `J26` | **0** |
| `U10` | **0** |
| `MODEM_RST` | **0** |
| `5V_PROT` | **0** |
| `WDT_WDI` | 2 ✅ — the only change that was synced |
| instances | 377 → 377 (nothing added) |

Parity: `extra_footprint 4 → 6` — J26 and U10 exist only in the board. **"Update PCB from schematic" would delete both and un-net three routes.** The 42 KB size drop between `4L\` and `pcb\` schematics is line-ending normalisation only (both are 717,853 characters of content) — no data was lost.

### 5.4 U10

At (141.00, 100.80), SOT-23-6. Pads 1–5 have **no net**; only pad 6 carries `/5V_PROT`, and that net touches nothing else. So today the input copper is re-routed *around an unconnected footprint*. Honest and correct as a placeholder — but R4 (reverse protection and over-voltage cut-off) is **positioned, not designed**, and the response sheet must say so.

Note also: once J26 and U10 are added to the schematic, U10's five netless pads become **five new unconnected items** unless they are explicitly marked `no_connect`. The current "0 unconnected" is partly propped up by U10 having no nets at all.

### 5.5 `/MODEM_RST` geometry

Final segment (241.00,141.50) → (269.50,131.25): dx 28.50, dy −10.25 → **19.8°**. The board's convention is strict 0/45/90. DRC does not check angles, so this passes silently and will be visible in the render. It also runs between J3 and J4 — under where the modem board sits — which needs a keep-out check against the modem's underside pads.

### 5.6 Leftovers, all pre-existing

3 dangling vias (`/PWR_EN`, `/I2C0_SDA`, `/BUZZER_EN`), one **13.00 mm dangling `3V3_C` track on B.Cu**, one 1.05 mm `/EVENT_BTN` stub, `lib_footprint_mismatch` on **Q9**, 78 `silk_over_copper`, 46 `silk_overlap`.

### 5.7 Folder hygiene before zipping

`.bak`, `.bak2`, `_geom.json` (214 KB), `_probe.kicad_prl` and the six screenshots are mixed in with design files. The screenshots are evidence and should move to `revC\G1\`; the rest must not ship.

## 6. Numbers, one table

| Check | 4L baseline | `pcb` as delivered | `pcb` after the library fix |
|---|---|---|---|
| ERC errors / warnings | 0 / 113 | 0 / 441 | **0 / 0** |
| DRC items | 165 | 164 | **132** |
| — of which `lib_footprint_issues` | 31 | 32 | **0** |
| Unconnected | 1 | 0 | **0** |
| Clearance / shorting | 0 | 0 | **0** |
| Parity `extra_footprint` | 4 | 6 | 6 ⚠ |
| Parity `net_conflict` | 58 | 58 | 58 |
