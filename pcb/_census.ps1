param(
    [Parameter(Mandatory=$true)][string]$Pcb,
    [string]$Out = ""
)
$lines = [System.IO.File]::ReadAllLines($Pcb)
$seg = 0; $via = 0; $zone = 0; $fp = 0; $arc = 0
foreach ($l in $lines) {
    $t = $l.TrimStart()
    if ($t -eq '(segment') { $seg++ }
    elseif ($t -eq '(via') { $via++ }
    elseif ($t -eq '(zone') { $zone++ }
    elseif ($t -eq '(footprint' -or $t.StartsWith('(footprint ')) { $fp++ }
    elseif ($t -eq '(arc' -or $t.StartsWith('(arc ')) { $arc++ }
}
$nets = New-Object System.Collections.Generic.HashSet[string]
$refs = New-Object System.Collections.Generic.HashSet[string]
$m = [regex]::Matches([System.IO.File]::ReadAllText($Pcb), '\(net (?:\d+ )?"([^"]*)"\)')
foreach ($x in $m) { [void]$nets.Add($x.Groups[1].Value) }
$m2 = [regex]::Matches([System.IO.File]::ReadAllText($Pcb), '\(property "Reference" "([^"]*)"')
foreach ($x in $m2) { [void]$refs.Add($x.Groups[1].Value) }
$result = [ordered]@{
    footprints = $fp
    segments   = $seg
    arcs       = $arc
    vias       = $via
    zones      = $zone
    net_names  = $nets.Count
    ref_count  = $refs.Count
    file       = $Pcb
    bytes      = (Get-Item $Pcb).Length
}
if ($Out) {
    $result | ConvertTo-Json -Depth 4 | Set-Content -Path $Out -Encoding UTF8
}
$result | ConvertTo-Json -Depth 4
