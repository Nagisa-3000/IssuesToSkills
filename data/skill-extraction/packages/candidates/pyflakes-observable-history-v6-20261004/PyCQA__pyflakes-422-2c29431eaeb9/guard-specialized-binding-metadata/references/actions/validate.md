# Validate the repair

Bind the oracles below to current public commands after locating the current test harness. Empty command arrays are intentionally unbound, not executable commands.

Run the ordinary-decorator reproduction and the relevant existing annotation/decorator tests. Include current public checks for supported import-backed overload recognition. Compare diagnostics, not merely process exit status. Inspect the diff to ensure the patch remains narrow.

The original commit supplies assertions rather than historical execution results. The contemporary changed-test qualification is not a whole-project guarantee.

```arex-contract-v4
{
  "id": "workflow:verified-history:314f3449f8ccd1beab92c625:validate",
  "intent": "Observe that the edited implementation and regression preserve the intended decorator diagnostics.",
  "mechanism": "Execute the focused public regression and adjacent public tests after both edits.",
  "semantic_role": "repair-validation",
  "owner_role": "decorator-regression-tests",
  "operation": "Run bound public current tests and record outcomes; do not modify source or assertions during validation.",
  "kind": "validate",
  "inputs": [
    {"name": "regression-ready-state", "semantic_role": "overload-detection-repair", "artifact_kind": "code_bundle", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "regression-ready", "optional": false}
  ],
  "outputs": [
    {"name": "validated-repair-state", "semantic_role": "overload-detection-repair", "artifact_kind": "code_bundle", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "validated", "optional": false}
  ],
  "preconditions": [
    {"key": "import-metadata-access-type-guarded", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-decorator-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-import-overload-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "ordinary-decorator-reproduction",
      "instruction": "Execute the current public regression and confirm exactly two ordinary unused-redefinition diagnostics without a metadata-access exception.",
      "evidence_refs": ["PyCQA/pyflakes:422:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-decorator-tests",
      "instruction": "Execute relevant existing public annotation/decorator tests, including supported import-backed overload forms; require unchanged expected behavior. Record the tested scope and any untested project-wide behavior.",
      "evidence_refs": ["PyCQA/pyflakes:422:fix", "PyCQA/pyflakes:422:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:314f3449f8ccd1beab92c625:guard",
    "workflow:verified-history:314f3449f8ccd1beab92c625:regression"
  ],
  "read_set": ["role:special-decorator-recognizer", "role:decorator-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:422:repair:2c29431eaeb9"],
  "evidence_refs": ["PyCQA/pyflakes:422:fix", "PyCQA/pyflakes:422:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:314f3449f8ccd1beab92c625"
}
```
