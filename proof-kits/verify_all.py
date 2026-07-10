#!/usr/bin/env python3
"""Verify the public TSmithCode proof-kit catalog without private source access."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "reports" / "quickstart-report.json"
KITS = {
    "dotnet-modernization": "dotnet-modernization/README.md",
    "data-integration": "data-integration/README.md",
    "api-contract": "api-contract/README.md",
    "release-readiness": "release-readiness/README.md",
    "reporting-quality": "reporting-quality/README.md",
    "ai-workflow-boundary": "ai-workflow-boundary/README.md",
    "typescript-ui": "typescript-ui/README.md",
    "autodesk-software-bridge": "autodesk-software-bridge/README.md",
}
REQUIRED_SECTIONS = (
    "## Buyer question",
    "## Review boundary",
    "## Expected decision output",
)


def verify(slug: str | None = None) -> dict[str, object]:
    selected = {slug: KITS[slug]} if slug else KITS
    failures: list[str] = []

    for kit_slug, relative_path in selected.items():
        path = ROOT / relative_path
        if not path.is_file():
            failures.append(f"{kit_slug}: missing README")
            continue

        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                failures.append(f"{kit_slug}: missing section {section}")

    result: dict[str, object] = {
        "brand": "TSmithCode.ai",
        "operator": "CAD Guardian LLC",
        "repository": "tsmithcode/tsmithcode",
        "kit_count": len(selected),
        "score": 100 if not failures else 0,
        "decision": "public-proof-ready" if not failures else "blocked",
        "failures": failures,
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify public TSmithCode proof kits.")
    parser.add_argument("--kit", choices=sorted(KITS), help="Verify one proof kit.")
    args = parser.parse_args()
    result = verify(args.kit)
    print(json.dumps(result, indent=2))
    return 0 if result["score"] == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
