# Validate the modified state

Run the current public analyzer trigger and matcher checks. Observe that invalid results are skipped before attribute access and that valid simple-name matches, qualified-name matches and nonmatches retain their meaning. A mixed stream must still recognize a valid result after invalid results.

Compare existing inference-error handling with the pinned base. These checks are authored preservation obligations, not claims of additional historical assertions.

Record PASS/FAIL/UNKNOWN for every required check. An unavailable required check yields UNKNOWN and blocks a passing repair claim.

```arex-contract-v4
{
  "id": "workflow:verified-history:7551c627c4b85df38e889528:validate",
  "intent": "Establish fresh public validation of the guarded matcher.",
  "mechanism": "Exercise the analyzer trigger and compare invalid-result safety with valid-result and exception behavior.",
  "semantic_role": "repair-validation",
  "owner_role": "analyzer-regression-suite",
  "operation": "Execute bound current public checks without modifying tracked source and record results for the exact edited state.",
  "kind": "validate",
  "inputs": [
    {"name": "guarded-checkout", "semantic_role": "decorator-matcher-repair", "artifact_kind": "source-change", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "pending-validation", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "decorator-repair-validation", "artifact_kind": "test-observations", "language": "python", "scope": "current-checkout", "phase": "post-validation", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "invalid-results-filtered-before-name-access", "value": true, "evaluator": "evidence"},
    {"key": "trigger-regression-retained", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observation-current", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-passed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "resolvable-decorator-matching-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inference-error-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-trigger",
      "instruction": "Run the current public analyzer regression containing the fixture-decorated open(...).read() input. Record its result and verify absence of the decorator-inference membership crash.",
      "evidence_refs": ["pylint-dev/pylint:4612:regression", "pylint-dev/pylint:4612:fix"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "check-adjacent-matching",
      "instruction": "Run current public checks for absent, uninferable, mixed, matching and nonmatching results. Compare valid-result and InferenceError behavior with the pinned base. Record PASS, FAIL or UNKNOWN for each required assurance.",
      "evidence_refs": ["pylint-dev/pylint:4612:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4612:repair:93d6c39e8fbb"],
  "evidence_refs": ["pylint-dev/pylint:4612:fix", "pylint-dev/pylint:4612:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:7551c627c4b85df38e889528",
  "validation_for": ["workflow:verified-history:7551c627c4b85df38e889528:guard"],
  "read_set": ["role:decorator-name-matcher", "role:analyzer-regression-suite"],
  "write_set": []
}
```

The declared effects describe successful validation. A record containing FAIL or UNKNOWN does not establish `public-validation-passed`. Any later edit makes the observation stale; prior passing evidence cannot authorize success for a different source state.
