"""Bounded reads of already public evidence without command execution or promotion."""

from __future__ import annotations

import hashlib
import json
import re

from .action_contracts import digest
from .task_context import assert_public


def _select_json_pointer(value, pointer):
    if pointer:
        if not pointer.startswith("/"):
            raise ValueError("JSON pointer must be empty or start with /")
        for token in pointer[1:].split("/"):
            if re.search(r"~(?![01])", token):
                raise ValueError("invalid JSON pointer escape")
            token = token.replace("~1", "/").replace("~0", "~")
            if isinstance(value, dict) and token in value:
                value = value[token]
            elif (
                isinstance(value, list)
                and re.fullmatch(r"0|[1-9][0-9]*", token)
                and int(token) < len(value)
            ):
                value = value[int(token)]
            else:
                raise ValueError("JSON pointer does not select an existing value")
    return value


def read_public_evidence(task, broker_observations, arguments):
    """Read a stored representation by ID; never resolve a filesystem path."""
    allowed = {"evidence_id", "field", "offset", "limit", "json_pointer", "json_pointers"}
    if set(arguments) - allowed:
        raise ValueError("unknown public evidence reader arguments")
    identity = arguments.get("evidence_id")
    field = arguments.get("field", "record")
    offset, limit = arguments.get("offset", 0), arguments.get("limit", 4000)
    pointer = arguments.get("json_pointer")
    pointers = arguments.get("json_pointers")
    if "json_pointers" in arguments and (
        "json_pointer" in arguments
        or not isinstance(pointers, list)
        or not 1 <= len(pointers) <= 16
        or any(not isinstance(p, str) or len(p) > 512 for p in pointers)
        or len(set(pointers)) != len(pointers)
    ):
        raise ValueError("invalid grouped JSON selection")
    if (
        not isinstance(identity, str)
        or not identity
        or not isinstance(field, str)
        or field not in {"record", "output", "content", "observation"}
        or type(offset) is not int
        or offset < 0
        or type(limit) is not int
        or not 1 <= limit <= 4000
        or (pointer is not None and (not isinstance(pointer, str) or len(pointer) > 512))
    ):
        raise ValueError("invalid public evidence pagination or selection")
    if identity in broker_observations:
        record = broker_observations[identity]
        if record.get("observation_id") != identity:
            raise ValueError("public evidence identity mismatch")
        source = "current_run_broker_record"
        if field == "record":
            text = json.dumps(record, ensure_ascii=False, sort_keys=True)
        elif field in {"output", "content"} and isinstance(record.get(field), str):
            text = record[field]
        else:
            raise ValueError("requested field is absent from this broker record")
        record_hash = digest(record)
    else:
        anchor = next((a for a in task.anchors if a.id == identity), None)
        if anchor is None:
            raise ValueError("unknown public evidence ID")
        source = "retained_task_anchor_representation"
        text = anchor.observation
        record_hash = hashlib.sha256(text.encode()).hexdigest()
        if field != "observation":
            try:
                record = json.loads(text)
            except (ValueError, TypeError) as error:
                raise ValueError("anchor contains text; use field=observation") from error
            if not isinstance(record, dict):
                raise ValueError("anchor does not contain a broker object")
            if field == "record":
                text = json.dumps(record, ensure_ascii=False, sort_keys=True)
            elif field in {"output", "content"} and isinstance(record.get(field), str):
                text = record[field]
            else:
                raise ValueError("requested field is absent from this anchor representation")
    assert_public(text)
    field_hash = hashlib.sha256(text.encode()).hexdigest()
    if pointer is not None or pointers is not None:
        try:
            selected = json.loads(text)
        except (ValueError, TypeError) as error:
            raise ValueError("JSON selection requires a complete stored JSON value") from error
        selected = (
            {p: _select_json_pointer(selected, p) for p in pointers}
            if pointers is not None
            else _select_json_pointer(selected, pointer)
        )
        text = json.dumps(selected, ensure_ascii=False, sort_keys=True)
    assert_public(text)
    end = min(offset + limit, len(text))
    return {
        "operation": "read_public_evidence",
        "evidence_id": identity,
        "source": source,
        "field": field,
        "json_pointer": pointer,
        **({"json_pointers": pointers} if pointers is not None else {}),
        "stored_record_sha256": record_hash,
        "field_sha256": field_hash,
        "selection_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "offset": offset,
        "total_characters": len(text),
        "next_offset": end if end < len(text) else None,
        "content": text[offset:end],
        "assurance": (
            "Read of stored public evidence only; not fresh execution, a new Oracle witness, "
            "semantic acceptance, fact promotion or edit authorization. "
            "Retained anchor representations may already contain excerpts."
        ),
    }


