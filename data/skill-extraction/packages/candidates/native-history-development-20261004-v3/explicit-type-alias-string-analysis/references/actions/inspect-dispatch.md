# Inspect assignment dispatch

Locate the current semantic owners. Compare the public quoted-alias reproduction with ordinary quoted function annotations. Review the typing marker's actual scope binding and the value-dispatch branch. Do not infer marker identity from spelling.

Produce an inspected checkout and a report with code anchors, diagnostics, and tri-state applicability checks. An observation that applicability was assessed is not itself a PASS applicability result.

```arex-contract-v4
{
  "id": "explicit-type-alias-string-analysis.inspect",
  "intent": "Determine whether the explicit-alias value-dispatch mechanism explains the current public failure.",
  "mechanism": "Compare assignment-value traversal with annotation-string processing and inspect scope-aware marker recognition.",
  "semantic_role": "applicability-probe",
  "owner_role": "annotated-assignment-handler",
  "operation": "Locate current owners, observe the public contrast, and record applicability evidence.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "inspected-checkout", "semantic_role": "alias-analysis-checkout", "artifact_kind": "checkout", "language": "python", "scope": "current-public-checkout", "phase": "repair", "state": "inspected", "optional": false},
    {"name": "inspection-report", "semantic_role": "alias-applicability-evidence", "artifact_kind": "report", "language": "python", "scope": "current-public-checkout", "phase": "inspection", "state": "observed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "alias-dispatch-applicability-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-contrast",
      "instruction": "Record diagnostics for quoted explicit-alias and quoted function-annotation examples, inspect current marker binding and handler dispatch, and classify applicability as PASS, FAIL, or UNKNOWN.",
      "evidence_refs": ["PyCQA/pyflakes:671:body", "PyCQA/pyflakes:671:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:671"],
  "evidence_refs": ["PyCQA/pyflakes:671:body", "PyCQA/pyflakes:671:comment:1017848489", "PyCQA/pyflakes:671:fix"],
  "resource": "references/actions/inspect-dispatch.md",
  "package_id": "explicit-type-alias-string-analysis",
  "read_set": ["role:annotated-assignment-handler", "role:typing-marker-resolver", "role:annotation-value-handler"],
  "write_set": []
}
```
