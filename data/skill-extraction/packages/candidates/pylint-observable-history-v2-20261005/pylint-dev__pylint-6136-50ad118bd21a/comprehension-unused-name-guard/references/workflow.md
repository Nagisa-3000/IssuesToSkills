# Historical realization

The implementation and committed regression expectations support this conditional realization. Probe and validation contracts are authored operational definitions, not claims that those operations ran historically.

```arex-workflow-v4
{
  "id": "workflow:verified-history:d24c4831d73f4eeb9d623f2b",
  "goal": "Remove false unused-variable diagnostics for comprehension target homonyms while preserving adjacent name diagnostics.",
  "mechanism": "Move the existing comprehension-target-name exclusion before unused-argument/local-variable dispatch and retain focused regression expectations.",
  "action_ids": [
    "workflow:verified-history:d24c4831d73f4eeb9d623f2b:probe",
    "workflow:verified-history:d24c4831d73f4eeb9d623f2b:repair",
    "workflow:verified-history:d24c4831d73f4eeb9d623f2b:validate"
  ],
  "source_ids": ["pylint-dev/pylint:6136:repair:50ad118bd21a"],
  "required_effects": [
    {"key": "shared-target-exclusion", "value": true, "evaluator": "evidence"},
    {"key": "homonym-regression-covered", "value": true, "evaluator": "evidence"},
    {"key": "current-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-unused-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-name-errors-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:d24c4831d73f4eeb9d623f2b:probe",
      "after": "workflow:verified-history:d24c4831d73f4eeb9d623f2b:repair",
      "reason": "Establish the public symptom and argument-only guard boundary before editing.",
      "evidence_refs": ["pylint-dev/pylint:6136:body", "pylint-dev/pylint:6136:fix"]
    },
    {
      "before": "workflow:verified-history:d24c4831d73f4eeb9d623f2b:repair",
      "after": "workflow:verified-history:d24c4831d73f4eeb9d623f2b:validate",
      "reason": "Changed dispatch and diagnostic fixtures require fresh observable validation.",
      "evidence_refs": ["pylint-dev/pylint:6136:fix", "pylint-dev/pylint:6136:regression"]
    }
  ]
}
```
