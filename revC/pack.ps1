# Builds the Rev C release zip from the live design files.
# Run it at send time - never ship a zip built from an earlier run.
$ErrorActionPreference = 'Stop'
$root = 'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
$src  = Join-Path $root 'pcb'
$out  = Join-Path $root 'revC'
$stamp = Get-Date -Format 'yyyy-MM-dd'
$zip   = Join-Path $root ("MoriShield_Carrier_RevC_{0}.zip" -f $stamp)

$board  = Join-Path $src 'MoriShield_Carrier.kicad_pcb'
$sch    = Join-Path $src 'MoriShield_Carrier.kicad_sch'
$pro    = Join-Path $src 'MoriShield_Carrier.kicad_pro'
$dru    = Join-Path $src 'MoriShield_Carrier.kicad_dru'
$sym    = Join-Path $src 'MoriShield_Carrier.kicad_sym'
$pretty = Join-Path $root 'morishield\morishield_hardware\libraries\MoriShield_Carrier.pretty'
$drc    = Join-Path $out 'drc_RevC.json'
$erc    = Join-Path $out 'erc_RevC.json'

# --- GATE 2: the inputs the package needs must all be present ---
foreach ($f in @($board, $sch, $pro, $dru, $sym)) {
    if (-not (Test-Path $f)) { throw "missing design file: $f" }
}
if (-not (Test-Path $pretty)) { throw "missing footprint library: $pretty" }

# --- GATE 1: the reports must describe the design files that ship ---
if ((Get-Item $board).LastWriteTime -gt (Get-Item $drc).LastWriteTime) {
    throw 'GATE 1 REPORTS: the DRC report is OLDER than the board. Re-run DRC before packing. (Finding R1.)'
}
if ((Get-Item $sch).LastWriteTime -gt (Get-Item $erc).LastWriteTime) {
    throw 'GATE 1 REPORTS: the ERC report is OLDER than the schematic. Re-run ERC before packing.'
}

# --- GATE 4: derived files must be newer than the board they describe ---
# A BOM or placement file older than the board describes a different board,
# which is exactly the Rev B defect C6 names.
$bom  = Join-Path $out 'MoriShield_Carrier_RevC_bom.csv'
$posf = Join-Path $out 'MoriShield_Carrier_RevC_pos_front.csv'
$posb = Join-Path $out 'MoriShield_Carrier_RevC_pos_back.csv'
foreach ($f in @($bom, $posf)) {
    if (-not (Test-Path $f)) { throw "GATE 4 DERIVED: missing $f" }
    if ((Get-Item $f).LastWriteTime -lt (Get-Item $board).LastWriteTime) {
        throw ("GATE 4 DERIVED: {0} is OLDER than the board (C6). Regenerate BOM and placement from the saved board." -f (Split-Path $f -Leaf))
    }
}
if (Test-Path $posb) {
    if ((Get-Item $posb).LastWriteTime -lt (Get-Item $board).LastWriteTime) {
        throw 'GATE 4 DERIVED: the back placement file is OLDER than the board (C6).'
    }
}

# --- GATE 3: the response sheet must exist, and must be the first file ---
$sheet = Join-Path $out 'ResponseSheet_RevC.csv'
if (-not (Test-Path $sheet)) {
    throw 'GATE 3 SHEET: ResponseSheet_RevC.csv is missing. It must be the FIRST file in the zip (CHK section 7).'
}

# --- GATE 5: production files must exist and post-date both the board and the DRC ---
# CHK C3: refill -> save -> DRC -> plot. A Gerber set older than the DRC was
# plotted from a different state, which is the failure that caught Rev B (R1).
$gerb = Join-Path $out 'gerber'
if (-not (Test-Path $gerb)) {
    throw 'GATE 5 PRODUCTION: no release Gerber set at revC\gerber. Plot after the design settles (S4). No zip is built.'
}
$oldest = (Get-ChildItem $gerb -File -Recurse | Measure-Object -Property LastWriteTime -Minimum).Minimum
if (-not $oldest) { throw 'GATE 5 PRODUCTION: revC\gerber is empty. No zip is built.' }
if ($oldest -lt (Get-Item $drc).LastWriteTime) {
    throw 'GATE 5 PRODUCTION: the Gerbers are OLDER than the DRC report. Re-plot, then pack (CHK C3).'
}
$drill = Join-Path $out 'drill'
if (-not (Test-Path $drill)) { throw 'GATE 5 PRODUCTION: no drill files at revC\drill. No zip is built.' }

