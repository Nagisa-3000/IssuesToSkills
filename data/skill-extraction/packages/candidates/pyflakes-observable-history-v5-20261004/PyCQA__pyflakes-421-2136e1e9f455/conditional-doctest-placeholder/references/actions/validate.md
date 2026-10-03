# Validate the guard and regression

Bind public current-checkout commands for the reproduction, the new regression, and the existing doctest suite. Render the bound argv commands in the current task plan before execution. No executable historical test command was supplied.

Run the reproduction and regression after both modifications. Confirm the unused-import diagnostic is retained. Run adjacent public doctest tests, including the no-module-underscore path; if coverage is absent, use a public probe and explicitly report the coverage gap. Do not infer whole-project success from a changed-file suite.

```arex-contract-v4
{
  "id": "workflow:verified-history:c76d35c9a48e360887b3c443:validate",
  "intent": "Observe repaired collision behavior and preserved adjacent doctest behavior.",
  "mechanism": "Execute current public reproduction and regression checks plus adjacent doctest validation.",
  "semantic_role": "repair-validation",
  "owner_role": "doctest-regression-tests",
  "operation": "Validate both modified owners with current public Oracle bindings.",
  "kind": "validate",
  "inputs": [
    {"name": "initializer", "semantic_role": "doctest-initializer-code", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "conditionally-guarded", "optional": false},
    {"name": "tests", "semantic_role": "doctest-regression-tests", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "collision-regression-added", "optional": false}
  ],
  "outputs": [
    {"name": "validation", "semantic_role": "public-doctest-validation", "artifact_kind": "test-report", "language": "agnostic", "scope": "current-checkout", "phase": "verification", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "current-public-oracle-bindings", "value": "recorded", "evaluator": "evidence"},
    {"key": "synthetic-underscore-initialization", "value": "conditional-on-module-absence", "evaluator": "evidence"},
    {"key": "global-underscore-regression", "value": "asserts-unused-import-without-crash", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-public-validation", "value": "passed", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unused-import-diagnostic", "value": "preserved", "evaluator": "evidence"},
    {"key": "no-module-underscore-doctests", "value": "preserved", "evaluator": "evidence"},
    {"key": "current-checkout-content", "value": "unchanged-by-validation", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "reproduction-no-crash",
      "instruction": "Run the adapted public reported reproduction with doctest analysis enabled; require completion without the source-less binding AttributeError.",
      "evidence_refs": ["PyCQA/pyflakes:421:body", "PyCQA/pyflakes:421:fix"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "unused-import-regression",
      "instruction": "Run the added current public regression; require analysis to complete and produce the expected unused-import diagnostic for the module-level underscore alias.",
      "evidence_refs": ["PyCQA/pyflakes:421:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-doctest-behavior",
      "instruction": "Run the current public doctest suite and inspect or probe the no-module-underscore path to confirm synthetic initialization is retained. Report scope and any untested behavior.",
      "evidence_refs": ["PyCQA/pyflakes:421:fix", "PyCQA/pyflakes:421:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:c76d35c9a48e360887b3c443:guard",
    "workflow:verified-history:c76d35c9a48e360887b3c443:regression"
  ],
  "read_set": ["role:doctest-initializer", "role:doctest-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:421:repair:2136e1e9f455"],
  "evidence_refs": ["PyCQA/pyflakes:421:body", "PyCQA/pyflakes:421:fix", "PyCQA/pyflakes:421:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:c76d35c9a48e360887b3c443"
}
```

The `passed` effect is a required acceptance condition, not an observed result. A failed or unbound Oracle does not establish it.
