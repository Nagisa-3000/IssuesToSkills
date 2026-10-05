# Inspect startup and early reporting

Read public code and reproduce the failure without editing. Resolve semantic owners in the current checkout rather than reusing historical paths.

Trace configured-name retention, duplicate suppression, loading, registration, configuration hooks, diagnostic definitions, statistics, file context, and reporter templates. Record baseline behavior for valid plugins and ordinary analysis. Determine the actual exception boundary and whether configuration messages precede normal reporter initialization.

Unknown facts authorize further read-only probes, not repair.

```arex-contract-v4
{
  "id": "workflow:verified-history:855459481b02863b85df5b59:inspect",
  "intent": "Determine whether the current failure matches the evidenced plugin startup mechanism.",
  "mechanism": "Trace missing configured modules through registration, configuration, and early reporting.",
  "semantic_role": "lifecycle-inspection",
  "owner_role": "plugin-startup",
  "operation": "Read public code and reproduce startup failure without editing; bind plugin startup, configuration, diagnostic handler, text reporter, and regression suite owners.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "lifecycle-review", "semantic_role": "plugin-lifecycle-review", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "startup", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "public-checkout-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-lifecycle-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-analysis-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "valid-plugin-lifecycle-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-exception-propagation-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "observe-startup-boundary",
      "instruction": "Use current public reproduction and code inspection to record the exception, phase ordering, retained plugin identity, early reporter state, and adjacent baselines. Confirm inspection introduced no edits.",
      "evidence_refs": ["pylint-dev/pylint:4555:body", "pylint-dev/pylint:4555:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4555:repair:cbd3cc07515e"],
  "evidence_refs": ["pylint-dev/pylint:4555:body", "pylint-dev/pylint:4555:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:855459481b02863b85df5b59",
  "read_set": ["role:plugin-startup", "role:plugin-configuration", "role:diagnostic-handler", "role:text-reporter", "role:regression-suite"],
  "write_set": []
}
```
