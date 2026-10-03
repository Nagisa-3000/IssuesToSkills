# Add the public regression

At the bound undefined-name harness, assert that a bare module-level `__annotations__` reference produces no undefined-name warning on Python 3.6 and later. Guard the test below Python 3.6 using the current public harness convention.

Do not narrow the assertion to modules containing an annotation: the historical added test used the bare reference. The annotated original reproduction remains an additional validation check. Preserve existing tests and older-interpreter test compatibility.

```arex-contract-v4
{
  "id": "workflow:verified-history:4817630500584ee0981edde8:regression",
  "intent": "Protect the module-level allowance with a focused version-gated regression.",
  "mechanism": "Add a bare-reference no-warning assertion guarded below Python 3.6.",
  "semantic_role": "implicit-name-regression",
  "owner_role": "undefined-name-regressions",
  "operation": "add-version-gated-regression",
  "kind": "edit",
  "inputs": [
    {
      "name": "owner-context",
      "semantic_role": "implicit-name-repair-context",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "module-name-checking",
      "phase": "pre-edit",
      "state": "owners-and-semantics-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "regression-edit",
      "semantic_role": "implicit-name-regression-change",
      "artifact_kind": "test-change",
      "language": "python",
      "scope": "module-name-checking",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:undefined-name-regressions", "value": true, "evaluator": "file_exists"},
    {"key": "repair-owners", "value": "located", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "module-annotations-regression", "value": "present", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-undefined-name-tests", "value": "preserved", "evaluator": "evidence"},
    {"key": "older-interpreter-test-compatibility", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression-assertion",
      "instruction": "Review the current test diff: the checker receives a bare module-level __annotations__ reference, expects no undefined-name warning on Python 3.6-plus, and skips below 3.6 without weakening existing assertions.",
      "evidence_refs": ["PyCQA/pyflakes:395:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:395:repair:066ba4a93c10"],
  "evidence_refs": ["PyCQA/pyflakes:395:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:4817630500584ee0981edde8",
  "read_set": ["role:undefined-name-regressions", "role:interpreter-version-policy"],
  "write_set": ["role:undefined-name-regressions"],
  "invalidates": ["public-validation"]
}
```
