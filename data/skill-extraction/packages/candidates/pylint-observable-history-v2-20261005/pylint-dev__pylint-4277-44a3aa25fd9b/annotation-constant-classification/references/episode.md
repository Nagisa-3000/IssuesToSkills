# Historical episode

Authoritative source: `pylint-dev/pylint:4277:repair:44a3aa25fd9b`.

The reporter described lowercase class attributes annotated with bare `ClassVar` and `typing.ClassVar` receiving class-constant uppercase diagnostics on Pylint 2.7.4 and a preview release. The report also mentions subscripted annotations and says 2.7.2 did not emit the complaints. Those version comparisons are report observations, not independently executed historical comparisons.

## Implementation and assertions

Historical `pylint/checkers/base.py` replaced `utils.is_class_var(node)` in the class-constant alternative with `utils.is_assign_name_annotated_with(node, "Final")`. The existing Enum ancestor condition remained.

Historical `pylint/checkers/utils.py` renamed and parameterized the helper. It requires an `AnnAssign` parent, unwraps a `Subscript` annotation to its value, and compares `Name.name` or `Attribute.attrname` with the requested typing name. This is syntactic matching, not alias or import-origin inference.

Committed assertions were in:

- `tests/functional/n/name/name_final.py`, `.rc`, and `.txt`;
- `tests/functional/n/name/name_final_snake_case.py`, `.rc`, and `.txt`;
- modified `tests/functional/n/name/name_styles.py` and `.txt`.

Default-style Final assertions expect diagnostics for lowercase `variable` and annotation-only `variable2`. The snake_case fixture expects diagnostics for four uppercase Final names. Two ClassVar class-constant diagnostics were removed. The bad Enum-name expectation remained. New Final fixtures require Python 3.8.

`Final[typing.ClassVar[str]]` appears in the fixtures. It demonstrates outer-annotation recognition in this naming checker, not general typing validity of combining those forms.

## Evidence cards

- [Title](evidence/title.md)
- [Report](evidence/body.md)
- [Implementation](evidence/fix.md)
- [Regression assertions](evidence/regression.md)

## Qualification boundary

Historical CI/test execution is **unknown** from the supplied historical core.

The supplied independent qualification, checked at `2026-10-04T10:36:30.034945+00:00`, pins base `8cab76fc6ad64e6f4efddf9d8cab95973bfb4609` and repair `44a3aa25fd9b5b3469b3e24179798d67ef604eeb`. Historical artifact identity and direct closure were verified.

Complete supplied controls show:

- Original base: six selected existing cases passed; exit 0.
- Base with committed regressions: `name_final`, `name_final_snake_case`, and replacement `name_styles` failed; five selected controls passed; exit 1.
- Historical fixed revision: all eight selected cases passed; exit 0.

The regression-loaded base retained removed ClassVar diagnostics and lacked the expected Final diagnostics. Original and replacement `name_styles` are distinct controls. All three runs reported the same runtime digest, adopted isolated workspaces, and no timeout.

This is changed-test qualification with original-base controls. It does not establish whole-project correctness or cross-project transfer. Contemporary replay is validation-only provenance, not a historical execution event, historical dependency prescription, or execution of newly authored Skill functional cases.
