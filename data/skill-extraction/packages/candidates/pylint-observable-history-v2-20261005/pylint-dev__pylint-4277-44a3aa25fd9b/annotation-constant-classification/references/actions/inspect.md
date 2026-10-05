# Inspect classification

Locate the current classifier, recognizer, and public naming suite. Read code and public diagnostics without editing tracked files. Distinguish annotation classification from configuration, and record actual AST forms.

```arex-contract-v4
{
  "id": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:inspect",
  "intent": "Determine whether ClassVar storage annotations cause constant classification.",
  "mechanism": "Compare public diagnostics with the annotation-driven naming branch and its recognizer.",
  "semantic_role": "classification-boundary-probe",
  "owner_role": "class-attribute-naming-classifier",
  "operation": "Read current owners and public reproductions; record hashed bindings and applicability findings without editing tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "reviewed-classification-bindings", "semantic_role": "classification-repair-context", "artifact_kind": "binding-record", "language": "Python", "scope": "current-public-checkout", "phase": "pre-edit", "state": "reviewed"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "classification-bindings-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "enum-naming-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "configured-constant-style-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-naming-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-boundary",
      "instruction": "Record current owner anchors, naming configuration, annotation AST forms, and public ClassVar diagnostics. Determine whether ClassVar alone selects constant naming. Verify tracked files remain unchanged by inspection.",
      "evidence_refs": ["pylint-dev/pylint:4277:body", "pylint-dev/pylint:4277:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:class-attribute-naming-classifier", "role:annotated-assignment-recognizer", "role:naming-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4277:repair:44a3aa25fd9b"],
  "evidence_refs": ["pylint-dev/pylint:4277:body", "pylint-dev/pylint:4277:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0"
}
```

Reviewed bindings do not alone establish applicability. Unknown causes authorize further probes only; a different responsible mechanism rejects this repair.
