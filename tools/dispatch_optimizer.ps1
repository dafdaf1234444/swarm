#!/usr/bin/env pwsh
# Portable dispatch-optimizer wrapper for PowerShell hosts.

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$startupHelper = Join-Path $PSScriptRoot "pwsh_startup.ps1"
$dispatchOptimizerPy = Join-Path $PSScriptRoot "dispatch_optimizer.py"
. $startupHelper

Show-PwshGitRecoveryNotice -RepoRoot $repoRoot

if (Get-Command bash -ErrorAction SilentlyContinue) {
    exit (Invoke-BashPythonTool -RepoRoot $repoRoot -ToolPath "tools/dispatch_optimizer.py" -ToolArgs $Args)
}

$pythonCmd = $null
$pythonArgs = @()

if (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
    $pythonArgs = @("-3")
}

if (-not $pythonCmd) {
    Write-Error "FAIL: No runnable runtime found (bash/python3/python/py -3)."
    exit 1
}

Push-Location $repoRoot
try {
    & $pythonCmd @pythonArgs $dispatchOptimizerPy @Args
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
