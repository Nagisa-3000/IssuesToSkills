"""Seal declared generation-context metadata without authoring Skill semantics.

Models author every instruction, Action, realization and evaluation resource.
An opt-in digest reference names the caller's complete immutable input context;
the publisher expands only that provenance field and records exact byte hashes.
"""

from __future__ import annotations

import hashlib
import json
import re

from .action_contracts import digest
from .direct_skill_extraction import parse_bundle
from .generation_context import GenerationContext

SCHEMA = "arex-generation-context-authority-v1"
MATERIALIZATION_FIELD = "generation_context_materialization"


def generation_context_reference(context: GenerationContext) -> dict:
    if not isinstance(context, GenerationContext):
        raise TypeError("generation authority requires a complete typed context")
    return {"schema": SCHEMA, "sha256": digest(context.to_dict())}


def materialize_generation_context(response: str, context: GenerationContext):
    """Expand an exact declared metadata reference; preserve all other resources.

    Existing complete, matching provenance is also accepted unchanged. Missing,
    shortened, forged or differently bound context is never repaired. The helper
    is pure: publication and semantic validation remain separate mandatory gates.
    """
    expected = generation_context_reference(context)
    complete = context.to_dict()
    packages, deferred = parse_bundle(response)
    replacements, audits = [], {}
    for name, files in packages.items():
        relative = "references/provenance.json"
        if relative not in files:
            raise ValueError("generation authority cannot create missing provenance")
        provenance = json.loads(files[relative])
        if not isinstance(provenance, dict) or MATERIALIZATION_FIELD in provenance:
            raise ValueError("model cannot author the reserved materialization attestation")
        declared = provenance.get("generation_context")
        materialized = declared == expected
        if not materialized and declared != complete:
            raise ValueError("declared generation context differs from exact caller authority")
        untouched = {
            path: hashlib.sha256(content.encode()).hexdigest()
            for path, content in files.items()
            if path != relative
        }
        if materialized:
            provenance["generation_context"] = complete
            provenance[MATERIALIZATION_FIELD] = {
                **expected,
                "authorship": "deterministic_input_authority",
                "semantic_resources_modified": False,
            }
            text = json.dumps(provenance, ensure_ascii=False, indent=2) + "\n"
            marker = rf"^<<<FILE {re.escape(name)}/references/provenance\.json>>>\r?\n"
            pattern = marker + r"(.*?)(?=^<<<END FILE>>>\r?$)"
            matches = list(re.finditer(pattern, response, re.MULTILINE | re.DOTALL))
            if len(matches) != 1:
                raise ValueError("generation authority requires one exact provenance FILE block")
            match = matches[0]
            replacements.append((match.start(1), match.end(1), text))
        audits[name] = {
            "declared_generation_context_reference": expected,
            "materialized": materialized,
            "source_count": len(context.sources),
            "source_package_count": len(context.source_package_hashes),
            "unchanged_authored_resources_sha256": untouched,
            "semantic_resources_modified": False,
        }
    result = response
    for start, end, text in sorted(replacements, reverse=True):
        result = result[:start] + text + result[end:]
    completed, _ = parse_bundle(result)
    if set(completed) != set(packages):
        raise ValueError("generation materialization changed package identities")
    for name, files in packages.items():
        if set(completed[name]) != set(files) or any(
            completed[name][path] != content
            for path, content in files.items()
            if path != "references/provenance.json"
        ):
            raise ValueError("generation materialization changed authored semantic resources")
    return result, {
        "schema": SCHEMA,
        "author_bundle_sha256": hashlib.sha256(response.encode()).hexdigest(),
        "materialized_bundle_sha256": hashlib.sha256(result.encode()).hexdigest(),
        "deferred": bool(deferred),
        "packages": audits,
        "semantic_resources_modified": False,
    }
