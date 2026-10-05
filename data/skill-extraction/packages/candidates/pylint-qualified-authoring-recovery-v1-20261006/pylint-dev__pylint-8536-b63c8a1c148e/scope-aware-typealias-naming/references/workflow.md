# Historical realization

The supplied implementation and committed regression support this single realization. Probe and validation contracts specify public checks without inventing historical execution.

```arex-workflow-v4
{
  "id": "workflow:verified-history:b980c9ec644c821d41e50e10",
  "goal": "Apply existing alias naming policy to explicit function-local aliases while retaining ordinary-variable behavior.",
  "mechanism": "Within eligible function-local assignment dispatch, guard annotation inspection by annotated-assignment node kind, reuse explicit-alias recognition, and select the alias naming category with a variable fallback.",
  "action_ids": [
    "workflow:verified-history:b980c9ec644c821d41e50e10:probe",
    "workflow:verified-history:b980c9ec644c821d41e50e10:route",
    "workflow:verified-history:b980c9ec644c821d41e50e10:regression",
    "workflow:verified-history:b980c9ec644c821d41e50e10:validate"
  ],
  "source_ids": ["pylint-dev/pylint:8536:repair:b63c8a1c148e"],
  "required_effects": [
    {"key": "explicit-local-alias-routing", "value": "typealias", "evaluator": "evidence"},
    {"key": "local-alias-controls-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-variable-routing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "scope-guards-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-alias-policy-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-regression-assertions-retained", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:b980c9ec644c821d41e50e10:probe",
      "after": "workflow:verified-history:b980c9ec644c821d41e50e10:route",
      "reason": "Confirm the classification defect and compatible guarded owner before editing.",
      "evidence_refs": ["pylint-dev/pylint:8536:body", "pylint-dev/pylint:8536:fix"]
    },
    {
      "before": "workflow:verified-history:b980c9ec644c821d41e50e10:probe",
      "after": "workflow:verified-history:b980c9ec644c821d41e50e10:regression",
      "reason": "Bind controls to the public scope-specific reproduction.",
      "evidence_refs": ["pylint-dev/pylint:8536:body", "pylint-dev/pylint:8536:regression"]
    },
    {
      "before": "workflow:verified-history:b980c9ec644c821d41e50e10:route",
      "after": "workflow:verified-history:b980c9ec644c821d41e50e10:validate",
      "reason": "Validation observes final classifier state.",
      "evidence_refs": ["pylint-dev/pylint:8536:fix", "pylint-dev/pylint:8536:regression"]
    },
    {
      "before": "workflow:verified-history:b980c9ec644c821d41e50e10:regression",
      "after": "workflow:verified-history:b980c9ec644c821d41e50e10:validate",
      "reason": "Validation executes final diagnostic and non-alias controls.",
      "evidence_refs": ["pylint-dev/pylint:8536:regression"]
    }
  ]
}
```

The two edits have no required relative order. Both retain final validation in their verification closure.
