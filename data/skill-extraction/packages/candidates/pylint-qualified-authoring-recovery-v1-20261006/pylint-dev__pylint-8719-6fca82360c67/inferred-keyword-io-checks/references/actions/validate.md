# Validate diagnostics and confidence

Bind current public commands. Execute targeted regressions and applicable adjacent direct-argument tests without editing implementation or assertions. Do not blindly regenerate snapshots.

Evidence-grounded expected observations:
- Dictionary `mode="rb"`: no unspecified-encoding warning.
- Dictionary `mode="w", encoding="utf-8"`: no encoding warning for supported builtin, IO-module, and path-open calls.
- Dictionary `mode=5`: invalid-mode warning with inference confidence; absent-encoding warning with high confidence.
- Dictionary `mode="wt", encoding=None`: encoding warning with inference confidence.
- Path text reader/writer dictionary encoding: `None` warns, `"utf-8"` does not.
- Direct invalid-mode and missing/None-encoding cases retain diagnostics, with high confidence as specified by the repair.

These are assertions to check, not observed Skill outcomes.

```arex-contract-v4
{
  "id": "workflow:verified-history:0a9b8ce52750bdf712058d20:validate",
  "package_id": "workflow:verified-history:0a9b8ce52750bdf712058d20",
  "resource": "references/actions/validate.md",
  "kind": "validate",
  "intent": "Observe repaired diagnostics and preserved adjacent behavior.",
  "mechanism": "Execute public regressions and compare message presence, locations, and confidence.",
  "semantic_role": "io-diagnostic-validation",
  "owner_role": "io-functional-tests",
  "operation": "Run bound public checks and record fresh actual results without modifying source or expected assertions.",
  "inputs": [
    {"name": "candidate", "semantic_role": "io-keyword-repair-candidate", "artifact_kind": "checkout-change", "language": "python", "scope": "current-public-checkout", "phase": "post-edit", "state": "unvalidated"}
  ],
  "outputs": [
    {"name": "validation", "semantic_role": "io-keyword-validation-results", "artifact_kind": "test-observations", "language": "python", "scope": "current-public-checkout", "phase": "post-validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "dictionary-keyword-fallback-integrated", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-assertions-added", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-argument-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "binary-and-none-encoding-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "validation_for": ["workflow:verified-history:0a9b8ce52750bdf712058d20:repair"],
  "read_set": ["role:python-call-analysis", "role:io-diagnostic-checker", "role:io-functional-tests"],
  "write_set": [],
  "oracle": [
    {
      "id": "io-regression-matrix",
      "instruction": "Execute current public dictionary mode/encoding fixtures across supported IO APIs and adjacent direct-argument cases. Compare actual messages, locations and confidence with reviewed assertions. Record exit status, failures and skips; unexpected results prevent acceptance.",
      "kind": "repository_test",
      "command": [],
      "evidence_refs": ["pylint-dev/pylint:8719:regression"]
    }
  ],
  "source_ids": ["pylint-dev/pylint:8719:repair:6fca82360c67"],
  "evidence_refs": ["pylint-dev/pylint:8719:fix", "pylint-dev/pylint:8719:regression"]
}
```
