# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:3092:repair:ce2af67d0e96`.

## Report

On September 5, 2019, the reporter supplied:

```python
def indentifier_kwarg_method(arg1: int, arg2: int, *, value1: str, value2: str):
    """Code to show failure in missing-type-doc

    Args:
        arg1: First argument.
        arg2: Second argument.
        value1: First kwarg.
        value2: Second kwarg.
    """
    print("NOTE: It doesn't like anything after the '*'.")
```

The reported command was:

```text
python3 -m pylint --disable=all --enable=missing-type-doc pylint_failure.py
```

It reportedly emitted W9016 `missing-type-doc` for `value1, value2`. The reported environment was Pylint 2.3.1, astroid 2.2.5, Python 3.7.3, and Mac OSX 10.14.6. This command is historical data, not a current binding. Positional-only `/` syntax was not tested.

## Implementation and assertion

The September 23 repair in `pylint/extensions/docparams.py`, within `DocstringParameterChecker`, retained the ordinary argument/annotation traversal and added:

```python
for index, arg_name in enumerate(arguments_node.kwonlyargs):
    if arguments_node.kwonlyargs_annotations[index]:
        params_with_type.add(arg_name.name)
```

The addition precedes the existing `_compare_missing_args` call. It credits a keyword-only name only when its corresponding annotation is present.

In `tests/extensions/test_check_docs.py`, the commit added `test_missing_type_doc_google_docstring_exempt_kwonly_args`. It constructs a function with two ordinary annotated parameters, two annotated keyword-only parameters, and a Google-style `Args:` section describing all four without explicit docstring types. It invokes `self.checker.visit_functiondef(node)` under `self.assertNoMessages()`.

These are public implementation and assertion facts at the historical commit. Historical execution and CI status are unknown. The authored Actions are a conditional operationalization, not a claim that historical developers executed this exact plan.

## Validation-only qualification review

The supplied complete report pins original base `939f91c886deb989ae4c5e2698c0d0d483e7bfec`, repair `ce2af67d0e96e26c1999e1a53e36cf1460d9d647`, the issue identity, and verified direct closure. The closure locator belongs to qualification metadata, not the core historical evidence set.

The three observations and corresponding run outputs agree:

- Original base: 109 passed, exit 0.
- Base with the committed regression: that regression failed with `missing-type-doc` for `value1, value2`; 109 passed, exit 1.
- Historical fixed checkout: 110 passed, exit 0.

All three runs used the same runtime digest, adopted their workspaces, and did not time out. The original base lacks the new regression; the augmented base isolates its failure; the fixed checkout resolves it while preserving the 109 existing cases.

Checked at `2026-10-04T09:05:54.227394+00:00`, this qualification is validation-only and not backdated historical learning. Its scope is `changed-test-files-with-original-base-control`. Whole-project regression, cross-project transfer, formal SWE evaluation, and newly authored Skill functional cases were not tested. Contemporary runtime details are not historical repair mechanisms.

## Packaged historical evidence

- [Issue title](evidence/title.md)
- [Report and reproduction](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed regression assertion](evidence/regression.md)
