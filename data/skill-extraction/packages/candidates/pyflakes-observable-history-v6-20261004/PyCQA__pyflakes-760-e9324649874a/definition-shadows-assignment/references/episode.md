# Historical episode

SourceRecord: `PyCQA/pyflakes:760:repair:e9324649874a`

Issue title: [should produce error for attribute hidden by a method](evidence/title.md).

The [original report](evidence/body.md) showed that two same-name methods produced F811, while a class assignment followed by a same-name method produced no diagnostic. Its motivating example was a factory attribute accidentally replaced by a decorated method far below the assignment. The report also explicitly distinguished useful ordinary variable rebinding from the suspected error.

The [merged implementation](evidence/fix.md) added `Definition.redefines` in historical `pyflakes/checker.py`:

```python
def redefines(self, other):
    return (
        super().redefines(other) or
        (isinstance(other, Assignment) and self.name == other.name)
    )
```

Thus the correction preserves the superclass predicate and adds the assignment/same-name case. `Definition` represents a binding defining a function or class; the patch is not limited to class attributes.

The [regression assertion](evidence/regression.md), in historical `pyflakes/test/test_other.py`, adds `test_redefined_function_shadows_variable`:

```python
self.flakes('''
x = 1
def x(): pass
''', m.RedefinedWhileUnused)
```

These paths identify historical resources only. Current resources must be located by semantic role.

## Resolution and execution status

The authoritative SourceRecord marks this repair as verified, at revision `e9324649874a7124a08c3826d4cf78a4dc3aa32c`. The supplied historical core contains a merged implementation and regression assertion, not a historical test execution transcript.

The later qualification attestation was checked on 2026-10-03. It reports one fail-to-pass and 127 pass-to-pass cases under changed-test-file/original-base control. This supplies limited resolution qualification; it is neither pre-cutoff learned content nor evidence of whole-project or cross-project success.

The packaged Workflow is an operational reconstruction from the supplied report, implementation, and assertion. It does not claim the historical author executed these authored Action cards or that any current task plan is verified historical knowledge.
