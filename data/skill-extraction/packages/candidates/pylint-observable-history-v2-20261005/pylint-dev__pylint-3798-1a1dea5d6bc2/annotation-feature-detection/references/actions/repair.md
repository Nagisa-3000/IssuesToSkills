# Replace namespace-based detection

At the currently bound detector, replace local-name inference with membership of the canonical feature `annotations` in module future-feature metadata. Preserve the detector's purpose and callers.

The historical implementation used `node.root().future_imports`. Bind that API only if current observations establish its compatible semantics. Do not rename user imports or suppress diagnostic categories.

The effect below is an intended repair property, not an observed test result. Retain [validation](validate.md) and refresh stale observations.

```arex-contract-v4
{
  "id": "workflow:verified-history:ca64407d3ccfea06d7171181:repair",
  "intent": "Make postponed-annotation detection independent of local aliases.",
  "mechanism": "Use canonical future-feature membership rather than namespace bindings.",
  "semantic_role": "feature-detection-repair",
  "owner_role": "annotation-feature-detector",
  "operation": "Edit the located detector to query canonical annotations feature membership on the enclosing module; inspect the diff and preserve callers.",
  "kind": "edit",
  "inputs": [
    {"name": "assessment", "semantic_role": "annotation-feature-assessment", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "pre-edit", "state": "observed", "optional": false}
  ],
  "outputs": [],
  "preconditions": [
    {"key": "role:annotation-feature-detector", "value": true, "evaluator": "symbol_exists"},
    {"key": "alias-sensitive-namespace-detection-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "canonical-feature-metadata-compatible", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "detector-edit-present", "value": true, "evaluator": "evidence"},
    {"key": "alias-independent-feature-detection", "value": true, "evaluator": "evidence", "description": "Intended semantic effect; execution success requires post-edit checks."}
  ],
  "preserves": [
    {"key": "unaliased-feature-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "feature-absent-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-name-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed", "target-and-controls-passed", "detector-code-observation-current"],
  "oracle": [
    {
      "id": "review-canonical-membership",
      "instruction": "Inspect the current public diff: canonical annotations membership replaces local-binding inference, callers remain intact, and no diagnostic category is disabled. Record that execution validation is still required.",
      "evidence_refs": ["pylint-dev/pylint:3798:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3798:repair:1a1dea5d6bc2"],
  "evidence_refs": ["pylint-dev/pylint:3798:fix"],
  "read_set": ["role:annotation-feature-detector", "role:module-feature-metadata"],
  "write_set": ["role:annotation-feature-detector"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:ca64407d3ccfea06d7171181"
}
```
