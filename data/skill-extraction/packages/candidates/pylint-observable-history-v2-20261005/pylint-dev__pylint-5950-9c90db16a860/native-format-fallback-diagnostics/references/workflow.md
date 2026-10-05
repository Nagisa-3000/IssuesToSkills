# Historical Workflow

This single-source realization models the verified repair's mechanism. Contract effects are requirements for current use, not newly observed execution results. Current ordering follows semantic prerequisites, compatible ports, and validation closure.

```arex-workflow-v4
{
  "id": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb",
  "goal": "Distinguish native formats from Graphviz fallback and provide accurate diagnostics without blocking generation on inconclusive capability discovery.",
  "mechanism": "Centralize native inventory for help and routing, preflight delegated requests, and preserve warning-and-continue behavior for uninterpretable backend output.",
  "action_ids": [
    "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:inspect",
    "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:repair",
    "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5950:repair:9c90db16a860"],
  "required_effects": [
    {"key": "format-ownership-established", "value": true, "evaluator": "evidence"},
    {"key": "native-and-backend-diagnostics-separated", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "native-output-independent-of-graphviz", "value": true, "evaluator": "evidence"},
    {"key": "supported-output-writing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inconclusive-capability-fallback-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-import-path-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:inspect",
      "after": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:repair",
      "reason": "Locate and establish compatible native and Graphviz owners before changing routing.",
      "evidence_refs": ["pylint-dev/pylint:5950:body", "pylint-dev/pylint:5950:fix"]
    },
    {
      "before": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:repair",
      "after": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:validate",
      "reason": "Observe final diagnostics, writer behavior, exits and adjacent behavior after implementation and assertion edits.",
      "evidence_refs": ["pylint-dev/pylint:5950:fix", "pylint-dev/pylint:5950:regression"]
    }
  ]
}
```
