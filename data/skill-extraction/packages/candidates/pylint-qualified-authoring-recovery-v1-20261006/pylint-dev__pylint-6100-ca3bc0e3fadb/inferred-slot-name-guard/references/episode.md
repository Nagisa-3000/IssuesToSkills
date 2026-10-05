# Historical episode

Authoritative source: `pylint-dev/pylint:6100:repair:ca3bc0e3fadb`.

The report described a crash in Pylint 2.13.4 with astroid 2.11.2, using Python 3.8.8 on macOS 11.6.4. Its minimal public reproduction was:

```python
class MyClass:
    __slots__ = [str]
```

The command reported was `pylint test.py`. The traceback reached `_check_redefined_slots`, where `slots_names.append(inferred_slot.value)` raised `AttributeError: 'ClassDef' object has no attribute 'value'`. The expected behavior was that the analyzer not crash.

The merged repair at revision `ca3bc0e3fadb83972ba339cb4a0de99fc0300d8c` changed the inferred branch in historical `pylint/checkers/classes/class_checker.py`:

```python
inferred_slot = safe_infer(slot)
inferred_slot_value = getattr(inferred_slot, "value", None)
if isinstance(inferred_slot_value, str):
    slots_names.append(inferred_slot_value)
```

It replaced a truthiness check followed by unconditional `.value` access. It did not rewrite the direct constant branch or the ancestor-slot comparison.

The committed regression in historical `tests/functional/r/redefined/redefined_slots.py` added the `[str]` class and disabled `invalid-slots-object` alongside `too-few-public-methods` for that fixture. Existing inherited-slot assertions remained. This suppression isolates a no-crash test; it is not a recommendation to suppress invalid-slot diagnostics in normal use.

Historical CI/test execution is unknown from the supplied historical entries. The assertions were available at the repair commit, not evidence of a newly executed Skill evaluation.

## Validation-only qualification

The independently supplied qualification was checked at `2026-10-04T13:55:08.540823+00:00`. It pinned original base `fcf220dde5370967c2320a2fd66c2b633b9cc68b`, the supplied repair revision, and a direct-closure relationship to issue 6100 / PR 6112.

Complete supplied controls show:
- Original base: six selected functional cases passed.
- Base with the committed regression: the slot case failed with the reported missing-`value` crash; five other selected cases passed.
- Historical fixed revision: all six selected cases passed.

The runs used the same supplied runtime digest, did not time out, and exited respectively 0, 1, and 0. The qualification's closure reference is validation metadata, not a newly authored historical evidence card.

Scope: `changed-test-files-with-original-base-control`.

Limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

This qualification neither backdates its observations nor executes the authored Skill functional cases.

## Historical evidence

- [Title](evidence/title.md)
- [Report](evidence/body.md)
- [Implementation](evidence/fix.md)
- [Committed regression assertions](evidence/regression.md)
