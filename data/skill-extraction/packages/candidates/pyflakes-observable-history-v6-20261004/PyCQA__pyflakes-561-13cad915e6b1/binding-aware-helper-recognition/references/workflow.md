# Canonical Workflow

Resolve helper receivers by lexical import provenance instead of identifier spelling. This reconstruction preserves the historical implementation and regression facts while requiring fresh owner discovery and validation in any current checkout.

```arex-workflow-v4
{
  "id": "workflow:verified-history:2f5b3f202404ca13ec4e8055",
  "goal": "Recognize supported typing-module aliases without treating unrelated or shadowing bindings as typing modules.",
  "mechanism": "Resolve a simple-name attribute receiver through the nearest lexical binding and inspect its import provenance.",
  "action_ids": [
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:probe",
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:repair",
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:validate"
  ],
  "source_ids": [
    "PyCQA/pyflakes:561:repair:13cad915e6b1"
  ],
  "required_effects": [
    {
      "key": "receiver-recognition",
      "value": "nearest-binding-import-provenance",
      "evaluator": "evidence"
    },
    {
      "key": "public-validation-observed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "invariants": [
    {
      "key": "adjacent-helper-behavior-preserved",
      "value": true,
      "evaluator": "evidence",
      "description": "Existing direct-name recognition, unrelated receivers, and nearest-binding shadowing semantics must survive."
    }
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:2f5b3f202404ca13ec4e8055:probe",
      "after": "workflow:verified-history:2f5b3f202404ca13ec4e8055:repair",
      "reason": "Current binding representation and semantic owners must be known before replacing receiver recognition.",
      "evidence_refs": ["PyCQA/pyflakes:561:fix"]
    },
    {
      "before": "workflow:verified-history:2f5b3f202404ca13ec4e8055:repair",
      "after": "workflow:verified-history:2f5b3f202404ca13ec4e8055:validate",
      "reason": "The modified detector and regression must be checked together; prior validation observations become stale.",
      "evidence_refs": ["PyCQA/pyflakes:561:fix", "PyCQA/pyflakes:561:regression"]
    }
  ]
}
```

Dependencies express semantic prerequisites, not proof of historical execution order. Already satisfied probes may be omitted from a current task DAG only when their bindings and observations remain fresh. The modifying operation always retains explicit validation.
