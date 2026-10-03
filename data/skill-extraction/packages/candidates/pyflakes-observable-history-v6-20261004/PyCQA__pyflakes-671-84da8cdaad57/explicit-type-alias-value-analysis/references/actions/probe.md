# Probe the alias-value dispatch boundary

Locate the current annotated-assignment visitor, annotation-analysis entry point, binding-aware typing-marker recognizer, and annotation regression suite. Inspect how value-bearing and valueless annotated assignments are handled.

Use a public reproduction based on the reported `PathLike` alias and compare it with the function-annotation control. Also inspect an ordinary string-valued assignment as a negative boundary. Record baseline diagnostics and code anchors. These probes read code and run analysis without modifying source.

Do not infer typing-marker recognition from the spelling `TypeAlias` alone. If compatibility is unknown, collect more public evidence; if incompatible, stop.

```arex-contract-v4
{
  "id": "workflow:verified-history:d3771ee821e88935b9bcf1ce:probe",
  "intent": "Establish whether the current analyzer has the supported explicit-alias value dispatch defect.",
  "mechanism": "Compare annotated-assignment value traversal with existing annotation analysis and typing-marker recognition.",
  "semantic_role": "alias-dispatch-applicability",
  "owner_role": "annotated-assignment-analysis",
  "operation": "Read the bound owners, run public baseline reproductions, and record compatible bindings and baseline observations; do not edit source.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "checked-alias-dispatch",
      "semantic_role": "alias-dispatch-review",
      "artifact_kind": "code-and-probe-record",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "pre-edit",
      "state": "compatible-and-defect-observed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "compatible-alias-dispatch-owner-observed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "ordinary-assignment-value-semantics-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "valueless-assignment-use-accounting-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "existing-annotation-analysis-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "inspect-and-reproduce",
      "instruction": "Bind current public commands to reproduce the alias-string diagnostic and the function-annotation control. Review owner code for annotation-handler compatibility and typing-marker recognition. Record FAIL or UNKNOWN rather than emitting a compatible output when the prerequisites are not established.",
      "evidence_refs": ["PyCQA/pyflakes:671:body", "PyCQA/pyflakes:671:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:671:repair:84da8cdaad57"],
  "evidence_refs": ["PyCQA/pyflakes:671:body", "PyCQA/pyflakes:671:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:d3771ee821e88935b9bcf1ce",
  "read_set": [
    "role:annotated-assignment-analysis",
    "role:annotation-analysis",
    "role:typing-marker-recognition",
    "role:annotation-regression-tests"
  ],
  "write_set": []
}
```
