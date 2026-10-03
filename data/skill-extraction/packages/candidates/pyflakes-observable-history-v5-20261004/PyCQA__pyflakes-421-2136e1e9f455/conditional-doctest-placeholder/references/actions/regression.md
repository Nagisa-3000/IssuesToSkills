# Add the global-underscore regression

At the current doctest test owner, add a public regression equivalent to the historical assertion: import a name as `_`, define a function with a `>>> pass` doctest, analyze it with doctest checking enabled, and require the ordinary unused-import diagnostic without an exception.

The historical test imported `ugettext` from `gettext`; it was analyzer input, not evidence that the import was executed at runtime. Adapt the test harness to the current public suite without changing the relevant binding and diagnostic semantics.

```arex-contract-v4
{
  "id": "workflow:verified-history:c76d35c9a48e360887b3c443:regression",
  "intent": "Make the global-underscore collision and preserved diagnostic observable.",
  "mechanism": "Add an analyzer regression with a module import aliased to underscore and a pass-only function doctest.",
  "semantic_role": "collision-regression-addition",
  "owner_role": "doctest-regression-tests",
  "operation": "Add a public test asserting analysis completes and reports the aliased import as unused.",
  "kind": "edit",
  "inputs": [
    {"name": "tests", "semantic_role": "doctest-regression-tests", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "baseline-reviewed", "optional": false}
  ],
  "outputs": [
    {"name": "tests", "semantic_role": "doctest-regression-tests", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "collision-regression-added", "optional": false}
  ],
  "preconditions": [
    {"key": "role:doctest-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "doctest-test-harness", "value": "confirmed-enabled", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "global-underscore-regression", "value": "asserts-unused-import-without-crash", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-doctest-test-assertions", "value": "retained", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "regression-review",
      "instruction": "Inspect the added public test for a module-level import alias underscore, a function containing a pass-only doctest, enabled doctest analysis, and an explicit unused-import assertion.",
      "evidence_refs": ["PyCQA/pyflakes:421:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:doctest-regression-tests"],
  "write_set": ["role:doctest-regression-tests"],
  "invalidates": ["doctest-suite-result", "regression-tests-code-anchor"],
  "source_ids": ["PyCQA/pyflakes:421:repair:2136e1e9f455"],
  "evidence_refs": ["PyCQA/pyflakes:421:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:c76d35c9a48e360887b3c443"
}
```

Adding the assertion is not evidence that it passes. [Validate](validate.md) remains mandatory.
