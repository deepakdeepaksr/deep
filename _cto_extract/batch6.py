import json, collections, os, io

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
d = json.load(open(os.path.join(P, 'revC', 'drc_RevC.json'), encoding='utf-8'))

print('=== the 124 silk items, classified so the work can be targeted ===')
kinds = collections.Counter()
bypart = collections.Counter()
for v in d['violations']:
    if v['type'] not in ('silk_over_copper', 'silk_overlap'):
        continue
    its = v.get('items') or []
    descs = [(i.get('description') or '') for i in its]
    who = ' / '.join(descs[:2])
    kind = 'other'
    for k in ('Reference field', 'Value field', 'F.Silkscreen', 'Segment', 'Footprint'):
        if any(k in x for x in descs):
            kind = k
            break
    kinds[(v['type'], kind)] += 1
    for x in descs:
        for tok in x.replace(' of ', ' ').split():
            if tok.startswith(('J', 'U', 'R', 'C', 'Q', 'D', 'ESD', 'TP', 'H', 'F', 'SW', 'FB')) and \
               tok[1:].isdigit():
                bypart[tok] += 1
                break
        break

for (t, k), n in sorted(kinds.items(), key=lambda x: -x[1]):
    print('   %-18s %-18s %4d' % (t, k, n))
print('\n   worst offenders (parts appearing in the most silk violations):')
for part, n in bypart.most_common(18):
    print('     %-8s %3d' % (part, n))
print('   distinct parts involved: %d' % len(bypart))

# ---------------- pack script ----------------
pack = r'''# Builds the Rev C release zip from the live design files.
# Run it at send time - never ship a zip built from an earlier run.
$ErrorActionPreference = 'Stop'
$root = 'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
$src  = Join-Path $root 'pcb'
$out  = Join-Path $root 'revC'
$stamp = Get-Date -Format 'yyyy-MM-dd'
$zip   = Join-Path $root ("MoriShield_Carrier_RevC_{0}.zip" -f $stamp)

# --- gate 1: the design files must be the ones that were checked ---
$board = Join-Path $src 'MoriShield_Carrier.kicad_pcb'
$sch   = Join-Path $src 'MoriShield_Carrier.kicad_sch'
$pro   = Join-Path $src 'MoriShield_Carrier.kicad_pro'
$drc   = Join-Path $out 'drc_RevC.json'
$erc   = Join-Path $out 'erc_RevC.json'

if ((Get-Item $board).LastWriteTime -gt (Get-Item $drc).LastWriteTime) {
    throw 'DRC report is OLDER than the board. Re-run DRC before packing. (This is finding R1.)'
}
if ((Get-Item $sch).LastWriteTime -gt (Get-Item $erc).LastWriteTime) {
    throw 'ERC report is OLDER than the schematic. Re-run ERC before packing.'
}

# --- gate 2: production files must be newer than the board they describe ---
$prev = Join-Path $out 'preview_do_not_ship'
if (Test-Path $prev) {
    $oldest = (Get-ChildItem $prev -File | Measure-Object -Property LastWriteTime -Minimum).Minimum
    if ($oldest -and $oldest -lt (Get-Item $board).LastWriteTime) {
        Write-Warning 'Gerbers in preview_do_not_ship are stale relative to the board. Re-plot for a release package.'
    }
}

# --- gate 3: nothing from the previous revision, no working files ---
$exclude = @('*.bak', '*.bak2', '_geom.json', '_probe.kicad_prl', '__pycache__', '_snap', '_shots_revC', '_evidence')
$stage = Join-Path $env:TEMP ("revC_stage_{0}" -f $stamp)
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Path (Join-Path $stage 'project') | Out-Null

foreach ($f in @('MoriShield_Carrier.kicad_pcb','MoriShield_Carrier.kicad_sch','MoriShield_Carrier.kicad_pro',
                'MoriShield_Carrier.kicad_sym','fp-lib-table','sym-lib-table')) {
    Copy-Item (Join-Path $src $f) (Join-Path $stage 'project')
}
Copy-Item $drc, $erc -Destination $stage
Copy-Item (Join-Path $out 'MoriShield_Carrier_RevC_schematic.pdf') -Destination $stage -ErrorAction SilentlyContinue
Copy-Item (Join-Path $out '*_bom.csv'), (Join-Path $out '*_pos_*.csv') -Destination $stage -ErrorAction SilentlyContinue
if (Test-Path (Join-Path $out 'ResponseSheet_RevC.csv')) {
    Copy-Item (Join-Path $out 'ResponseSheet_RevC.csv') -Destination (Join-Path $stage '00_ResponseSheet_RevC.csv')
} else {
    throw 'ResponseSheet_RevC.csv is missing. It must be the FIRST file in the zip (CHK section 7).'
}

$files = Get-ChildItem $stage -Recurse -File | Where-Object {
    $n = $_.Name
    -not ($exclude | Where-Object { $n -like $_ })
}
Compress-Archive -Path $files.FullName -DestinationPath $zip -Force

# --- checksums, which is how the release is named in writing ---
$files | Get-FileHash -Algorithm SHA256 |
    ForEach-Object { '{0}  {1}' -f $_.Hash, (Split-Path $_.Path -Leaf) } |
    Set-Content (Join-Path $root ("MoriShield_Carrier_RevC_{0}_SHA256.txt" -f $stamp))

Write-Host ("packed {0} files -> {1}" -f $files.Count, $zip)
Write-Host 'save, DRC and plot timestamps are recorded in the SHA256 file timestamp'
'''
io.open(os.path.join(P, 'revC', 'pack.ps1'), 'w', encoding='utf-8').write(pack)
print('\nrevC\\pack.ps1 written - it refuses to pack if the reports are stale')

