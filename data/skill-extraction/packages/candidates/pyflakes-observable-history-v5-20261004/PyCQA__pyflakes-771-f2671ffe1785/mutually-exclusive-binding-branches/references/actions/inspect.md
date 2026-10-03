# Inspect alternative-branch classification

Locate the semantic owner that classifies mutually exclusive statement branches for binding/redefinition analysis and the public regression-test owner. Compare the public `match` reproduction with `if`/`else`. Confirm the downstream diagnostic actually consults this classifier.

Do not infer applicability solely from a diagnostic number or a symbol name. The expected output is an inspected checkout with evidence-backed owner bindings, not an observed result supplied by this package.

```arex-contract-v4
{
  "id": "workflow:verified-history:45a56eede77a20492da56a49:inspect",
  "intent": "Establish whether missing match-case alternatives explain the reported false positive.",
  "mechanism": "Compare the public reproduction and inspect the branch-alternative classifier used by binding analysis.",
  "semantic_role": "mechanism-inspection",
  "owner_role": "alternative-branch-classifier",
  "operation": "Locate owners and probe match versus if/else binding diagnostics.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "inspected-checkout",
      "semantic_role": "branch-analysis-checkout",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "inspected",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "current-mechanism-inspected",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "checkout-unmodified",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "confirm-mechanism",
      "instruction": "Bind a current public reproduction and inspect the diagnostic's branch-classification path. Record whether separate match-case bodies are missing alternatives and compare the equivalent if/else case.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:771:repair:f2671ffe1785"],
  "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix"],
  "read_set": ["role:alternative-branch-classifier", "role:binding-diagnostic-regression-tests"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:45a56eede77a20492da56a49"
}
```
