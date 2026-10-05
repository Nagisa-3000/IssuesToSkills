# Historical episode

SourceRecord: `pylint-dev/pylint:5989:repair:5c8384e811e3`.

The March 26, 2022 report described a missing `W0212` / `protected-access` diagnostic in version 2.13.0 that had appeared in 2.12.2. Its reproduction accessed a protected property through the first argument of an ordinary function:

```python
class Light:
    @property
    def _light_internal(self) -> set[str]:
        return set()

def func(light: Light) -> None:
    print(light._light_internal)
```

The report identified `_is_mandatory_method_param` as the exemption path preventing the protected-access check.

## Historical implementation

In `pylint/checkers/classes/class_checker.py`, the repair added:

```python
if not closest_func.is_bound():
    return False
```

This guard was placed after the nearest-function absence check and before the empty-argument check in the fallback first-parameter classification. The helper documentation explicitly stated that static methods return false.

A separate changed branch in the same file replaced:

```python
if self._is_type_self_call(attribute.expr):
```

with:

```python
if isinstance(attribute.expr, nodes.Call):
```

The supplied diff supports that replacement, but does not independently demonstrate its causal contribution to the reported ordinary-function false negative.

## Historical regression assertions

`tests/functional/p/protected_access.py` added a `Light` protected property returning `None`, a static method accessing that property through its first argument, and an ordinary function doing the same. Both accesses carried `[protected-access]` annotations.

`tests/functional/p/protected_access.txt` added expected diagnostics for `Light.func` at line 39 and `func` at line 43. The previous expectations at lines 17 and 29 remained.

The ChangeLog described a false-negative regression in 2.13.0 where protected-access was not raised on functions, with “Fixes #5989.”

These are implementation and committed assertion facts, not a claim that historical CI ran successfully. Historical execution status is unknown.

## Validation-only qualification

A later report checked the pinned original base `6279ab18f5cb9e74f83ff48e353ddef769fac7a7` and historical fixed revision `5c8384e811e39aa59bf7d6f627293f0b7675e057`, with direct-closure identity evidence for issue 5989 and PR 5990.

The complete supplied controls show:
- Original base: exit 0; 18 passed, 2 skipped.
- Base with committed regression: exit 1; 1 failed, 17 passed, 2 skipped. The protected-access case lacked the expected diagnostic at line 43.
- Historical fixed state: exit 0; 18 passed, 2 skipped.
- Runtime digests agree across all three runs; none timed out.
- The reported fail-to-pass set contains the protected-access functional case.

This qualification was performed on October 4, 2026. It is validation-only and is not backdated historical knowledge. Its scope is changed test files with original-base control, not whole-project regression or transfer. It supplies no execution result for newly authored Skill evaluation cases.