# ---------------- fab notes ----------------
notes = """# Fabrication and assembly notes - MoriShield Carrier, Rev C

**Status: draft.** Written from our own rule set, not from a fab capability sheet.
Everything marked ASSUMPTION must be confirmed against Serigreen's or the fab's
document before a release package is built (dependency D-7).

## Board
| | |
|---|---|
| Layers | 4 |
| Finished thickness | 1.6 mm |
| Copper, outer | 1 oz (35 um) - ASSUMPTION |
| Copper, inner | 1/2 oz (17.5 um), half-etched - ASSUMPTION |
| Laminate | Tg 150 C or better |
| Build standard | IPC-6012 Class 2 |
| Solder mask | Green, LPI |
| Silkscreen | White, minimum stroke 0.15 mm, minimum height 1.0 mm |
| Surface finish | ENIG - to be confirmed (F3) |

## Minimum features (our rules, not the fab's)
| | |
|---|---|
| Track / gap | 0.20 mm |
| Via | 0.60 mm pad / 0.30 mm drill, annular 0.15 mm minimum |
| Copper to board edge | 0.50 mm |
| Clearance, signal | 0.20 mm |
| Clearance, 5 V power | 0.25 mm |
| Clearance, PE to any other net | 0.30 mm |

## Vias in SMD pads
**To be counted and declared.** Rev B had 65. Hand assembly means unfilled vias in a
pad drain solder and starve the joint, so any via remaining inside a pad must be
specified **filled and capped** on the fab drawing. This is finding R16 and it is
still open.

## Power copper
The 5 V input run from J18 through the protection to the plane is required to be a
**pour of 3 mm or more with six or more 0.3 mm vias at every layer change**
(condition 3, MS-CAR-CHK-001 C10). Today it is a 1.5 mm track. This is open.

## Resistances used in the design justification
0.505 mOhm per square outer, 1.01 mOhm per square inner, at 1 oz / 1/2 oz and 20 C.
Add 0.39 % per C. **These follow from the copper weights above, which are assumptions.**

## Assembly
Hand soldered, no panelisation, individual boards. Fiducials not required.
The modem board on J3/J4 is **not keyed** - the silkscreen now carries a `1` mark at
each socket's pin 1 and the note `MODEM THIS WAY UP`. Confirm during assembly that
the modem's UART row lands on the carrier's J4.
"""
io.open(os.path.join(P, 'revC', 'FAB_NOTES.md'), 'w', encoding='utf-8').write(notes)
print('revC\\FAB_NOTES.md written - assumptions labelled as assumptions')
