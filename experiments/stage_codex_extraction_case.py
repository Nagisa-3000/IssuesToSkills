#!/usr/bin/env python3
"""Stage one verified extraction case for a local Windows Codex checkout."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--issue", type=int, required=True)
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    document = json.loads(args.manifest.read_text(encoding="utf-8"))
    cases = document.get("cases", []) if isinstance(document, dict) else document
    if not isinstance(cases, list):
        raise ValueError("manifest must contain a cases array")
    matches = [
        dict(case) for case in cases
        if str(case.get("repository")) == args.repository and int(case.get("issue", 0)) == args.issue
    ]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one case, found {len(matches)}")
    case: dict[str, Any] = matches[0]
    case["checkout"] = str(args.checkout.expanduser().resolve())
    case["staged_for_windows_codex"] = True
    output = {
        "schema_version": "universal-extraction-staged-case-v1",
        "source_manifest": str(args.manifest),
        "cases": [case],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "repository": case["repository"],
        "issue": case["issue"],
        "checkout": case["checkout"],
        "ref": case.get("ref") or case.get("extraction_ref"),
        "output": str(args.output),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
