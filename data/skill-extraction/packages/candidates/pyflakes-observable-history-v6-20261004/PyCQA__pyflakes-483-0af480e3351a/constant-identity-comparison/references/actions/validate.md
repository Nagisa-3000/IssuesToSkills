# Validate public diagnostic boundaries

Bind the current public test command and execute it after the edit. Do not treat the historical regression assertions or later qualification as a current test result.

Required historical regression boundaries:
- `x = 5; if x is (): ...` produces the literal-identity diagnostic.
- `x = 5; if x is (1, '2', True, (1.5, ())): ...` produces that diagnostic.
- `x = 5; if x is (x,): ...` does not produce that diagnostic.

Also check the mechanism's preservation boundaries in current public tests or probes: singleton operands remain exempt unless another operand independently warrants the diagnostic; existing ordinary literal diagnostics remain; `is not`, both operand orientations, and chained comparisons behave consistently; equality and ordering are not newly diagnosed by this identity rule.

```arex-contract-v4
{
  "id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:validate",
  "intent": "Observe corrected constant-tuple diagnostics and preserved adjacent behavior in the current checkout.",
  "mechanism": "Execute public regression assertions and mechanism-derived preservation probes after the modification.",
  "semantic_role": "public-regression-validation",
  "owner_role": "comparison-regressions",
  "operation": "Run the current bound targeted public suite and preservation probes without editing source. Record commands, outcomes, diagnostic observations, and any unsupported runtime coverage.",
  "kind": "validate",
  "inputs": [
    {
      "name": "patched-target",
      "semantic_role": "identity-diagnostic-target",
      "artifact_kind": "source-and-regression-suite",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "validation",
      "state": "patched",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "identity-diagnostic-validation",
      "artifact_kind": "public-test-observation-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:comparison-regressions", "value": true, "evaluator": "file_exists"},
    {"key": "current-public-oracle-bound", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-boundaries-added", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "singleton-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nonconstant-tuple-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-literal-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nonidentity-comparison-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-public-comparison-regressions",
      "instruction": "Execute the bound current public regression command. Confirm diagnostics for empty and recursively constant tuples and no diagnostic for a variable-containing tuple. Check singleton exemptions, ordinary literals, both operand orientations, is not, chained comparisons, and non-identity operators using existing tests or explicit public probes. Record failures and unknown coverage rather than asserting success.",
      "evidence_refs": ["PyCQA/pyflakes:483:regression", "PyCQA/pyflakes:483:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:483:repair:0af480e3351a"],
  "evidence_refs": ["PyCQA/pyflakes:483:regression", "PyCQA/pyflakes:483:fix"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f",
  "read_set": ["role:comparison-classifier", "role:literal-diagnostic", "role:comparison-regressions"],
  "write_set": [],
  "validation_for": ["workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair"]
}
```

A completed run can still fail. Record validation freshness separately from behavioral assurances. Any later source edit makes the validation observation stale and requires another public run. Broader project checks may be appropriate in a current task, but this source does not establish their historical success.
