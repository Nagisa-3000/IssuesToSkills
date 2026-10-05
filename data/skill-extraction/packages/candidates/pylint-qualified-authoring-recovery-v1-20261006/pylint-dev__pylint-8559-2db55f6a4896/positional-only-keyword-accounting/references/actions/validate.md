# Validate the diagnostic and legal controls

Use the current public harness to check diagnostic contents, not simply analyzer exit status. An analyzer may return nonzero for expected diagnostics; the assertion harness determines success.

Historical regression matrix:

```python
def name1(param1, /, **kwargs): ...
def name2(param1, /, param2, **kwargs): ...
def name3(param1=True, /, **kwargs): ...
def name4(param1, **kwargs): ...

name1(param1=43)        # no-value-for-parameter
name1(43)              # legal control
name2(1, param2=False)  # legal control
name3()                # legal control
name4(param1=43)        # legal control
```

Inspect or publicly test the unchanged no-collector path using current expectations, and run relevant public neighboring argument checks. Those additional checks are current guidance, not claimed historical execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:33b6359d2826e0cbb3dcbe89:validate",
  "intent": "Observe the target diagnostic and preservation of adjacent behavior.",
  "mechanism": "Execute the public regression matrix and review or test neighboring accounting after the edit.",
  "semantic_role": "public-repair-validation",
  "owner_role": "argument-regression-harness",
  "operation": "Run current bound public oracles and record fresh diagnostic and test observations without source edits.",
  "kind": "validate",
  "inputs": [
    {
      "name": "modified-accounting",
      "semantic_role": "call-accounting-repair-context",
      "artifact_kind": "code-and-test-bindings",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "public-call-accounting-validation",
      "artifact_kind": "oracle-observations",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "regression-matrix-authored", "value": true, "evaluator": "evidence"},
    {"key": "current-test-harness-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {
      "key": "public-validation-observed",
      "value": true,
      "evaluator": "evidence",
      "description": "Established only by fresh passing public observations; unavailable or failing checks do not establish it."
    }
  ],
  "preserves": [
    {"key": "adjacent-binding-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "required-and-adjacent-calls",
      "instruction": "Run the bound public regression harness. Require the missing-required-positional-only diagnostic for same-name keyword-only supply and no missing-argument diagnostics for the four legal controls.",
      "evidence_refs": ["pylint-dev/pylint:8559:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "preserve-neighboring-accounting",
      "instruction": "Run current public neighboring argument checks and inspect the no-collector rejection branch for unintended changes. Record evidence and stop on diagnostic regressions.",
      "evidence_refs": ["pylint-dev/pylint:8559:fix", "pylint-dev/pylint:8559:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:33b6359d2826e0cbb3dcbe89:repair"],
  "read_set": ["role:call-argument-accounting", "role:argument-regression-harness"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:8559:repair:2db55f6a4896"],
  "evidence_refs": ["pylint-dev/pylint:8559:fix", "pylint-dev/pylint:8559:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:33b6359d2826e0cbb3dcbe89"
}
```

Bind and render current public commands before execution. Record FAIL or UNKNOWN honestly. Further modifications invalidate validation freshness, not the requirement to preserve adjacent behavior.
