# Add the aliased overload regression

Bind the current public annotation regression owner and encode the supplied assertion with its diagnostic harness:

```python
import typing as t

@t.overload
def f(s):  # type: (None) -> None
    pass

@t.overload
def f(s):  # type: (int) -> int
    pass

def f(s):
    return s
```

Assert no unexpected diagnostics. Preserve existing tests. Shadowing and unrelated-import checks are current preservation checks derived from the implementation, not additional supplied historical regressions.

```arex-contract-v4
{
  "id": "workflow:verified-history:2f5b3f202404ca13ec4e8055:regression",
  "intent": "Encode the historical aliased-module overload assertion in the current public harness.",
  "mechanism": "Analyze two aliased overload declarations followed by their implementation and assert no unexpected diagnostics.",
  "semantic_role": "alias-regression-authoring",
  "owner_role": "typing-annotation-regressions",
  "operation": "Add an equivalent aliased typing.overload regression to the bound test owner.",
  "kind": "edit",
  "inputs": [
    {"name": "corrected_snapshot", "semantic_role": "recognition-repair-snapshot", "artifact_kind": "checkout", "language": "python", "scope": "helper-recognition-and-tests", "phase": "repair", "state": "origin-resolution-edited", "optional": false}
  ],
  "outputs": [
    {"name": "test_ready_snapshot", "semantic_role": "recognition-repair-snapshot", "artifact_kind": "checkout", "language": "python", "scope": "helper-recognition-and-tests", "phase": "repair", "state": "regression-ready", "optional": false}
  ],
  "preconditions": [
    {"key": "role:typing-annotation-regressions", "value": true, "evaluator": "file_exists"},
    {"key": "public-diagnostic-harness-understood", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "alias-overload-regression", "value": "present", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-regression-assertions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "production-recognition-edit-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-alias-regression",
      "instruction": "Inspect the current test for an aliased typing module, two overload declarations with the supplied type comments, a concrete implementation, and a no-unexpected-diagnostics assertion. Execute it through the explicit validation Action.",
      "evidence_refs": ["PyCQA/pyflakes:561:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "evidence_refs": ["PyCQA/pyflakes:561:regression"],
  "read_set": ["role:typing-annotation-regressions"],
  "write_set": ["role:typing-annotation-regressions"],
  "invalidates": ["current-public-validation"],
  "resource": "references/actions/add-alias-regression.md",
  "package_id": "workflow:verified-history:2f5b3f202404ca13ec4e8055"
}
```

[Validation](validate-recognition.md) remains required after test modification.