# --- stage ---
$exclude = @('*.bak', '*.bak2', '_geom.json', '_probe.kicad_prl', '__pycache__', '_snap', '_shots_revC', '_evidence')
$stage = Join-Path $env:TEMP ("revC_stage_{0}" -f $stamp)
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
$proj = Join-Path $stage 'project'
New-Item -ItemType Directory -Path $proj | Out-Null
New-Item -ItemType Directory -Path (Join-Path $proj 'libraries') | Out-Null

foreach ($f in @('MoriShield_Carrier.kicad_pcb','MoriShield_Carrier.kicad_sch','MoriShield_Carrier.kicad_pro',
                'MoriShield_Carrier.kicad_sym','MoriShield_Carrier.kicad_dru')) {
    Copy-Item (Join-Path $src $f) $proj
}

# The footprint and symbol libraries travel INSIDE the project folder, and the
# staged tables point at them with ${KIPRJMOD}/libraries/... . Paths use forward
# slashes: backslashes are eaten as escapes by the table parser.
Copy-Item $sym (Join-Path $proj 'libraries')
Copy-Item $pretty (Join-Path $proj 'libraries') -Recurse
Set-Content (Join-Path $proj 'sym-lib-table') @'
(sym_lib_table
  (version 7)
  (lib (name "MoriShield_Carrier")(type "KiCad")(uri "${KIPRJMOD}/libraries/MoriShield_Carrier.kicad_sym")(options "")(descr "MoriShield Carrier symbols"))
)
'@ -Encoding UTF8
Set-Content (Join-Path $proj 'fp-lib-table') @'
(fp_lib_table
  (version 7)
  (lib (name "MoriShield_Carrier")(type "KiCad")(uri "${KIPRJMOD}/libraries/MoriShield_Carrier.pretty")(options "")(descr "MoriShield Carrier footprints"))
)
'@ -Encoding UTF8

Copy-Item $drc, $erc -Destination $stage
Copy-Item $gerb, $drill -Destination $stage -Recurse
Copy-Item (Join-Path $out 'MoriShield_Carrier_RevC_schematic.pdf') -Destination $stage -ErrorAction SilentlyContinue
Copy-Item $bom, $posf -Destination $stage -ErrorAction SilentlyContinue
if (Test-Path $posb) { Copy-Item $posb -Destination $stage }
Copy-Item $sheet -Destination (Join-Path $stage '00_ResponseSheet_RevC.csv')
Copy-Item (Join-Path $out 'EVIDENCE_RevC.md') -Destination $stage -ErrorAction SilentlyContinue
Copy-Item (Join-Path $out 'FAB_NOTES.md') -Destination $stage -ErrorAction SilentlyContinue
Copy-Item (Join-Path $out 'decoupling_map.csv') -Destination $stage -ErrorAction SilentlyContinue
Copy-Item (Join-Path $out 'vias_in_pads.txt') -Destination $stage -ErrorAction SilentlyContinue

$files = Get-ChildItem $stage -Recurse -File | Where-Object {
    $n = $_.Name
    -not ($exclude | Where-Object { $n -like $_ })
}
Compress-Archive -Path $files.FullName -DestinationPath $zip -Force

$files | Get-FileHash -Algorithm SHA256 |
    ForEach-Object { '{0}  {1}' -f $_.Hash, (Split-Path $_.Path -Leaf) } |
    Set-Content (Join-Path $root ("MoriShield_Carrier_RevC_{0}_SHA256.txt" -f $stamp))

Write-Host ("packed {0} files -> {1}" -f $files.Count, $zip)
Write-Host 'save, DRC and plot timestamps are recorded in the SHA256 file timestamp'
