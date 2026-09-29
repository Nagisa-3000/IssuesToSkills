#!/usr/bin/env python3
"""Create a leakage-safe cross-project train/held-out split for issue episodes.

The input manifest is expected to contain one implementation-bearing issue/PR
case per project for each shared category. A whole project/repository is held
out: its issue in every category is excluded from Atomic/Workflow/Pattern
extraction and is reserved for downstream retrieval + guided-agent evaluation.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any, Iterable


def _case_key(case: dict[str, Any]) -> tuple[str, int]:
    return str(case["repository"]), int(case["issue"])


def _category(case: dict[str, Any]) -> str:
    value = case.get("category") or case.get("theme")
    if not value:
        raise ValueError(f"case {_case_key(case)!r} has no category/theme")
    return str(value)


def build_split(
    cases: Iterable[dict[str, Any]],
    *,
    holdout_repository: str,
    require_four_or_five: bool = True,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    values = [dict(case) for case in cases]
    if not values:
        raise ValueError("manifest is empty")
    keys = [_case_key(case) for case in values]
    duplicates = [key for key, count in Counter(keys).items() if count > 1]
    if duplicates:
        raise ValueError(f"duplicate repository/issue cases: {duplicates[:5]}")

    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in values:
        by_category[_category(case)].append(case)
    missing_holdout: list[str] = []
    invalid_sizes: dict[str, int] = {}
    train: list[dict[str, Any]] = []
    test: list[dict[str, Any]] = []
    category_rows: list[dict[str, Any]] = []
    for category in sorted(by_category):
        group = sorted(by_category[category], key=lambda item: _case_key(item))
        # A shared class may contain more than one episode per repository.  The
        # old pilot used exactly four or five cases, but the universal study
        # deliberately keeps train candidates and per-episode holdouts.  A
        # lower bound is the meaningful invariant; there is no semantic reason
        # to reject six or sixteen independently keyed cases.
        if require_four_or_five and len(group) < 4:
            invalid_sizes[category] = len(group)
        held = [case for case in group if str(case["repository"]) == holdout_repository]
        if not held:
            missing_holdout.append(f"{category}: expected at least one {holdout_repository!r}, got {len(held)}")
            continue
        held_keys = {_case_key(case) for case in held}
        train_cases = [case for case in group if _case_key(case) not in held_keys]
        for case in train_cases:
            item = dict(case)
            item["split"] = "train"
            item["split_group"] = category
            item["held_out_repository"] = holdout_repository
            train.append(item)
        for held_case in held:
            item = dict(held_case)
            item["split"] = "held_out_test"
            item["split_group"] = category
            item["held_out_repository"] = holdout_repository
            test.append(item)
        category_rows.append(
            {
                "category": category,
                "total_cases": len(group),
                "train_cases": len(train_cases),
                "held_out_cases": len(held),
                "repositories": sorted({str(case["repository"]) for case in group}),
                "train_case_keys": [f"{case['repository']}#{case['issue']}" for case in train_cases],
                "held_out_case_keys": [f"{case['repository']}#{case['issue']}" for case in held],
            }
        )
    if invalid_sizes:
        raise ValueError(f"categories must contain at least 4 cases: {invalid_sizes}")
    if missing_holdout:
        raise ValueError("; ".join(missing_holdout))
    if not category_rows:
        raise ValueError("no categories were split")
    train.sort(key=lambda item: (_category(item), _case_key(item)))
    test.sort(key=lambda item: (_category(item), _case_key(item)))
    train_keys = {_case_key(case) for case in train}
    test_keys = {_case_key(case) for case in test}
    if train_keys & test_keys:
        raise AssertionError("train/test leakage")
    train_repositories = {str(case["repository"]) for case in train}
    if holdout_repository in train_repositories:
        raise AssertionError("held-out repository leaked into train")
    summary = {
        "schema_version": "cross-project-holdout-split-v1",
        "holdout_repository": holdout_repository,
        "input_cases": len(values),
        "train_cases": len(train),
        "held_out_cases": len(test),
        "category_count": len(category_rows),
        "categories": category_rows,
        "train_repositories": sorted(train_repositories),
        "held_out_repositories": sorted({str(case["repository"]) for case in test}),
        "leakage_check": {
            "train_test_key_intersection": [],
            "held_out_repository_in_train": False,
        },
    }
    return train, test, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--holdout-repository", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--allow-other-cardinality", action="store_true")
    args = parser.parse_args()
    raw = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("manifest must contain a JSON array")
    train, test, summary = build_split(
        raw,
        holdout_repository=args.holdout_repository,
        require_four_or_five=not args.allow_other_cardinality,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "train.json").write_text(json.dumps(train, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "held-out-test.json").write_text(json.dumps(test, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "split-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(args.output_dir), **{key: summary[key] for key in ("train_cases", "held_out_cases", "category_count")}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
