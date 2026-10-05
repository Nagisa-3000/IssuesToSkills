"""Recover known timeline omissions into a separate, checkpointed census version.

Fresh API observations supplement archived event identities. Historical text is
projected before storage; contemporary metadata is not backdated as knowledge.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from copy import deepcopy
from pathlib import Path

from .action_contracts import utc
from .direct_skill_extraction import safe_text
from .history_census import fingerprint, now, write_json
from .history_timeline import (
    TimelineCensus,
    state_title_coverage_gaps,
    temporal_event_view,
    timeline_selection,
)
from .skill_packages import _resolve


def _implementation_identity():
    root = Path(__file__).resolve().parent
    return fingerprint(
        {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in (
                "action_contracts.py",
                "direct_skill_extraction.py",
                "history_census.py",
                "history_timeline.py",
                "history_timeline_recovery.py",
                "history_http.py",
                "skill_packages.py",
            )
        }
    )


class _RecoveryAPI:
    """Journal dispatches, including failures and interrupted requests, without payloads."""

    def __init__(self, api, output, config):
        self.api, self.root = api, output / "recovery-api-calls"
        self.config_sha256, self.context = fingerprint(config), None
        self.root.mkdir(parents=True, exist_ok=True)
        self.sequence = len(list(self.root.glob("request-*.json")))
        self.summary()

    @property
    def calls(self):
        return self.api.calls

    @property
    def rate_limit(self):
        return self.api.rate_limit

    def graphql(self, query, variables):
        self.sequence += 1
        path = self.root / f"request-{self.sequence:06}.json"
        if path.exists():
            raise ValueError("recovery API journal sequence changed")
        record = {
            "sequence": self.sequence,
            "config_sha256": self.config_sha256,
            "context_sha256": self.context,
            "query_sha256": fingerprint(query),
            "variables_sha256": fingerprint(variables),
            "started_at": now(),
            "status": "started",
            "transport_calls_delta": None,
        }
        write_json(path, record)
        before = self.api.calls
        try:
            result = self.api.graphql(query, variables)
        except Exception as error:
            record.update({"status": "failed", "failure_type": type(error).__name__})
            raise
        else:
            record["status"] = "successful"
            return result
        finally:
            record.update({"finished_at": now(), "transport_calls_delta": self.api.calls - before})
            write_json(path, record)

    def summary(self):
        records = [json.loads(p.read_text()) for p in sorted(self.root.glob("request-*.json"))]
        if any(
            r["sequence"] != index
            or r["config_sha256"] != self.config_sha256
            or r["status"] not in {"started", "successful", "failed"}
            for index, r in enumerate(records, 1)
        ):
            raise ValueError("recovery API journal configuration/sequence changed")
        return {
            "request_attempts": len(records),
            "successful_requests": sum(r["status"] == "successful" for r in records),
            "failed_requests": sum(r["status"] == "failed" for r in records),
            "unfinished_requests": sum(r["status"] == "started" for r in records),
            "transport_calls_recorded": sum(r["transport_calls_delta"] or 0 for r in records),
            "records_sha256": fingerprint(records),
        }


def _source_files(root):
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError("timeline recovery source cannot contain symlinks")
        if path.is_file():
            if path.suffix != ".json":
                raise ValueError("timeline recovery accepts only public JSON census files")
            raw = path.read_bytes()
            text = raw.decode("utf-8")
            if safe_text(text) != text:
                raise ValueError("restricted census artifact rejected; values suppressed")
            json.loads(text)
            files[path.relative_to(root).as_posix()] = hashlib.sha256(raw).hexdigest()
    return files


def _checked(path, expected, *, records=False):
    value = json.loads(path.read_text())
    if fingerprint(value["records"] if records else value) != expected:
        raise ValueError("source census checkpoint integrity failed")
    return value


def _repository_input(source, repository, cutoff):
    folder = source / repository.replace("/", "__")
    manifest = json.loads((folder / "manifest.json").read_text())
    if (
        manifest["cutoff_exclusive"] != cutoff
        or not manifest["issue_pagination_complete"]
        or not manifest["identity_second_pass_verified"]
        or not manifest["comments_pagination_complete"]
    ):
        raise ValueError("recovery needs the complete matching issue population")
    issues = [
        row
        for page in manifest["issue_pages"]
        for row in _checked(_resolve(folder, page["file"]), page["sha256"])["records"]
    ]
    for page in manifest["comment_pages"]:
        _checked(_resolve(folder, page["file"]), page["sha256"])
    tm = json.loads((folder / "timeline-manifest.json").read_text())
    if (
        tm["cutoff_exclusive"] != cutoff
        or tm["identity_set_sha256"] != manifest["identity_set_sha256"]
    ):
        raise ValueError("source timeline population identity changed")
    pages = [
        (page, _checked(_resolve(folder, page["file"]), page["sha256"], records=True))
        for page in tm["batches"]
    ]
    timelines = {}
    for _, page in pages:
        for record in page["records"]:
            number = record["identity"]["number"]
            if number in timelines:
                raise ValueError("duplicate source timeline identity")
            timelines[number] = record
    identities = {row["identity"]["number"]: row["identity"] for row in issues}
    if (
        any(
            ident["repository"] != repository or utc(ident["created_at"]) >= utc(cutoff)
            for ident in identities.values()
        )
        or fingerprint(
            sorted(
                (ident["node_id"], ident["number"], ident["created_at"])
                for ident in identities.values()
            )
        )
        != manifest["identity_set_sha256"]
    ):
        raise ValueError("source issue population seal changed")
    if len(identities) != len(issues) or not set(timelines) <= set(identities):
        raise ValueError("source issue/timeline population differs")
    for number, record in timelines.items():
        if record["identity"] != identities[number]:
            raise ValueError("timeline belongs to another issue identity")
    return issues, timelines, tm, pages


def _merge_record(row, archived, fresh, cutoff):
    previous = {
        event["id"]: temporal_event_view(event, cutoff) for event in archived.get("events", [])
    }
    events = dict(previous)
    for event in fresh["events"]:
        event = temporal_event_view(event, cutoff)
        old = previous.get(event["id"])
        if old and (old["__typename"], utc(old["createdAt"])) != (
            event["__typename"],
            utc(event["createdAt"]),
        ):
            raise ValueError("historical event identity/type/date changed")
        events[event["id"]] = event
    if any(utc(event["createdAt"]) >= utc(cutoff) for event in events.values()):
        raise ValueError("post-cutoff event entered recovery")
    gaps = state_title_coverage_gaps(
        row["as_of"]["state_title_events"], list(events.values()), cutoff
    )
    unavailable = {
        fingerprint(gap): gap
        for gap in [
            *archived.get("unavailable_event_metadata", []),
            *fresh["unavailable_event_metadata"],
        ]
    }
    result = {
        **fresh,
        "events": sorted(events.values(), key=lambda event: (utc(event["createdAt"]), event["id"])),
        "unavailable_event_metadata": list(unavailable.values()),
        "state_title_coverage_gaps": gaps,
        "selected_event_metadata_complete": not unavailable and not gaps,
        "recovery_lineage": {
            "archived_record_sha256": fingerprint(archived),
            "fresh_record_sha256": fingerprint(fresh),
            "retained_archived_only_events": len(
                set(previous) - {e["id"] for e in fresh["events"]}
            ),
            "observed_at": now(),
            "attestation_is_not_historical_learned_text": True,
        },
    }
    return result


def recover_timeline_coverage(source, output, cutoff, api, *, batch_size=50):
    source_path, output_path = Path(source).absolute(), Path(output).absolute()
    if any(p.is_symlink() for path in (source_path, output_path) for p in (path, *path.parents)):
        raise ValueError("timeline recovery paths cannot contain symlinks")
    source, output = source_path.resolve(), output_path.resolve()
    if output.exists() and any(p.is_symlink() for p in output.rglob("*")):
        raise ValueError("timeline recovery output cannot contain symlinks")
    if source == output or source.is_relative_to(output) or output.is_relative_to(source):
        raise ValueError("recovery output must be separate from its immutable source")
    if not 1 <= batch_size <= 75:
        raise ValueError("recovery batch size must be between 1 and 75")
    files = _source_files(source)
    repositories = []
    for path in sorted(source.glob("*/manifest.json")):
        repository = json.loads(path.read_text())["repository"]
        if (
            not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
            or (path.parent.name != repository.replace("/", "__"))
            or repository in repositories
        ):
            raise ValueError("source repository manifest identity changed")
        repositories.append(repository)
    if not repositories:
        raise ValueError("source census has no repository manifests")
    config = {
        "schema": "historical-timeline-state-recovery-v3",
        "implementation_sha256": _implementation_identity(),
        "source_root": str(source),
        "source_files_sha256": fingerprint(files),
        "cutoff_exclusive": cutoff,
        "batch_size": batch_size,
        "repositories": repositories,
    }
    marker = output / "timeline-recovery-manifest.json"
    if output.exists():
        if not marker.exists():
            raise ValueError("preserve existing output without a matching recovery marker")
        state = json.loads(marker.read_text())
        if state["config"] != config:
            raise ValueError("recovery source/configuration changed")
    else:
        output.mkdir(parents=True)
        state = {
            "config": config,
            "source_copy_completed": False,
            "completed": False,
            "formal_SWE_runs": 0,
            "actual_LLM_calls": 0,
        }
        write_json(marker, state)
    state["completed"] = False
    write_json(marker, state)
    if not state["source_copy_completed"]:
        for relative, sha in files.items():
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if hashlib.sha256(target.read_bytes()).hexdigest() != sha:
                    raise ValueError("incomplete recovery source copy changed")
            else:
                shutil.copy2(source / relative, target)
        state["source_copy_completed"] = True
        write_json(marker, state)
    source_seal = output / "recovery-source-files.json"
    if source_seal.exists() and json.loads(source_seal.read_text()) != files:
        raise ValueError("recovery source file seal changed")
    write_json(source_seal, files)
    for relative, sha in files.items():
        if "/timeline/" not in relative and not relative.endswith("/timeline-manifest.json"):
            if hashlib.sha256((output / relative).read_bytes()).hexdigest() != sha:
                raise ValueError("recovery copied census/schema changed")
    api = _RecoveryAPI(api, output, config)
    summaries = []
    for repository in repositories:
        rows, archived, tm, pages = _repository_input(source, repository, cutoff)
        targets = [
            row
            for row in rows
            if row["identity"]["number"] not in archived
            or state_title_coverage_gaps(
                row["as_of"]["state_title_events"],
                archived[row["identity"]["number"]]["events"],
                cutoff,
            )
        ]
        collector = TimelineCensus(output, repository, cutoff, api, progress=lambda _: None)
        state_collector = TimelineCensus(output, repository, cutoff, api, progress=lambda _: None)
        state_collector.selection = timeline_selection(
            {
                "possibleTypes": [
                    entry
                    for entry in collector.schema["possibleTypes"]
                    if entry["name"] in {"ClosedEvent", "ReopenedEvent", "RenamedTitleEvent"}
                ]
            }
        )
        recovered, total_calls = {}, 0
        for start in range(0, len(targets), batch_size):
            batch = targets[start : start + batch_size]
            identities = [row["identity"] for row in batch]
            checkpoint = (
                output
                / "recovery"
                / repository.replace("/", "__")
                / f"batch-{start // batch_size + 1:05}.json"
            )
            expected = {
                **config,
                "repository": repository,
                "selection_sha256": fingerprint(collector.selection),
                "state_view_selection_sha256": fingerprint(state_collector.selection),
                "identities": identities,
            }
            api.context = fingerprint(expected)
            if checkpoint.exists():
                payload = json.loads(checkpoint.read_text())
                if (
                    payload["config"] != expected
                    or fingerprint(payload["records"]) != payload["records_sha256"]
                ):
                    raise ValueError("recovery checkpoint changed")
            else:
                before = api.calls
                query = (
                    "query($ids:[ID!]!){nodes(ids:$ids){... on Issue{id timelineItems(first:100){nodes{"
                    + collector.selection
                    + "} pageInfo{hasNextPage endCursor}}}} rateLimit{cost remaining resetAt}}"
                )
                data = api.graphql(query, {"ids": [identity["node_id"] for identity in identities]})
                nodes = data["nodes"]
                if len(nodes) != len(identities) or any(
                    node and node.get("id") != identity["node_id"]
                    for node, identity in zip(nodes, identities)
                ):
                    raise ValueError("recovery API population identity changed")
                records = []
                for row, node in zip(batch, nodes):
                    if node:
                        fresh = collector.collect_issue(row["identity"], node["timelineItems"])
                    else:
                        fresh = {
                            "identity": row["identity"],
                            "events": [],
                            "all_event_types_paginated": False,
                            "unavailable_event_metadata": [
                                {"reason": "issue-node-currently-unavailable"}
                            ],
                            "selected_event_metadata_complete": False,
                            "all_event_payload_fields_collected": False,
                        }
                    records.append(
                        _merge_record(
                            row, archived.get(row["identity"]["number"], {}), fresh, cutoff
                        )
                    )
                residual = [
                    (row, record)
                    for row, record in zip(batch, records)
                    if record["state_title_coverage_gaps"] and record["all_event_types_paginated"]
                ]
                if residual:
                    state_query = (
                        "query($ids:[ID!]!){nodes(ids:$ids){... on Issue{id "
                        "timelineItems(first:100,itemTypes:[CLOSED_EVENT,REOPENED_EVENT,RENAMED_TITLE_EVENT]){nodes{"
                        + state_collector.selection
                        + "} pageInfo{hasNextPage endCursor}}}} rateLimit{cost remaining resetAt}}"
                    )
                    state_nodes = api.graphql(
                        state_query, {"ids": [row["identity"]["node_id"] for row, _ in residual]}
                    )["nodes"]
                    if len(state_nodes) != len(residual) or any(
                        node and node.get("id") != row["identity"]["node_id"]
                        for (row, _), node in zip(residual, state_nodes)
                    ):
                        raise ValueError("state timeline view population identity changed")
                    for (row, record), node in zip(residual, state_nodes):
                        if not node:
                            record["unavailable_event_metadata"].append(
                                {"reason": "state-view-issue-node-currently-unavailable"}
                            )
                            record["selected_event_metadata_complete"] = False
                            continue
                        state_record = state_collector.collect_issue(
                            row["identity"], node["timelineItems"], state_title_only=True
                        )
                        if any(
                            event["__typename"]
                            not in {"ClosedEvent", "ReopenedEvent", "RenamedTitleEvent"}
                            for event in state_record["events"]
                        ):
                            raise ValueError("state timeline view returned unrelated events")
                        merged_view = _merge_record(row, record, state_record, cutoff)
                        for key in (
                            "events",
                            "unavailable_event_metadata",
                            "state_title_coverage_gaps",
                            "selected_event_metadata_complete",
                        ):
                            record[key] = merged_view[key]
                        record["state_title_view_lineage"] = {
                            "selection_sha256": fingerprint(state_collector.selection),
                            "query_sha256": fingerprint(state_query),
                            "record_sha256": fingerprint(state_record),
                            "all_selected_state_event_types_paginated": state_record[
                                "all_event_types_paginated"
                            ],
                            "events_observed": len(state_record["events"]),
                            "supplements_unfiltered_view_without_invented_event_ids": True,
                        }
                payload = {
                    "config": expected,
                    "records": records,
                    "records_sha256": fingerprint(records),
                    "api_calls": api.calls - before,
                    "rate_limit": api.rate_limit,
                    "observed_at": now(),
                }
                write_json(checkpoint, payload)
            if [r["identity"] for r in payload["records"]] != identities:
                raise ValueError("recovery checkpoint population changed")
            recovered.update({r["identity"]["number"]: r for r in payload["records"]})
            total_calls += payload["api_calls"]
            write_json(
                output / "recovery-progress.json",
                {
                    "repository": repository,
                    "recovered_issues": len(recovered),
                    "target_issues": len(targets),
                    "completed_repositories": summaries,
                    "api_journal": api.summary(),
                    "actual_LLM_calls": 0,
                    "formal_SWE_runs": 0,
                },
            )
        merged = {**archived, **recovered}
        for page, content in pages:
            value = deepcopy(content)
            value["records"] = [merged[r["identity"]["number"]] for r in content["records"]]
            value["sha256"] = fingerprint(value["records"])
            write_json(output / repository.replace("/", "__") / page["file"], value)
        missing = sorted(set(merged) - set(archived))
        updated = deepcopy(tm)
        for page in updated["batches"]:
            value = json.loads((output / repository.replace("/", "__") / page["file"]).read_text())
            page.update(
                {
                    "sha256": fingerprint(value["records"]),
                    "events": sum(len(r["events"]) for r in value["records"]),
                    "unavailable_events": sum(
                        len(r["unavailable_event_metadata"]) for r in value["records"]
                    ),
                }
            )
        if missing:
            path = "timeline/recovered-missing-issues.json"
            records = [merged[n] for n in missing]
            write_json(
                output / repository.replace("/", "__") / path,
                {"records": records, "sha256": fingerprint(records), "recovery_config": config},
            )
            updated["batches"].append(
                {
                    "file": path,
                    "sha256": fingerprint(records),
                    "issues": len(records),
                    "events": sum(len(r["events"]) for r in records),
                    "unavailable_events": sum(
                        len(r["unavailable_event_metadata"]) for r in records
                    ),
                }
            )
        remaining = [
            row["identity"]["number"]
            for row in rows
            if state_title_coverage_gaps(
                row["as_of"]["state_title_events"],
                merged[row["identity"]["number"]]["events"],
                cutoff,
            )
        ]
        updated.update(
            {
                "observed_at": now(),
                "issue_count": len(merged),
                "event_count": sum(len(r["events"]) for r in merged.values()),
                "recovery_api_calls": total_calls,
                "recovery_source_manifest_sha256": fingerprint(tm),
                "known_state_title_gaps_remaining": len(remaining),
                "full_history_qualified": False,
            }
        )
        write_json(output / repository.replace("/", "__") / "timeline-manifest.json", updated)
        summaries.append(
            {
                "repository": repository,
                "issue_count": len(rows),
                "target_issues": len(targets),
                "recovered_issues": len(recovered),
                "remaining_gap_issues": remaining,
                "api_calls": total_calls,
            }
        )
    if _source_files(source) != files:
        raise ValueError("immutable source changed during recovery")
    state.update(
        {
            "completed": True,
            "completed_at": now(),
            "api_journal": api.summary(),
            "repositories": summaries,
            "all_known_state_events_recovered": all(
                not r["remaining_gap_issues"] for r in summaries
            ),
            "serving_KB_admitted": False,
            "full_history_qualified": False,
        }
    )
    write_json(marker, state)
    return state
