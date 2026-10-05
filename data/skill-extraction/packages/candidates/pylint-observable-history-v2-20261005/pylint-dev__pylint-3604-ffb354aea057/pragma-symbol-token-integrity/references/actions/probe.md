# Locate owners and establish fragmentation

Read the current Python pragma parser, token specification, and public parser tests. Bind their semantic roles to real current objects and record code hashes. Run a public minimal parser probe without editing source. Determine whether underscore omission actually fragments the supported name.

Check registration or documented supported naming when available. Numeric-ID success alone is not proof of this mechanism. Do not install historical plugins or clone historical applications merely because the issue report did so.

Output the diagnosed PortValue only if owners and omission are established. If evidence is incomplete, record UNKNOWN and request additional public probes; do not certify the output state.

```arex-contract-v4
{
  "id": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:probe",
  "intent": "Determine whether symbolic-message fragmentation is caused by an omitted underscore.",
  "mechanism": "Compare exact parser output with the current symbolic-message token class and public adjacent controls.",
  "semantic_role": "diagnose-identifier-fragmentation",
  "owner_role": "pragma-parser",
  "operation": "Locate current parser and test owners, inspect supported naming, and run read-only public parser probes without source edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "diagnosed-checkout", "semantic_role": "bound-pragma-repair-target", "artifact_kind": "checkout-evidence", "language": "python", "scope": "current-public-checkout", "phase": "diagnosis", "state": "owners-bound-and-omission-established"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "repair-owner-bound", "value": true, "evaluator": "evidence"},
    {"key": "underscore-omission-established", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-pragma-grammar-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "establish-fragmentation",
      "instruction": "Record current owner anchors and exact parser action/messages output. Establish underscore exclusion, its causal fragmentation, and consistency of underscore with supported message naming. Compare ordinary symbols and numeric identifiers where supported. Confirm no source writes.",
      "evidence_refs": ["pylint-dev/pylint:3604:body", "pylint-dev/pylint:3604:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3604:repair:ffb354aea057"],
  "evidence_refs": ["pylint-dev/pylint:3604:body", "pylint-dev/pylint:3604:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8",
  "read_set": ["role:pragma-parser", "role:pragma-message-token-specification", "role:pragma-parser-tests", "role:message-registry"],
  "write_set": [],
  "exclusions": [
    {"key": "identifier-already-intact", "value": true, "evaluator": "evidence"},
    {"key": "underscore-intentionally-forbidden", "value": true, "evaluator": "evidence"}
  ]
}
```
