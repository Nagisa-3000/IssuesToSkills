# Add focused regression assertions

At the bound public test owner, add equivalent assertions for:

- Two class-local overload declarations using an enclosing `from typing import overload`, followed by an implementation.
- Two declarations with another decorator above `@overload`, followed by an implementation using that other decorator.

Assert no unused-redefinition diagnostics. Keep adjacent expectations unchanged. The report's opposite decorator order supplies a further public validation probe.

Nearest-binding and ordinary-redefinition probes are preservation checks, not claims that the historical commit added those tests. Retain the [validation Action](validate.md).

```arex-contract-v4
{
  "id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:regressions",
  "intent": "Make the two historically demonstrated false positives observable in public regression tests.",
  "mechanism": "Add class-local and multiple-decorator overload diagnostic assertions.",
  "semantic_role": "regression-authoring",
  "owner_role": "type-annotation-regressions",
  "operation": "Add focused public regression cases.",
  "kind": "edit",
  "inputs": [
    {"name": "assessment", "semantic_role": "overload-repair-assessment", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "inspection", "state": "assessed", "optional": false}
  ],
  "outputs": [
    {"name": "assertions", "semantic_role": "overload-regression-change", "artifact_kind": "test-change", "language": "Python", "scope": "current-checkout", "phase": "regression", "state": "authored", "optional": false}
  ],
  "preconditions": [
    {"key": "role:type-annotation-regressions", "value": true, "evaluator": "file_exists"},
    {"key": "public-reproductions-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-test-expectations", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression-coverage",
      "instruction": "Inspect added tests for repeated overload signatures followed by an implementation, covering enclosing imports in classes and additional decorators without expected redefinition diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:434:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "evidence_refs": ["PyCQA/pyflakes:434:body", "PyCQA/pyflakes:434:regression"],
  "read_set": ["role:type-annotation-regressions"],
  "write_set": ["role:type-annotation-regressions"],
  "invalidates": ["public-validation-passed"],
  "resource": "references/actions/regressions.md",
  "package_id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0"
}
```
