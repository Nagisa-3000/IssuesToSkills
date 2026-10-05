# Historical episode

## Source identity

- SourceRecord: `pylint-dev/pylint:5000:repair:bbaa7bc9200a`
- Issue: `pylint-dev/pylint:5000`
- Fix: `pylint-dev/pylint:pr:5001`
- Revision: `bbaa7bc9200abaab5b32de8d55ae5cc6fbbbcece`
- Repair available: `2021-09-14T07:56:58Z`
- Exclusive cutoff: `2024-01-01T00:00:00Z`

The contracts reconstruct this repair from supplied evidence; they are not historically executed contracts.

## Report

With `use-symbolic-message-instead` enabled, the reporter observed that `# pylint: disable=W0223` produced I0023 suggesting `# pylint: disable=abstract-method`, but `# pylint: disable=w0223` produced no output. Lowercase numeric IDs were nevertheless accepted.

## Implementation

In historical `pylint/message/message_id_store.py`, `MessageIdStore.get_symbol` changed:

```python
return self.__msgid_to_symbol[msgid]
```

to:

```python
return self.__msgid_to_symbol[msgid.upper()]
```

The `KeyError` handler remained unchanged. It used the original `msgid` when constructing `UnknownMessageError`. The repair normalized the lookup key, not the original input or the whole directive.

## Regression assertions

Historical `tests/functional/u/use/use_symbolic_message_instead.py` changed line 2 from `enable=C0111` to:

```python
# pylint: enable=c0111,w0223   # [use-symbolic-message-instead,use-symbolic-message-instead]
```

The companion `.txt` asserted two line-2 recommendations: original spelling `'c0111'` with `enable=missing-docstring`, and `'w0223'` with `enable=abstract-method`. Other uppercase recommendations and the invalid `T1234` diagnostic remained. The expected-output diff also added `:HIGH` confidence suffixes; those are not the lookup-normalization mechanism.

Historical execution of these committed assertions is unknown.

## Evidence

- [Issue title](evidence/title.md)
- [Original report](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed assertions](evidence/regression.md)

## Validation-only qualification audit

The supplied independent report was checked at `2026-10-04T11:44:10.122137+00:00`. Its identity pins original base `cb7bba41e598aa7aa57f71f987fd92d7704f4f78`, the issue and fix above, the repair revision, and a verified direct-closure relationship.

The complete observations and run outputs agree:

| Control | Result |
|---|---|
| Original base, original assertions | 14 passed, exit 0 |
| Original base, strengthened regression | 13 passed, one symbolic-recommendation failure, exit 1 |
| Historical fixed implementation, strengthened regression | 14 passed, exit 0 |

The failing control reported a missing expected line-2 `use-symbolic-message-instead` result, not an environment or collection failure. All controls completed without timeout, adopted their isolated workspaces, and shared runtime digest `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

The report's 14 pass-to-pass entries compare original assertions with the fixed implementation; its single fail-to-pass entry describes the strengthened symbolic-recommendation regression. These do not constitute 15 distinct tests.

Scope is `changed-test-files-with-original-base-control`; whole-project regression was explicitly unchecked. Cross-project transfer is untested. Qualification is later validation, not historical learned content or execution of the authored functional cases. The report hash is retained in [provenance](provenance.json).
