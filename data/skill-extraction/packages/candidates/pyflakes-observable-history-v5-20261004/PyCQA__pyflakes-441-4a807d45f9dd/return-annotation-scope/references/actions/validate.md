# Validate both sides of the scope boundary

Bind the public regression scenarios and annotation suite to the current checkout. Run both scenarios and the suite, retain outputs, and inspect the final diff. Do not substitute hidden tests or gold-derived commands.

Class-bound case:

```python
from typing import TypeVar

class Test:
    Y = TypeVar('Y')

    def t(self, x: Y) -> Y:
        return x
```

Body-local negative case:

```python
class Test:
    def t(self) -> Y:
        Y = 2
        return Y
```

The first must produce no undefined-name diagnostic for `Y`. The second must still produce an undefined-name diagnostic for the return annotation.

```arex-contract-v4
{
  "id": "workflow:verified-history:46d18832864f51ea6f6d3968:validate",
  "intent": "Verify the corrected annotation scope and preserve rejection of body-local annotation names.",
  "mechanism": "Run the two public boundary regressions and the current annotation regression suite.",
  "semantic_role": "verify-annotation-scope-repair",
  "owner_role": "annotation-regression-suite",
  "operation": "Execute bound public regression checks and record current results.",
  "kind": "validate",
  "inputs": [
    {
      "name": "traversal-patch",
      "semantic_role": "annotation-traversal-change",
      "artifact_kind": "source-change",
      "language": "python",
      "scope": "function-definition-traversal",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "annotation-scope-validation",
      "artifact_kind": "test-result",
      "language": "python",
      "scope": "annotation-regression-suite",
      "phase": "post-edit",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:annotation-regression-suite", "value": true, "evaluator": "file_exists"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "annotation-validation-results-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified-by-validation", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "class-bound-name",
      "instruction": "Run the public class-level TypeVar example and verify no undefined-name diagnostic for Y in either method annotation.",
      "evidence_refs": ["PyCQA/pyflakes:441:body", "PyCQA/pyflakes:441:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "body-local-name",
      "instruction": "Run the public body-local Y example and verify an undefined-name diagnostic remains for the return annotation.",
      "evidence_refs": ["PyCQA/pyflakes:441:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-suite",
      "instruction": "Run the bound current annotation regression suite and compare results with the pinned-base observations; report failures and unknown coverage explicitly.",
      "evidence_refs": ["PyCQA/pyflakes:441:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:46d18832864f51ea6f6d3968:edit"],
  "read_set": ["role:function-definition-traversal", "role:annotation-regression-suite"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:441:repair:4a807d45f9dd"],
  "evidence_refs": ["PyCQA/pyflakes:441:body", "PyCQA/pyflakes:441:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:46d18832864f51ea6f6d3968"
}
```

Commands remain unbound in this historical package. Failed or unknown results are not success. Broader repository checks may be required by the current task, but historical whole-project coverage is not established here.
