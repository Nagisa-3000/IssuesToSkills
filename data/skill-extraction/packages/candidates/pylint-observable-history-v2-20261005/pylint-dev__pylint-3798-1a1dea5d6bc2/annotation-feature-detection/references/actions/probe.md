# Locate and discriminate the mechanism

Read the current detector and inspect canonical module metadata. Compare public reproductions with aliased, unaliased, and absent future imports. Record actual metadata values, diagnostics, current owner bindings, and hashed anchors. Locate a supported fixture runner.

This operation does not edit tracked files. Metadata compatibility requires observation, not attribute-name matching. If the target has a different mechanism or incompatible representation, stop rather than inventing an adapter.

```arex-contract-v4
{
  "id": "workflow:verified-history:ca64407d3ccfea06d7171181:probe",
  "intent": "Establish current applicability of alias-independent canonical feature detection.",
  "mechanism": "Compare import forms and inspect namespace-based detection against canonical module metadata.",
  "semantic_role": "mechanism-assessment",
  "owner_role": "annotation-feature-detector",
  "operation": "Read current semantic owners and execute bound public reproductions without editing tracked source; record findings, including incompatible or unknown findings.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "assessment", "semantic_role": "annotation-feature-assessment", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "pre-edit", "state": "observed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "mechanism-assessment-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unaliased-feature-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "feature-absent-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-name-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "discriminate-alias-mechanism",
      "instruction": "Record current detector anchors, metadata values and diagnostics for aliased, unaliased and absent-feature forms. Evaluate namespace sensitivity, metadata compatibility and fixture runtime support separately as PASS/FAIL/UNKNOWN. Confirm tracked source remains unchanged.",
      "evidence_refs": ["pylint-dev/pylint:3798:body", "pylint-dev/pylint:3798:fix", "pylint-dev/pylint:3798:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3798:repair:1a1dea5d6bc2"],
  "evidence_refs": ["pylint-dev/pylint:3798:body", "pylint-dev/pylint:3798:fix", "pylint-dev/pylint:3798:regression"],
  "read_set": ["role:annotation-feature-detector", "role:module-feature-metadata", "role:annotation-regression-suite"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:ca64407d3ccfea06d7171181"
}
```
