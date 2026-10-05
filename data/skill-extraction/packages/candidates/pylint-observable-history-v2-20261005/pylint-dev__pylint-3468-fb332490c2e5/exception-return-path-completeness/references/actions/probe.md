# Probe and bind

Read the current diagnostic owner and public test harness. Run the public reproduction and both explicit-`None` counterexamples. Inspect AST children and neighboring conditional, nested-function, and raise rules. Do not edit tracked code.

An output binding is usable for repair only when the matching-defect and compatible-semantics checks are PASS. UNKNOWN permits further probes only.

```arex-contract-v4
{
  "id": "workflow:verified-history:3d852bae39e6f31c4d255bd3:probe",
  "intent": "Establish semantic owner bindings and current applicability.",
  "mechanism": "Compare public diagnostics and inspect try/handler aggregation.",
  "semantic_role": "return-analysis-applicability",
  "owner_role": "return-completeness-analyzer",
  "operation": "Read current analyzer and harness; observe public diagnostics and AST semantics without tracked-code edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "probed-analysis", "semantic_role": "return-analysis-checkout", "artifact_kind": "checkout-binding", "language": "python", "scope": "return-consistency", "phase": "repair", "state": "probed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "applicability-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "explicit-none-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-control-flow-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-runtime-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "observe-handler-paths",
      "instruction": "Record current hashed owner bindings, AST children, missing-warning reproduction, both explicit-None diagnostics, and adjacent expectations. Confirm no tracked-code edits. Mark compatibility and defect checks from actual observations.",
      "evidence_refs": ["pylint-dev/pylint:3468:body", "pylint-dev/pylint:3468:fix", "pylint-dev/pylint:3468:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3468:repair:fb332490c2e5"],
  "evidence_refs": ["pylint-dev/pylint:3468:body", "pylint-dev/pylint:3468:fix", "pylint-dev/pylint:3468:regression"],
  "read_set": ["role:return-completeness-analyzer", "role:return-consistency-regression-suite"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:3d852bae39e6f31c4d255bd3"
}
```

Empty source commands mean no current executable binding is supplied. Bind and render public current commands. Effects and outputs describe intended observations, not authoring-time execution.
