#!/usr/bin/env pwsh
# Portable orient wrapper for PowerShell hosts.

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$startupHelper = Join-Path $PSScriptRoot "pwsh_startup.ps1"
$orientPy = Join-Path $PSScriptRoot "orient.py"
. $startupHelper

Show-PwshGitRecoveryNotice -RepoRoot $repoRoot

$effectiveArgs = @($Args)
$gitDir = Join-Path $repoRoot ".git"
$hasExplicitMode = $false
foreach ($arg in $effectiveArgs) {
    if ([string]::IsNullOrEmpty($arg)) {
        continue
    }
    if (
        $arg -eq "--coord" -or
        $arg -eq "--help" -or
        $arg -eq "-h" -or
        $arg -eq "--classify" -or
        $arg.StartsWith("--classify=")
    ) {
        $hasExplicitMode = $true
        break
    }
}

if ((-not $hasExplicitMode) -and (Test-PwshGitWriteLockActive -GitDir $gitDir)) {
    Write-Host "[NOTICE] orient.ps1 auto-selecting --coord while a live git writer is active."
    $effectiveArgs += "--coord"
}

if (Get-Command bash -ErrorAction SilentlyContinue) {
    exit (Invoke-BashPythonTool -RepoRoot $repoRoot -ToolPath "tools/orient.py" -ToolArgs $effectiveArgs)
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
    & $pythonCmd @pythonArgs $orientPy @effectiveArgs
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
