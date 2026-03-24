#!/usr/bin/env pwsh
# Portable question-gen wrapper for PowerShell hosts.

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$startupHelper = Join-Path $PSScriptRoot "pwsh_startup.ps1"
$questionGenPy = Join-Path $PSScriptRoot "question_gen.py"
. $startupHelper

Show-PwshGitRecoveryNotice -RepoRoot $repoRoot

if (Get-Command bash -ErrorAction SilentlyContinue) {
    exit (Invoke-BashPythonTool -RepoRoot $repoRoot -ToolPath "tools/question_gen.py" -Args $Args)
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
    & $pythonCmd @pythonArgs $questionGenPy @Args
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
