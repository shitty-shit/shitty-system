$ErrorActionPreference = 'Stop'

$memoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$server = Join-Path $env:USERPROFILE '.ijfw\mcp-server\src\server.js'

if (-not (Test-Path -LiteralPath $server -PathType Leaf)) {
    throw "IJFW MCP server not found: $server"
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw 'Node.js is not available on PATH.'
}

$env:IJFW_PROJECT_DIR = $memoryRoot

$initialize = @{
    jsonrpc = '2.0'
    id = 1
    method = 'initialize'
    params = @{
        protocolVersion = '2024-11-05'
        capabilities = @{}
        clientInfo = @{ name = 'freebuff-memory-verify'; version = '1' }
    }
} | ConvertTo-Json -Compress -Depth 8

$prelude = @{
    jsonrpc = '2.0'
    id = 2
    method = 'tools/call'
    params = @{
        name = 'ijfw_memory_prelude'
        arguments = @{ detail_level = 'summary' }
    }
} | ConvertTo-Json -Compress -Depth 8

$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = 'node'
$startInfo.Arguments = '"' + $server + '"'
$startInfo.UseShellExecute = $false
$startInfo.RedirectStandardInput = $true
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$startInfo.CreateNoWindow = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $startInfo
[void]$process.Start()
# Windows PowerShell's redirected StreamWriter may emit a UTF-8 BOM on its
# first write. Flush it on an empty line so the first JSON-RPC object remains
# valid JSON for Node's line parser.
$process.StandardInput.WriteLine('')
$process.StandardInput.WriteLine($initialize)
$process.StandardInput.WriteLine($prelude)
$process.StandardInput.Close()

$joined = $process.StandardOutput.ReadToEnd()
$stderr = $process.StandardError.ReadToEnd()
$process.WaitForExit()

if ($process.ExitCode -ne 0) {
    throw "IJFW MCP server exited with code $($process.ExitCode): $stderr"
}

if ($joined -notmatch '"name":"ijfw-memory"') {
    throw 'IJFW initialize response was missing.'
}

if ($joined -notmatch '<ijfw-memory>') {
    throw 'IJFW prelude response was missing.'
}

if ($joined -notmatch 'FREEBUFF-CROSSCHAT-CANARY-20260816') {
    throw 'The setup-time cross-chat canary was not recalled.'
}

if ($joined -match '"isError":true') {
    throw 'IJFW returned a tool error.'
}

Write-Host "PASS: IJFW transport, prelude, and cross-chat canary use $memoryRoot"
