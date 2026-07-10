$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
New-Item -ItemType Directory -Force -Path reports | Out-Null
Remove-Item reports/api.stdout.log -ErrorAction SilentlyContinue
Remove-Item reports/api.stderr.log -ErrorAction SilentlyContinue

Write-Host "[1/6] Build proof tests and modern API"
dotnet build tests/Modernization.ProofTests/Modernization.ProofTests.csproj --configuration Release
dotnet build src/Modernization.Api/Modernization.Api.csproj --configuration Release

Write-Host "[2/6] Run characterization, parity, idempotency, validation, and outbox tests"
dotnet run --project tests/Modernization.ProofTests/Modernization.ProofTests.csproj --configuration Release --no-build

Write-Host "[3/6] Reconcile synthetic legacy and modern order fixtures"
py -3 tools/proof_harness.py reconcile

Write-Host "[4/6] Start API for contract and reliability smoke checks"
$env:ASPNETCORE_URLS = "http://127.0.0.1:5078"
$Api = Start-Process dotnet -ArgumentList @(
  "run",
  "--project", "src/Modernization.Api/Modernization.Api.csproj",
  "--configuration", "Release",
  "--no-build"
) -RedirectStandardOutput reports/api.stdout.log -RedirectStandardError reports/api.stderr.log -PassThru
try {
  py -3 tools/proof_harness.py smoke --base-url http://127.0.0.1:5078
}
finally {
  Stop-Process -Id $Api.Id -Force -ErrorAction SilentlyContinue
  Wait-Process -Id $Api.Id -ErrorAction SilentlyContinue
}

Write-Host "[5/6] Generate engineer and executive evidence packet"
py -3 tools/proof_harness.py evidence

Write-Host "[6/6] Complete"
Write-Host "Open reports/modernization-readiness.md and reports/executive-decision-brief.md"
