# Repair format routing and diagnostics

Use the inspected owners and current native inventory. Share that inventory between help and native/delegated routing; do not blindly copy historical formats.

For delegated requests, check Graphviz availability, announce fallback, and query `dot -T?` using captured UTF-8 output with `check=False`. Parse the advertised stderr list and compare exact tokens. Explicit non-support produces a Graphviz-specific diagnostic and the compatible application failure code; historically this was 32. Missing Graphviz uses a dependency-specific message. Unparseable capability output warns and continues.

Remove downstream availability checks only when every affected conversion path is protected. Add public supported, uninterpretable-capability, and unsupported regression assertions; update public help and relevant release documentation. Do not normalize leading dots.

```arex-contract-v4
{
  "id": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:repair",
  "intent": "Separate native support from Graphviz fallback diagnostics.",
  "mechanism": "Shared native inventory plus early backend availability and exact-token capability checks, with permissive inconclusive discovery.",
  "semantic_role": "format-diagnostic-repair",
  "owner_role": "output-format-routing",
  "operation": "Edit currently bound inventory/help, routing, Graphviz utilities, safely redundant conversion checking, public assertions and associated documentation according to this card.",
  "kind": "edit",
  "inputs": [
    {
      "name": "ownership-map",
      "semantic_role": "format-ownership-map",
      "artifact_kind": "public-code-observations",
      "language": "python",
      "scope": "current-checkout-output-format-routing",
      "phase": "pre-edit",
      "state": "inspected",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "format-repair",
      "semantic_role": "format-diagnostic-change",
      "artifact_kind": "code-and-test-diff",
      "language": "python",
      "scope": "current-checkout-output-format-routing",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "format-ownership-established", "value": true, "evaluator": "evidence"},
    {"key": "graphviz-fallback-semantics-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:output-format-routing", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:graphviz-capability-check", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "native-and-backend-diagnostics-separated", "value": true, "evaluator": "evidence"},
    {"key": "public-format-regressions-defined", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "native-output-independent-of-graphviz", "value": true, "evaluator": "evidence"},
    {"key": "supported-output-writing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inconclusive-capability-fallback-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-import-path-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-format-diff",
      "instruction": "Review the public diff for shared native inventory, native bypass, delegated preflight, exact-token membership, distinct missing and unsupported messages, warning-and-continue on unparseable output, protected conversion paths, regression definitions and absence of new leading-dot normalization. This review does not replace executable validation.",
      "evidence_refs": ["pylint-dev/pylint:5950:fix", "pylint-dev/pylint:5950:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:output-format-routing", "role:native-format-inventory", "role:graphviz-capability-check", "role:conversion-dispatch", "role:format-regression-tests"],
  "write_set": ["role:output-format-routing", "role:native-format-inventory", "role:graphviz-capability-check", "role:conversion-dispatch", "role:format-regression-tests", "role:cli-format-documentation"],
  "source_ids": ["pylint-dev/pylint:5950:repair:9c90db16a860"],
  "evidence_refs": ["pylint-dev/pylint:5950:fix", "pylint-dev/pylint:5950:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb"
}
```

The modifying operation retains the [validation Action](validate.md) in its verification closure. `public-validation-observed` becomes stale; preservation assurances remain required and are not invalidated.
