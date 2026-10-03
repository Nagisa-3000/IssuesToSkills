# Recognize match-case alternatives

Modify the shared classifier, not the entire diagnostic policy. For a match node, return each case body as a separate alternative. Preserve the existing shapes returned for other supported constructs.

```arex-contract-v4
{
  "id": "workflow:verified-history:45a56eede77a20492da56a49:classify",
  "intent": "Correct branch exclusivity classification for definitions in separate match cases.",
  "mechanism": "Add guarded match recognition returning one body list per case.",
  "semantic_role": "alternative-classifier-edit",
  "owner_role": "diagnostic-alternative-classifier",
  "operation": "In the bound Python alternative classifier, recognize match nodes and return a list of their case bodies. Retain existing if and try results. Guard ast.Match access where supported older runtimes require it; the historical implementation short-circuited on Python version before referring to ast.Match.",
  "kind": "edit",
  "inputs": [
    {
      "name": "bindings",
      "semantic_role": "branch-redefinition-owner-bindings",
      "artifact_kind": "binding-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "applicability",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "classifier",
      "semantic_role": "branch-alternative-classifier",
      "artifact_kind": "source-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "modified",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "classifier-owner-located", "value": true, "evaluator": "symbol_exists", "description": "Resolve role:diagnostic-alternative-classifier in the current checkout."},
    {"key": "missing-match-alternatives-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "runtime-guard-requirement-known", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "match-case-alternatives-recognized", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-if-try-classification-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-redefinition-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-compatibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-case-alternatives",
      "instruction": "Inspect the current diff for one alternative per match-case body, unchanged existing if/try return semantics, and safe AST access under the current runtime policy. This review alone is not execution validation.",
      "evidence_refs": ["PyCQA/pyflakes:771:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:diagnostic-alternative-classifier"],
  "write_set": ["role:diagnostic-alternative-classifier"],
  "exclusions": [
    {"key": "requires-case-scope-redesign", "value": true, "evaluator": "evidence"},
    {"key": "symptom-is-sequential-redefinition", "value": true, "evaluator": "evidence"}
  ],
  "source_ids": ["PyCQA/pyflakes:771:repair:f2671ffe1785"],
  "evidence_refs": ["PyCQA/pyflakes:771:fix"],
  "resource": "references/actions/classify.md",
  "package_id": "workflow:verified-history:45a56eede77a20492da56a49"
}
```

Bind `classifier-owner-located` through `role:diagnostic-alternative-classifier`, not a historical path. The effect is a repair objective until current inspection and validation observe it.
