# Historical episode

Authoritative repair source: `pylint-dev/pylint:8735:repair:33d3f22b767e`.

The [title](evidence/title.md) and [report](evidence/body.md) describe an analyzer crash on:

```python
nonlocal X
X = whatever
```

The reported assignment callback reached `VariablesChecker._check_self_cls_assign` in `pylint/checkers/variables.py`. It tried `node.scope().parent.scope()` when the current scope was a module with no parent. The output already included `nonlocal-without-binding`, then an `AttributeError` and fatal `astroid-error`. The report's environment was Ubuntu 18.04, CPython 3.11.3, Pylint 3.0.0b1, and astroid 3.0.0a3; those details are historical, not current requirements.

The [merged implementation](evidence/fix.md) changed the branch-selection expression from:

```python
nonlocals_with_same_name = any(
    child for child in scope.body if isinstance(child, nodes.Nonlocal)
)
```

to:

```python
nonlocals_with_same_name = node.scope().parent and any(
    child for child in scope.body if isinstance(child, nodes.Nonlocal)
)
```

The variable name does not imply a newly introduced matching-name filter: the shown expression detects the presence of a `Nonlocal` node. The repair short-circuits that branch when there is no parent. It does not catch all exceptions, remove the invalid-declaration diagnostic, or change Python language validity.

The [regression](evidence/regression.md) appended the following to `tests/functional/n/nonlocal_without_binding.py`:

```python
nonlocal APPLE  # [nonlocal-without-binding]
APPLE = 42
```

The paired `.txt` file added:

```text
nonlocal-without-binding:74:0:74:14::nonlocal name APPLE found without binding:HIGH
```

These are committed assertions available at the repair revision. The supplied historical core does not establish contemporaneous CI execution.

## Validation-only qualification

The later qualification was checked at `2026-10-04T18:16:27.409238+00:00`, after the learning cutoff. It pinned original base `59194ebfa600b91ec4d5cef49370b7132b0413a3` and fixed revision `33d3f22b767e4d4c959a7619d6e3c9f7e617e092`, verified direct closure of issue 8735 by PR 8737, and used the same runtime digest in all three controls.

The original base passed 19 selected tests. The base with committed regression failed `nonlocal_without_binding` with the missing-parent traceback and unexpected `astroid-error`; 18 other selected tests passed. The historical fixed revision passed all 19 selected tests. No run timed out. The report lists 19 original-base-to-fixed pass-to-pass cases, including the target fixture; that is distinct from the 18 unaffected cases in the base-with-regression control.

Scope: `changed-test-files-with-original-base-control`.
Limits: “Changed test files only; whole-project regression and cross-project transfer are untested.”

This qualification supports the historical repair's causal identity within that scope. Runtime details and replay logs are not new historical mechanism evidence. None of the newly authored Skill evaluation cases has been executed.
