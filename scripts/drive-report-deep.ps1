$ErrorActionPreference = 'SilentlyContinue'

function Show-DirSizes($path, $title) {
    Write-Output "=== $title ==="
    Get-ChildItem $path -Directory -Force | ForEach-Object {
        $size = (Get-ChildItem $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        if ($null -eq $size) { $size = 0 }
        Write-Output ("{0,-30} {1,10:N2} GB" -f $_.Name, ($size/1GB))
    }
    Write-Output ""
}

Show-DirSizes 'D:\AI\apps' 'AI\apps breakdown'
Show-DirSizes 'D:\AI' 'AI top-level'
Show-DirSizes 'D:\Docker' 'Docker top-level'
Show-DirSizes 'D:\Docker\volumes' 'Docker volumes (service data)'

Write-Output "=== TOP 25 LARGEST FILES ON D: ==="
Get-ChildItem 'D:\AI', 'D:\Docker' -Recurse -File -Force -ErrorAction SilentlyContinue |
    Sort-Object Length -Descending |
    Select-Object -First 25 |
    ForEach-Object {
        Write-Output ("{0,10:N2} GB  {1}" -f ($_.Length/1GB), $_.FullName)
    }
