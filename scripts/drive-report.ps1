$ErrorActionPreference = 'SilentlyContinue'

Write-Output "=== DRIVE D: CAPACITY ==="
$d = Get-PSDrive D
$total = [math]::Round(($d.Used + $d.Free)/1GB, 1)
$used  = [math]::Round($d.Used/1GB, 1)
$free  = [math]::Round($d.Free/1GB, 1)
Write-Output ("Total: {0} GB | Used: {1} GB | Free: {2} GB | Utilization: {3}%" -f $total, $used, $free, [math]::Round($used/($used+$free)*100,1))

Write-Output ""
Write-Output "=== TOP-LEVEL DIRECTORY SIZES (D:\) ==="
$results = @()
Get-ChildItem 'D:\' -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    if ($null -eq $size) { $size = 0 }
    $results += [PSCustomObject]@{
        Dir  = $_.Name
        GB   = [math]::Round($size/1GB, 2)
        MB   = [math]::Round($size/1MB, 0)
        Files = (Get-ChildItem $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object).Count
    }
}
$results | Sort-Object GB -Descending | Format-Table Dir, GB, MB, Files -AutoSize

Write-Output "=== ROOT-LEVEL LOOSE FILES ==="
Get-ChildItem 'D:\' -File -Force -ErrorAction SilentlyContinue | Select-Object Name, @{n='MB';e={[math]::Round($_.Length/1MB,1)}} | Format-Table -AutoSize
