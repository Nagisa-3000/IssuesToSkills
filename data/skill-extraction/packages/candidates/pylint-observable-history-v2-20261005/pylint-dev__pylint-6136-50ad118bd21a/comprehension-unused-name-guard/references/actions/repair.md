# Broaden the existing exclusion

At the bound unused-name dispatch owner, move the existing target-membership early return before argument/local classification. Remove redundant argument-only nesting while retaining ordinary argument-check invocation. Do not alter target collection, global handling, or unrelated diagnostic branches.

At the bound fixture owner, add or maintain these analyzer regression shapes:

```python
def container_case():
    x = []
    assert [True for x in x]

def annotation_case():
    my_int: int
    _ = [print(sep=my_int, end=my_int) for my_int in range(10)]
```

Preserve the homonym. Remove only the affected unused-variable expectation. Retain neighboring undefined-name and used-before-assignment expectations.

These are analyzer inputs, not application programs to execute. The empty-list assertion is not expected to pass at runtime. The annotation case encodes historical checker behavior, not a general Python scoping rule or proof that the outer annotation is read.

Effects are intended until observed by validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:d24c4831d73f4eeb9d623f2b:repair",
  "intent": "Extend the existing target-name exclusion to both unused-name branches and maintain regression coverage.",
  "mechanism": "Place target-name membership return before argument/local dispatch instead of globally suppressing diagnostics.",
  "semantic_role": "shared-exclusion-repair",
  "owner_role": "unused-name-dispatch",
  "operation": "Edit the bound dispatch and diagnostic fixture owners; broaden the existing guard and maintain the container-homonym and annotation-comprehension expectations.",
  "kind": "edit",
  "inputs": [
    {"name": "confirmed-context", "semantic_role": "confirmed-unused-name-mechanism", "artifact_kind": "evidence-record", "language": "python", "scope": "current-checkout", "phase": "pre-edit", "state": "confirmed"}
  ],
  "outputs": [
    {"name": "candidate-change", "semantic_role": "unused-name-repair-candidate", "artifact_kind": "checkout-diff", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "unvalidated"}
  ],
  "preconditions": [
    {"key": "dispatch-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:unused-name-dispatch", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:diagnostic-fixtures", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "shared-target-exclusion", "value": true, "evaluator": "evidence"},
    {"key": "homonym-regression-covered", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-unused-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-name-errors-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["current-validation-observed"],
  "oracle": [
    {
      "id": "inspect-candidate",
      "instruction": "Inspect the current diff for target exclusion before both branches, unchanged checking of non-target arguments, both regression shapes with retained homonyms, and unchanged neighboring name-error expectations.",
      "evidence_refs": ["pylint-dev/pylint:6136:fix", "pylint-dev/pylint:6136:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:unused-name-dispatch", "role:comprehension-target-collection", "role:diagnostic-fixtures"],
  "write_set": ["role:unused-name-dispatch", "role:diagnostic-fixtures"],
  "source_ids": ["pylint-dev/pylint:6136:repair:50ad118bd21a"],
  "evidence_refs": ["pylint-dev/pylint:6136:fix", "pylint-dev/pylint:6136:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:d24c4831d73f4eeb9d623f2b"
}
```
