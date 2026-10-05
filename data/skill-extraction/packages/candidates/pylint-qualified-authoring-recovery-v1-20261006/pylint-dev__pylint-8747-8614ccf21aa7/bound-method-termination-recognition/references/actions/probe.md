# Probe the callable-kind guard

Locate the recognizer, reproduce the public warning, and inspect inference and annotation access. Do not edit tracked source or regression fixtures. Record the excluding guard as well as the wrapper type.

```arex-contract-v4
{
  "id": "workflow:verified-history:1ae2f8b80e4aba1ad79b8e22:probe",
  "intent": "Determine whether bound-method annotations are skipped by an accepted-kind guard.",
  "mechanism": "Compare inferred callable kind and annotation access with the termination recognizer's guard.",
  "semantic_role": "callable-kind-diagnosis",
  "owner_role": "return-termination-recognizer",
  "operation": "Locate the current recognizer and inspect the public reproduction, callable inference, annotation access, and guard without modifying tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "guard-diagnosis",
      "semantic_role": "bound-method-guard-mismatch",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "return-termination-recognizer",
      "phase": "diagnosis",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:return-termination-recognizer", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "callable-guard-diagnosis-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-returning-method-warning-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-function-annotation-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "annotation-trust-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "observe-wrapper-mismatch",
      "instruction": "Record the current public diagnostic, inferred bound-method representation, accessible NoReturn annotation, and excluding guard. Check that tracked source and fixtures were not changed by the probe.",
      "evidence_refs": ["pylint-dev/pylint:8747:body"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:return-termination-recognizer"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:8747:repair:8614ccf21aa7"],
  "evidence_refs": ["pylint-dev/pylint:8747:title", "pylint-dev/pylint:8747:body"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:1ae2f8b80e4aba1ad79b8e22"
}
```

Bind the semantic owner to a current symbol; the historical helper name is not an automatic binding. Unknown inference or annotation access permits further probes only. If the guard already accepts the wrapper, reject this mechanism.
