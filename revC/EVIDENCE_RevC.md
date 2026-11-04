# Evidence index — MoriShield Carrier Rev C

| | |
|---|---|
| **Document** | EV-CAR-4L-RevC-01 |
| **Date** | 2026-11-01 |
| **Board file** | `pcb\MoriShield_Carrier.kicad_pcb` (2,191,893 bytes, 159 footprints) |
| **Status** | Evidence for the items named below. Not a release package. |

Every number here comes from a tool run or a measurement recorded in the file named beside it.
Where a measurement could not be taken, the row says so.

## 1. Tool reports

| Report | Result | Command |
|---|---|---|
| ERC | **0 errors, 0 warnings** | `kicad-cli sch erc --severity-all --format json -o revC\erc_RevC.json pcb\MoriShield_Carrier.kicad_sch` |
| DRC | **0 violations, 0 unconnected, 0 parity** | `kicad-cli pcb drc --refill-zones --schematic-parity --severity-all --all-track-errors --format json -o revC\drc_RevC.json pcb\MoriShield_Carrier.kicad_pcb` |
| Census | 159 footprints · 1171 segments · 314 vias · 6 zones · 134 net names | `pcb\_census.ps1` |

The DRC report was produced on the saved board with zones refilled, parity tested, every
severity included and all track errors reported. The three numbers are reported separately
because a parity section left untested reads as a false zero.

## 2. Decoupling map (B12, C7, C9)

`revC\decoupling_map.csv` — one row per supply-net load pad: the net, the load, the nearest
capacitor on the same net, its value, the distance, and the method.

| Measure | Value |
|---|---|
| Load pads on the supply nets | 92 |
| Within 10 mm | **17** |
| Distance measured along a track path | 30 rows |
| Distance through a plane (straight-line lower bound) | 54 rows |
| No path found | 8 rows |

**Method.** Distances are shortest paths on the track-and-via graph, each via counted as zero
length. Where a pad connects to a copper plane rather than a track, the straight-line distance
is recorded and the row is marked `plane-lower-bound`: the real path through the plane is not
longer in resistance terms but cannot be measured as a track length. This is a partial
evidence document: it does not close B12, which asks for 10 mm or a stated reason for every
supply point.

## 3. Ground stitching (E1)

`revC\_evidence_maps.json` — sampling of the filled GND plane on In1.Cu at a 1 mm grid.

| Measure | Value |
|---|---|
| Ground links that touch the plane (GND vias and GND through-hole pads inside the fill) | **58** |
| Plane samples at 0.5 mm | 78,406 |
| Farthest point of the plane from a ground link | **35.36 mm** |
| Share of the plane more than 10 mm from a link | **55.6 %** |
| Plot | `revC\E1_stitching_plot.png` |

**E1 is not met.** The acceptance is "no point of either ground pour more than 10 mm from a
ground link (antenna keep-out excepted)". The plane is continuous, but more than half of it is
beyond 10 mm and the worst point is 35.36 mm away.

**Correction to the earlier figure.** The previous 25.9 mm / 37.4 % counted 87 links by taking
every through-hole GND pad regardless of whether it lay inside the plane fill. A pad outside the
fill does not connect to the plane, so it is not a link. The strict set is 58, and the metric is
worse than reported.

**Why stitching vias cannot fix this.** 114 vias were planned at a 0.5 mm grid and added; DRC
reported **all 114 as `via_dangling`**. The board has GND copper only on In1 — there is no GND
pour on F.Cu or B.Cu — so a via dropped into the plane connects on one layer only and is
electrically a stub. This was proved by a control: one via placed **on** an existing F.Cu GND
track produced **0 violations**, while the same via in the pour alone was flagged. The best case
obtainable from existing copper, adding a link every 1 mm along every GND track, leaves
**33.1 % of the plane beyond 10 mm** and the same 24.12 mm worst point (measured with the looser
99-link set). Meeting E1 needs new ground copper on an outer layer, which is a stack-up and
layout decision and cannot be added through this build's zone API (it crashes on save).

## 4. ESD placement (C8)

`revC\_esd_measure.json` — shortest copper path from each field connector pad to a pad of its
protecting array.

