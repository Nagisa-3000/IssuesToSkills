# Historical reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8120:body",
  "source_id": "pylint-dev/pylint:8120:repair:660405e62182",
  "available_at": "2023-01-27T18:14:29Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used Pylint 2.15.10 with pylint.extensions.redefined_variable_type loaded and ran 'pylint a.py'. Separate async methods assigned potato to Root() and {}; supplied output reported R0204 at the second assignment, from a.Root to dict. The synchronous equivalent produced no warning and a 10.00/10 score. The body's phrase 'false negative' conflicts with its unwanted-warning output and expected behavior. These are reporter-supplied reproduction observations, not independently executed historical CI."
}
```