def _small_broker_output_page(identity, record):
    """Project only a complete small stored output of an actual this-run command."""
    if (
        record.get("observation_id") != identity
        or record.get("operation") != "run_public_command"
        or record.get("denied")
        or not isinstance(record.get("output"), str)
        or len(record["output"]) > 4000
    ):
        return None
    content = record["output"]
    assert_public(content)
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    return {
        "operation": "run_public_command",
        "projection_kind": "current_run_broker_output",
        "observation_id": identity,
        "evidence_id": identity,
        "source": "current_run_broker_record",
        "field": "output",
        "json_pointer": None,
        "stored_record_sha256": digest(record),
        "field_sha256": content_hash,
        "selection_sha256": content_hash,
        "offset": 0,
        "total_characters": len(content),
        "next_offset": None,
        "content": content,
        **{
            key: record[key]
            for key in (
                "exit_code",
                "process_exit_code",
                "execution_available",
                "timed_out",
                "context_revision",
                "protocol_error",
                "workspace_rollback",
                "write_scope_accepted",
            )
            if key in record
        },
        "assurance": (
            "Model projection of the complete small stored output of this-run broker execution; "
            "not a reader event, fresh execution, a new witness, semantic acceptance or authorization. "
            "Original process status and record identity remain authoritative."
        ),
    }


def solver_evidence_working_set(task, broker_observations, reads, *, workspace_execution_sha256):
    """Retain exact reads and small broker outputs, without creating observations."""
    candidates = []
    for identity, record in broker_observations.items():
        page = _small_broker_output_page(identity, record)
        if page is not None:
            candidates.append(page)
    broker_output_count = len(candidates)
    for read in reads.values():
        if (
            not read.get("denied")
            and isinstance(read.get("content"), str)
            and len(read["content"]) <= 4000
        ):
            candidates.append({**read, "projection_kind": "explicit_evidence_read"})

    def sequence(item):
        index, page = item
        match = re.fullmatch(r"public:observation:([0-9]+)", page.get("observation_id", ""))
        return (int(match[1]) if match else -1, index)

    pages, seen, characters, deduplicated = [], set(), 0, 0
    for _, read in reversed(sorted(enumerate(candidates), key=sequence)):
        selector = (
            read["evidence_id"],
            read["field"],
            read["stored_record_sha256"],
            read.get("json_pointer"),
            tuple(sorted(read.get("json_pointers") or [])),
            read["offset"],
            read.get("total_characters"),
            read.get("next_offset"),
            hashlib.sha256(read["content"].encode()).hexdigest(),
        )
        if selector in seen:
            deduplicated += 1
            continue
        seen.add(selector)
        if len(pages) >= 8 or characters + len(read["content"]) > 12000:
            continue
        page = dict(read)
        record = broker_observations.get(read["evidence_id"])
        record_unchanged = False
        if record is not None:
            record_unchanged = digest(record) == read["stored_record_sha256"]
        else:
            anchor = next((a for a in task.anchors if a.id == read["evidence_id"]), None)
            if anchor is not None:
                record_unchanged = (
                    hashlib.sha256(anchor.observation.encode()).hexdigest()
                    == read["stored_record_sha256"]
                )
                try:
                    record = json.loads(anchor.observation)
                except (ValueError, TypeError):
                    record = None
        page["source_record_status"] = (
            "unchanged_stored_record" if record_unchanged else "changed_or_unavailable"
        )
        source_workspace = (
            record.get("workspace_execution_sha256")
            if isinstance(record, dict) and record_unchanged
            else None
        )
        page["source_workspace_status"] = (
            "matches_current_workspace"
            if source_workspace == workspace_execution_sha256
            else "stale_workspace"
            if source_workspace
            else "not_established"
        )
        pages.append(page)
        characters += len(read["content"])
    retained_reads = sum(p["projection_kind"] == "explicit_evidence_read" for p in pages)
    retained_outputs = len(pages) - retained_reads
    return {
        "schema": "solver-public-evidence-working-set-v2",
        "max_pages": 8,
        "max_page_content_characters": 4000,
        "max_content_characters": 12000,
        "pages": list(reversed(pages)),
        "omitted_read_count": len(reads) - retained_reads,
        "eligible_broker_output_count": broker_output_count,
        "omitted_broker_output_count": broker_output_count - retained_outputs,
        "deduplicated_page_count": deduplicated,
        "assurance": (
            "Exact bounded reads and complete small outputs of actual this-run broker executions; "
            "identical pages are deduplicated and old pages may be evicted. Projection does not "
            "create a reader event, execution, witness, fact, authorization or finish. "
            "Source/workspace identity is not semantic acceptance or prerequisite satisfaction. "
            "Full original reads and broker records remain sealed."
        ),
    }
