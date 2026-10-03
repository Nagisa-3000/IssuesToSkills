# Canonical historical Workflow

The Actions describe supported operations and validation obligations. Their inclusion does not claim present-day execution or an undocumented historical test run.

```arex-workflow-v4
{
  "id": "explicit-type-alias-string-analysis",
  "goal": "Count references in quoted explicit type-alias values without changing ordinary assignment-value analysis.",
  "mechanism": "Use scope-aware TypeAlias recognition to route a present alias value through existing annotation processing.",
  "action_ids": [
    "explicit-type-alias-string-analysis.inspect",
    "explicit-type-alias-string-analysis.route",
    "explicit-type-alias-string-analysis.tests",
    "explicit-type-alias-string-analysis.validate"
  ],
  "source_ids": ["PyCQA/pyflakes:671"],
  "required_effects": [
    {"key": "quoted-alias-import-counted", "value": true, "evaluator": "evidence"},
    {"key": "targeted-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "public-regressions-checked", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-value-dispatch-preserved", "value": true, "evaluator": "evidence"},
    {"key": "no-value-does-not-use-unrelated-import", "value": true, "evaluator": "evidence"},
    {"key": "target-and-marker-analysis-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "explicit-type-alias-string-analysis.inspect",
      "after": "explicit-type-alias-string-analysis.route",
      "reason": "Establish current dispatch applicability and bind existing handlers before editing.",
      "evidence_refs": ["PyCQA/pyflakes:671:body", "PyCQA/pyflakes:671:fix"]
    },
    {
      "before": "explicit-type-alias-string-analysis.route",
      "after": "explicit-type-alias-string-analysis.tests",
      "reason": "This realization adds assertions for the changed dispatch; current plans may reuse equivalent existing coverage after inspection.",
      "evidence_refs": ["PyCQA/pyflakes:671:fix", "PyCQA/pyflakes:671:regression"]
    },
    {
      "before": "explicit-type-alias-string-analysis.route",
      "after": "explicit-type-alias-string-analysis.validate",
      "reason": "The implementation modification requires final behavioral validation.",
      "evidence_refs": ["PyCQA/pyflakes:671:fix", "PyCQA/pyflakes:671:regression"]
    },
    {
      "before": "explicit-type-alias-string-analysis.tests",
      "after": "explicit-type-alias-string-analysis.validate",
      "reason": "Execute assertions against the final modified implementation and tests.",
      "evidence_refs": ["PyCQA/pyflakes:671:regression"]
    }
  ]
}
```
