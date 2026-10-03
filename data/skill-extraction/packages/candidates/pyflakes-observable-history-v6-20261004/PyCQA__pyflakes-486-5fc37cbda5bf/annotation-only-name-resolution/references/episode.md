# Historical episode

Source: `PyCQA/pyflakes:486:repair:5fc37cbda5bf`.

The [original title](evidence/title.md) and [report](evidence/report.md) describe an undefined-name diagnostic for:

```python
Type: object
def foo(x: Type) -> None: ...
```

The reporter observed this with version 2.1.1 on Python 3.8.0 and 3.7.3 and identified stub files as a concern. The report alone does not establish that an eagerly evaluated bare annotation should be accepted.

The merged [implementation](evidence/implementation.md), in historical `pyflakes/checker.py`, introduced a distinct `Annotation` binding. Annotation-only declarations became represented in the binding model, but name lookup skipped these bindings unless postponed-annotation context applied. String annotations received a separate state; the future-annotations flag also qualified lookup.

The [regression assertions](evidence/regression.md), in historical `pyflakes/test/test_type_annotations.py`, explicitly kept the undefined-name result for bare `T` without future annotations while allowing quoted `T` and both forms with future annotations. They also protected unused-variable accounting.

This supplied evidence supports a narrower repair than “all annotations define runtime names.”

## Execution status and qualification

The supplied historical diff records test assertions available at the repair commit, not a historical test-run transcript.

A later qualification attestation dated 2026-10-03 reports verified resolution, two fail-to-pass cases, and 39 pass-to-pass cases using changed test files with original-base control. It is provenance, not knowledge available before the 2024 cutoff. Its scope does not establish whole-project safety or transfer to another analyzer.
