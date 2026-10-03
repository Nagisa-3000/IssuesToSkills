# Repair annotation-only binding semantics

Use the observed map to bind the operation to current owners.

1. Distinguish annotation assignments without values from ordinary value bindings.
2. Visit no-value annotation targets so the declaration can be recorded. Preserve applicable AST-version compatibility.
3. Track no annotation context, bare context, and string context. Restore prior state after nested traversal, including exceptions.
4. Route string-annotation entry points through string context. The historical postponed condition is string context or the annotations future flag.
5. Skip annotation-only bindings outside that condition and continue scope lookup, rather than accepting them as runtime values.
6. Preserve binding replacement and unused-variable behavior when a subsequent assignment supplies a value.

The future flag directly participates in the historical property. Do not infer unsupported runtime-read policy for future-enabled modules; review current semantics separately.

Effects below are repair targets, not observed success. Retain validation after this edit.

```arex-contract-v4
{
  "id": "workflow:verified-history:be71c3f9e9544046d28904cd:repair",
  "intent": "Correct postponed annotation-only references without conflating declarations with value assignments.",
  "mechanism": "Introduce distinct annotation-only bindings and context-sensitive lookup with scoped state restoration.",
  "semantic_role": "annotation-binding-repair",
  "owner_role": "python-analyzer-binding-and-annotation-owners",
  "operation": "Edit current annotation traversal, binding construction, lookup, and context entry points according to observed applicability.",
  "kind": "edit",
  "inputs": [
    {
      "name": "binding-context-map",
      "semantic_role": "binding-context-map",
      "artifact_kind": "review-report",
      "language": "Python",
      "scope": "current-analyzer",
      "phase": "diagnosis",
      "state": "owners-and-behavior-observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "annotation-binding-patch",
      "semantic_role": "annotation-binding-patch",
      "artifact_kind": "source-change",
      "language": "Python",
      "scope": "current-analyzer",
      "phase": "repair",
      "state": "modified-awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:python-analyzer-binding-and-annotation-owners",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "Current role bindings resolve to existing owner symbols."
    },
    {"key": "current-binding-context-observed", "value": true, "evaluator": "evidence"},
    {
      "key": "historical-mechanism-applicable",
      "value": true,
      "evaluator": "evidence",
      "description": "Current public probes and review establish semantic applicability, not merely matching names."
    }
  ],
  "effects": [
    {"key": "annotation-only-binding-distinguished", "value": true, "evaluator": "evidence"},
    {"key": "postponed-context-lookup-implemented", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "bare-reference-without-postponement-remains-undefined", "value": true, "evaluator": "evidence"},
    {"key": "annotation-only-is-not-runtime-value-assignment", "value": true, "evaluator": "evidence"},
    {"key": "later-unused-value-assignment-reported-once", "value": true, "evaluator": "evidence"},
    {"key": "annotation-context-restored-after-traversal", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-binding-context-change",
      "instruction": "Review the diff for distinct no-value bindings, preserved value assignments, restored context, postponed eligibility, and lookup continuation; follow with the explicit validation Action.",
      "evidence_refs": ["PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:486:repair:5fc37cbda5bf"],
  "evidence_refs": ["PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
  "read_set": ["role:python-analyzer-binding-and-annotation-owners", "role:python-analyzer-public-regression-suite"],
  "write_set": ["role:python-analyzer-binding-and-annotation-owners"],
  "invalidates": ["current-binding-context-observed", "postponed-reference-matrix-validated", "adjacent-diagnostics-validated"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:be71c3f9e9544046d28904cd"
}
```
