# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:5406:repair:608ed329aaee`.

The [title](evidence/title.md) identified a version-2.12 regression. The [report](evidence/body.md), with `pylint.extensions.docparams` enabled, compared three spellings for `echo(*args)`:

- `:param args:` produced missing `*args` and differing `args` diagnostics.
- `:param *args:` satisfied the checker but caused a Sphinx inline-emphasis warning.
- `:param \*args:` satisfied Sphinx but caused an anomalous-backslash warning in a non-raw Python string.

These are reported observations. The requested acceptance of bare names is not evidence that the merged repair implemented it.

## Historical realization

At `608ed329aaee9e457ac51347699d4892d29df802`, the [implementation](evidence/fix.md) changed `SphinxDocstring` in `pylint/extensions/_check_docs_utils.py`. Its parameter-name regex accepts an ordinary word name or a backslash followed by one or two asterisks and a word name. Extraction retains `match.group(2)` and removes backslashes before adding the name to the documented-parameter set.

In `pylint/reporters/text.py`, the `colorize_ansi` docstring became raw and changed its kwargs field to `:param \**kwargs:`.

The [assertions](evidence/regression.md) in `tests/functional/ext/docparams/parameter/missing_param_doc_required_Sphinx.py` and its `.txt` expectations add missing-parameter diagnostics for unescaped starred fields. New raw escaped cases do not expect missing-parameter diagnostics. Missing-documentation cases and unrelated diagnostics remain.

These assertions were public at the repair date. Historical CI/test execution is unknown.

## Validation-only qualification review

The independent report was checked at `2026-10-04T12:27:45.718379+00:00`, not at the historical repair date. Its original base is `f89a3374ec7d49d2a984c90530758a506eaa4384`; issue, fix, merged revision, repair availability, and direct-closure identity match the authoritative source.

The complete supplied controls were reviewed:

- Original base: selected Google and original Sphinx cases passed; exit code 0.
- Base with committed regression assertions: Google passed, Sphinx failed; exit code 1. The failure identified missing expected diagnostics at unescaped-field lines 184/201 and unexpected diagnostics at escaped-field lines 218/237.
- Historical fixed revision: both selected cases passed; exit code 0.

All three runs completed without timeout, adopted their workspaces, and reported the same runtime digest. The report verifies the historical artifact and closure relationship. It records one fail-to-pass observation and two pass-to-pass controls.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression, actual Sphinx rendering, cross-project transfer, and newly authored Skill cases were not checked. Later commands, dependencies, and logs are validation context, not historical mechanisms. The report hash and audit facts are in [provenance](provenance.json). The closure-event reference is validation metadata, not an invented historical evidence card.