| Connector | Worst copper-path distance | Array |
|---|---|---|
| J11 | 23.78 mm | ESD7 |
| J12 | 24.47 mm | ESD8 |
| J13 | 20.76 mm | ESD11 |
| J14 | 13.03 mm | ESD10 |
| J15 | 27.62 mm | ESD4 |
| J16 | 26.54 mm | ESD3 |
| J17 | 17.82 mm | ESD9 |
| J20 | 14.44 mm | ESD18 |
| J21 | 11.29 mm | ESD12 |
| J22 | 18.19 mm | ESD17 |
| J23 | 15.67 mm | ESD20 |
| J24 (lamps) | — | **none** |
| J25 (buzzer) | — | **none** |
| J26 (wind vane) | — | **none** |

No connector meets the 5 mm rule. J24, J25 and J26 have no protection at all. Panel lamps,
buttons and buzzers count as leaving the box under C8.

## 5. Vias inside SMD pads (R16)

| Measure | Value |
|---|---|
| Vias on the board | 314 |
| Vias whose centre lies inside an SMD pad | **65** |
| Positions | `revC\vias_in_pads.txt` |

DRC cannot see this: KiCad does not flag via-in-pad by default. The count is unchanged from
Rev B.

## 6. Copper on the plane layer (R12, C10)

| Measure | Value |
|---|---|
| Track segments on In2.Cu | **63** |
| Total length on In2.Cu | **448.41 mm** |
| Nets | `/LED_DRV2` 14, `/+5V_SENS` 13, `3V3_C` 10, `/LED_DRV1` 8, `/I2C0_SCL` 7, `/SENS_EN` 7, `+5V` 2, `/I2C0_MUX_SC0` 2 |
| Track on In1.Cu (the ground plane) | 0 mm |

## 7. Sensor rail resistance (B4, C7)

`/+5V_SENS`, measured from the board file at 0.505 mΩ/square outer and 1.01 mΩ/square inner,
20 °C, the copper weights being assumptions until the fab confirms them.

| Layer | Width | Segments | Length | Resistance |
|---|---|---|---|---|
| B.Cu | 0.8 mm | 5 | 16.6 mm | 10.5 mΩ |
| F.Cu | 0.8 mm | 9 | 12.5 mm | 7.9 mΩ |
| F.Cu | 0.6 mm | 8 | 12.4 mm | 10.4 mΩ |
| F.Cu | 0.5 mm | 2 | 9.5 mm | 9.6 mΩ |
| In2.Cu | 0.8 mm | 7 | 21.1 mm | 26.6 mΩ |
| In2.Cu | 0.6 mm | 1 | 0.3 mm | 0.5 mΩ |
| In2.Cu | 0.5 mm | 5 | 55.4 mm | 111.9 mΩ |
| **Total** | | **37** | **127.8 mm** | **177.4 mΩ** |

It was 313 mΩ before this session. The remaining 112 mΩ sits in 55.4 mm of 0.5 mm In2 copper
along the J7 pad row: at 0.8 mm the track breaks J7's pad clearance, and the F.Cu corridor is
occupied. Widening it further needs J7 moved or the run rerouted.

## 8. Renders

`revC\render_top.png`, `render_bottom.png`, `render_iso.png` — 1800 × 1000, high quality,
plotted from the current board.

**What they do not show:** the plug-in modules and the enclosure. The module outlines are on
Dwgs.User and F.Fab at their real sizes but carry no heights, two of them are on the wrong
sockets (R14), and no 3D model is attached to the sockets. A4 and C9 therefore remain open;
the renders prove the carrier only.

## 9. C3 timestamp record, 2026-11-02

| Event | Time |
|---|---|
| Board saved | 2026-11-02 22:31:44 |
| DRC on the saved file | 2026-11-02 22:45:13 |
| Gerber + drill plot into `revC\silk_check\` | 2026-11-02 22:45:15 |

The order save -> DRC -> plot is correct. J18 marks on this plot: `+` centre y 107.20 against pad 1 at 107.25
(**Delta 0.05 mm**), `-` centre y 102.20 against pad 2 at 102.25 (**Delta 0.05 mm**), both 6.3 mm beside their pads.
