# Probe annotation and deferred traversal

Read the current public reproduction and implementation. Compare a partially quoted annotation with its fully quoted counterpart. Locate the annotation entry points, string AST dispatch, typing binding recognition, and deferred runner. Inspect supported Python AST versions and current regression conventions.

This operation is read-only. Running a public reproduction may produce logs or temporary test artifacts, but it must not edit source. Record failure, success, or unknown explicitly; do not infer a current failure from the historical report.

```arex-contract-v4
{
  "id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:probe",
  "intent": "Establish whether the current failure is caused by missed nested annotation strings.",
  "mechanism": "Compare public annotation forms and inspect the semantic traversal owners.",
  "semantic_role": "annotation-traversal-diagnosis",
  "owner_role": "python-static-analysis-annotation-traversal",
  "operation": "Read current public code and run bound public probes without source edits; produce hashed owner bindings and mechanism observations.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "traversal-context",
      "semantic_role": "bound-annotation-traversal-context",
      "artifact_kind": "task-context",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-checkout-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "annotation-mechanism-observed", "value": true, "evaluator": "evidence"},
    {"key": "semantic-owners-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "runtime-strings-remain-data", "value": true, "evaluator": "evidence"},
    {"key": "literal-strings-remain-data", "value": true, "evaluator": "evidence"},
    {"key": "existing-overload-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "analysis-phase-integrity-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-public-mechanism",
      "instruction": "Use current bound public commands to compare partially and wholly quoted annotations; inspect the corresponding traversal and deferred owners. Confirm no source changes and record actual diagnostics and code anchors.",
      "evidence_refs": ["PyCQA/pyflakes:447:body", "PyCQA/pyflakes:447:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:447:repair:c9708a18a17f"],
  "evidence_refs": ["PyCQA/pyflakes:447:body", "PyCQA/pyflakes:447:fix"],
  "read_set": ["role:python-static-analysis-annotation-traversal", "role:python-static-analysis-deferred-runner", "role:python-typing-binding-recognition"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0"
}
```

If owners or public reproduction are missing, the output state is not established: return UNKNOWN and continue investigation rather than authorizing the edit.
