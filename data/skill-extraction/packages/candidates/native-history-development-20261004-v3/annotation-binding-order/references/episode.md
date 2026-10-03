# Historical episode

Source `PyCQA/pyflakes:728` was resolved by PR 729 at merge revision `4dcd92e45efeb0615ba1c96d45241a037d30abe0`, available at 2022-09-08T22:10:17Z.

## Reported symptom

The issue title was `annotated variable hides "undefined name"`. The issue body showed:

```console
$ pyflakes /dev/stdin <<< 'x = x'
/dev/stdin:1:5: undefined name 'x'
$ pyflakes /dev/stdin <<< 'x: int = x'
$
```

These are reported historical console observations, not package executions.

## Merged implementation

The historical owner was `Checker.ANNASSIGN` in `pyflakes/checker.py`. The merged diff removed `self.handleNode(node.target, node)` from the start of the handler and inserted the same call after annotation and optional value processing.

`self.handleAnnotation(node.annotation, node)` remained. Existing value-processing paths retained `self.handleAnnotation(node.value, node)` or `self.handleNode(node.value, node)`. The complete specialized branch condition is not exposed by the supplied diff and is not invented here.

The supported mechanism is delayed target registration during static analysis, so the initializer does not resolve its own otherwise-unbound target prematurely. This is not a change to runtime Python evaluation semantics.

## Historical regression assertion

In `pyflakes/test/test_type_annotations.py`, `TestTypeAnnotations` gained:

```python
def test_variable_annotation_references_self_name_undefined(self):
    self.flakes("""
    x: int = x
    """, m.UndefinedName)
```

This assertion was available at the merged historical commit. Historical test execution is unknown because no historical test-run output was supplied.

## Contemporary qualification

The supplied attestation was checked at 2026-10-03T17:33:20.215658+00:00. It reports verified resolution under `changed-test-files-with-original-base-control`: one fail-to-pass and 53 pass-to-pass cases. Whole-project regression and cross-project transfer remain untested.

This attestation is retained separately in provenance with its original timestamp and non-pre-cutoff status. It does not constitute a historical event or execution of this package's eval definitions.

## Evidence inventory

- [Title](evidence/title.md)
- [Body](evidence/body.md)
- [Label event](evidence/label-event.md)
- [Cross-reference](evidence/cross-reference.md)
- [Merged fix](evidence/fix.md)
- [Regression assertion](evidence/regression.md)
