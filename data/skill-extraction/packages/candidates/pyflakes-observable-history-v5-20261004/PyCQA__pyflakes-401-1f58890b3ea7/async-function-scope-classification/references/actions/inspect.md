# Inspect the missing scope boundary

Locate current semantic owners, inspect the ordinary function registry representation, and establish the async AST capability policy. Trace the public failure through argument binding and scope lookup. Compare the asynchronous definition's classification with ordinary function classification.

Record owner anchors and public results, including UNKNOWN facts. Do not infer the cause from the exception text alone. This probe does not modify source or tests.

```arex-contract-v4
{
  "id": "workflow:verified-history:76dfcbfcb074afe10f1cb891:inspect",
  "intent": "Determine whether missing asynchronous-function scope classification explains the public failure.",
  "mechanism": "Trace annotation argument binding to scope classification and compare asynchronous and ordinary function boundaries.",
  "semantic_role": "diagnose-missing-async-scope",
  "owner_role": "python-ast-scope-classifier",
  "operation": "Inspect current owners, reproduce the public symptom where possible, and record mechanism and compatibility observations.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosis",
      "semantic_role": "async-scope-repair-diagnosis",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "scope-classifier-and-annotation-tests",
      "phase": "current",
      "state": "observed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-scope-diagnosis-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-mechanism",
      "instruction": "Record public reproduction results, scope lookup anchors, the missing or present AsyncFunctionDef classification, ordinary function value representation, runtime policy, and annotation-test harness bindings. Mark unresolved facts UNKNOWN.",
      "evidence_refs": ["PyCQA/pyflakes:401:title", "PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:python-ast-scope-classifier",
    "role:python-runtime-capability-policy",
    "role:annotation-regression-tests"
  ],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "evidence_refs": ["PyCQA/pyflakes:401:title", "PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:76dfcbfcb074afe10f1cb891"
}
```
