# Add the export/annotation regression

Bind the current annotation test harness and express the public reproduction:

```python
from typing import TYPE_CHECKING, List

from y import z

if not TYPE_CHECKING:
    __all__ = ("z",)
else:
    __all__: List[str]
```

Assert no unexpected diagnostics, specifically no unused-import report for `z`. Follow current syntax-version conventions if supported interpreters require a guard. Do not silently reuse the historical test path.

```arex-contract-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489:regression",
  "intent": "Make export usage loss from annotation replacement observable.",
  "mechanism": "Add the assigned-export and alternative annotation-only reproduction with no expected diagnostics.",
  "semantic_role": "export-annotation-regression",
  "owner_role": "annotation-test-suite",
  "operation": "Add a focused regression assertion through the current public analyzer test harness.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosis",
      "semantic_role": "annotation-binding-repair-context",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "owners-bound-and-overwrite-confirmed"
    }
  ],
  "outputs": [
    {
      "name": "regression-edit",
      "semantic_role": "export-annotation-regression-test",
      "artifact_kind": "test-edit",
      "language": "python",
      "scope": "current-checkout",
      "phase": "implementation",
      "state": "edited-unvalidated"
    }
  ],
  "preconditions": [
    {"key": "role:annotation-test-suite", "value": true, "evaluator": "file_exists"},
    {"key": "current-owner-bindings-established", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "export-annotation-regression-covered", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-annotation-tests-retained", "value": true, "evaluator": "evidence"},
    {"key": "supported-interpreter-test-compatibility", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression-assertion",
      "instruction": "Review the assertion for the z import, assigned __all__, alternative annotation-only branch, and absence of expected diagnostics. Check current supported-interpreter conventions and retention of existing tests.",
      "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:eedcc58f60ba24cb02758489",
  "read_set": ["role:annotation-test-suite"],
  "write_set": ["role:annotation-test-suite"],
  "invalidates": ["current-public-validation-passes"]
}
```

Coverage is an intended effect requiring current review and [validation](validate.md), not a claim that the authored test has run.
