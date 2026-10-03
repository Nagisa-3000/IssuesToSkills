# Historical episode

Authoritative source: `PyCQA/pyflakes:395:repair:066ba4a93c10`.

The [issue title](evidence/title.md) and [report](evidence/body.md) describe a false undefined-name diagnostic under Python 3.7.1 and pyflakes 2.0.0:

```python
a: int = 2
print(__annotations__)
```

The report says this emitted `t.py:3: undefined name '__annotations__'`. Its proposed magic-global solution is a reporter suggestion, not an instruction or proof of a general policy.

The [merged implementation](evidence/fix.md), available at revision `066ba4a93c1077f9154d6ff3806fe1e3a66843a1`, added a Python 3.6 capability flag and conditionally appended `__annotations__` to the module magic-global registry. It also replaced the negative Python-before-3.5 flag with a positive Python-3.5-and-later flag while preserving the corresponding synchronous and asynchronous loop type branches.

The [regression assertion](evidence/regression.md) added a test of bare module-level `__annotations__`, skipped before Python 3.6. This establishes the historical analyzer policy, which is broader than proving runtime initialization in the particular reported program.

## Historical resource locations

- `pyflakes/checker.py`: version flags, `_MAGIC_GLOBALS`, `FOR_TYPES`, and `LOOP_TYPES`.
- `pyflakes/test/test_undefined_names.py`: `test_moduleAnnotations` and adjacent magic-global tests.

These paths are historical locators, not current bindings. Reusable operations use semantic owners.

## Verification status

The supplied source is marked independently resolved. No historical command execution or whole-project test result is supplied. Regression code is recorded as an assertion available at the historical commit.

A qualification attestation checked on `2026-10-03T19:13:03.255984+00:00` reports one fail-to-pass and 61 pass-to-pass cases with changed-test-files-with-original-base-control scope. It is later provenance, not pre-cutoff learned content or a backdated historical execution.

The canonical Workflow reconstructs inspection, editing, and validation obligations from these artifacts. It does not claim that every operation was logged as an executed historical step.
