# Diagnose the module-name policy

Inspect the current public reproduction, registry consumption, version policy, and regression suite. This operation is read-only; it must not modify code or tests. Produce a reviewed diagnosis only after public evidence establishes scope and version compatibility. Unknown facts remain unknown.

```arex-contract-v4
{
  "id": "workflow:verified-history:4817630500584ee0981edde8:diagnose",
  "intent": "Establish that the current false warning matches the historical module-name policy.",
  "mechanism": "Read scope lookup and version capability owners and probe the public reproduction.",
  "semantic_role": "diagnose-implicit-module-name",
  "owner_role": "implicit-module-name-registry",
  "operation": "Locate current semantic owners, inspect their consumers, and collect a read-only public diagnostic and policy review.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "reviewed-policy",
      "semantic_role": "module-name-policy-diagnosis",
      "artifact_kind": "review-record",
      "language": "text",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "reviewed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "compatible-policy-reviewed", "value": true, "evaluator": "evidence", "description": "Current public review confirms module scope and a Python 3.6 capability boundary."},
    {"key": "owners-bound", "value": true, "evaluator": "evidence", "description": "Actual checkout anchors bind all three semantic owners."}
  ],
  "preserves": [
    {"key": "existing-magic-global-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "version-dependent-loop-types-preserved", "value": true, "evaluator": "evidence"},
    {"key": "pre36-registration-boundary-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "diagnose-public-policy",
      "instruction": "Read current bindings and run the public reproduction without editing. Confirm the warning, module-scope owner, supported-version boundary, and baseline adjacent behavior; report UNKNOWN rather than assuming missing observations.",
      "evidence_refs": ["PyCQA/pyflakes:395:body", "PyCQA/pyflakes:395:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:implicit-module-name-registry", "role:python-version-capability-policy", "role:undefined-name-regression-suite"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:395:repair:066ba4a93c10"],
  "evidence_refs": ["PyCQA/pyflakes:395:title", "PyCQA/pyflakes:395:body", "PyCQA/pyflakes:395:fix"],
  "resource": "references/actions/diagnose.md",
  "package_id": "workflow:verified-history:4817630500584ee0981edde8"
}
```

The expected output is a current diagnosis, not a claim that a historical probe was executed. A diagnosis identifying a different scope or incompatible target-version model does not satisfy this Action's effects.
