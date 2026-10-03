# Validate nested annotation analysis and adjacent behavior

Run public checks against the patched current checkout. Record the command, interpreter, exit status, diagnostics and tested scope. Refresh invalidated anchors and observations.

## Public regression matrix

- `Optional['Queue[str]']` uses the imported `Queue`.
- `"Optional['Queue[str]']"` processes a nested quoted annotation discovered during deferred work.
- With postponed annotations, `Optional['Queue[str]']` retains annotation context.
- `Literal['some string']` is not parsed as Python syntax.
- `Literal['some string', 'foo bar']` likewise remains value syntax.
- Check recognized `typing` and `typing_extensions` forms.
- Preserve existing overload behavior, including qualified `typing_extensions.overload`.
- Check ordinary strings, context restoration and string-valued AST constants for the supported interpreter range.

The supplied historical regressions directly assert the first seven areas, with some recognized forms established by implementation rather than a dedicated new test. The final checks are current preservation probes derived from changed visitor/context behavior; they are not invented historical test executions.

```arex-contract-v4
{
  "id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:validate",
  "intent": "Observe whether the candidate fixes nested annotation name usage without regressing adjacent typing or string behavior.",
  "mechanism": "Run bound public reproductions and repository annotation regressions, then inspect context and dispatch preservation.",
  "semantic_role": "annotation-traversal-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "validate-target-and-preservation",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate-analysis",
      "semantic_role": "annotation-analysis-candidate",
      "artifact_kind": "patched-python-checkout",
      "language": "python",
      "scope": "annotation-analysis",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-observations",
      "semantic_role": "annotation-analysis-validation",
      "artifact_kind": "public-validation-report",
      "language": "python",
      "scope": "annotation-analysis",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "candidate-patch-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "target-and-preservation-results-recorded", "value": true, "evaluator": "evidence"},
    {"key": "invalidated-observations-refreshed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "candidate-source-unmodified-by-validation", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "nested-annotation-public-reproduction",
      "instruction": "Run the current public partial-quotation reproduction and nested whole-quotation variant; verify imported types are treated as used and no spurious forward-annotation diagnostic appears. Also check postponed annotations when supported.",
      "evidence_refs": ["PyCQA/pyflakes:447:body", "PyCQA/pyflakes:447:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-adjacent-regressions",
      "instruction": "Run the bound current annotation regression suite, including Literal values from both typing modules, multi-value Literal strings, existing overload cases and supported AST string forms. Record preservation probes for ordinary strings and exception-safe context restoration, and report skipped or unavailable checks as unknown.",
      "evidence_refs": ["PyCQA/pyflakes:447:fix", "PyCQA/pyflakes:447:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:447:repair:c9708a18a17f"],
  "evidence_refs": ["PyCQA/pyflakes:447:body", "PyCQA/pyflakes:447:fix", "PyCQA/pyflakes:447:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0",
  "validation_for": ["workflow:verified-history:b2b64a5ca411f99a2e3c45e0:repair"],
  "read_set": [
    "role:python-annotation-analysis",
    "role:python-string-node-dispatch",
    "role:python-deferred-analysis",
    "role:typing-construct-recognition",
    "role:annotation-regression-tests"
  ],
  "write_set": []
}
```

A report may contain `FAIL` or `UNKNOWN`; producing it does not imply success. No historical command is supplied or authorized by the evidence. Adapt to the current public test runner and render the bound argv before execution. Do not incorporate hidden-test or gold-derived commands.
