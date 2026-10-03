# Expose separate case bodies

Edit the bound shared classifier to return one body per match case. Do not
flatten all cases into one body. Preserve existing `if` and `try` alternative
shapes and the diagnostic logic outside this omission.

The historical implementation guarded `ast.Match` access with
`sys.version_info >= (3, 10)`. Respect the same availability property wherever
older runtimes remain supported. Review the diff and retain explicit validation.

```arex-contract-v4
{
  "id": "mutually-exclusive-match-bindings:recognize",
  "intent": "Expose mutually exclusive match case bodies to branch-sensitive redefinition logic.",
  "mechanism": "Extend shared alternative classification with guarded Python match handling.",
  "semantic_role": "alternative-classifier-repair",
  "owner_role": "python-branch-alternative-classifier",
  "operation": "Edit the current classifier to return a separate body for each match case.",
  "kind": "edit",
  "inputs": [
    {"name": "located-context", "semantic_role": "confirmed-match-alternative-omission", "artifact_kind": "binding-and-probe-record", "language": "python", "scope": "current-analyzer", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "classifier-change", "semantic_role": "match-alternative-implementation", "artifact_kind": "source-change", "language": "python", "scope": "current-analyzer", "phase": "repair", "state": "modified-unvalidated", "optional": false}
  ],
  "preconditions": [
    {"key": "current-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:python-branch-alternative-classifier", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "match-cases-recognized-as-alternatives", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-if-try-alternatives-preserved", "value": true, "evaluator": "evidence"},
    {"key": "sequential-redefinition-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "python-ast-availability-respected", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-alternative-shape",
      "instruction": "Inspect the current diff and classifier result: every case contributes a separate body, existing if/try shapes are unchanged, and ast.Match availability is respected. Require later behavioral validation.",
      "evidence_refs": ["PyCQA/pyflakes:771:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:771"],
  "evidence_refs": ["PyCQA/pyflakes:771:fix"],
  "read_set": ["role:python-branch-alternative-classifier"],
  "write_set": ["role:python-branch-alternative-classifier"],
  "invalidates": ["current-diagnostic-results", "current-adjacent-behavior-results"],
  "resource": "references/actions/recognize.md",
  "package_id": "mutually-exclusive-match-bindings"
}
```

Effects and preservation predicates require current review and probes; their
names do not prove the claims.
