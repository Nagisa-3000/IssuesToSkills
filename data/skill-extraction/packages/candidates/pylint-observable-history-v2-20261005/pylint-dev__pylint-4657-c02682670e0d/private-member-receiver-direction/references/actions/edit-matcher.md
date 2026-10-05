# Modify the directional matcher

Retain private-attribute filtering and equal attribute names. Permit a `cls` write to match `cls` or `self` reads; permit a `self` write to match only `self` reads. Do not replace this with symmetric receiver equivalence.

These effects describe the intended edit, not observed repair success. The retained [validation Action](validate.md) must establish the public behavior.

```arex-contract-v4
{
  "id": "workflow:verified-history:8486fdf9c04144c10d14213f:edit-matcher",
  "intent": "Correct recognition of used class-private writes.",
  "mechanism": "Apply directional receiver compatibility while retaining attribute-name equality.",
  "semantic_role": "matcher-repair",
  "owner_role": "private-member-use-matcher",
  "operation": "Edit the located private assignment/read condition to allow cls-to-cls/self and self-to-self matching only.",
  "kind": "edit",
  "inputs": [
    {"name": "receiver-analysis", "semantic_role": "receiver-match-analysis", "artifact_kind": "evidence-record", "language": "Python", "scope": "current-private-member-checker", "phase": "inspection", "state": "confirmed"}
  ],
  "outputs": [
    {"name": "matcher-change", "semantic_role": "directional-private-member-matcher", "artifact_kind": "source-change", "language": "Python", "scope": "current-private-member-checker", "phase": "repair", "state": "edited"}
  ],
  "preconditions": [
    {"key": "role:private-member-use-matcher", "value": true, "evaluator": "symbol_exists"},
    {"key": "receiver-mechanism-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "directional-matcher-installed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "attribute-name-equality-required", "value": true, "evaluator": "evidence"},
    {"key": "instance-write-not-used-by-class-read", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-private-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-directional-edit",
      "instruction": "Review the diff for equal attribute names, retained private filtering, cls writes accepting cls/self reads, and self writes accepting self reads only. Retain runtime verification through the validate Action.",
      "evidence_refs": ["pylint-dev/pylint:4657:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:private-member-use-matcher"],
  "write_set": ["role:private-member-use-matcher"],
  "source_ids": ["pylint-dev/pylint:4657:repair:c02682670e0d"],
  "evidence_refs": ["pylint-dev/pylint:4657:fix"],
  "resource": "references/actions/edit-matcher.md",
  "package_id": "workflow:verified-history:8486fdf9c04144c10d14213f"
}
```
