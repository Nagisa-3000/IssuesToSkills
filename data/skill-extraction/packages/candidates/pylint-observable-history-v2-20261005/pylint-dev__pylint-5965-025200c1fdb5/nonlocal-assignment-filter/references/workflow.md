# Historical realization: nonlocal-aware exception assignment filtering

The repair and paired assertions establish the dependency structure below. Inspection and validation are source-grounded operation contracts, not claims that these authored operations ran historically.

```arex-workflow-v4
{
  "id": "workflow:verified-history:88758c6085df4be35e45f76d",
  "goal": "Avoid a false used-before-assignment diagnostic for an explicitly declared nonlocal read in a try block while retaining genuine local diagnostics.",
  "mechanism": "Return the previously resolved candidates before exception-handler assignment filtering only when the queried name occurs in a Nonlocal declaration in its own frame.",
  "action_ids": [
    "workflow:verified-history:88758c6085df4be35e45f76d:inspect",
    "workflow:verified-history:88758c6085df4be35e45f76d:repair",
    "workflow:verified-history:88758c6085df4be35e45f76d:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5965:repair:025200c1fdb5"],
  "required_effects": [
    {"key": "name-specific-nonlocal-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "paired-regression-assertions-installed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "unrelated-nonlocal-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-control-flow-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:88758c6085df4be35e45f76d:inspect",
      "after": "workflow:verified-history:88758c6085df4be35e45f76d:repair",
      "reason": "A current name-specific frame declaration and the filtering boundary must be established before adding the exemption.",
      "evidence_refs": ["pylint-dev/pylint:5965:body", "pylint-dev/pylint:5965:fix"]
    },
    {
      "before": "workflow:verified-history:88758c6085df4be35e45f76d:repair",
      "after": "workflow:verified-history:88758c6085df4be35e45f76d:validate",
      "reason": "The changed filter and paired expectations require fresh public checks, including the unrelated-nonlocal negative control.",
      "evidence_refs": ["pylint-dev/pylint:5965:fix", "pylint-dev/pylint:5965:regression"]
    }
  ]
}
```
