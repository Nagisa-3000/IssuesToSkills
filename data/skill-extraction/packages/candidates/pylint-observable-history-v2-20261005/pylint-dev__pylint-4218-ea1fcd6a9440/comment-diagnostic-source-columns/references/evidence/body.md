# Original public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4218:body",
  "source_id": "pylint-dev/pylint:4218:repair:ea1fcd6a9440",
  "available_at": "2021-03-09T05:38:32Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report supplies bug.py with '# TODO 1', 'print(1)  # TODO 2', an indented '# TODO 3', and a more deeply indented '# TODO 4'. Reported pylint output places W0511 at column 2 on lines 3, 4, 9, and 12, with messages TODO 1 through TODO 4. The reporter asks whether the position should be the start of the comment or of TODO. This is reported reproduction output; it does not itself establish the anchor selected by the repair or an independently executed historical test."
}
```
