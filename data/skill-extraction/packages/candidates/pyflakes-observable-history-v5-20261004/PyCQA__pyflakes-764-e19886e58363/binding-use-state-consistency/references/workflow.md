# Historical workflow: restore structured use metadata

The evidenced repair restores a producer representation relied on by a downstream consumer. Inspection is a reusable operation grounded in the reported traceback and supplied diff; it is not a claim that a particular historical investigation sequence was executed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:a9020121b14a346d4f659c0e",
  "goal": "Prevent the annotation-read and local-assignment interaction from crashing while retaining undefined-name and unused-local diagnostics.",
  "mechanism": "Store scope and node metadata for annotation-only binding reads instead of a boolean, then assert the interacting diagnostic behavior.",
  "action_ids": [
    "workflow:verified-history:a9020121b14a346d4f659c0e:inspect",
    "workflow:verified-history:a9020121b14a346d4f659c0e:repair",
    "workflow:verified-history:a9020121b14a346d4f659c0e:regression",
    "workflow:verified-history:a9020121b14a346d4f659c0e:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:764:repair:e19886e58363"],
  "required_effects": [
    {"key": "annotation-use-metadata", "value": "scope-and-node", "evaluator": "evidence"},
    {"key": "interaction-regression", "value": "present", "evaluator": "evidence"},
    {"key": "interaction-diagnostics", "value": "undefined-name-and-unused-local-without-crash", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "annotation-read-remains-undefined", "value": true, "evaluator": "evidence"},
    {"key": "unused-local-remains-reported", "value": true, "evaluator": "evidence"},
    {"key": "postponed-annotation-branch-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:a9020121b14a346d4f659c0e:inspect",
      "after": "workflow:verified-history:a9020121b14a346d4f659c0e:repair",
      "reason": "Confirm the producer writes a boolean and the scope-sensitive consumer expects structured use metadata before editing.",
      "evidence_refs": ["PyCQA/pyflakes:764:body", "PyCQA/pyflakes:764:fix"]
    },
    {
      "before": "workflow:verified-history:a9020121b14a346d4f659c0e:inspect",
      "after": "workflow:verified-history:a9020121b14a346d4f659c0e:regression",
      "reason": "Locate the current public diagnostic harness and preserve the three-part reproduction.",
      "evidence_refs": ["PyCQA/pyflakes:764:body", "PyCQA/pyflakes:764:regression"]
    },
    {
      "before": "workflow:verified-history:a9020121b14a346d4f659c0e:repair",
      "after": "workflow:verified-history:a9020121b14a346d4f659c0e:validate",
      "reason": "The modified producer must be checked for crash freedom and preserved diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:764:fix", "PyCQA/pyflakes:764:regression"]
    },
    {
      "before": "workflow:verified-history:a9020121b14a346d4f659c0e:regression",
      "after": "workflow:verified-history:a9020121b14a346d4f659c0e:validate",
      "reason": "Execute the added assertion and adjacent annotation tests against the final implementation.",
      "evidence_refs": ["PyCQA/pyflakes:764:regression"]
    }
  ]
}
```
