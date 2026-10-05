# Public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4238:body",
  "source_id": "pylint-dev/pylint:4238:repair:5d5f65727829",
  "available_at": "2021-03-16T09:48:31Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter states that var = f'The number {(count := 4)} is equal to {count}' is clean, but splitting it into backslash-continued adjacent f-strings produces E0601 for count despite assignment preceding the read. The reported environment is Pylint 2.7.2, astroid 2.5.1, and Python 3.8.8 on macOS. One command/output filename is inconsistently labeled. This is a reported reproduction, not an independently executed historical test."
}
```
