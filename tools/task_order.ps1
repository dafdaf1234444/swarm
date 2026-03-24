#!/usr/bin/env pwsh
# Portable task-order wrapper for PowerShell hosts.

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$startupHelper = Join-Path $PSScriptRoot "pwsh_startup.ps1"
$taskOrderPy = Join-Path $PSScriptRoot "task_order.py"
. $startupHelper

Show-PwshGitRecoveryNotice -RepoRoot $repoRoot

if (Get-Command bash -ErrorAction SilentlyContinue) {
    exit (Invoke-BashPythonTool -RepoRoot $repoRoot -ToolPath "tools/task_order.py" -Args $Args)
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
    & $pythonCmd @pythonArgs $taskOrderPy @Args
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
