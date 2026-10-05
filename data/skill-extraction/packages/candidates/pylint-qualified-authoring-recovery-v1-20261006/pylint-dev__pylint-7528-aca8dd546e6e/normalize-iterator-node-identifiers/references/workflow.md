# Historical Workflow

Required effects describe successful completion, not already observed execution of this authored Skill.

```arex-workflow-v4
{
  "id": "workflow:verified-history:bc4129e7b226dfae4c87ca01",
  "goal": "Prevent an iteration-mutation checker crash on an Attribute iterable while retaining existing diagnostics.",
  "mechanism": "Select Attribute.attrname or Name.name, retain inferred-object equality, and cover the copied class-attribute-set case.",
  "action_ids": [
    "workflow:verified-history:bc4129e7b226dfae4c87ca01:inspect",
    "workflow:verified-history:bc4129e7b226dfae4c87ca01:repair",
    "workflow:verified-history:bc4129e7b226dfae4c87ca01:regression",
    "workflow:verified-history:bc4129e7b226dfae4c87ca01:validate"
  ],
  "source_ids": ["pylint-dev/pylint:7528:repair:aca8dd546e6e"],
  "required_effects": [
    {"key": "iterable-identifier-selection", "value": "Attribute.attrname-or-Name.name", "evaluator": "evidence"},
    {"key": "attribute-copy-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": "PASS", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "inference-equality-guard-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-iteration-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "separate-copy-not-diagnosed-as-iterated-set", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:bc4129e7b226dfae4c87ca01:inspect",
      "after": "workflow:verified-history:bc4129e7b226dfae4c87ca01:repair",
      "reason": "Confirm the unsafe iterable field, supported node shapes, and receiver safety before editing.",
      "evidence_refs": ["pylint-dev/pylint:7528:body", "pylint-dev/pylint:7528:fix"]
    },
    {
      "before": "workflow:verified-history:bc4129e7b226dfae4c87ca01:inspect",
      "after": "workflow:verified-history:bc4129e7b226dfae4c87ca01:regression",
      "reason": "Bind the reported case and current fixture conventions before adding coverage.",
      "evidence_refs": ["pylint-dev/pylint:7528:body", "pylint-dev/pylint:7528:regression"]
    },
    {
      "before": "workflow:verified-history:bc4129e7b226dfae4c87ca01:repair",
      "after": "workflow:verified-history:bc4129e7b226dfae4c87ca01:validate",
      "reason": "The condition edit requires fresh public behavior and preservation checks.",
      "evidence_refs": ["pylint-dev/pylint:7528:fix", "pylint-dev/pylint:7528:regression"]
    },
    {
      "before": "workflow:verified-history:bc4129e7b226dfae4c87ca01:regression",
      "after": "workflow:verified-history:bc4129e7b226dfae4c87ca01:validate",
      "reason": "Final validation includes the added reproduction and retained expectations.",
      "evidence_refs": ["pylint-dev/pylint:7528:regression"]
    }
  ]
}
```

There is no required order between the two edits. An isolated current baseline probe may precede either; final validation follows both retained modifications.
