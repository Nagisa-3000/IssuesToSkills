# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4218:regression",
  "source_id": "pylint-dev/pylint:4218:repair:ea1fcd6a9440",
  "available_at": "2021-03-25T20:01:54Z",
  "kind": "historical_regression_assertions",
  "observation": "In tests/functional/f/fixme.txt, expected columns change by line as follows: 5 from 2 to 1; 11 from 2 to 20; 14 from 2 to 5; 16 from 2 to 18; 18 from 1 to 5; 20 from 1 to 5; 25 from 2 to 5; 27 from 2 to 5. Line 23 remains at column 2. Message strings include FIXME, TODO, XXX, unspaced-hash notes, lowercase todo, './TODO: find with notes', and 'TO make something DO: find with regex'; warning labels, lines, and messages are unchanged by the diff. In tests/functional/f/fixme_bad_formatting_1139.txt, line 6 changes from column 2 to 1 while retaining the TODO message and its trailing '# [fixme]'. These are committed expected-output assertions, not evidence of historical test execution."
}
```
