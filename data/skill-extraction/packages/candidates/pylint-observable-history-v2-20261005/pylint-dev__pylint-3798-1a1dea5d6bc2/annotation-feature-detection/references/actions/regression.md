# Add focused alias regressions

Add an aliased `annotations` future import fixture covering:

1. A containing-class return annotation.
2. A parameter annotation referring to a later class.
3. An attribute annotation referring to a later class.
4. A self-referencing attribute annotation.

Assert absence of spurious undefined-variable and used-before-assignment diagnostics in these positions. Keep those categories enabled. Narrowly configure unrelated diagnostics if needed. Bind runtime restrictions to current supported syntax and collection behavior; the historical fixture required Python 3.7.

Fixture definition is not proof of collection or execution. Retain [validation](validate.md).

```arex-contract-v4
{
  "id": "workflow:verified-history:ca64407d3ccfea06d7171181:regression",
  "intent": "Retain explicit alias-specific self and forward annotation assertions.",
  "mechanism": "Exercise the four annotation positions present in the committed historical regression.",
  "semantic_role": "annotation-regression-coverage",
  "owner_role": "annotation-regression-suite",
  "operation": "Add or extend public annotation assertions and runtime configuration for four aliased-future reference cases without disabling target diagnostic categories.",
  "kind": "edit",
  "inputs": [
    {"name": "assessment", "semantic_role": "annotation-feature-assessment", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "pre-edit", "state": "observed", "optional": false}
  ],
  "outputs": [],
  "preconditions": [
    {"key": "role:annotation-regression-suite", "value": true, "evaluator": "file_exists"},
    {"key": "alias-sensitive-namespace-detection-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "supported-fixture-runtime-located", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "alias-regression-defined", "value": true, "evaluator": "evidence", "description": "Assertions are present; collection and outcomes remain to be observed."}
  ],
  "preserves": [
    {"key": "unaliased-feature-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "feature-absent-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-name-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed", "target-and-controls-passed", "fixture-collection-observation-current"],
  "oracle": [
    {
      "id": "review-alias-assertions",
      "instruction": "Inspect all four annotation cases, alias syntax and collection configuration. Confirm undefined-variable and used-before-assignment remain enabled and identify the supported public runner.",
      "evidence_refs": ["pylint-dev/pylint:3798:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3798:repair:1a1dea5d6bc2"],
  "evidence_refs": ["pylint-dev/pylint:3798:body", "pylint-dev/pylint:3798:regression"],
  "read_set": ["role:annotation-regression-suite"],
  "write_set": ["role:annotation-regression-suite"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:ca64407d3ccfea06d7171181"
}
```
