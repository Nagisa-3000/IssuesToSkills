# Canonical Workflow

Establish the scope/traversal defect before applying the narrow exclusion, then verify both sides of the annotation/body boundary. The edit must not eliminate all processing of return annotations.

```arex-workflow-v4
{
  "id": "workflow:verified-history:46d18832864f51ea6f6d3968",
  "goal": "Resolve method return annotations in the appropriate enclosing context without accepting body-local names.",
  "mechanism": "Exclude return annotations from function-child traversal after function scope entry, preserving their appropriate enclosing-context processing and the existing decorator exclusion.",
  "action_ids": [
    "workflow:verified-history:46d18832864f51ea6f6d3968:inspect",
    "workflow:verified-history:46d18832864f51ea6f6d3968:edit",
    "workflow:verified-history:46d18832864f51ea6f6d3968:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:441:repair:4a807d45f9dd"],
  "required_effects": [
    {"key": "class-bound-return-name-accepted", "value": true, "evaluator": "evidence"},
    {"key": "body-only-return-name-rejected", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "decorator-inner-traversal-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "return-annotations-still-analyzed", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:46d18832864f51ea6f6d3968:inspect",
      "after": "workflow:verified-history:46d18832864f51ea6f6d3968:edit",
      "reason": "The traversal owner and a retained correct annotation-processing pass must be established before omitting the inner visit.",
      "evidence_refs": ["PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:body"]
    },
    {
      "before": "workflow:verified-history:46d18832864f51ea6f6d3968:edit",
      "after": "workflow:verified-history:46d18832864f51ea6f6d3968:validate",
      "reason": "The traversal change must satisfy both class-bound and body-local regression assertions.",
      "evidence_refs": ["PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"]
    }
  ]
}
```
