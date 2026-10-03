# Historical episode

Authoritative source: `PyCQA/pyflakes:633:repair:e02336c3d47c`  
Issue: `PyCQA/pyflakes:633`  
Fix: `PyCQA/pyflakes:pr:698`  
Revision: `e02336c3d47c621feed730f5bdaa792babca75be`

## Report

The [issue title](evidence/title.md) states that an assignment expression in a comprehension should target the outer scope.

The [original report](evidence/body.md) uses:

```python
if any((match := pattern.match(item)) for item in list):
    word = match.group(0)
```

For the supplied names and pattern, the reporter described runtime output `"JOHN"` but an F821 undefined-name diagnostic for `match` at the enclosing use. The reported environment was flake8 3.9.2, Pyflakes 2.3.1, and CPython 3.9.5 on Windows. This is a user-reported reproduction, not an independent execution transcript.

## Merged repair

The [implementation evidence](evidence/fix.md) changes historical `pyflakes/checker.py`:

- Adds `NamedExprAssignment`, subclassing `Assignment`.
- Classifies a stored name as `NamedExprAssignment` when `PY38_PLUS` and `parent_stmt` is `ast.NamedExpr`.
- Starts binding insertion at scope-stack position `-1`.
- For `NamedExprAssignment` only, walks outward while the selected scope is `GeneratorScope`.
- Inserts into the resulting scope instead of unconditionally into `self.scope`.

The implementation comment identifies the scope in which the outermost generator is defined. The existing annotation guard remains. Ordinary assignment bindings do not enter the new outward-routing loop.

These historical symbols locate the evidenced implementation; current use must bind equivalent semantic owners explicitly.

## Added assertions

The [regression evidence](evidence/regression.md) changes historical `pyflakes/test/test_other.py`, adding two methods to `TestUnusedAssignment`. Both skip runtimes older than Python 3.8.

`test_assign_expr_generator_scope` supplies:

```python
if (any((y := x[0]) for x in [[True]])):
    print(y)
```

`test_assign_expr_nested` supplies:

```python
if ([(y:=x) for x in range(4) if [(z:=q) for q in range(4)]]):
    print(y)
    print(z)
```

Both call `self.flakes` without expected diagnostic arguments, asserting diagnostic-free analysis. Their historical execution status is unknown from the supplied assertions; no test log was provided.

## Qualification boundary

The supplied qualification attestation was checked at `2026-10-03T19:13:35.956664+00:00`. It reports verified resolution within `changed-test-files-with-original-base-control`, with two fail-to-pass and 123 pass-to-pass checks.

This later qualification is not backdated to the historical commit or the 2024 cutoff. It does not establish whole-project regression safety or cross-project transfer. It is retained separately in [provenance](provenance.json).

The applicability probe and adjacent checks in this package are current-use obligations grounded in the report and repair, not invented historical investigation or execution events.
