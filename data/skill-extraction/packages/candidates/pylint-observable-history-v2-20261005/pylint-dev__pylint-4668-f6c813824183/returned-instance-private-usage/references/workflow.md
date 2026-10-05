# Historical Workflow

The source supports the diagnosis, narrow implementation change, and committed regression assertions. Validation is an explicit repair obligation grounded in those assertions; historical execution is unknown.

```arex-workflow-v4
{
  "id": "workflow:verified-history:c87ac9d043b1a02e14aba0d2",
  "goal": "Recognize private attributes initialized on named locals returned by __new__ and consumed through self.",
  "mechanism": "Collect guarded Name-valued returns for assignments scoped to __new__ and use those names in the existing private-member receiver matcher.",
  "action_ids": [
    "workflow:verified-history:c87ac9d043b1a02e14aba0d2:locate",
    "workflow:verified-history:c87ac9d043b1a02e14aba0d2:repair",
    "workflow:verified-history:c87ac9d043b1a02e14aba0d2:regressions",
    "workflow:verified-history:c87ac9d043b1a02e14aba0d2:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4668:repair:f6c813824183"],
  "required_effects": [
    {"key": "returned-local-consumption-recognized", "value": true, "evaluator": "evidence"},
    {"key": "constructor-return-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-private-member-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "non-name-return-safety-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:locate",
      "after": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:repair",
      "reason": "Confirm assignment scope and receiver mismatch before editing the matcher.",
      "evidence_refs": ["pylint-dev/pylint:4668:body", "pylint-dev/pylint:4668:fix"]
    },
    {
      "before": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:locate",
      "after": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:regressions",
      "reason": "Confirm the public symptom and fixture owner before adding assertions.",
      "evidence_refs": ["pylint-dev/pylint:4668:body", "pylint-dev/pylint:4668:regression"]
    },
    {
      "before": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:repair",
      "after": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:validate",
      "reason": "Validate the changed receiver rules after implementation edits.",
      "evidence_refs": ["pylint-dev/pylint:4668:fix", "pylint-dev/pylint:4668:regression"]
    },
    {
      "before": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:regressions",
      "after": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:validate",
      "reason": "Execute the final regression assertions and adjacent cases after fixture edits.",
      "evidence_refs": ["pylint-dev/pylint:4668:regression"]
    }
  ]
}
```

Repair and regression edits need not be ordered relative to each other. Both require diagnosis and both precede final validation. Dependencies express semantic prerequisites, not an asserted historical execution sequence.
