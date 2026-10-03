# Historical workflow: extend identity diagnostics to constant tuples

The historical repair combined recursive constant classification, singleton exclusions, comparison traversal, message wording, and regression assertions. The inspection Action describes the evidence-backed checks needed to adapt that repair; it does not claim a separately observed historical inspection session. Likewise, the validation Action operationalizes supplied assertions without inventing a historical test run.

```arex-workflow-v4
{
  "id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f",
  "goal": "Diagnose identity comparisons involving non-singleton constants, including recursively constant tuples, without diagnosing singleton-only or nonconstant-tuple cases.",
  "mechanism": "Separate singleton classification from recursive constant classification and apply the non-singleton constant predicate to either operand of every identity comparison pair.",
  "action_ids": [
    "workflow:verified-history:e84da27a5b8d26a58fc90e6f:inspect",
    "workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair",
    "workflow:verified-history:e84da27a5b8d26a58fc90e6f:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:483:repair:0af480e3351a"],
  "required_effects": [
    {"key": "constant-tuple-identity-diagnosed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "singleton-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nonconstant-tuple-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-literal-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nonidentity-comparison-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:inspect",
      "after": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair",
      "reason": "Version-dependent singleton and constant AST representations and comparison owners must be established before applying the mechanism.",
      "evidence_refs": ["PyCQA/pyflakes:483:fix"]
    },
    {
      "before": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair",
      "after": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:validate",
      "reason": "Edited classification and diagnostic behavior must be checked against the constant-tuple and nonconstant-tuple regression boundaries.",
      "evidence_refs": ["PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"]
    }
  ]
}
```

The Action cards are [inspect](actions/inspect.md), [repair](actions/repair.md), and [validate](actions/validate.md). Current ordering follows their ports, semantic prerequisites, and verification dependencies. Already satisfied inspection may be omitted from a current plan only when fresh public observations supply its required outputs. Any retained modifying Action must retain its validation.
