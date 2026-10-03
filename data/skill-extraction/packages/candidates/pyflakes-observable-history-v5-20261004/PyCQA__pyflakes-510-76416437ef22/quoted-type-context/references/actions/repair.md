# Repair annotation-context entry at typing boundaries

Operate on the current semantic owner, not on historical filenames.

1. Reuse or generalize typing-member recognition. The historical helper checked nearest-scope bindings for direct imports from `typing` or `typing_extensions`, used the imported real name, and supported simple attributes rooted at those literal module names.
2. Introduce or reuse annotation-context entry that saves the prior state and restores it in `finally`. Route existing annotation entry through it where appropriate.
3. In subscription traversal, retain existing `Literal` special handling. Otherwise, enter annotation context for recognized typing members before visiting children. This permits nested quoted type expressions in aliases.
4. In call traversal, recognize typing `cast`; if a first positional argument exists and is a string literal, visit that argument under annotation context. Continue normal child traversal afterward. Do not put the whole call or second argument into annotation context.
5. Add or adapt public regression assertions for the supplied positive and negative cases.

The historical code used `ast.Str`; bind the equivalent string-literal predicate appropriate to the current Python AST. This adaptation is a current engineering decision, not separately verified historical support.

```arex-contract-v4
{
  "id": "workflow:verified-history:3f957b40be188975fdc11a7e:repair",
  "intent": "Recognize quoted type names at supported typing boundaries while preserving value-string semantics.",
  "mechanism": "Import-aware typing recognition plus scoped annotation-context traversal.",
  "semantic_role": "typing-boundary-repair",
  "owner_role": "python-annotation-traversal",
  "operation": "Modify typing-boundary traversal and add public regression assertions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "inspected-owner",
      "semantic_role": "python-annotation-traversal",
      "artifact_kind": "code-and-observation-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "inspection",
      "state": "inspected",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "modified-owner",
      "semantic_role": "python-annotation-traversal",
      "artifact_kind": "code-and-observation-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:python-annotation-traversal",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "Current traversal and annotation-state owners have been bound."
    },
    {
      "key": "supported-quoted-type-failure-reproduced",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "compatible-string-annotation-handler",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "quoted-type-names-count-as-used",
      "value": true,
      "evaluator": "evidence",
      "description": "Expected behavior after modification; must be independently validated."
    },
    {
      "key": "public-regression-assertions-added",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "ordinary-value-strings-not-type-parsed",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "annotation-context-restored",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "literal-special-handling-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "genuine-undefined-name-diagnostics-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "review-context-boundaries",
      "instruction": "Review the current diff for recognized typing boundaries, first-argument-only cast handling, preserved Literal handling, and exception-safe restoration; runtime acceptance is delegated to the validation Action.",
      "evidence_refs": ["PyCQA/pyflakes:510:fix", "PyCQA/pyflakes:510:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:python-annotation-traversal", "role:annotation-regression-tests"],
  "write_set": ["role:python-annotation-traversal", "role:annotation-regression-tests"],
  "invalidates": [
    "current-applicability-recorded",
    "quoted-type-diagnostic-observations",
    "adjacent-string-diagnostic-observations"
  ],
  "exclusions": [
    {
      "key": "interpret-all-strings-as-types",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "source_ids": ["PyCQA/pyflakes:510:repair:76416437ef22"],
  "evidence_refs": ["PyCQA/pyflakes:510:fix", "PyCQA/pyflakes:510:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:3f957b40be188975fdc11a7e"
}
```

Always retain [validation](validate.md) after this modification. Editing alone establishes no passing result.
