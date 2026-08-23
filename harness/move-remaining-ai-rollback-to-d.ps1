$ErrorActionPreference = 'Stop'
$rollbackRoot = 'D:\AI\rollback\20260818-193645'
$moves = @(
    @{ Source = 'C:\Users\idfk\AppData\Local\Programs\Ollama.c-backup-20260818-193645'; Destination = 'D:\AI\rollback\20260818-193645\AppData-Local-Programs-Ollama.c-backup-20260818-193645' },
    @{ Source = 'C:\Users\idfk\AppData\Roaming\anythingllm-desktop.c-backup-20260818-193645'; Destination = 'D:\AI\rollback\20260818-193645\AppData-Roaming-anythingllm-desktop.c-backup-20260818-193645' },
    @{ Source = 'C:\Users\idfk\AppData\Roaming\ComfyUI.c-backup-20260818-193645'; Destination = 'D:\AI\rollback\20260818-193645\AppData-Roaming-ComfyUI.c-backup-20260818-193645' },
    @{ Source = 'C:\Users\idfk\AppData\Roaming\LM Studio.c-backup-20260818-193645'; Destination = 'D:\AI\rollback\20260818-193645\AppData-Roaming-LM-Studio.c-backup-20260818-193645' },
    @{ Source = 'C:\Users\idfk\ComfyUI.c-backup-20260818-193645'; Destination = 'D:\AI\rollback\20260818-193645\User-ComfyUI.c-backup-20260818-193645' }
)

New-Item -ItemType Directory -Path $rollbackRoot -Force | Out-Null
foreach ($move in $moves) {
    if (-not (Test-Path -LiteralPath $move.Source)) {
        Write-Output "ALREADY ABSENT $($move.Source)"
        continue
    }
    if (Test-Path -LiteralPath $move.Destination) {
        throw "Destination already exists: $($move.Destination)"
    }
    $resolved = (Resolve-Path -LiteralPath $move.Source).Path
    if (-not $resolved.StartsWith('C:\Users\idfk\', [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Unsafe source: $resolved"
    }
    Move-Item -LiteralPath $resolved -Destination $move.Destination
    Write-Output "MOVED $resolved -> $($move.Destination)"
}
