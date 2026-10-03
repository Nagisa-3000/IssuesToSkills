# Historical episode

SourceRecord: `PyCQA/pyflakes:728:repair:4dcd92e45efe`  
Repository: `PyCQA/pyflakes`  
Issue cluster: `PyCQA/pyflakes:728`  
Fix: `PyCQA/pyflakes:pr:729`  
Revision: `4dcd92e45efeb0615ba1c96d45241a037d30abe0`

## Report

The [title](evidence/title.md) described an annotated variable hiding an undefined-name diagnostic.

The [original reproduction](evidence/body.md) compared:

```console
$ pyflakes /dev/stdin <<< 'x = x'
/dev/stdin:1:5: undefined name 'x'
$ pyflakes /dev/stdin <<< 'x: int = x'
$
```

This establishes the reported diagnostic asymmetry, not a claim about every scope or annotation form.

## Implementation

In historical `pyflakes/checker.py`, `Checker.ANNASSIGN` initially called `self.handleNode(node.target, node)` before `self.handleAnnotation(node.annotation, node)` and before initializer processing.

The [merged diff](evidence/fix.md) removed that first target visit and placed it after initializer processing. It preserved the annotation visit and the existing conditional initializer paths, including a branch using `self.handleAnnotation(node.value, node)` and another using `self.handleNode(node.value, node)`.

The supported repair mechanism is to avoid exposing the new target binding during initializer analysis. The record does not support replacing all annotation handling with ordinary expression handling.

## Regression assertion

Historical `pyflakes/test/test_type_annotations.py` added the following test inside `TestTypeAnnotations`:

```python
def test_variable_annotation_references_self_name_undefined(self):
    self.flakes("""
    x: int = x
    """, m.UndefinedName)
```

The [regression card](evidence/regression.md) records this assertion at the repair commit. Historical execution output is not supplied.

## Qualification boundary

A contemporary attestation, checked on `2026-10-03T19:13:44.022061+00:00`, reports verified resolution under `changed-test-files-with-original-base-control`: one fail-to-pass and 53 pass-to-pass cases. Its stated limits are changed test files only; whole-project regression and cross-project transfer are untested.

The attestation is retained in provenance, not converted into a historical evidence card or backdated into the 2024 cutoff.
