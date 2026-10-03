# Historical episode

Authoritative SourceRecord: `PyCQA/pyflakes:728:repair:4dcd92e45efe`.

The [title](evidence/title.md) identifies an annotated variable hiding an undefined-name diagnostic. The [report](evidence/body.md) contrasts a diagnostic for `x = x` with no diagnostic for `x: int = x`.

In historical `pyflakes/checker.py`, `Checker.ANNASSIGN` handled `node.target` before the annotation and optional initializer. The [repair](evidence/fix.md) removed that initial target visit and appended it after existing annotation and initializer processing. The existing conditional dispatch between `handleAnnotation(node.value, node)` and `handleNode(node.value, node)` remained intact.

Historical `pyflakes/test/test_type_annotations.py` added `test_variable_annotation_references_self_name_undefined`, asserting `m.UndefinedName` for `x: int = x`. The [regression evidence](evidence/regression.md) establishes a committed assertion, not an executed historical test command.

The qualification dated 2026-10-03 is after the cutoff and is provenance metadata only. It records one fail-to-pass and 53 pass-to-pass cases in changed test files with original-base control. It does not establish whole-project correctness or cross-project transfer.

## Reusable semantic owners

- `annotated-assignment-analyzer`: the Python visitor responsible for annotation analysis, initializer dispatch, and target binding.
- `annotation-regression-suite`: the public Python test suite covering annotated assignment and adjacent annotation behavior.

Locate these owners anew in the current checkout. Historical paths are episode details, not portable execution bindings.
