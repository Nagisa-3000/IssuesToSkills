# Historical episode

SourceRecord: `PyCQA/pyflakes:617:repair:3de8e6120291`

Issue cluster: `PyCQA/pyflakes:617`. Verified repair: `PyCQA/pyflakes:pr:619`, revision `3de8e61202910033b1f8af96a1afcf8faabc37a0`, available March 24, 2021.

## Report

The [title](evidence/title.md) identifies an incorrect F811 diagnostic for annotating an imported variable. The [body](evidence/body.md) reports that pyflakes 2.3.0, used through flake8, emitted:

```text
F811 redefinition of unused 'default_storage' from line 124
```

at `default_storage: Storage`, despite subsequent use of `default_storage.save(...)`. This was a reported observation, not an execution performed by this package.

## Implementation

The [merged implementation](evidence/fix.md) changes the historical `Annotation(Binding)` class in `pyflakes/checker.py` by adding:

```python
def redefines(self, other):
    """An Annotation doesn't define any name, so it cannot redefine one."""
    return False
```

The scope is the annotation-only binding abstraction, not all assignments with annotations.

## Regression assertion

The [regression diff](evidence/regression.md) adds `test_annotating_an_import` to historical `pyflakes/test/test_type_annotations.py`:

```python
@skipIf(version_info < (3, 6), 'new in Python 3.6')
def test_annotating_an_import(self):
    self.flakes('''
        from a import b, c
        b: c
        print(b)
    ''')
```

The test asserts no diagnostics through the existing test helper. The Python-version guard reflects annotation syntax availability. The supplied historical evidence contains a test assertion, not a historical execution log.

## Qualification boundary

A contemporary qualification attestation dated `2026-10-03T19:13:34.091136+00:00` reports verified resolution with one fail-to-pass and 49 pass-to-pass cases, using changed test files with original-base control. Whole-project regression and cross-project transfer remain untested. This attestation is recorded separately in provenance and is not backdated into the historical evidence cards.
