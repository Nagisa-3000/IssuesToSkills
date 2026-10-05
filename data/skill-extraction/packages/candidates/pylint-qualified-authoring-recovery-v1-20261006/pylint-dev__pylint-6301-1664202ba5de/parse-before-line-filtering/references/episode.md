# Historical episode

Authoritative source: `pylint-dev/pylint:6301:repair:1664202ba5de`.

The report supplied valid Python:

```python
#!/usr/bin/python
import os

def bug():
    # pylint:disable=R
    if not os.path.exists('/bug'):
        os.mkdir("/bug")
```

The reported command was `python -m pylint --ignore-imports=y ./bootstrap.py`, using Pylint 2.13.5, Astroid 2.11.2, and Python 3.10.4. The traceback reached `stripped_lines` in `pylint/checkers/similar.py`; `astroid.parse("".join(lines))` failed with an expected-indented-block error. Removing the suppression comment or omitting the import-ignore option reportedly avoided the crash.

The merged implementation removed early `active_lines` filtering from `Similar.append_stream`. It read complete source and passed an optional `_is_one_message_enabled` callback through `LineSet` to `stripped_lines`. After AST-dependent import/signature preparation, the normalization loop called the callback with `"R0801"` and original one-based line numbers. Without a linter, the callback was `None`.

The implementation also used an empty list after a Unicode decode error and still appended a `LineSet`. This is an implementation observation, not permission to alter unrelated current decode policy.

Historical paths were `pylint/checkers/similar.py`, `tests/test_similar.py`, `ChangeLog`, and `doc/whatsnew/2.13.rst`. The changelog described the duplicate-code error with import/signature exclusion and stated closure of issue 6301.

Committed assertions enabled parser-error reporting and both secondary-parse exclusion options. They retained expected-output containment and independently rejected `"Fatal error"`. Historical execution of these assertions is unknown.

## Validation-only qualification

The complete supplied controls pin base `58a4067d4b70c5e05eca23d57c3e6ad30d1788bd`, fix `pylint-dev/pylint:pr:6357`, and merged revision `1664202ba5de84149d0a2eeb078b1731d1782fbb`. Historical artifact identity and direct closure were verified.

The original base passed eleven tests. The base with committed regression changes failed four and passed seven. The historical fixed revision passed eleven. All runs had identical runtime digests, used the same test argv, and did not time out.

The exposed failures concerned all-lines inline suppression, inner-scope suppression, suppression in two files, and a suppressed function alongside an enabled function. The regression control demonstrated that expected duplicate output could coexist with fatal output.

Qualification was checked at `2026-10-04T14:05:13.295088+00:00`, not at the historical evidence date. Its exact scope is `changed-test-files-with-original-base-control`. Its exact limits are: **Changed test files only; whole-project regression and cross-project transfer are untested.**

Qualification supports the historical repair within that scope, not execution of newly authored Skill cases. See [provenance](provenance.json) for immutable identities and hashes.
