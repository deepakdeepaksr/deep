param([string]$Pcb)
$lines = [System.IO.File]::ReadAllLines($Pcb)
$segs = New-Object System.Collections.Generic.List[string]
$vias = New-Object System.Collections.Generic.List[string]
$i = 0
while ($i -lt $lines.Count) {
    $t = $lines[$i].Trim()
    if ($t -eq '(segment' -or $t -eq '(via') {
        $kind = $t.Substring(1)
        $uuid = $null
        $j = $i
        while ($j -lt $lines.Count -and $lines[$j].Trim() -ne ')') {
            if ($lines[$j].Trim().StartsWith('(uuid ')) { $uuid = $lines[$j].Trim(); break }
            $j++
        }
        if ($kind -eq 'segment') { $segs.Add($uuid) } else { $vias.Add($uuid) }
    }
    $i++
}
[ordered]@{ segments = $segs; vias = $vias } | ConvertTo-Json -Depth 3
