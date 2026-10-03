# Historical episode

Authoritative source: `PyCQA/pyflakes:486:repair:5fc37cbda5bf`.

The original report supplied:

```python
Type: object
def foo(x: Type) -> None: ...
```

It reported `foo.py:2: undefined name 'Type'` with Pyflakes 2.1.1 on Python 3.8.0 on Linux or Python 3.7.3 and identified stub-file checking as problematic. The report is not the resolved specification.

The merged revision `5fc37cbda5bf4e5afcb64c45caa62062979256b4` changed `pyflakes/checker.py`. It introduced a distinct `Annotation` binding for declarations without values, `AnnotationState.NONE`, `STRING`, and `BARE`, and a postponed-condition property based on string context or `annotationsFutureEnabled`. Lookup continued past annotation-only bindings outside that condition. Annotation assignment traversal visited the target even when no value existed.

String-annotation parsing and an existing recognized string-argument annotation entry point entered string context. The context manager restored the prior state in `finally`.

The accompanying diff in `pyflakes/test/test_type_annotations.py` asserted `UndefinedName` for a bare `T` parameter annotation after `T: object` without the future import, no diagnostic for quoted `'T'`, and no diagnostic for both forms with the future import. It also covered unused declarations and a later value assignment.

This package reconstructs the mechanism and supported dependencies. Inspection instructions are authored current guidance, not a claim that a historical maintainer executed that plan. Historical test execution is unknown; the supplied evidence records assertions.

The qualification dated 2026-10-03 is retained separately in provenance, not backdated into pre-cutoff content. It verifies changed test files with original-base control only; whole-project regression and cross-project transfer remain untested.
