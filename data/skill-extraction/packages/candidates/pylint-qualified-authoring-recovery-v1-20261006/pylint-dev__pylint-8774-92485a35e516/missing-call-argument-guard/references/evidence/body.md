# Historical reproduction and failure

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8774:body",
  "source_id": "pylint-dev/pylint:8774:repair:92485a35e516",
  "available_at": "2023-06-13T20:54:04Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report reproduced the crash with `from copy import copy` followed by `copy()`, analyzed using `pylint a.py`. Its traceback shows StdlibChecker._check_shallow_copy_environ calling utils.get_argument_from_call(node, position=0), which raises utils.NoSuchArgumentError; the linter then raises astroid.AstroidError from that exception. Expected behavior was no crash. Reported versions were pylint 3.0.0b1, astroid 3.0.0a6-dev0 and Python 3.11.2. This is a reported failure, not historical fixed-revision test execution."
}
```
