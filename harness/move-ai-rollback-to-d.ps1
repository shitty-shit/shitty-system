$ErrorActionPreference = 'Stop'
$stamp = '20260818-193645'
$rollbackRoot = "D:\AI\rollback\$stamp"
$backupPaths = @(
    "C:\Users\idfk\.docker.c-backup-$stamp",
    "C:\Users\idfk\.lmstudio.c-backup-$stamp",
    "C:\Users\idfk\.ollama.c-backup-$stamp",
    "C:\Users\idfk\.unsloth.c-backup-$stamp",
    "C:\Users\idfk\anaconda3.c-backup-$stamp",
    "C:\Users\idfk\.cache\huggingface.c-backup-$stamp",
    "C:\Users\idfk\AppData\Local\Ollama.c-backup-$stamp",
    "C:\Users\idfk\AppData\Local\Programs\AnythingLLM.c-backup-$stamp",
    "C:\Users\idfk\AppData\Local\Programs\ComfyUI.c-backup-$stamp",
    "C:\Users\idfk\AppData\Local\Programs\LM Studio.c-backup-$stamp",
    "C:\Users\idfk\AppData\Local\Programs\Ollama.c-backup-$stamp",
    "C:\Users\idfk\AppData\Roaming\anythingllm-desktop.c-backup-$stamp",
    "C:\Users\idfk\AppData\Roaming\ComfyUI.c-backup-$stamp",
    "C:\Users\idfk\AppData\Roaming\LM Studio.c-backup-$stamp",
    "C:\Users\idfk\ComfyUI.c-backup-$stamp"
)

New-Item -ItemType Directory -Path $rollbackRoot -Force | Out-Null

foreach ($source in $backupPaths) {
    if (-not (Test-Path -LiteralPath $source)) {
        Write-Output "ALREADY ABSENT $source"
        continue
    }

    $resolved = (Resolve-Path -LiteralPath $source).Path
    if (-not $resolved.StartsWith('C:\Users\idfk\', [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Unsafe rollback source: $resolved"
    }
    $destination = Join-Path $rollbackRoot (Split-Path -Leaf $resolved)
    if (Test-Path -LiteralPath $destination) {
        throw "Rollback destination already exists: $destination"
    }

    Move-Item -LiteralPath $resolved -Destination $destination
    Write-Output "MOVED $resolved -> $destination"
}
