# Historical episode

SourceRecord: `PyCQA/pyflakes:617:repair:3de8e6120291`.

The report concerned Pyflakes 2.3.0, used through flake8. An imported `default_storage` received an annotation-only statement, `default_storage: Storage`, and was subsequently used in `default_storage.save(...)`. The diagnostic was `F811 redefinition of unused 'default_storage'`.

The merged implementation at revision `3de8e61202910033b1f8af96a1afcf8faabc37a0` changed the annotation binding owner in historical `pyflakes/checker.py`:

```python
def redefines(self, other):
    """An Annotation doesn't define any name, so it cannot redefine one."""
    return False
```

Historical `pyflakes/test/test_type_annotations.py` added `test_annotating_an_import`, guarded for Python 3.6 or later:

```python
self.flakes('''
    from a import b, c
    b: c
    print(b)
''')
```

No expected diagnostic argument was supplied. This is a regression assertion for the import/annotation/use sequence, not a recorded historical test run.

The supplied verified resolution identifies PR 619 as the repair. The later qualification covers changed test files with an original-base control: one fail-to-pass and 49 pass-to-pass. Its scope does not establish whole-project regression safety or cross-project applicability.

Evidence: [title](evidence/title.md), [report](evidence/body.md), [implementation](evidence/fix.md), [regression](evidence/regression.md).
