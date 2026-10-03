# Repair the annotation-read producer

At the bound producer, replace the boolean used marker with the same structured scope-and-read-node metadata expected by the bound consumer. The evidenced Python realization is `(self.scope, node)`.

Keep the annotation-kind check, the non-postponed-annotation guard, and continuation behavior unchanged. Do not alter the consumer simply to tolerate malformed state. If the current metadata contract differs, stop rather than invent an adapter.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9020121b14a346d4f659c0e:repair",
  "intent": "Restore use-state representation consistency.",
  "mechanism": "Replace the annotation-only read's boolean marker with the current scope and read node.",
  "semantic_role": "metadata-producer-repair",
  "owner_role": "binding-use-producer",
  "operation": "Edit the annotation-read producer to emit scope-and-node use metadata.",
  "kind": "edit",
  "inputs": [
    {"name": "inspected-contract", "semantic_role": "binding-use-contract", "artifact_kind": "analysis-record", "language": "Python", "scope": "binding-use-analysis", "phase": "current", "state": "inspected", "optional": false}
  ],
  "outputs": [
    {"name": "repaired-producer", "semantic_role": "binding-use-implementation", "artifact_kind": "source-code", "language": "Python", "scope": "binding-use-analysis", "phase": "current", "state": "edited", "optional": false}
  ],
  "preconditions": [
    {"key": "role:binding-use-producer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:binding-use-consumer", "value": true, "evaluator": "symbol_exists"},
    {"key": "boolean-to-structured-mismatch", "value": true, "evaluator": "evidence"},
    {"key": "scope-and-node-contract", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "annotation-use-metadata", "value": "scope-and-node", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "annotation-read-remains-undefined", "value": true, "evaluator": "evidence"},
    {"key": "unused-local-remains-reported", "value": true, "evaluator": "evidence"},
    {"key": "postponed-annotation-branch-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-producer-diff",
      "instruction": "Review the edit for scope-and-node metadata and unchanged annotation guard and continuation; use the linked validation Action to check behavior.",
      "evidence_refs": ["PyCQA/pyflakes:764:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:764:repair:e19886e58363"],
  "evidence_refs": ["PyCQA/pyflakes:764:fix", "PyCQA/pyflakes:764:body"],
  "read_set": ["role:binding-use-producer", "role:binding-use-consumer"],
  "write_set": ["role:binding-use-producer"],
  "invalidates": ["current-reproduction-result", "annotation-suite-result", "interaction-diagnostics"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:a9020121b14a346d4f659c0e"
}
```

The effect is an intended edit outcome, not a recorded execution result. [Validation](validate.md) is mandatory after this modification.
