"""Bounded reads of already public evidence without command execution or promotion."""

from __future__ import annotations

import hashlib
import json
import re

from .action_contracts import digest
from .task_context import assert_public


def read_public_evidence(task, broker_observations, arguments):
    """Read a stored representation by ID; never resolve a filesystem path."""
    allowed = {"evidence_id", "field", "offset", "limit", "json_pointer"}
    if set(arguments) - allowed:
        raise ValueError("unknown public evidence reader arguments")
    identity = arguments.get("evidence_id")
    field = arguments.get("field", "record")
    offset, limit = arguments.get("offset", 0), arguments.get("limit", 4000)
    pointer = arguments.get("json_pointer")
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
    if pointer is not None:
        try:
            selected = json.loads(text)
        except (ValueError, TypeError) as error:
            raise ValueError("JSON selection requires a complete stored JSON value") from error
        if pointer:
            if not pointer.startswith("/"):
                raise ValueError("JSON pointer must be empty or start with /")
            for token in pointer[1:].split("/"):
                if re.search(r"~(?![01])", token):
                    raise ValueError("invalid JSON pointer escape")
                token = token.replace("~1", "/").replace("~0", "~")
                if isinstance(selected, dict) and token in selected:
                    selected = selected[token]
                elif (
                    isinstance(selected, list)
                    and re.fullmatch(r"0|[1-9][0-9]*", token)
                    and int(token) < len(selected)
                ):
                    selected = selected[int(token)]
                else:
                    raise ValueError("JSON pointer does not select an existing value")
        text = json.dumps(selected, ensure_ascii=False, sort_keys=True)
    assert_public(text)
    end = min(offset + limit, len(text))
    return {
        "operation": "read_public_evidence",
        "evidence_id": identity,
        "source": source,
        "field": field,
        "json_pointer": pointer,
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
