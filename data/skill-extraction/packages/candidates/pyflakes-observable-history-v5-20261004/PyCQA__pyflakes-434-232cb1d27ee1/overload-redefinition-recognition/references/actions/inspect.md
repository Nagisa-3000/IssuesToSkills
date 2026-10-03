# Inspect recognition and diagnostic ownership

Locate the current public owners and record code anchors, scope ordering, import-binding representation, decorator AST shapes, and whether the reporting gate examines the existing binding. Reproduce the class and multiple-decorator symptoms.

A matching symptom alone does not establish applicability. Record observed results separately from historical assertions. This probe does not modify checkout content.

```arex-contract-v4
{
  "id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:inspect",
  "intent": "Determine whether the evidenced recognition repair applies.",
  "mechanism": "Inspect public reproductions and current scope/decorator recognition owners.",
  "semantic_role": "applicability-inspection",
  "owner_role": "overload-recognition",
  "operation": "Locate owners and produce an evidence-backed applicability assessment.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "assessment", "semantic_role": "overload-repair-assessment", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "inspection", "state": "assessed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-owners-and-defect-assessed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "assess-public-defect",
      "instruction": "Inspect bound owners and reproduce public class-scope and multiple-decorator cases; record affected cases and compatibility of the nearest-binding/import model.",
      "evidence_refs": ["PyCQA/pyflakes:434:body", "PyCQA/pyflakes:434:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "evidence_refs": ["PyCQA/pyflakes:434:title", "PyCQA/pyflakes:434:body", "PyCQA/pyflakes:434:fix"],
  "read_set": ["role:overload-recognition", "role:unused-redefinition-reporting", "role:type-annotation-regressions"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0"
}
```
