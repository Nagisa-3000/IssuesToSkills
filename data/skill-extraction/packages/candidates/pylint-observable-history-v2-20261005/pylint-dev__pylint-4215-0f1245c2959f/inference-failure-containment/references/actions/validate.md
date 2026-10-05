# Validate containment and preservation

Run the bound current public checks after both edits. Capture command, exit status, diagnostics, and traceback presence. Compare existing inferable-length and generator/comprehension cases with retained expectations. Report only the scope actually executed.

```arex-contract-v4
{
  "id": "workflow:verified-history:4cd11cf9432439d81e30121e:validate",
  "intent": "Observe containment and retained independent and adjacent diagnostics.",
  "mechanism": "Execute public diagnostic regressions and compare complete expected output for unresolved and supported inputs.",
  "semantic_role": "post-edit-public-validation",
  "owner_role": "length-condition-regression-suite",
  "operation": "Run current bound public commands after both modifications and record actual outcomes, including any diagnostic or traceback mismatch.",
  "kind": "validate",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "inference-failure-contained", "value": true, "evaluator": "evidence"},
    {"key": "unresolved-length-regressions-defined", "value": true, "evaluator": "evidence"},
    {"key": "role:length-condition-regression-suite", "value": true, "evaluator": "file_exists", "description": "The current public fixture suite is located and bound."}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "independent-variable-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inferable-length-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "unresolved-and-adjacent-diagnostics",
      "instruction": "Execute the bound public diagnostic suite. Both unresolved forms must retain undefined-variable diagnostics without uncaught inference tracebacks or speculative len-as-condition messages. Existing inferable-length and generator/comprehension expectations must remain unchanged. Interpret exit status using the current harness.",
      "evidence_refs": ["pylint-dev/pylint:4215:fix", "pylint-dev/pylint:4215:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4215:repair:0f1245c2959f"],
  "evidence_refs": ["pylint-dev/pylint:4215:fix", "pylint-dev/pylint:4215:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:4cd11cf9432439d81e30121e",
  "read_set": ["role:length-condition-checker", "role:length-condition-regression-suite"],
  "write_set": [],
  "validation_for": [
    "workflow:verified-history:4cd11cf9432439d81e30121e:guard",
    "workflow:verified-history:4cd11cf9432439d81e30121e:regression"
  ]
}
```

A failing run is an observation, not successful validation. Mark the Oracle FAIL. Stop or revise within supported bounds; subsequent edits make the observation stale and require re-execution.
