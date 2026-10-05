# Historical episode

SourceRecord: `pylint-dev/pylint:4265:repair:c92e3ab78778`.

The [title](evidence/title.md) described a 2.7.3 regression ignoring disabled warnings. The [report](evidence/body.md) said an unchanged repository went from no errors under 2.7.2 to hundreds under 2.7.3, with many messages believed to have been disabled. The reported environment was pylint 2.7.3, astroid 2.5.2, and Python 3.7.9. The report is a symptom account, not proof that every disable was broken.

The [implementation](evidence/fix.md) changed historical
`pylint/message/message_handler_mix_in.py`,
`MessagesHandlerMixIn._register_by_id_managed_msg`. The helper recognizes a numeric-looking identifier using `msgid_or_symbol[1:].isdigit()`, looks up its symbol, and appends advisory data. The repair wrapped that bookkeeping in `try`/`except KeyError: pass`. Successful registration retained the tuple fields, with an explicit local `msgid` variable.

The [regression assertions](evidence/regression.md) added:
- `tests/functional/d/disabled_msgid_in_pylintrc.py`, containing an `open('test')` inside `try` and `except Exception: pass`.
- `tests/functional/d/disabled_msgid_in_pylintrc.rc`, whose `[MESSAGES CONTROL]` disable list is `C0111,C0326,W0703`.

The supplied diff does not independently enumerate which configured identifier is unresolved. Bind that fact by inspecting the current registry rather than generalizing historical identifier validity to a new checkout.

The changelog says disabled msgids were not being ignored, closes #4265, and dates 2.7.4 to 2021-03-30. Package version metadata was also changed to 2.7.4. Those release edits are historical context, not reusable repair operations.

## Resolution qualification, not historical execution

The supplied independent report pins original base
`c1c41b849ce070447f3efe4ed1a91068d4c85362` and fixed revision
`c92e3ab78778aa1afcf4ddca4829245d37fbc095`, with a verified direct-closure relationship to PR 4268.

At validation time 2026-10-04T10:35:54.040641+00:00:
- Original base: seventeen selected existing tests passed; the new regression was absent.
- Base with regression: the regression failed with unexpected `broad-except` at line 5; seventeen adjacent tests passed.
- Historical fixed: all eighteen selected tests passed.
- All three runs reported the same runtime digest, no timeout, and adopted workspaces. Exit codes were respectively 0, 1, and 0.

These controls independently support the supplied repair's regression-specific resolution. The report explicitly excludes whole-project regression coverage and is not a formal SWE run. Historical CI status remains unknown. Neither these results nor their contemporary runtime details are execution results for the newly authored Skill.

The qualification hash and validation scope are recorded in [provenance](provenance.json). The package's historical mechanism is supported only by the public pre-cutoff report, implementation, and committed assertions.
