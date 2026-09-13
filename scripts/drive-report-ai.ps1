$ErrorActionPreference = 'SilentlyContinue'

Write-Output "=== AI\data breakdown ==="
Get-ChildItem 'D:\AI\data' -Directory -Force | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    if ($null -eq $size) { $size = 0 }
    if ($size -gt 100MB) {
        Write-Output ("{0,-30} {1,10:N2} GB" -f $_.Name, ($size/1GB))
    }
}

Write-Output ""
Write-Output "=== AI\rollback contents ==="
Get-ChildItem 'D:\AI\rollback' -Directory -Force | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    if ($null -eq $size) { $size = 0 }
    Write-Output ("{0,-50} {1,10:N2} GB" -f $_.Name, ($size/1GB))
}

Write-Output ""
Write-Output "=== AI\cache breakdown ==="
Get-ChildItem 'D:\AI\cache' -Directory -Force | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    if ($null -eq $size) { $size = 0 }
    if ($size -gt 50MB) {
        Write-Output ("{0,-30} {1,10:N2} GB" -f $_.Name, ($size/1GB))
    }
}
