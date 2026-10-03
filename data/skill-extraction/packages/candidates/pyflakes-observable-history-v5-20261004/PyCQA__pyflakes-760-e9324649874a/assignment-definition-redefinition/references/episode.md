# Historical episode

- Authoritative repair source: `PyCQA/pyflakes:760:repair:e9324649874a`
- Repository: `PyCQA/pyflakes`
- Issue cluster: `PyCQA/pyflakes:760`
- Fix: `PyCQA/pyflakes:pr:761`
- Revision: `e9324649874a7124a08c3826d4cf78a4dc3aa32c`
- Repair available: `2023-01-12T16:26:28Z`

## Reported discrepancy

The [issue title](evidence/title.md) described an attribute hidden by a method. The [report](evidence/report.md) compared two class bodies under flake8 6.0.0 with pyflakes 3.0.1:

```python
class Foo:
    def bar(self):
        return 0

    def bar(self):
        return 1
```

This produced `F811 redefinition of unused 'bar' from line 2`. The following produced no output in the reported reproduction:

```python
class Foo:
    bar = 0

    def bar(self):
        return 1
```

The reporter also described a factory attribute hidden by a later decorated method and acknowledged that ordinary variable rebinding can be useful. The proposal to deny attribute redefinition was part of the report, not the full semantics of the implemented repair.

## Actual implementation

The [merged implementation](evidence/implementation.md) added this method to `Definition` in the historical `pyflakes/checker.py`:

```python
def redefines(self, other):
    return (
        super().redefines(other) or
        (isinstance(other, Assignment) and self.name == other.name)
    )
```

`Definition` is documented there as a binding defining a function or class. The repair expands the directional predicate of the new definition; it does not modify assignment rebinding into a blanket duplicate-name error. The inherited predicate remains a disjunct.

## Historical regression assertion

The [regression diff](evidence/regression.md), in historical `pyflakes/test/test_other.py`, added:

```python
def test_redefined_function_shadows_variable(self):
    self.flakes('''
    x = 1
    def x(): pass
    ''', m.RedefinedWhileUnused)
```

This assertion tests a module-level assignment followed by a same-name function definition. The supplied historical evidence does not include execution logs or a dedicated test for the class-body reproduction.

## Later qualification, not historical execution

The supplied attestation was checked at `2026-10-03T19:13:47.549571+00:00`, after the knowledge cutoff. It reports verified resolution under `changed-test-files-with-original-base-control`, with one fail-to-pass case and 127 pass-to-pass cases. It is retained as provenance only. Whole-project regression and cross-project transfer are untested.

The [Workflow](workflow.md) expresses supported repair operations and their conditional dependencies; its inspection instructions and current validation requirements are not a claim that an identical historical task plan was executed.
