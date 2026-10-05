# Historical Workflow

This realization separates literal representation, Sphinx recognition, and signature-name normalization. Dependencies express semantic requirements, not a claim about the historical author's exact editing chronology.

```arex-workflow-v4
{
  "id": "workflow:verified-history:f2490b7f20db2a942170750b",
  "goal": "Recognize escaped Sphinx variadic fields and match their normalized names to signatures.",
  "mechanism": "Accept ordinary names or backslash-prefixed one/two-star names in the Sphinx recognizer, remove the recognized escape during extraction, and align raw examples and diagnostic assertions.",
  "action_ids": [
    "workflow:verified-history:f2490b7f20db2a942170750b:probe",
    "workflow:verified-history:f2490b7f20db2a942170750b:repair",
    "workflow:verified-history:f2490b7f20db2a942170750b:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5406:repair:608ed329aaee"],
  "required_effects": [
    {"key": "escaped-variadics-match-signatures", "value": true, "evaluator": "evidence"},
    {"key": "unescaped-starred-fields-do-not-satisfy-docs", "value": true, "evaluator": "evidence"},
    {"key": "required-public-checks-pass", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-parameter-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-google-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:f2490b7f20db2a942170750b:probe",
      "after": "workflow:verified-history:f2490b7f20db2a942170750b:repair",
      "reason": "Locate recognition/extraction owners and confirm the style-specific escape policy before editing.",
      "evidence_refs": ["pylint-dev/pylint:5406:body", "pylint-dev/pylint:5406:fix"]
    },
    {
      "before": "workflow:verified-history:f2490b7f20db2a942170750b:repair",
      "after": "workflow:verified-history:f2490b7f20db2a942170750b:validate",
      "reason": "Validate recognition, normalized matching, raw examples, and diagnostic assertions against the modified state.",
      "evidence_refs": ["pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"]
    }
  ]
}
```
