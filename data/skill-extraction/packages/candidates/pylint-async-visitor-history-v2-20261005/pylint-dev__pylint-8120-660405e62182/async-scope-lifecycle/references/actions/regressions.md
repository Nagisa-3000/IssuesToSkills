# Add independent async scope assertions

Use the bound public fixture's established expectation syntax. Add separate async functions and separate async methods reusing a local name with differing inferred types. Assert no cross-scope warning, retaining legitimate within-scope diagnostic expectations.

Do not regenerate expected output to accept the false positive. Where practical, use an isolated regression-only base to verify that the assertions expose the missing hooks. This is a current validation procedure, not a historical execution claim.

```arex-contract-v4
{
  "id": "workflow:verified-history:9a2315892fecfccf9d5c6c14:regressions",
  "intent": "Make independent async scope isolation observable in public tests.",
  "mechanism": "Reuse local names with different types in separate async functions and methods.",
  "semantic_role": "assert-async-isolation",
  "owner_role": "checker-regression-suite",
  "operation": "Add no-warning cases for independent async functions and methods while retaining existing positive diagnostic assertions.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "scope-mechanism-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "role:checker-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "async-isolation-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-lifecycle-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "within-scope-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-regression-coverage",
      "instruction": "Inspect the fixture for independent async function and method pairs, differing types under reused local names, no accepted cross-scope warning, and retained positive within-scope expectations.",
      "kind": "public_probe",
      "evidence_refs": ["pylint-dev/pylint:8120:regression"]
    }
  ],
  "read_set": ["role:checker-regression-suite"],
  "write_set": ["role:checker-regression-suite"],
  "source_ids": ["pylint-dev/pylint:8120:repair:660405e62182"],
  "evidence_refs": ["pylint-dev/pylint:8120:regression"],
  "resource": "references/actions/regressions.md",
  "package_id": "workflow:verified-history:9a2315892fecfccf9d5c6c14"
}
```
