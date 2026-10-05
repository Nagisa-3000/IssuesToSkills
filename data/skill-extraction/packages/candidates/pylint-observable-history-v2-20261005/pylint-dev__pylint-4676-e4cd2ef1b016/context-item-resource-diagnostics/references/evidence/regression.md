# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4676:regression",
  "source_id": "pylint-dev/pylint:4676:repair:e4cd2ef1b016",
  "available_at": "2021-07-06T19:46:15Z",
  "kind": "historical_regression_assertions",
  "observation": "The functional open fixture retained a with-open header followed by `open(\"bar\")  # [consider-using-with]` in its body. New assertions cover `with (open(file1) if which else open(file2)) as input_file`, a direct single-line `with open(file1): return file1.read()`, and a multiline conditional context item with an inline body. The first two additions explicitly say `must not trigger`; the multiline addition carries no expected diagnostic annotation. The fixture also disables multiple-statements. These are committed assertions, not evidence of historical execution; historical CI/test execution is unknown."
}
```
