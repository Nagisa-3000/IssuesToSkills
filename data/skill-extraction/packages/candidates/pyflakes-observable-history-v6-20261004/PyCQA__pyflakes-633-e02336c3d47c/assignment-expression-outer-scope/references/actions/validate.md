# Validate target and adjacent scope behavior

Bind and render public commands for the current checkout before running them. Execute both target cases on a Python runtime supporting assignment expressions. A pre-3.8 skip is not evidence of corrected behavior.

Check ordinary assignment ownership and comprehension iteration-variable isolation using current public tests or explicit public probes. Review the final diff for preserved annotation and insertion bookkeeping. These adjacent checks are current preservation obligations, not claims of supplied historical execution.

Record results, failures, skips, runtime version, and validation scope. Do not infer whole-project safety from changed-file checks.

```arex-contract-v4
{
  "id": "workflow:verified-history:fd9457af9cbbabf21f89fac4:validate",
  "intent": "Observe corrected enclosing-target diagnostics and preserved adjacent binding behavior.",
  "mechanism": "Execute current public single and nested target assertions and adjacent scope checks after the edit.",
  "semantic_role": "scope-routing-validation",
  "owner_role": "scope-regression-tests",
  "operation": "Run current-bound public checks without editing source; record actual commands and outcomes, and review the final diff for retained binding bookkeeping.",
  "kind": "validate",
  "inputs": [
    {
      "name": "patched-routing",
      "semantic_role": "assignment-expression-routing-state",
      "artifact_kind": "source-and-probe-record",
      "language": "python",
      "scope": "analyzer-binding-and-regressions",
      "phase": "post-repair",
      "state": "awaiting-validation"
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "assignment-expression-validation",
      "artifact_kind": "public-test-results",
      "language": "python",
      "scope": "analyzer-binding-and-regressions",
      "phase": "post-repair",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "single-and-nested-regressions-added", "value": true, "evaluator": "evidence"},
    {"key": "public-oracle-bindings-recorded", "value": true, "evaluator": "evidence"},
    {"key": "assignment-expression-syntax-supported", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-assignment-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "iteration-variable-isolation-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-binding-bookkeeping-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "single-and-nested-target-checks",
      "instruction": "Execute public assertions equivalent to the historical single-generator y case and nested y/z case on a syntax-capable runtime. Require no unexpected diagnostics on enclosing uses. Record actual execution; skipped or unexecuted assertions are insufficient.",
      "evidence_refs": ["PyCQA/pyflakes:633:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-scope-checks",
      "instruction": "Run current public ordinary-assignment and comprehension iteration-variable scope checks. Confirm ordinary bindings retain their established owners and iteration variables do not leak. Review annotation guards and unrelated insertion bookkeeping. Report only the actual validation scope.",
      "evidence_refs": ["PyCQA/pyflakes:633:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:633:repair:e02336c3d47c"],
  "evidence_refs": ["PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:fd9457af9cbbabf21f89fac4",
  "read_set": [
    "role:assignment-binding-router",
    "role:scope-regression-tests"
  ],
  "write_set": [],
  "validation_for": ["workflow:verified-history:fd9457af9cbbabf21f89fac4:repair"]
}
```
