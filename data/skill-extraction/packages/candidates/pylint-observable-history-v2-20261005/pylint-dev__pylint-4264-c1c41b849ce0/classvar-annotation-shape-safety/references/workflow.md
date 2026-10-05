# Historical realization

The contracts below derive from the original report, merged repair and committed assertions. Newly authored inspection and validation procedures are guidance, not claims that those procedures were historically executed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:8196d401013577b7b429876a",
  "goal": "Recognize direct and qualified ClassVar annotations safely while preserving naming behavior.",
  "mechanism": "Reject non-annotated assignments, unwrap one Subscript, and dispatch between Name.name and Attribute.attrname under type guards.",
  "action_ids": [
    "workflow:verified-history:8196d401013577b7b429876a:inspect",
    "workflow:verified-history:8196d401013577b7b429876a:repair",
    "workflow:verified-history:8196d401013577b7b429876a:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4264:repair:c1c41b849ce0"],
  "required_effects": [
    {"key": "shape-safe-classvar-recognition", "value": true, "evaluator": "evidence"},
    {"key": "qualified-classvar-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "direct-classvar-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-naming-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:8196d401013577b7b429876a:inspect",
      "after": "workflow:verified-history:8196d401013577b7b429876a:repair",
      "reason": "Confirm the annotation shape assumption and current owner bindings before editing.",
      "evidence_refs": ["pylint-dev/pylint:4264:body", "pylint-dev/pylint:4264:fix"]
    },
    {
      "before": "workflow:verified-history:8196d401013577b7b429876a:repair",
      "after": "workflow:verified-history:8196d401013577b7b429876a:validate",
      "reason": "Validate modified recognition and diagnostic assertions together; edits stale prior validation observations.",
      "evidence_refs": ["pylint-dev/pylint:4264:fix", "pylint-dev/pylint:4264:regression"]
    }
  ]
}
```
