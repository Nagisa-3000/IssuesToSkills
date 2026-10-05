# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:2729:repair:183dcc4cb134`.

The [report](evidence/body.md) describes false `W9006` / `missing-raises-doc` warnings with `load-plugins=pylint.extensions.docparams`. A function raised `TypeError`, `ValueError`, and custom `ValidationError`, with this declaration:

```text
:raises TypeError, ValueError, ValidationError:
```

The reporter observed warnings for all three and reported Pylint 2.2.2, astroid 2.1.0, and Python 3.7.2. These are report facts, not current runtime requirements.

## Implementation

The [merged diff](evidence/fix.md) at `183dcc4cb134d3dab2696e2d28c51c5a3577e358` changed historical owner `pylint/extensions/_check_docs_utils.py`:

- Introduced `_split_multiple_exc_types`, using `re.split` with `(\s*,(?:\s*or\s)?\s*|\s+or\s+)`.
- Introduced a Sphinx multiple-simple-type grammar accepting existing forms joined by `of`, `or`, or commas; used it in parameter-type, property-type, and raises recognition.
- Added comma separators to Google's multiple-type grammar and used that grammar for raises recognition.
- Changed Sphinx and Google raises collectors from adding one captured declaration to updating sets from the splitter.
- Retained Google's nonempty-description gate.
- Added a changelog statement supporting multiple raises types and commas in valid sections, closing #2729.

The splitter uses a capturing delimiter, so split results can include separator strings. This patch does not establish a names-only exact set. Current validation must ensure individual names reach the comparison and incidental tokens cannot conceal genuine missing documentation.

## Assertions and execution status

Historical test owner `tests/extensions/test_check_raise_docs.py` received [two regressions](evidence/regression.md), one Sphinx and one Google. Each documents singleton `RuntimeError` and list `NameError, OSError, ValueError`, includes corresponding raises, extracts the marked `NameError` raise node, and asserts no checker messages.

The added assertions directly exercise `NameError`, not separate visits to every fixture raise. Per-member and broader adjacent checks in this Skill are new validation definitions, not historical execution observations.

Historical CI/test execution is unknown. These authored contracts describe the supplied mechanism, not a recovered historical task log.

## Validation-only qualification

The supplied independent report pins original base `e1f8fdef9d5438701e852f285f0ac537203881e6`, the authoritative issue/fix identity, and fixed revision `183dcc4cb134d3dab2696e2d28c51c5a3577e358`. It reports direct closure and verified historical artifacts.

At `2026-10-04T08:50:55.714946+00:00`, the complete controls showed:

- Original base: exit 0, 44 passed.
- Base with regressions: exit 1, 44 passed and two failed, both with `missing-raises-doc` for `NameError`.
- Historical fixed tree: exit 0, 46 passed.

All three runs shared the supplied runtime digest and none timed out. The qualification command was:

```text
python3 -m pytest tests/extensions/test_check_raise_docs.py -q
```

This replay qualifies the source only within the changed-test-file scope. It is not historical execution, current execution authority, a formal SWE run, whole-project validation, transfer evidence, or execution of authored Skill functional cases. Later runtime dependencies and logs do not become historical mechanisms. See [provenance](provenance.json).
