# Edit the version-gated registry

At the currently bound registry owner, add `__annotations__` only under the confirmed Python 3.6-or-later interpreter condition. Preserve existing entries. Reuse an equivalent predicate if available.

The historical repair also inverted a Python 3.5 predicate and its loop-type branch. That refactor is not mandatory. If a predicate is changed, inspect all affected consumers and preserve their old truth tables, including asynchronous-loop type selection. Do not create a universal builtin allowance.

All effects and preservation predicates below are obligations pending current review and validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:4817630500584ee0981edde8:register",
  "intent": "Correct the false diagnostic through version-gated implicit-name registration.",
  "mechanism": "Register __annotations__ only when the runtime interpreter is Python 3.6 or later.",
  "semantic_role": "version-gated-name-registration",
  "owner_role": "implicit-module-name-model",
  "operation": "edit-version-gated-registry",
  "kind": "edit",
  "inputs": [
    {
      "name": "owner-context",
      "semantic_role": "implicit-name-repair-context",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "module-name-checking",
      "phase": "pre-edit",
      "state": "owners-and-semantics-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "registry-edit",
      "semantic_role": "implicit-name-registration-change",
      "artifact_kind": "code-change",
      "language": "python",
      "scope": "module-name-checking",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:implicit-module-name-model", "value": true, "evaluator": "symbol_exists"},
    {"key": "registry-version-semantics", "value": "confirmed", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "implicit-name-registration", "value": "version-gated", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-magic-names", "value": "preserved", "evaluator": "evidence"},
    {"key": "pre-3.6-registry-behavior", "value": "preserved", "evaluator": "evidence"},
    {"key": "async-loop-version-selection", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-undefined-name-behavior", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-gate-and-consumers",
      "instruction": "Review the current diff for a Python 3.6-plus registry gate, unchanged existing entries, and unchanged branch truth tables for every affected version-predicate consumer. Retain the explicit public validation Action.",
      "evidence_refs": ["PyCQA/pyflakes:395:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:395:repair:066ba4a93c10"],
  "evidence_refs": ["PyCQA/pyflakes:395:body", "PyCQA/pyflakes:395:fix"],
  "resource": "references/actions/register.md",
  "package_id": "workflow:verified-history:4817630500584ee0981edde8",
  "read_set": ["role:implicit-module-name-model", "role:interpreter-version-policy"],
  "write_set": ["role:implicit-module-name-model", "role:interpreter-version-policy"],
  "invalidates": ["registry-version-semantics", "public-validation", "async-loop-version-selection"]
}
```
