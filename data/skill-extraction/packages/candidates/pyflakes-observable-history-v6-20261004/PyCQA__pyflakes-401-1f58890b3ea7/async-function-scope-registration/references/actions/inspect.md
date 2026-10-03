# Inspect scope classification and reproduce the failure

Locate the current scope-classification and annotation-test owners. Inspect ordinary function registration, asynchronous handling, scope lookup, argument binding, and the supported-runtime gate. Compare ordinary and asynchronous versions of the public annotation/name-collision reproduction.

Run only bound public commands. Keep probe source in memory or outside tracked files; this operation does not modify tracked code or tests. An exception-string match alone is insufficient. Emit an applicability-established context only when current evidence supports this mechanism; otherwise report insufficient or not applicable and stop before editing.

```arex-contract-v4
{
  "id": "workflow:verified-history:76dfcbfcb074afe10f1cb891:inspect",
  "intent": "Determine whether missing asynchronous-function scope registration causes the current annotated-argument failure.",
  "mechanism": "Inspect current scope classification and compare public asynchronous and ordinary-function probes.",
  "semantic_role": "scope-registration-diagnosis",
  "owner_role": "ast-scope-classification",
  "operation": "Locate current semantic owners, read scope classification and argument binding, and run a bound public reproduction without modifying tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "scope-diagnosis",
      "semantic_role": "async-scope-repair-context",
      "artifact_kind": "reviewed-code-and-probe-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-checkout-available", "value": true, "evaluator": "evidence"},
    {"key": "public-inspection-oracle-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "scope-applicability-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-function-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-version-import-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "diagnose-missing-async-scope",
      "instruction": "Record actual current owner bindings, registry representation, version policy, argument-binding scope path, and public probe outcomes. Establish whether absent asynchronous-function classification explains the failure; verify tracked files are unchanged.",
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:ast-scope-classification", "role:annotation-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "evidence_refs": ["PyCQA/pyflakes:401:title", "PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:76dfcbfcb074afe10f1cb891"
}
```

This probe can begin while owner locations are unknown. Discovery must resolve real current bindings before the repair's owner predicates can pass. Applicability and preserved-behavior claims require evidence-backed review or probes, not merely matching predicate labels.
