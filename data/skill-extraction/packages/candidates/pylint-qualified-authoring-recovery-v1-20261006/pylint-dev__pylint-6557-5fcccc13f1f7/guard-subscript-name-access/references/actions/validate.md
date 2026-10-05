# Validate public behavior

Bind and render current public reproduction and fixture commands. Run against the edited candidate with the relevant checker enabled. Inspect diagnostic messages and suite expectations as well as process status: unrelated ordinary lint warnings may produce a nonzero linter exit code.

Require absence of the reported exception and fatal analysis message, retention of supported Name-based diagnostics, and unchanged negative expectations.

```arex-contract-v4
{
  "id": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:validate",
  "intent": "Observe post-edit crash prevention and preserved diagnostic behavior.",
  "mechanism": "Analyze the public attribute-subscript reproduction and compare supported and negative cases with public diagnostic expectations.",
  "semantic_role": "public-repair-validation",
  "owner_role": "lookup-regression-suite",
  "operation": "Execute current bound public reproduction and repository fixture checks; record actual argv, exit statuses, messages, tested code anchors, and freshness relative to the candidate.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "guarded-lookup-candidate",
      "artifact_kind": "code-and-regression",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "lookup-validation-observations",
      "artifact_kind": "public-test-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "unsafe-name-read-guarded", "value": true, "evaluator": "evidence"},
    {"key": "attribute-subscript-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "supported-name-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-negative-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "attribute-subscript-no-crash",
      "instruction": "Run the current bound public static-analysis reproduction. Confirm the checker analyzes the loop and produces neither the reported AttributeError nor a fatal analysis message.",
      "evidence_refs": ["pylint-dev/pylint:6557:body", "pylint-dev/pylint:6557:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "lookup-diagnostics-retained",
      "instruction": "Run current bound public diagnostic fixtures and adjacent public checks. Verify supported Name-based redundant lookups retain their warnings, the attribute-subscript case gains no inappropriate lookup warning, and established negative expectations remain unchanged.",
      "evidence_refs": ["pylint-dev/pylint:6557:fix", "pylint-dev/pylint:6557:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6557:repair:5fcccc13f1f7"],
  "evidence_refs": ["pylint-dev/pylint:6557:body", "pylint-dev/pylint:6557:fix", "pylint-dev/pylint:6557:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0",
  "validation_for": ["workflow:verified-history:7c6d31165b0fa4f2628a0ec0:repair"],
  "read_set": ["role:lookup-checker", "role:lookup-regression-suite"],
  "write_set": []
}
```

A record containing failed checks is not successful validation. Establish the required successful effect only from passing current observations; record failures and stop. Running tests does not itself authorize further edits.
