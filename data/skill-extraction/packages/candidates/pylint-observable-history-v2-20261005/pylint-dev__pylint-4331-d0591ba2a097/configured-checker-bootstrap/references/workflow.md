# Historical realization

The contract represents the reported diagnosis, merged lifecycle change, and
committed assertion obligations. Its validation effects describe required
current observations, not an invented historical successful run.

```arex-workflow-v4
{
  "id": "workflow:verified-history:a8b32e3610a8e5ec2b10b833",
  "goal": "Make functional fixtures honor explicitly configured optional checkers and their options.",
  "mechanism": "Parse configuration, register requested modules before applying options, and distinguish activation from silent omission using reviewed diagnostic assertions.",
  "action_ids": [
    "workflow:verified-history:a8b32e3610a8e5ec2b10b833:inspect",
    "workflow:verified-history:a8b32e3610a8e5ec2b10b833:register",
    "workflow:verified-history:a8b32e3610a8e5ec2b10b833:fixtures",
    "workflow:verified-history:a8b32e3610a8e5ec2b10b833:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4331:repair:d0591ba2a097"],
  "required_effects": [
    {"key": "configured-registration-before-application", "value": true, "evaluator": "evidence"},
    {"key": "discriminating-plugin-assertions", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "public-checks-passed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-harness-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "missing-config-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:inspect",
      "after": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:register",
      "reason": "Confirm the omitted lifecycle step and compatible parser/loader semantics before editing.",
      "evidence_refs": ["pylint-dev/pylint:4331:body", "pylint-dev/pylint:4331:fix"]
    },
    {
      "before": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:inspect",
      "after": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:fixtures",
      "reason": "Identify the configured checker and silent plugin fixtures before authoring discriminating expectations.",
      "evidence_refs": ["pylint-dev/pylint:4331:body", "pylint-dev/pylint:4331:regression"]
    },
    {
      "before": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:register",
      "after": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:validate",
      "reason": "Public validation must observe the modified initialization sequence.",
      "evidence_refs": ["pylint-dev/pylint:4331:fix", "pylint-dev/pylint:4331:regression"]
    },
    {
      "before": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:fixtures",
      "after": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:validate",
      "reason": "Nonempty reviewed assertions must exist before validation can distinguish plugin activation from omission.",
      "evidence_refs": ["pylint-dev/pylint:4331:regression"]
    }
  ]
}
```

See [inspect](actions/inspect.md), [register](actions/register.md),
[fixtures](actions/fixtures.md), and [validate](actions/validate.md).
Current ordering follows semantic prerequisites and ports, not historical list
position.
