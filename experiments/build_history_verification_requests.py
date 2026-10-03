#!/usr/bin/env python3
"""Schedule every repair candidate in a completed census review, without family sampling."""

import argparse
import json
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import utc
from arex_skill_graph.history_census import GitHubCLI, fingerprint, now, redact_history, write_json
from arex_skill_graph.history_learning import load_population_reviews, observable_evidence


def repair_metadata(api, locator):
    owner, name = locator["repository"].split("/")
    if locator.get("kind") == "commit":
        data = api.graphql(
            "query($owner:String!,$name:String!,$oid:String!){repository(owner:$owner,name:$name){"
            "object(expression:$oid){... on Commit {oid parents(first:1){nodes{oid}}}}}"
            "rateLimit{cost remaining resetAt}}",
            {"owner": owner, "name": name, "oid": locator["commit"]},
        )["repository"]["object"]
        if not data or data["oid"] != locator["commit"]:
            raise ValueError("historical commit identity unavailable")
        return {
            "number": None,
            "mergedAt": locator["available_at"],
            "mergeCommit": data,
            "repair_availability_basis": "pre-cutoff-public-timeline-commit-reference",
            "fix_id": locator["repository"] + ":commit:" + data["oid"],
        }
    data = api.graphql(
        "query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){"
        "pullRequest(number:$number){number createdAt mergedAt commits(first:1){nodes{commit{authoredDate committedDate}}} "
        "mergeCommit{oid parents(first:1){nodes{oid}}}}}"
        "rateLimit{cost remaining resetAt}}",
        {"owner": owner, "name": name, "number": locator["pull_number"]},
    )["repository"]["pullRequest"]
    if (
        not data
        or not data["mergedAt"]
        or not data["mergeCommit"]
        or (locator.get("commit") and data["mergeCommit"]["oid"] != locator["commit"])
    ):
        raise ValueError("historical PR identity unavailable or changed")
    possible_public_times = [
        data["createdAt"],
        *(
            time
            for row in data["commits"]["nodes"]
            for time in (row["commit"]["authoredDate"], row["commit"]["committedDate"])
        ),
    ]
    return {
        **data,
        "repair_availability_basis": "github-merged-at",
        "first_possible_public_repair_at": min(possible_public_times, key=utc),
        "first_possible_public_repair_time_basis": "earliest PR creation/first surviving commit authored or committed timestamp; conservative chronology, not an exact publication observation",
        "fix_id": locator["repository"] + ":pr:" + str(data["number"]),
    }


