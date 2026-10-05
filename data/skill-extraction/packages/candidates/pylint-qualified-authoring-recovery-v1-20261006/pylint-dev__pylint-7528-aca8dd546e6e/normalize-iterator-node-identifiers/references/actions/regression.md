# Add the separate-copy regression

Add a fixture equivalent to this supported reproduction:

```python
from enum import Enum

class MyEnum(Enum):
    FOO = 1
    BAR = 2

class EnumClass:
    ENUM_SET = {MyEnum.FOO, MyEnum.BAR}

    def useless(self):
        other_set = set(self.ENUM_SET)
        for obj in self.ENUM_SET:
            other_set.remove(obj)
```

Adapt names and formatting to current public conventions. Suppress only unrelated fixture diagnostics if necessary; keep the target checker enabled. Retain existing diagnostic identities and text, changing locations only when justified by inserted lines. Add no mutation warning for this separate-copy case.

```arex-contract-v4
{
  "id": "workflow:verified-history:bc4129e7b226dfae4c87ca01:regression",
  "intent": "Cover the Attribute iterable crash and separate-copy non-warning behavior.",
  "mechanism": "Add an enum-backed class-attribute set whose separate constructed copy is mutated during attribute iteration.",
  "semantic_role": "regression-edit",
  "owner_role": "iteration-regression-owner",
  "operation": "Add the reproduction shape to current public fixtures and reconcile justified location shifts without deleting existing mutation expectations.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "role:iteration-regression-owner", "value": true, "evaluator": "file_exists"},
    {"key": "supported-node-shapes-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "fixture-expectation-format-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "attribute-copy-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "inference-equality-guard-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-iteration-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "separate-copy-not-diagnosed-as-iterated-set", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-regression-coverage",
      "instruction": "Inspect the fixture for Attribute iteration, a separately constructed set copy, and removal from that copy. Confirm the target checker remains enabled. Compare expectations: retain diagnostic identities and text, allow only justified location changes, and add no target warning for this case.",
      "evidence_refs": ["pylint-dev/pylint:7528:body", "pylint-dev/pylint:7528:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:iteration-regression-owner"],
  "write_set": ["role:iteration-regression-owner"],
  "source_ids": ["pylint-dev/pylint:7528:repair:aca8dd546e6e"],
  "evidence_refs": ["pylint-dev/pylint:7528:body", "pylint-dev/pylint:7528:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:bc4129e7b226dfae4c87ca01"
}
```
