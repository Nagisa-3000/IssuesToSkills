# Canonical historical realization

This contract represents the supplied implementation and committed assertions. Dependencies are authored semantic requirements, not claims that historical commands ran.

```arex-workflow-v4
{
  "id": "workflow:verified-history:ca64407d3ccfea06d7171181",
  "goal": "Correct alias-sensitive postponed-annotation detection while preserving adjacent diagnostic behavior.",
  "mechanism": "Replace local-binding inference with canonical module future-feature membership and retain aliased self/forward annotation assertions.",
  "action_ids": [
    "workflow:verified-history:ca64407d3ccfea06d7171181:probe",
    "workflow:verified-history:ca64407d3ccfea06d7171181:repair",
    "workflow:verified-history:ca64407d3ccfea06d7171181:regression",
    "workflow:verified-history:ca64407d3ccfea06d7171181:validate"
  ],
  "source_ids": ["pylint-dev/pylint:3798:repair:1a1dea5d6bc2"],
  "required_effects": [
    {"key": "alias-independent-feature-detection", "value": true, "evaluator": "evidence"},
    {"key": "alias-regression-defined", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "target-and-controls-passed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "unaliased-feature-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "feature-absent-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-name-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:ca64407d3ccfea06d7171181:probe",
      "after": "workflow:verified-history:ca64407d3ccfea06d7171181:repair",
      "reason": "Locate the detector and establish canonical metadata compatibility before editing.",
      "evidence_refs": ["pylint-dev/pylint:3798:body", "pylint-dev/pylint:3798:fix"]
    },
    {
      "before": "workflow:verified-history:ca64407d3ccfea06d7171181:probe",
      "after": "workflow:verified-history:ca64407d3ccfea06d7171181:regression",
      "reason": "Bind regression assertions to the current diagnostic owner and supported runtime.",
      "evidence_refs": ["pylint-dev/pylint:3798:body", "pylint-dev/pylint:3798:regression"]
    },
    {
      "before": "workflow:verified-history:ca64407d3ccfea06d7171181:repair",
      "after": "workflow:verified-history:ca64407d3ccfea06d7171181:validate",
      "reason": "Observe detector behavior after modification.",
      "evidence_refs": ["pylint-dev/pylint:3798:fix", "pylint-dev/pylint:3798:regression"]
    },
    {
      "before": "workflow:verified-history:ca64407d3ccfea06d7171181:regression",
      "after": "workflow:verified-history:ca64407d3ccfea06d7171181:validate",
      "reason": "Collect and execute the added assertions before claiming coverage or success.",
      "evidence_refs": ["pylint-dev/pylint:3798:regression"]
    }
  ]
}
```
