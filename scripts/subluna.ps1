# SUBLUNA-MANAGED: Windows installer and uninstaller launcher.
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('install', 'uninstall', 'doctor', 'verify')]
    [string]$Command
)

$sublunaScript = Join-Path $PSScriptRoot 'subluna.py'
$sublunaPython3 = Get-Command python3 -ErrorAction SilentlyContinue
$sublunaPython = Get-Command python -ErrorAction SilentlyContinue
$sublunaPy = Get-Command py -ErrorAction SilentlyContinue

if ($sublunaPython3) {
    & $sublunaPython3.Source $sublunaScript $Command
    exit $LASTEXITCODE
}
if ($sublunaPython) {
    & $sublunaPython.Source $sublunaScript $Command
    exit $LASTEXITCODE
}
if ($sublunaPy) {
    & $sublunaPy.Source -3 $sublunaScript $Command
    exit $LASTEXITCODE
}

Write-Error 'SubLuna requires Python 3.'
exit 1
