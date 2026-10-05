# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:3604:repair:ffb354aea057`.

The [title](evidence/title.md) identified an underscore-sensitive pragma failure. The [report](evidence/body.md) described regression after upgrading from pylint 2.4.4 to 2.5.0. Disabling `found-_-in-module-class` emitted bad-option-value diagnostics for `found-` and `-in-module-class`; W9902 remained enabled. Substituting numeric identifier `W9902` produced no output in the reported reproduction.

The historical lexer owner was `pylint/utils/pragma_parser.py`, specifically `TOKEN_SPECIFICATION`. The [implementation](evidence/fix.md) changed `MESSAGE_STRING` from `r"[A-Za-z\-]{2,}"` to `r"[A-Za-z\-\_]{2,}"`. It retained the minimum length and other shown token definitions. Although the changelog described messages “with dash,” the added character was underscore.

The historical test owner was `tests/test_pragma_parser.py`. The [regression](evidence/regression.md), named `test_parse_message_with_dash`, parsed `#pylint: disable = raw_input-builtin` using `OPTION_PO` and `parse_pragma`. It asserted action `disable` and messages `["raw_input-builtin"]`. These are committed assertions; historical execution is unknown.

The [Workflow](workflow.md) is an authored conditional reconstruction from report, implementation, and assertions. Its task plan and functional cases are not newly verified historical knowledge and must not be published as such during formal evaluation.

## Validation-only qualification audit

The supplied independent report was checked at `2026-10-04T09:51:25.935947+00:00`, after the historical cutoff. It pinned original base `b73afc8e3d89df143ce686c7086939710ebf29c3`, fixed revision `ffb354aea057c25d9e48fa22da2840a450d99f3e`, the issue/fix identity, and a verified direct closure relationship. All three supplied runs used the same runtime digest and completed without timeout.

Original base: ten existing tests passed, exit 0. Base with committed regression: those ten passed, the new exact-output assertion failed, exit 1; it observed `['raw', 'input-builtin']` instead of `['raw_input-builtin']`. Historical fixed revision: all eleven passed, exit 0.

These controls support independent source qualification only within `changed-test-files-with-original-base-control`. Whole-project regression and cross-project transfer are untested. They do not establish historical CI status or execution of this authored Skill, and their later runtime details are not historical repair mechanisms. The report hash and control audit are retained in [provenance](provenance.json).
