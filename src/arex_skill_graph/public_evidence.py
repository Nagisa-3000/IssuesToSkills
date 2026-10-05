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


def solver_evidence_working_set(task, broker_observations, reads, *, workspace_execution_sha256):
    """Retain bounded exact this-run reads, with explicit stale-source information."""
    pages, seen, characters = [], set(), 0
    for read in reversed(list(reads.values())):
        if read.get("denied") or not isinstance(read.get("content"), str):
            continue
        selector = (
            read["evidence_id"],
            read["field"],
            read.get("json_pointer"),
            tuple(sorted(read.get("json_pointers") or [])),
            read["offset"],
        )
        if selector in seen:
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
    return {
        "schema": "solver-public-evidence-working-set-v1",
        "max_pages": 8,
        "max_content_characters": 12000,
        "pages": list(reversed(pages)),
        "omitted_read_count": len(reads) - len(pages),
        "assurance": (
            "Exact bounded pages actually read in this run; old pages may be evicted. "
            "Source/workspace identity is not semantic acceptance, prerequisite satisfaction, "
            "an Oracle witness or edit authorization. Full original reads remain sealed."
        ),
    }
