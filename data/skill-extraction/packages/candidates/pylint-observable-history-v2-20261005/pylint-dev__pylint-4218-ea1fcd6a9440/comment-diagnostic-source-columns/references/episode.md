# Historical episode

Authoritative source: `pylint-dev/pylint:4218:repair:ea1fcd6a9440`.

## Report

The [title](evidence/title.md) and [original report](evidence/body.md), available on 2021-03-09, describe W0511 warnings all appearing at column 2 despite comments occurring at different horizontal positions. The reproduction includes a standalone comment, an inline comment after `print(1)`, and comments inside a function and nested block.

The reporter asked whether the location should be the start of the comment or TODO. The report alone does not select the anchor. The merged implementation selects the position immediately after the hash.

## Repair

At revision `ea1fcd6a94403c1c17718c934903f0f57b51aba5`, available 2021-03-25T20:01:54Z, the [implementation](evidence/fix.md) changed the `EncodingChecker` comment-note emitter in historical `pylint/checkers/misc.py`:

```python
# Before:
note = match.group(1)
col_offset = comment.string.lower().index(note.lower())

# After:
col_offset = comment.start[1] + 1
```

The `note` extraction was removed. The matching operation remained:

```python
match = self._fixme_pattern.search("#" + comment_text.lower())
```

Message arguments remained `comment_text`, and the line remained `comment.start[0]`. The ChangeLog says “Fix column index on FIXME warning messages” and closes #4218.

## Committed assertions

The [regression evidence](evidence/regression.md) updates historical `tests/functional/f/fixme.txt` and `tests/functional/f/fixme_bad_formatting_1139.txt`. Columns depend on the token's position, not the matched note's local index. Warning labels, lines, and message strings remain unchanged in these diffs.

These are assertions present at the repair commit. No historical CI or test execution result was supplied.

## Validation-only qualification

The supplied independent report was checked at `2026-10-04T10:31:27.895643+00:00`. Its identity pins base `d274b660a7b7cc4b6910bf69a33dae0a7d5d9c53`, repair revision `ea1fcd6a94403c1c17718c934903f0f57b51aba5`, issue #4218, fix PR #4246, and a verified direct closure relationship.

Complete supplied controls show:

- Original base with its original expectations: 13 selected tests passed, exit 0.
- Original base with committed regression expectations: the two affected fixtures failed on column differences; 11 others passed, exit 1.
- Historical fixed state: all 13 selected tests passed, exit 0.
- All three runs used the same reported runtime digest, had no timeout, and adopted the controlled workspace.

The report lists 13 original-base-to-fixed pass-to-pass cases, including the two affected fixtures whose old expectations passed on the original base. This does not erase their base-with-regression failures.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression and cross-project transfer were not checked. This later qualification is not a historical event, does not supply a historical mechanism, and did not execute this Skill's functional cases. Exact report and runtime hashes are retained in [provenance](provenance.json).

## Authored reconstruction boundary

The Workflow and Action cards are a conditional reconstruction of the supplied repair mechanism, with explicit current probes and validation requirements. They do not claim that the historical author executed these newly authored operations or commands.
