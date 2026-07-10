$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
New-Item -ItemType Directory -Force -Path reports | Out-Null
Remove-Item reports/api.stdout.log -ErrorAction SilentlyContinue
Remove-Item reports/api.stderr.log -ErrorAction SilentlyContinue

if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
  throw ".NET 8 SDK is required. Install it from https://dotnet.microsoft.com/download/dotnet/8.0"
}

$PythonExe = $null
$PythonPrefix = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
  $PythonExe = "py"
  $PythonPrefix = @("-3")
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
  $PythonExe = "python"
}
elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
  $PythonExe = "python3"
}
else {
  throw "Python 3 is required. Install it from https://www.python.org/downloads/"
}

function Invoke-Python {
  param([string[]]$PythonArgs)
  & $PythonExe @PythonPrefix @PythonArgs
  if ($LASTEXITCODE -ne 0) {
    throw "Python command failed with exit code $LASTEXITCODE: $($PythonArgs -join ' ')"
  }
}

Write-Host "[1/7] Validate public artifact completeness and safety"
Invoke-Python @("tools/preflight.py")

Write-Host "[2/7] Build proof tests and modern API"
dotnet build tests/Modernization.ProofTests/Modernization.ProofTests.csproj --configuration Release
dotnet build src/Modernization.Api/Modernization.Api.csproj --configuration Release

Write-Host "[3/7] Run characterization, parity, idempotency, validation, and outbox tests"
dotnet run --project tests/Modernization.ProofTests/Modernization.ProofTests.csproj --configuration Release --no-build

Write-Host "[4/7] Reconcile synthetic legacy and modern order fixtures"
Invoke-Python @("tools/proof_harness.py", "reconcile")

Write-Host "[5/7] Start API for contract and reliability smoke checks"
$env:ASPNETCORE_URLS = "http://127.0.0.1:5078"
$Api = Start-Process dotnet -ArgumentList @(
  "run",
  "--project", "src/Modernization.Api/Modernization.Api.csproj",
  "--configuration", "Release",
  "--no-build"
) -RedirectStandardOutput reports/api.stdout.log -RedirectStandardError reports/api.stderr.log -PassThru
try {
  Invoke-Python @("tools/proof_harness.py", "smoke", "--base-url", "http://127.0.0.1:5078")
}
finally {
  Stop-Process -Id $Api.Id -Force -ErrorAction SilentlyContinue
  Wait-Process -Id $Api.Id -ErrorAction SilentlyContinue
}

Write-Host "[6/7] Generate engineer and executive evidence packet"
Invoke-Python @("tools/proof_harness.py", "evidence")

Write-Host "[7/7] Complete"
Write-Host "Open reports/modernization-readiness.md and reports/executive-decision-brief.md"