def cached_repair_metadata(api, locator, directory):
    key = (
        locator["repository"],
        "pr" if locator.get("pull_number") is not None else "commit",
        locator.get("pull_number")
        if locator.get("pull_number") is not None
        else locator.get("commit"),
    )
    path = Path(directory) / (fingerprint(key) + ".json")
    if path.exists():
        saved = json.loads(path.read_text())
        if saved["locator_key"] != list(key) or saved["metadata_sha256"] != fingerprint(
            saved["metadata"]
        ):
            raise ValueError("historical repair metadata cache identity/integrity mismatch")
        return saved["metadata"]
    metadata = repair_metadata(api, locator)
    write_json(
        path,
        {
            "locator_key": key,
            "metadata": metadata,
            "metadata_sha256": fingerprint(metadata),
            "observed_at": now(),
        },
    )
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--review-dir", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--dependency-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--metadata-cache-dir", type=Path)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--gh-executable", default="gh")
    parser.add_argument("--text-recovery", type=Path)
    parser.add_argument("--strict-metadata", action="store_true")
    parser.add_argument(
        "--repair-locator-mode",
        choices=["closing_only", "all_pre_cutoff_mentions"],
        default="closing_only",
    )
    args = parser.parse_args(argv)
    if not (Path(args.gh_executable).is_file() or shutil.which(args.gh_executable)):
        raise ValueError("configured GitHub CLI executable is unavailable")
    if not args.repository_root.is_dir() or not (args.dependency_root / "pyvenv.cfg").is_file():
        raise ValueError(
            "prepared historical source repositories and isolated runtime are required"
        )
    records = observable_evidence(
        args.census,
        args.repository,
        args.cutoff,
        text_recovery=args.text_recovery,
        strict_metadata=args.strict_metadata,
        repair_locator_mode=args.repair_locator_mode,
    )
    review_manifest = json.loads((args.review_dir / "review-manifest.json").read_text())
    config = SimpleNamespace(model=review_manifest["model"], base_url=review_manifest["endpoint"])
    reviews = load_population_reviews(records, args.review_dir, config)
    api = GitHubCLI(args.gh_executable)
    requests, deferred, locators = [], [], {}
    metadata_cache = args.metadata_cache_dir or args.output_dir / "metadata-cache"
    for record in records:
        review = reviews[record["issue_id"]]
        if review["disposition"] != "repair_verification_pending":
            continue
        seen = set()
        # A PR is commonly mentioned before it closes the issue. Prefer the
        # strongest observed relationship before deduplication; first-seen
        # mention order must not discard a later explicit closure.
        priorities = {
            "direct_closure": 0,
            "closing_reference": 1,
            "mention_only_not_verified_resolution": 2,
        }
        candidates = sorted(
            record["resolution_candidates"], key=lambda x: priorities.get(x.get("relationship"), 1)
        )
        for locator in candidates:
            key = (
                locator["repository"],
                "pr" if locator.get("pull_number") is not None else "commit",
                locator.get("pull_number")
                if locator.get("pull_number") is not None
                else locator.get("commit"),
            )
            if key in seen:
                continue
            seen.add(key)
            try:
                if key not in locators:
                    locators[key] = cached_repair_metadata(api, locator, metadata_cache)
                metadata = {
                    **locators[key],
                    "resolution_relationship": locator.get("relationship")
                    or (
                        "closing_reference"
                        if args.repair_locator_mode == "closing_only"
                        else "unverified_reference"
                    ),
                    "resolution_relationship_evidence_refs": [locator["source_event_id"]]
                    if locator.get("source_event_id")
                    else review["evidence_refs"],
                }
                if utc(metadata["mergedAt"]) >= utc(args.cutoff):
                    raise ValueError("historical repair is not available before cutoff")
                if not metadata["mergeCommit"]["parents"]["nodes"]:
                    raise ValueError("historical repair lacks a parent control")
                path = args.repository_root / (locator["repository"].replace("/", "__") + ".git")
                if not path.is_dir():
                    raise ValueError("historical source repository checkout is unavailable")
                requests.append(
                    {
                        "issue_id": record["issue_id"],
                        "repository_path": str(path.resolve()),
                        "metadata": metadata,
                        "dependency_root": str(args.dependency_root.resolve()),
                        "locator": locator,
                        "review_evidence_refs": review["evidence_refs"],
                        "review_is_not_verified_resolution": True,
                    }
                )
            except (ValueError, RuntimeError, OSError, KeyError) as error:
                deferred.append(
                    {
                        "issue_id": record["issue_id"],
                        "locator": locator,
                        "reason": redact_history(str(error)),
                    }
                )
    audit = {
        "schema": "full-population-repair-verification-request-register-v1",
        "checked_at": now(),
        "repository": args.repository,
        "cutoff_exclusive": args.cutoff,
        "population_count": len(records),
        "population_sha256": fingerprint(records),
        "review_manifest_sha256": fingerprint(review_manifest),
        "repair_pending_issue_count": sum(
            r["disposition"] == "repair_verification_pending" for r in reviews.values()
        ),
        "scheduled_issue_count": len({r["issue_id"] for r in requests}),
        "request_count": len(requests),
        "requests_sha256": fingerprint(requests),
        "deferred": deferred,
        "api_calls": api.calls,
        "issue_family_sampling": False,
        "requests_are_verified_repairs": False,
        "full_history_qualified": False,
        "formal_SWE_runs": 0,
    }
    checkpoint = args.output_dir / "request-register.json"
    if checkpoint.exists():
        saved = json.loads(checkpoint.read_text())
        if (
            saved["requests_sha256"] != audit["requests_sha256"]
            or saved["population_sha256"] != audit["population_sha256"]
        ):
            raise ValueError(
                "historical verification request population changed; use a new version"
            )
        return 0
    write_json(args.output_dir / "verification-requests.json", requests)
    write_json(checkpoint, audit)
    print(
        json.dumps({key: value for key, value in audit.items() if key not in {"deferred"}}),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
