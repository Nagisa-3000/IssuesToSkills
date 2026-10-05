# Inspect applicability

Locate the current checker and functional-test owners. Inspect the iterator domain, assignment guards, inference comparison, and exact failing dereference. An attribute iterator and the assignment's receiver are distinct objects: the historical repair changes iterator identifier extraction, not arbitrary receiver handling.

Record current role bindings and hashed anchors. Use only a current bound public reproduction. This operation reads and reports evidence without editing source. Missing interfaces or reproduction evidence remain UNKNOWN.

```arex-contract-v4
{
  "id": "workflow:verified-history:d4547bc8e3248f1130d70f73:inspect",
  "intent": "Establish whether the narrow iterator-field repair applies.",
  "mechanism": "Inspect AST variants, dictionary assignment guards, and the public attribute-copy failure.",
  "semantic_role": "applicability-probe",
  "owner_role": "iteration-checker",
  "operation": "Locate current checker and test owners, review public source and reproduction, and report iterator and guarded receiver forms without editing source.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "inspection",
      "semantic_role": "iterator-field-inspection",
      "artifact_kind": "source-review",
      "language": "python",
      "scope": "iteration-checker-and-tests",
      "phase": "pre-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "applicability-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "simple-name-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inference-guards-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-mutation-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-ast-shapes",
      "instruction": "Record current owner bindings and hashed code anchors. Confirm Name.name, Attribute.attrname, the unsupported iterator access, the separately guarded target receiver, and the public copy-loop failure. Report absent evidence as UNKNOWN and confirm source was not edited.",
      "evidence_refs": ["pylint-dev/pylint:7461:body", "pylint-dev/pylint:7461:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:7461:repair:fb30fe09d74d"],
  "evidence_refs": ["pylint-dev/pylint:7461:body", "pylint-dev/pylint:7461:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:d4547bc8e3248f1130d70f73",
  "read_set": ["role:iteration-checker", "role:iteration-functional-tests"],
  "write_set": [],
  "exclusions": [
    {"key": "incompatible-ast-interface", "value": true, "evaluator": "evidence"}
  ]
}
```
