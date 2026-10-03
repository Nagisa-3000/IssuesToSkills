# Inspect annotation-only redefinition ownership

Locate current owners rather than substituting historical filenames. Inspect how annotation-only declarations reach the redefinition predicate. Capture the public reproduction's diagnostics and identify whether the later value usage and annotation-name usage remain connected to their imports.

The expected output is an evidence-backed inspection snapshot. It is not an observed result until the current probe runs. If the abstraction also owns value assignments, or the diagnosis is unrelated to redefinition, mark applicability UNKNOWN or FAIL and do not edit.

```arex-contract-v4
{
  "id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:inspect",
  "intent": "Establish whether annotation-only declarations incorrectly redefine imported names.",
  "mechanism": "Inspect the binding dispatch and redefinition operation, then probe the public annotation-only reproduction.",
  "semantic_role": "annotation-redefinition-diagnosis",
  "owner_role": "annotation-binding-analysis",
  "operation": "Locate owners and record current semantic applicability.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "inspected-checkout",
      "semantic_role": "annotation-redefinition-checkout",
      "artifact_kind": "checkout-snapshot",
      "language": "python",
      "scope": "annotation-binding-and-regression",
      "phase": "pre-repair",
      "state": "inspected",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "annotation-redefinition-applicability",
      "value": "recorded",
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "checkout-content",
      "value": "unchanged",
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "inspect-public-reproduction",
      "instruction": "Inspect the current annotation-only binding and redefinition owners; run the public imported-name annotation reproduction and record diagnostics and name-usage behavior.",
      "evidence_refs": ["PyCQA/pyflakes:617:body", "PyCQA/pyflakes:617:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:617:repair:3de8e6120291"],
  "evidence_refs": ["PyCQA/pyflakes:617:title", "PyCQA/pyflakes:617:body", "PyCQA/pyflakes:617:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7",
  "read_set": ["role:annotation-binding-analysis", "role:redefinition-analysis", "role:annotation-regression-tests"],
  "write_set": []
}
```
