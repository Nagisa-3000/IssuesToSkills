# Historical repair Workflow

This reconstructs the public repair mechanism and its binding/verification closure. Inspection is an authored prerequisite, not a claim of a separately recorded historical task. No authored Actions have been executed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0",
  "goal": "Remove ClassVar-induced constant naming false positives and apply configured constant naming to Final.",
  "mechanism": "Parameterize outer-annotation recognition and select Final instead of ClassVar while retaining Enum classification and configured naming.",
  "action_ids": [
    "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:inspect",
    "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:repair",
    "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4277:repair:44a3aa25fd9b"],
  "required_effects": [
    {"key": "annotation-constant-policy", "value": "Final-not-ClassVar", "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "public-naming-checks-passed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "enum-naming-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "configured-constant-style-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-naming-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:inspect",
      "after": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:repair",
      "reason": "Bind and confirm the responsible annotation branch before editing.",
      "evidence_refs": ["pylint-dev/pylint:4277:body", "pylint-dev/pylint:4277:fix"]
    },
    {
      "before": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:repair",
      "after": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:validate",
      "reason": "Implementation and assertion edits require fresh differential and adjacent checks.",
      "evidence_refs": ["pylint-dev/pylint:4277:fix", "pylint-dev/pylint:4277:regression"]
    }
  ]
}
```

Historical paths are in [the episode](episode.md), not assumed current bindings. Current ordering follows compatible ports, prerequisites, semantic dependencies, and verification. An already satisfied operation may be omitted only with current evidence.
