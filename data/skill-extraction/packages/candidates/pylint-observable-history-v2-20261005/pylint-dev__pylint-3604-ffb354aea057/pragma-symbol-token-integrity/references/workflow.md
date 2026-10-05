# Historical realization: preserve supported pragma message symbols

Current ordering follows bound ports, prerequisites, semantic dependencies, and verification rather than historical list position. A probe may be omitted only when its outputs and prerequisites are already established by current public evidence. Retaining the edit always retains validation.

```arex-workflow-v4
{
  "id": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8",
  "goal": "Keep supported underscore-containing pragma message symbols intact while preserving adjacent grammar.",
  "mechanism": "Establish an omitted underscore in the symbolic-message token class, add only that character, and validate exact parser output.",
  "action_ids": [
    "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:probe",
    "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:repair",
    "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:validate"
  ],
  "source_ids": ["pylint-dev/pylint:3604:repair:ffb354aea057"],
  "required_effects": [
    {"key": "underscore-symbol-intact", "value": true, "evaluator": "evidence"},
    {"key": "current-public-validation-passed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "adjacent-pragma-grammar-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:probe",
      "after": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:repair",
      "reason": "Establish current ownership and omission-driven fragmentation before editing grammar.",
      "evidence_refs": ["pylint-dev/pylint:3604:body", "pylint-dev/pylint:3604:fix"]
    },
    {
      "before": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:repair",
      "after": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:validate",
      "reason": "The changed token class and authored regression need fresh exact-output and adjacent checks.",
      "evidence_refs": ["pylint-dev/pylint:3604:fix", "pylint-dev/pylint:3604:regression"]
    }
  ]
}
```
