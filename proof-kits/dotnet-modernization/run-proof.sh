#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
mkdir -p reports
rm -f reports/api.log

echo "[1/6] Build proof tests and modern API"
dotnet build tests/Modernization.ProofTests/Modernization.ProofTests.csproj --configuration Release
dotnet build src/Modernization.Api/Modernization.Api.csproj --configuration Release

echo "[2/6] Run characterization, parity, idempotency, validation, and outbox tests"
dotnet run --project tests/Modernization.ProofTests/Modernization.ProofTests.csproj --configuration Release --no-build

echo "[3/6] Reconcile synthetic legacy and modern order fixtures"
python3 tools/proof_harness.py reconcile

echo "[4/6] Start API for contract and reliability smoke checks"
ASPNETCORE_URLS=http://127.0.0.1:5078 dotnet run --project src/Modernization.Api/Modernization.Api.csproj --configuration Release --no-build > reports/api.log 2>&1 &
API_PID=$!
trap 'kill "$API_PID" 2>/dev/null || true' EXIT
python3 tools/proof_harness.py smoke --base-url http://127.0.0.1:5078
kill "$API_PID" 2>/dev/null || true
wait "$API_PID" 2>/dev/null || true
trap - EXIT

echo "[5/6] Generate engineer and executive evidence packet"
python3 tools/proof_harness.py evidence

echo "[6/6] Complete"
echo "Open reports/modernization-readiness.md and reports/executive-decision-brief.md"
