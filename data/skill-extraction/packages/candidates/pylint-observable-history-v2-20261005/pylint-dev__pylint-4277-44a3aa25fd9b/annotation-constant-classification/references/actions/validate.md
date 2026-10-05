# Validate differential and adjacent behavior

Bind checks to the current public suite and supported runtime. Exercise ClassVar/Final, default/configured styles, annotation-only declarations, Enum, and surrounding naming controls.

Empty source command arrays are unbound placeholders. Render concrete current Oracle bindings before execution. Historical replay commands are not authorization.

```arex-contract-v4
{
  "id": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:validate",
  "intent": "Verify differential annotation naming and preserved adjacent behavior.",
  "mechanism": "Run public ClassVar-versus-Final assertions under default and snake_case constant styles, with Enum and surrounding naming controls.",
  "semantic_role": "annotation-naming-verification",
  "owner_role": "naming-regression-suite",
  "operation": "Render and execute current public checks; record commands, revision anchors, diagnostics, exit status, skips, and tri-state results. Assert passing effects only after all required checks pass.",
  "kind": "validate",
  "inputs": [
    {"name": "candidate-naming-repair", "semantic_role": "annotation-naming-candidate", "artifact_kind": "checkout-revision", "language": "Python", "scope": "current-public-checkout", "phase": "post-edit", "state": "unvalidated"}
  ],
  "outputs": [
    {"name": "public-naming-validation", "semantic_role": "annotation-naming-validation", "artifact_kind": "test-observation-record", "language": "Python", "scope": "current-public-checkout", "phase": "post-validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "annotation-constant-policy", "value": "Final-not-ClassVar", "evaluator": "evidence"},
    {"key": "differential-naming-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "role:naming-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "public-naming-checks-passed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "enum-naming-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "configured-constant-style-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-naming-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-differential-naming",
      "instruction": "Run public assertions for bare, qualified, and subscripted ClassVar and Final with initialized and annotation-only declarations. ClassVar alone must not select constant naming. Default uppercase constant style must diagnose lowercase Final names and accept uppercase Final names. Configured snake_case constant style must diagnose uppercase Final names and accept lowercase Final names.",
      "evidence_refs": ["pylint-dev/pylint:4277:body", "pylint-dev/pylint:4277:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "verify-adjacent-naming",
      "instruction": "Run public Enum and surrounding naming controls. Confirm the existing bad Enum-name diagnostic and configured naming behavior remain intact. Investigate unexplained diagnostic changes rather than treating regenerated expectations as proof.",
      "evidence_refs": ["pylint-dev/pylint:4277:fix", "pylint-dev/pylint:4277:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:repair"],
  "read_set": ["role:class-attribute-naming-classifier", "role:annotated-assignment-recognizer", "role:naming-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4277:repair:44a3aa25fd9b"],
  "evidence_refs": ["pylint-dev/pylint:4277:fix", "pylint-dev/pylint:4277:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0"
}
```

Effects describe successful completion. A record containing FAIL or UNKNOWN does not establish `public-naming-checks-passed`. Unexpected/missing diagnostics, unsupported runtime, or skipped essential cases prevent success. Later source or assertion edits require fresh validation.
