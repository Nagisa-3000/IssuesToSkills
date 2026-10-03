# Historical episode

Source: `PyCQA/pyflakes:674:repair:1fae3dea5108`.

The [title](evidence/title.md) and [report](evidence/body.md) identify an internal error on `__all__, = ...` in pyflakes 2.4.0. The reported traceback reaches `pyflakes/checker.py`, where accessing `source.value` fails because the source is a tuple target.

The reporter suggested treating this as invalid. That suggestion is not the merged behavior.

The [implementation](evidence/fix.md) instead restricts specialized `ExportBinding` construction. In `Checker`, the branch previously required only `name == '__all__'` and module scope. The merged branch also requires the name node's immediate `_pyflakes_parent` to be one of `ast.Assign`, `ast.AugAssign`, or `ast.AnnAssign`. Other cases continue through the ordinary binding dispatch.

The [regression assertion](evidence/regression.md), added in `pyflakes/test/test_imports.py` under `TestSpecialAll`, checks:

```python
import bar
(__all__,) = ("foo",)
```

The expected diagnostic is `m.UnusedImport`. Thus an unpacked export name is ignored for special export accounting; it does not suppress the import warning.

These changes were available at the authoritative repair revision on 2022-02-12. Supplied historical evidence contains the test assertion but no historical execution transcript.

A qualification checked on 2026-10-03 reports one fail-to-pass and 131 pass-to-pass cases using changed test files with an original-base control. This is later provenance, not pre-cutoff learned content. It does not establish whole-project or cross-project correctness.
