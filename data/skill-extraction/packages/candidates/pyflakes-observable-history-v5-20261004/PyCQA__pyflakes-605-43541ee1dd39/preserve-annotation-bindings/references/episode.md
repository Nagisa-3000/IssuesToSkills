# Historical episode

Authoritative source: `PyCQA/pyflakes:605:repair:43541ee1dd39`.

The report described a regression after #535. Its simplified example imported `TYPE_CHECKING`, `List`, and `z`; assigned `__all__ = ("z",)` under `if not TYPE_CHECKING`; and declared `__all__: List[str]` in the alternative branch. The report stated that this annotation clobbered the `ExportBinding`, preventing export-based usage credit for imports.

The merged implementation changed insertion in historical `pyflakes/checker.py` from unconditional assignment to:

```python
if value.name not in self.scope or not isinstance(value, Annotation):
    self.scope[value.name] = value
```

The preceding `value.used` propagation was unchanged in the supplied diff. This was not blanket `setdefault`: ordinary incoming bindings still replaced existing entries, while annotations still inserted when the name was absent.

Historical `pyflakes/test/test_type_annotations.py` gained `test_type_annotation_clobbers_all`. It used the reproduction in a `self.flakes` call with no expected diagnostics and skipped Python versions below 3.6. This is an assertion available at the repair commit; no historical execution log is supplied.

The operations in this package reconstruct the repair mechanism. They are not a claim that an inspection or execution sequence was historically recorded.

## Qualification provenance

The supplied attestation was checked at `2026-10-03T19:13:32.529573+00:00`, after the authoritative cutoff. It reports verified resolution, one fail-to-pass case, and 46 pass-to-pass cases under `changed-test-files-with-original-base-control`.

That attestation supports resolution qualification only within changed test files. Whole-project regression and cross-project transfer remain untested. It is not pre-cutoff learned content and does not establish execution of this package's evaluation definitions.

## Evidence

- [Title](evidence/title.md)
- [Report and reproduction](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Regression assertion](evidence/regression.md)
