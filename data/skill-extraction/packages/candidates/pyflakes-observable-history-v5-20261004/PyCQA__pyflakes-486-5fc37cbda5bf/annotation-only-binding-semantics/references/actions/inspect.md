# Inspect binding and context behavior

Locate semantic owners in the current checkout rather than assuming historical filenames. Review no-value target traversal, binding construction, scope lookup, annotation-state entry/restoration, string parsing, future flags, and unused diagnostics.

Execute public context probes and record actual diagnostics with hashed owner anchors. Matching symbols or predicate names alone do not prove semantic compatibility. The output contract describes a requested artifact, not an observed execution result.

```arex-contract-v4
{
  "id": "workflow:verified-history:be71c3f9e9544046d28904cd:inspect",
  "intent": "Determine whether annotation-only binding/context handling explains the public failure.",
  "mechanism": "Review binding creation and lookup and compare public examples across annotation evaluation contexts.",
  "semantic_role": "binding-context-diagnosis",
  "owner_role": "python-analyzer-binding-and-annotation-owners",
  "operation": "Locate current owners and produce an evidence-backed behavior map.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "binding-context-map",
      "semantic_role": "binding-context-map",
      "artifact_kind": "review-report",
      "language": "Python",
      "scope": "current-analyzer",
      "phase": "diagnosis",
      "state": "owners-and-behavior-observed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-binding-context-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "source-code-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-matrix",
      "instruction": "Bind and execute public probes for bare, quoted, future-postponed, and ordinary value references. Record actual diagnostics, owner anchors, and evidence supporting or rejecting mechanism applicability.",
      "evidence_refs": ["PyCQA/pyflakes:486:body", "PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:486:repair:5fc37cbda5bf"],
  "evidence_refs": ["PyCQA/pyflakes:486:body", "PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
  "read_set": ["role:python-analyzer-binding-and-annotation-owners", "role:python-analyzer-public-regression-suite"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:be71c3f9e9544046d28904cd"
}
```
