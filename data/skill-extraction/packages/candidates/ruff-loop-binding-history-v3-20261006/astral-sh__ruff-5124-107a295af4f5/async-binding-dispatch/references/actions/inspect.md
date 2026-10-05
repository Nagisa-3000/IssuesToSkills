# Inspect dispatch and variant coverage

Locate current semantic owners and trace the failing statement from the enabled rule dispatch to the rule's match. Record hashed anchors, admitted variants, handled variants, and the existing extraction/traversal used for context-manager bindings. Read-only inspection must not alter tracked source or expected outputs.

```arex-contract-v4
{
  "id": "workflow:verified-history:fa7c382943159e4d620bbbba:inspect",
  "intent": "Determine whether an asynchronous context-manager statement reaches a handler that omits its variant.",
  "mechanism": "Compare dispatcher admission with rule statement matching and inspect adjacent binding behavior.",
  "semantic_role": "variant-coverage-probe",
  "owner_role": "binding-redefinition-rule",
  "operation": "Read current dispatcher, rule, and regression owners; trace the public reproduction; produce evidence-backed owner bindings and a mismatch report without changing tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "coverage-report",
      "semantic_role": "binding-variant-coverage",
      "artifact_kind": "review-report",
      "language": "Rust",
      "scope": "binding-rule",
      "phase": "pre-edit",
      "state": "mismatch-confirmed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "variant-mismatch-established", "value": true, "evaluator": "evidence"},
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-binding-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "distinct-binding-non-diagnostic-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "coverage-review",
      "instruction": "Review current anchors to confirm that dispatch admits the asynchronous context-manager variant and the rule omits it. Record existing synchronous context-manager and loop behavior. If not confirmed, do not emit a mismatch-confirmed port. Verify inspection leaves tracked files unchanged.",
      "evidence_refs": ["astral-sh/ruff:5124:body", "astral-sh/ruff:5124:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["astral-sh/ruff:5124:repair:107a295af4f5"],
  "evidence_refs": ["astral-sh/ruff:5124:title", "astral-sh/ruff:5124:body", "astral-sh/ruff:5124:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:fa7c382943159e4d620bbbba",
  "read_set": ["role:binding-rule-dispatch", "role:binding-redefinition-rule", "role:binding-rule-regressions"],
  "write_set": []
}
```

The output and effects are intended outcomes, not observations from an executed Skill. Missing owners or uncertain semantics yield UNKNOWN and permit additional public probes only.
