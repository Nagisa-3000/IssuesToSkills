# Historical episode

SourceRecord: `pylint-dev/pylint:3666:repair:fe0a7f795343`.

## Report, implementation, and assertions

The reporter described Pylint 2.5.0 treating `pylint: disable=j3-no-jfly` as bad option value `-no-jfly`, reported working behavior in 2.4.4, and identified the digit-excluding symbolic token regex as a possible cause.

The merged repair at `fe0a7f7953430f10308d2ba94c14f056e166fe1c`, available at `2020-06-08T05:51:24Z`, changed `MESSAGE_STRING` in `pylint/utils/pragma_parser.py`:

```python
# Before
("MESSAGE_STRING", r"[A-Za-z\-\_]{2,}")
# After
("MESSAGE_STRING", r"[0-9A-Za-z\-\_]{2,}")
```

The displayed neighboring `KEYWORD`, `ASSIGN`, and `MESSAGE_NUMBER` entries were unchanged. The two-character minimum and existing letters, hyphens, and underscores were retained. The ChangeLog described the regression and recorded “Close #3666.”

The committed regression in `tests/test_pragma_parser.py` was:

```python
def test_disable_checker_with_number_in_name():
    comment = "#pylint: disable = j3-custom-checker"
    match = OPTION_PO.search(comment)
    for pragma_repr in parse_pragma(match.group(2)):
        assert pragma_repr.action == "disable"
        assert pragma_repr.messages == ["j3-custom-checker"]
```

These are committed assertions, not evidence of original execution. Historical CI/test execution is unknown. Current guidance adds a nonempty-result guard; that guard is not attributed to the historical test.

## Evidence

- [Title](evidence/title.md)
- [Report](evidence/body.md)
- [Implementation](evidence/fix.md)
- [Regression assertions](evidence/regression.md)

## Validation-only qualification audit

The independent qualification was checked at `2026-10-04T09:56:59.524131+00:00`, not at historical repair time. It pins issue `pylint-dev/pylint:3666`, fix `pylint-dev/pylint:pr:3667`, original base `627d07d249d17c12ed9e1a52044843607a5353d0`, and historical merge `fe0a7f7953430f10308d2ba94c14f056e166fe1c`. It reports verified artifact identity and direct closure. Its closure locator is `pylint-dev/pylint:3666:event:MDExOkNsb3NlZEV2ZW50MzQxODIxMDE5OA==`; this is validation provenance, not an additional historical evidence card.

The controls supplied were:

| Control | Outcome |
|---|---|
| Original base | Eleven existing tests passed; exit 0 |
| Base with committed regression | New regression failed; same eleven tests passed; exit 1 |
| Historical fixed revision | All twelve tests passed; exit 0 |

The fail-to-pass case was `tests.test_pragma_parser::test_disable_checker_with_number_in_name`. Its failing comparison was actual `['-custom-checker']` versus expected `['j3-custom-checker']`.

The eleven pass-to-pass cases, all under `tests.test_pragma_parser`, were:
`test_missing_assignment`, `test_missing_keyword`, `test_missing_message`,
`test_multiple_pragma_multiple_messages`, `test_parse_message_with_dash`,
`test_simple_pragma`, `test_simple_pragma_multiple_messages`,
`test_simple_pragma_no_messages`, `test_unknown_keyword_with_messages`,
`test_unknown_keyword_without_messages`, and `test_unsupported_assignment`.

All three runs used `python3 -m pytest tests/test_pragma_parser.py -q --junitxml=/workspace/verification-results.xml`, had no timeout, adopted the workspace, and used isolation `linux-copied-user-mount-pid-net-chroot-nobody-no-capabilities-v1`. Their runtime SHA-256 was consistently `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`. The observations SHA-256 was `3e14d1b577be791754602a68850f83456a937928d9d198ec4d5dab3c8d86c42d`.

These contemporary replay details validate the narrow causal relationship; they are not historical mechanisms or current execution authorization. The report hash is preserved in [provenance](provenance.json).

Scope is `changed-test-files-with-original-base-control`. Whole-project regression was not checked; this was not a formal SWE run. Cross-project transfer is untested. This qualification does not execute the authored Skill functional cases and does not backdate new information.

## Current binding boundary

Locate current semantic owners and public commands before using the [Workflow](workflow.md). Neither historical paths nor later replay argv establish current bindings.
