# Historical realization

The following contracts are authored reusable operations grounded in the supplied repair and assertions. Their ordering expresses semantic prerequisites, not a claim that these authored operations historically ran.

```arex-workflow-v4
{
  "id": "workflow:verified-history:00bdb5de0892c0cbbab00de9",
  "goal": "Recognize described NumPy parameters without inline types while retaining legitimate missing-type diagnostics.",
  "mechanism": "Accept newline-delimited parameter headers and collect documentation independently of docstring type declarations.",
  "action_ids": [
    "workflow:verified-history:00bdb5de0892c0cbbab00de9:inspect",
    "workflow:verified-history:00bdb5de0892c0cbbab00de9:repair",
    "workflow:verified-history:00bdb5de0892c0cbbab00de9:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5222:repair:1d3a7ff32b0f"],
  "required_effects": [
    {"key": "description-only-recognition", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "legitimate-type-diagnostics", "value": "preserved", "evaluator": "evidence"},
    {"key": "adjacent-docstring-behavior", "value": "preserved", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:00bdb5de0892c0cbbab00de9:inspect",
      "after": "workflow:verified-history:00bdb5de0892c0cbbab00de9:repair",
      "reason": "Current ownership and the entry-rejection mechanism must be established before editing.",
      "evidence_refs": ["pylint-dev/pylint:5222:body", "pylint-dev/pylint:5222:fix"]
    },
    {
      "before": "workflow:verified-history:00bdb5de0892c0cbbab00de9:repair",
      "after": "workflow:verified-history:00bdb5de0892c0cbbab00de9:validate",
      "reason": "Production and regression edits require exact-diagnostic and adjacent-behavior validation.",
      "evidence_refs": ["pylint-dev/pylint:5222:fix", "pylint-dev/pylint:5222:regression"]
    }
  ]
}
```
