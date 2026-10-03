# Canonical Workflow

Separate singleton exemption from constant recognition; classify tuple elements recursively; integrate the resulting predicate into pairwise identity comparison checking; update the message and public assertions; validate the target and adjacent behavior.

Inspection is an authored current applicability gate derived from the report and implementation, not a historical command execution. Validation reflects historical assertion content and required current observations, not a historical execution log.

```arex-workflow-v4
{
  "id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f",
  "goal": "Diagnose identity comparisons against non-singleton constant literals, including recursively constant tuples.",
  "mechanism": "Version-aware singleton exclusion and recursive tuple classification applied to either operand of each identity-comparison pair.",
  "action_ids": [
    "workflow:verified-history:e84da27a5b8d26a58fc90e6f:inspect",
    "workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair",
    "workflow:verified-history:e84da27a5b8d26a58fc90e6f:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:483:repair:0af480e3351a"],
  "required_effects": [
    {"key": "constant-tuple-identity-diagnostic", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "singleton-identity-exemption", "value": true, "evaluator": "evidence"},
    {"key": "variable-tuple-not-constant", "value": true, "evaluator": "evidence"},
    {"key": "scalar-literal-diagnostics", "value": true, "evaluator": "evidence"},
    {"key": "pairwise-chain-traversal", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:inspect",
      "after": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair",
      "reason": "Current owner bindings, AST representations, policy, and classification gap must be established before adapting the mechanism.",
      "evidence_refs": ["PyCQA/pyflakes:483:body", "PyCQA/pyflakes:483:fix"]
    },
    {
      "before": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair",
      "after": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:validate",
      "reason": "Regression assertions exercise the modified classifier and comparison diagnostic after editing.",
      "evidence_refs": ["PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"]
    }
  ]
}
```
