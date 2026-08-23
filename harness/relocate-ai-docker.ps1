param(
    [switch]$Execute
)

$ErrorActionPreference = 'Stop'

$moves = @(
    @{ Source = 'C:\Users\idfk\.docker'; Destination = 'D:\Docker\user\.docker'; Label = 'Docker user data and model store' },
    @{ Source = 'C:\Users\idfk\AppData\Local\Programs\Ollama'; Destination = 'D:\AI\apps\Ollama'; Label = 'Ollama application' },
    @{ Source = 'C:\Users\idfk\.ollama'; Destination = 'D:\AI\data\Ollama'; Label = 'Ollama models and manifests' },
    @{ Source = 'C:\Users\idfk\AppData\Local\Ollama'; Destination = 'D:\AI\data\Ollama-local'; Label = 'Ollama local support data' },
    @{ Source = 'C:\Users\idfk\AppData\Local\Programs\AnythingLLM'; Destination = 'D:\AI\apps\AnythingLLM'; Label = 'AnythingLLM application' },
    @{ Source = 'C:\Users\idfk\AppData\Roaming\anythingllm-desktop'; Destination = 'D:\AI\data\AnythingLLM'; Label = 'AnythingLLM models and workspace data' },
    @{ Source = 'C:\Users\idfk\AppData\Local\Programs\LM Studio'; Destination = 'D:\AI\apps\LM Studio'; Label = 'LM Studio application' },
    @{ Source = 'C:\Users\idfk\.lmstudio'; Destination = 'D:\AI\data\LM Studio'; Label = 'LM Studio models and data' },
    @{ Source = 'C:\Users\idfk\AppData\Roaming\LM Studio'; Destination = 'D:\AI\config\LM Studio'; Label = 'LM Studio configuration' },
    @{ Source = 'C:\Users\idfk\AppData\Local\Programs\ComfyUI'; Destination = 'D:\AI\apps\ComfyUI'; Label = 'ComfyUI application' },
    @{ Source = 'C:\Users\idfk\ComfyUI'; Destination = 'D:\AI\data\ComfyUI'; Label = 'ComfyUI project and models' },
    @{ Source = 'C:\Users\idfk\AppData\Roaming\ComfyUI'; Destination = 'D:\AI\config\ComfyUI'; Label = 'ComfyUI configuration' },
    @{ Source = 'C:\Users\idfk\.unsloth'; Destination = 'D:\AI\data\Unsloth'; Label = 'Unsloth runtime and caches' },
    @{ Source = 'C:\Users\idfk\anaconda3'; Destination = 'D:\AI\apps\Anaconda3'; Label = 'Anaconda runtime and packages' },
    @{ Source = 'C:\Users\idfk\.cache\huggingface'; Destination = 'D:\AI\cache\huggingface'; Label = 'Hugging Face model cache' }
)

function Get-Inventory([string]$Path) {
    $files = @(Get-ChildItem -LiteralPath $Path -File -Force -Recurse -ErrorAction Stop)
    $sum = ($files | Measure-Object -Property Length -Sum).Sum
    [pscustomobject]@{ Files = $files.Count; Bytes = [int64]$sum }
}

if (-not $Execute) {
    $moves | ForEach-Object { [pscustomobject]@{Label=$_.Label;Source=$_.Source;Destination=$_.Destination} } | Format-Table -AutoSize
    Write-Output 'DRY RUN ONLY. Re-run with -Execute to copy, verify, and junction the paths.'
    exit 0
}

if (Get-Process -Name ollama -ErrorAction SilentlyContinue) {
    throw 'Ollama is running. Stop Ollama, then rerun this migration.'
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$results = @()

foreach ($move in $moves) {
    $source = $move.Source
    $destination = $move.Destination
    $backup = "$source.c-backup-$stamp"

    if (-not (Test-Path -LiteralPath $source)) {
        $results += [pscustomobject]@{Label=$move.Label;Status='SKIPPED_SOURCE_MISSING';Source=$source;Destination=$destination}
        continue
    }
    if (Test-Path -LiteralPath $destination) {
        throw "Destination already exists: $destination"
    }
    if (Test-Path -LiteralPath $backup) {
        throw "Rollback path already exists: $backup"
    }

    $parent = Split-Path -Parent $destination
    New-Item -ItemType Directory -Path $parent -Force | Out-Null

    Write-Output "COPY $($move.Label): $source -> $destination"
    & robocopy.exe $source $destination /E /COPY:DAT /DCOPY:DAT /XJ /R:2 /W:2 /NP /NFL /NDL | Out-Host
    $robocopyCode = $LASTEXITCODE
    if ($robocopyCode -gt 7) {
        throw "Robocopy failed for $source with exit code $robocopyCode"
    }

    $sourceInventory = Get-Inventory $source
    $destinationInventory = Get-Inventory $destination
    if (($sourceInventory.Files -ne $destinationInventory.Files) -or ($sourceInventory.Bytes -ne $destinationInventory.Bytes)) {
        throw "Verification mismatch for ${source}: source $($sourceInventory.Files) files/$($sourceInventory.Bytes) bytes; destination $($destinationInventory.Files) files/$($destinationInventory.Bytes) bytes"
    }

    Move-Item -LiteralPath $source -Destination $backup
    New-Item -ItemType Junction -Path $source -Target $destination | Out-Null
    $results += [pscustomobject]@{Label=$move.Label;Status='MOVED_WITH_ROLLBACK';Source=$source;Destination=$destination;Backup=$backup;Files=$destinationInventory.Files;Bytes=$destinationInventory.Bytes}
}

[Environment]::SetEnvironmentVariable('OLLAMA_MODELS', 'D:\AI\data\Ollama\models', 'User')
$results | Format-Table -AutoSize
Write-Output 'OLLAMA_MODELS user environment variable now points to D:\AI\data\Ollama\models.'
Write-Output 'Rollback backups remain on C: until application validation passes.'
