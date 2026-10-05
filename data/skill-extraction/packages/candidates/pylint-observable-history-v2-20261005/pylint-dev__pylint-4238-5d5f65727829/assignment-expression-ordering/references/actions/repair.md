# Edit narrow ordering rules and fixtures

Apply only confirmed supported branches. Preserve existing scope/frame eligibility and normal source-position ordering; do not introduce a blanket diagnostic exemption.

The historical conditional-expression check recognized `Assign`, `AnnAssign`, `AugAssign`, and `Expr`. The separate f-string fallback recognized only `Assign`, `AnnAssign`, and `AugAssign`, with a `JoinedStr` value, equal definition/use lines, and `not PY39_PLUS`.

Add public positive fixtures and retained negative controls. Adjust expected line positions only as required by fixture additions.

```arex-contract-v4
{
  "id": "workflow:verified-history:611e9bc5eaac38ef599b59a7:repair",
  "intent": "Correct the supported false diagnostic without disabling real ordering checks.",
  "mechanism": "Broaden supported IfExp statement contexts and narrowly gate a JoinedStr coordinate fallback for older AST ambiguity.",
  "semantic_role": "ordering-repair",
  "owner_role": "assignment-use-checker",
  "operation": "Edit the bound diagnostic owner and runtime policy only for confirmed statement-kind and coordinate cases. Retain existing frame/scope guards and accurate normal ordering. Edit public fixtures and expected outputs for applicable f-string and conditional-expression variants, genuine earlier reads, and unrelated diagnostics.",
  "kind": "edit",
  "inputs": [
    {
      "name": "ordering-analysis",
      "semantic_role": "assignment-expression-ordering-analysis",
      "artifact_kind": "evidence-record",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "ordering-candidate",
      "semantic_role": "assignment-expression-ordering-candidate",
      "artifact_kind": "checkout-change",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "ordering-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {
      "key": "role:assignment-use-checker",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "The current diagnostic decision owner is bound."
    },
    {
      "key": "role:runtime-version-policy",
      "value": true,
      "evaluator": "file_exists",
      "description": "The current runtime feature-policy resource is bound."
    },
    {
      "key": "role:assignment-expression-regressions",
      "value": true,
      "evaluator": "file_exists",
      "description": "The current public regression resource is bound."
    }
  ],
  "effects": [
    {"key": "ordering-repair-present", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-controls-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-earlier-read-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-edit",
      "instruction": "Review the diff against current mechanism evidence. Check eligible IfExp statement kinds, unchanged frame/scope guards, normal ordering, and narrow runtime/equal-line/assignment-like JoinedStr fallback where applicable. Confirm positive fixtures and retained earlier-read and unrelated-diagnostic expectations. Diff review is not execution validation.",
      "evidence_refs": ["pylint-dev/pylint:4238:fix", "pylint-dev/pylint:4238:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4238:repair:5d5f65727829"],
  "evidence_refs": ["pylint-dev/pylint:4238:fix", "pylint-dev/pylint:4238:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:611e9bc5eaac38ef599b59a7",
  "read_set": ["role:assignment-use-checker", "role:runtime-version-policy", "role:assignment-expression-regressions"],
  "write_set": ["role:assignment-use-checker", "role:runtime-version-policy", "role:assignment-expression-regressions"],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "blanket-diagnostic-suppression-required", "value": true, "evaluator": "evidence"}
  ]
}
```

The output is a candidate awaiting validation, not an observed successful repair. Resolve current resource aliases before read/write conflict checks.
