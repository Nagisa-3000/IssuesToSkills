# Validate the candidate and retained diagnostics

Bind public commands to the current checkout's diagnostic runner. Run the paired cases and adjacent exception/control-flow fixtures. Record exact diagnostics and results, not merely command exit status. If any result is missing, validation remains UNKNOWN; if a retained diagnostic disappears, validation fails.

Historical fixtures and expected-message files supply assertions. They do not establish that historical CI ran, and the later qualification does not execute this Action.

```arex-contract-v4
{
  "id": "workflow:verified-history:88758c6085df4be35e45f76d:validate",
  "intent": "Observe that the nonlocal false positive is removed and genuine local/control-flow errors remain.",
  "mechanism": "Check paired name-specific fixtures and retained adjacent expected diagnostics against the edited analyzer.",
  "semantic_role": "public-repair-validation",
  "owner_role": "assignment-regression-suite",
  "kind": "validate",
  "operation": "Run bound public reproduction and repository fixture checks, review the guard placement, and record fresh results without editing source or expectations.",
  "inputs": [
    {"name": "candidate", "semantic_role": "nonlocal-filter-candidate", "artifact_kind": "checkout-change", "language": "python", "scope": "current-public-checkout", "phase": "post-edit", "state": "awaiting-validation", "optional": false}
  ],
  "outputs": [
    {"name": "validation", "semantic_role": "public-repair-validation", "artifact_kind": "validation-record", "language": "python", "scope": "current-public-checkout", "phase": "post-validation", "state": "observed-results", "optional": false}
  ],
  "preconditions": [
    {"key": "name-specific-nonlocal-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "paired-regression-assertions-installed", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unrelated-nonlocal-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-control-flow-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "paired-nonlocal-cases",
      "instruction": "Run the current public paired cases. Require no used-before-assignment for the explicitly declared nonlocal name, and require that diagnostic for the local queried name when only an unrelated name is declared nonlocal.",
      "evidence_refs": ["pylint-dev/pylint:5965:body", "pylint-dev/pylint:5965:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-diagnostic-fixtures",
      "instruction": "Run the bound public diagnostic fixture suite covering existing exception-handler and control-flow cases. Compare message identities and locations to the retained expectations. Review that earlier candidate resolution is preserved.",
      "evidence_refs": ["pylint-dev/pylint:5965:fix", "pylint-dev/pylint:5965:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:88758c6085df4be35e45f76d:repair"],
  "source_ids": ["pylint-dev/pylint:5965:repair:025200c1fdb5"],
  "evidence_refs": ["pylint-dev/pylint:5965:body", "pylint-dev/pylint:5965:fix", "pylint-dev/pylint:5965:regression"],
  "read_set": ["role:assignment-filter", "role:assignment-regression-suite"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:88758c6085df4be35e45f76d"
}
```
