#!/usr/bin/env pwsh
# Portable swarm check wrapper for PowerShell hosts.

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$checkSh = Join-Path $PSScriptRoot "check.sh"
$validatePy = Join-Path $PSScriptRoot "validate_beliefs.py"
$maintenancePy = Join-Path $PSScriptRoot "maintenance.py"
$missionConstraintsPy = Join-Path $PSScriptRoot "test_mission_constraints.py"

function Convert-ToBashPath {
    param([string]$PathText)
    $p = ($PathText -replace "\\", "/")
    if ($p -match "^[A-Za-z]:") {
        $drive = $p.Substring(0, 1).ToLower()
        $rest = $p.Substring(2)
        return "/mnt/$drive$rest"
    }
    return $p
}

function Invoke-NativeCapture {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [string[]]$CommandArgs = @()
    )
    $output = & $FilePath @CommandArgs 2>&1
    $exitCode = $LASTEXITCODE
    foreach ($line in $output) {
        Write-Output $line
    }
    return [pscustomobject]@{
        ExitCode = $exitCode
        Output = ($output | Out-String)
    }
}

function Test-GitIndexFailureText {
    param([string]$Text)
    if (-not $Text) {
        return $false
    }
    return $Text -match '(?im)(Tree-size guard triggered|corrupted the git index|unable to read index|could not read index|index file smaller than expected|fatal:\s+index file corrupt|index\.lock)'
}

function Write-GitIndexRecoveryHint {
    param([string]$Context)
    $repoBash = Convert-ToBashPath $repoRoot
    $recovery = "bash -lc 'cd $repoBash && rm -f .git/index.lock && git read-tree HEAD && git update-index --refresh'"
    Write-Warning "$Context Recover via WSL/bash: $recovery"
}

if (Get-Command bash -ErrorAction SilentlyContinue) {
    $bashScript = Convert-ToBashPath $checkSh
    $bashResult = Invoke-NativeCapture -FilePath "bash" -CommandArgs (@($bashScript) + $Args)
    if ($bashResult.ExitCode -ne 0 -and (Test-GitIndexFailureText $bashResult.Output)) {
        Write-GitIndexRecoveryHint "bash-backed check hit a git-index/tree corruption signature."
    }
    exit $bashResult.ExitCode
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

$quick = $Args -contains "--quick"
$pyArgs = @()
if ($quick) {
    $pyArgs += "--quick"
}

Push-Location $repoRoot
try {
    $validateResult = Invoke-NativeCapture -FilePath $pythonCmd -CommandArgs (@($pythonArgs) + @($validatePy) + $pyArgs)
    if ($validateResult.ExitCode -ne 0) {
        if (Test-GitIndexFailureText $validateResult.Output) {
            Write-GitIndexRecoveryHint "Belief validation failed with a git-index/tree corruption signature."
        }
        Write-Error "FAIL: Belief validation failed."
        exit $validateResult.ExitCode
    }

    $maintenanceResult = Invoke-NativeCapture -FilePath $pythonCmd -CommandArgs (@($pythonArgs) + @($maintenancePy) + $pyArgs)
    if ($maintenanceResult.ExitCode -ne 0) {
        if (Test-GitIndexFailureText $maintenanceResult.Output) {
            Write-GitIndexRecoveryHint "Maintenance failed with a git-index/tree corruption signature."
        }
        exit $maintenanceResult.ExitCode
    }

    if (Test-Path $missionConstraintsPy) {
        $missionResult = Invoke-NativeCapture -FilePath $pythonCmd -CommandArgs (@($pythonArgs) + @($missionConstraintsPy))
        if ($missionResult.ExitCode -ne 0) {
            Write-Error "FAIL: Mission constraints regression failed."
            exit $missionResult.ExitCode
        }
    }

    exit 0
} finally {
    Pop-Location
}
