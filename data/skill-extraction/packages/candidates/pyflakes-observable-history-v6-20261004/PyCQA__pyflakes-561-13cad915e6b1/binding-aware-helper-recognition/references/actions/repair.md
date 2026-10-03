# Repair binding-aware receiver recognition

Modify the semantic detector owner, not a historical path presumed to exist. For a simple-name attribute receiver:

1. Search scopes from nearest to farthest.
2. At the first binding of the receiver name, decide immediately.
3. Accept only an import binding whose full module identity belongs to the detector's existing supported typing-module set.
4. Reject non-import bindings and unsupported modules; reject an absent binding.
5. Preserve the existing attribute-name matcher, simple-name receiver restriction, and direct-name helper branch.

Add a regression at the current annotation-test owner corresponding to the supplied aliased `overload` assertion. Additional shadowing and unrelated-module checks are current preservation probes, not newly discovered historical tests.

```arex-contract-v4
{
  "id": "workflow:verified-history:2f5b3f202404ca13ec4e8055:repair",
  "intent": "Correct module-alias helper recognition and encode its regression.",
  "mechanism": "Replace receiver spelling membership with first-binding import-provenance membership.",
  "semantic_role": "receiver-recognition-repair",
  "owner_role": "typing-helper-detector",
  "operation": "Edit the bound detector and annotation regression owner using nearest-binding module provenance; add the aliased supported-module overload regression while retaining existing helper branches.",
  "kind": "edit",
  "inputs": [
    {
      "name": "reviewed-owners",
      "semantic_role": "typing-helper-repair-context",
      "artifact_kind": "owner-map",
      "language": "python",
      "scope": "typing-helper-recognition",
      "phase": "current",
      "state": "reviewed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "typing-helper-repair-candidate",
      "artifact_kind": "checkout-patch",
      "language": "python",
      "scope": "typing-helper-recognition",
      "phase": "current",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "detector-owner-located",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "role:typing-helper-detector"
    },
    {
      "key": "regression-owner-located",
      "value": true,
      "evaluator": "file_exists",
      "description": "role:annotation-regression-suite"
    },
    {
      "key": "module-alias-mechanism-applicable",
      "value": true,
      "evaluator": "evidence",
      "description": "Current review establishes spelling-based receiver recognition and reliable nearest-scope import provenance."
    }
  ],
  "effects": [
    {
      "key": "receiver-recognition",
      "value": "nearest-binding-import-provenance",
      "evaluator": "evidence"
    },
    {
      "key": "module-alias-regression",
      "value": "added",
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "adjacent-helper-behavior-preserved",
      "value": true,
      "evaluator": "evidence",
      "description": "Retain direct-name detection, attribute matching restrictions, unrelated-module rejection, and nearest-binding shadowing."
    }
  ],
  "oracle": [
    {
      "id": "inspect-repair-diff",
      "instruction": "Review the public diff for immediate termination at the first binding, supported import identity membership, unchanged adjacent branches, and an aliased overload regression.",
      "evidence_refs": ["PyCQA/pyflakes:561:fix", "PyCQA/pyflakes:561:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:typing-helper-detector",
    "role:lexical-import-binding-model",
    "role:annotation-regression-suite"
  ],
  "write_set": [
    "role:typing-helper-detector",
    "role:annotation-regression-suite"
  ],
  "invalidates": ["public-validation-observed"],
  "source_ids": ["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "evidence_refs": ["PyCQA/pyflakes:561:fix", "PyCQA/pyflakes:561:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:2f5b3f202404ca13ec4e8055"
}
```

Effects are intended postconditions and require validation. Do not expand recognition to arbitrary attributes or search past a shadowing binding.
