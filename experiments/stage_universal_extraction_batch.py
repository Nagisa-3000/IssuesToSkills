#!/usr/bin/env python3
"""Stage a small multi-repository extraction batch for local Windows Codex.

The source manifest keeps the canonical WSL checkouts.  This adapter rewrites
only the selected cases to their local Windows staging checkouts and records
the original path for auditability.  It deliberately refuses ambiguous case
selectors so a typo cannot silently select a different issue.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


def case_key(repository: str, issue: int) -> str:
    return f"{repository}#{issue}"


def parse_case_selector(value: str) -> tuple[str, int]:
    repository, separator, issue_text = value.rpartition("#")
    if not separator or not repository or not issue_text.isdigit():
        raise argparse.ArgumentTypeError(
            f"case must look like OWNER/REPO#ISSUE, got {value!r}"
        )
    return repository, int(issue_text)


def parse_checkout_mapping(value: str) -> tuple[str, Path]:
    repository, separator, checkout = value.partition("=")
    if not separator or not repository or not checkout:
        raise argparse.ArgumentTypeError(
            f"checkout must look like OWNER/REPO=/absolute/path, got {value!r}"
        )
    return repository, Path(checkout).expanduser().resolve()


def parse_ref_override(value: str) -> tuple[str, int, str]:
    selector, separator, ref = value.partition("=")
    if not separator or not ref:
        raise argparse.ArgumentTypeError(
            f"ref must look like OWNER/REPO#ISSUE=COMMIT, got {value!r}"
        )
    repository, issue = parse_case_selector(selector)
    return repository, issue, ref.strip()


def default_slug(repository: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", repository)


def read_cases(value: Any) -> list[dict[str, Any]]:
    cases = value.get("cases", []) if isinstance(value, dict) else value
    if not isinstance(cases, list):
        raise ValueError("manifest must contain a cases array")
    return [dict(item) for item in cases if isinstance(item, dict)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--case",
        dest="selectors",
        action="append",
        type=parse_case_selector,
        required=True,
        help="case selector OWNER/REPO#ISSUE; repeat for each selected case",
    )
    parser.add_argument(
        "--checkout-root",
        type=Path,
        help="default root; repositories use a sanitized OWNER__REPO child",
    )
    parser.add_argument(
        "--checkout",
        dest="checkout_mappings",
        action="append",
        type=parse_checkout_mapping,
        default=[],
        help="override checkout as OWNER/REPO=/absolute/path; repeat as needed",
    )
    parser.add_argument(
        "--ref",
        dest="ref_overrides",
        action="append",
        type=parse_ref_override,
        default=[],
        help="override implementation ref as OWNER/REPO#ISSUE=COMMIT; repeat as needed",
    )
    args = parser.parse_args()

    source = json.loads(args.manifest.read_text(encoding="utf-8"))
    cases = read_cases(source)
    requested = [case_key(repository, issue) for repository, issue in args.selectors]
    if len(set(requested)) != len(requested):
        raise ValueError("duplicate --case selector")

    by_key = {
        case_key(str(case.get("repository")), int(case.get("issue", 0))): case
        for case in cases
    }
    missing = [key for key in requested if key not in by_key]
    if missing:
        raise ValueError(f"case selector(s) not found: {', '.join(missing)}")

    checkout_map = dict(args.checkout_mappings)
    ref_map = {(repository, issue): ref for repository, issue, ref in args.ref_overrides}
    selected: list[dict[str, Any]] = []
    for key in requested:
        case = dict(by_key[key])
        repository = str(case["repository"])
        if repository in checkout_map:
            checkout = checkout_map[repository]
        elif args.checkout_root:
            checkout = args.checkout_root.expanduser().resolve() / default_slug(repository)
        else:
            raise ValueError(
                f"no staging checkout for {repository}; provide --checkout or --checkout-root"
            )
        case["original_checkout"] = case.get("checkout")
        case["checkout"] = str(checkout)
        ref_override = ref_map.get((repository, int(case["issue"])))
        if ref_override:
            case["original_extraction_ref"] = case.get("extraction_ref") or case.get("ref")
            case["ref"] = ref_override
            case["extraction_ref_override_reason"] = "selected merged implementation commit from linked-PR evidence"
        case["staged_for_windows_codex"] = True
        selected.append(case)

    output = {
        "schema_version": "universal-extraction-staged-batch-v1",
        "source_manifest": str(args.manifest),
        "cases": selected,
        "staging": {
            "purpose": "multi-repository Windows Codex extraction",
            "selected_case_keys": requested,
            "checkout_overrides": {key: str(path) for key, path in checkout_map.items()},
            "ref_overrides": {
                case_key(repository, issue): ref
                for (repository, issue), ref in ref_map.items()
            },
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "selected_rows": len(selected),
        "cases": [
            {
                "repository": case["repository"],
                "issue": case["issue"],
                "category": case.get("category"),
                "ref": case.get("ref") or case.get("extraction_ref"),
                "checkout": case["checkout"],
            }
            for case in selected
        ],
        "output": str(args.output),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
