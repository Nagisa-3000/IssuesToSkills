# Historical realization: directional private-member matching

This decomposition describes the supplied repair and its public verification obligations. It does not claim that these exact authored Actions or commands were historically executed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:8486fdf9c04144c10d14213f",
  "goal": "Remove the false unused-private-member diagnostic for a cls write read through self while retaining the inverse-direction warning boundary.",
  "mechanism": "Require equal private attribute names and directional receiver compatibility: cls writes accept cls/self reads; self writes accept self reads only.",
  "action_ids": [
    "workflow:verified-history:8486fdf9c04144c10d14213f:inspect",
    "workflow:verified-history:8486fdf9c04144c10d14213f:edit-matcher",
    "workflow:verified-history:8486fdf9c04144c10d14213f:edit-regressions",
    "workflow:verified-history:8486fdf9c04144c10d14213f:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4657:repair:c02682670e0d"],
  "required_effects": [
    {"key": "directional-matcher-installed", "value": true, "evaluator": "evidence"},
    {"key": "directional-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "attribute-name-equality-required", "value": true, "evaluator": "evidence"},
    {"key": "instance-write-not-used-by-class-read", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-private-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:8486fdf9c04144c10d14213f:inspect",
      "after": "workflow:verified-history:8486fdf9c04144c10d14213f:edit-matcher",
      "reason": "Confirm receiver-name equality as the cause and bind the current matcher before editing.",
      "evidence_refs": ["pylint-dev/pylint:4657:body", "pylint-dev/pylint:4657:fix"]
    },
    {
      "before": "workflow:verified-history:8486fdf9c04144c10d14213f:inspect",
      "after": "workflow:verified-history:8486fdf9c04144c10d14213f:edit-regressions",
      "reason": "Locate the public fixture owner and establish the diagnostic boundary.",
      "evidence_refs": ["pylint-dev/pylint:4657:regression"]
    },
    {
      "before": "workflow:verified-history:8486fdf9c04144c10d14213f:edit-matcher",
      "after": "workflow:verified-history:8486fdf9c04144c10d14213f:validate",
      "reason": "Public validation must observe the modified matcher.",
      "evidence_refs": ["pylint-dev/pylint:4657:fix", "pylint-dev/pylint:4657:regression"]
    },
    {
      "before": "workflow:verified-history:8486fdf9c04144c10d14213f:edit-regressions",
      "after": "workflow:verified-history:8486fdf9c04144c10d14213f:validate",
      "reason": "Public validation must exercise the positive and negative assertions.",
      "evidence_refs": ["pylint-dev/pylint:4657:regression"]
    }
  ]
}
```
