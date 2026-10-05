# Inspect applicability and owners

Read current public code and fixtures and probe the reported diagnostic without editing tracked files. Confirm that the defect is keyword loss in replacement text, not a reason to suppress the recommendation. Record current owner anchors, positional eligibility, and keyword-free baseline.

```arex-contract-v4
{
  "id": "workflow:verified-history:4f600acd843f37945bbd0765:inspect",
  "intent": "Establish current applicability and semantic owner bindings.",
  "mechanism": "Compare a keyword-bearing list-comprehension call with its emitted suggestion and review the replacement-rendering branch.",
  "semantic_role": "applicability-probe",
  "owner_role": "generator-suggestion-renderer",
  "operation": "Read current public code and fixtures, bind renderer and regression owners, and record diagnostic observations without editing tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "rendering-review",
      "semantic_role": "generator-rendering-applicability",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "rendering-applicability-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "keyword-free-suggestion-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-eligibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-keyword-loss",
      "instruction": "Record original call, actual suggestion, keyword loss, current renderer and regression anchors, positional eligibility gate, and keyword-free baseline. Confirm inspection made no tracked-file edits. A mismatching mechanism is a failure of applicability, not permission to widen the repair.",
      "evidence_refs": ["pylint-dev/pylint:8563:body", "pylint-dev/pylint:8563:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8563:repair:4a485e28f0a5"],
  "evidence_refs": ["pylint-dev/pylint:8563:title", "pylint-dev/pylint:8563:body", "pylint-dev/pylint:8563:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:4f600acd843f37945bbd0765",
  "read_set": ["role:generator-suggestion-renderer", "role:generator-suggestion-regressions"],
  "write_set": []
}
```

An UNKNOWN finding permits more public inspection only. Bind the Oracle to current instructions and commands before execution.
