# Historical report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3468:body",
  "source_id": "pylint-dev/pylint:3468:repair:fb332490c2e5",
  "available_at": "2020-04-01T02:15:10Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied a function with try returning bar.baz and except AttributeError containing pass. No inconsistent-return-statements warning was reported; returning a value in the except clause reportedly did warn. Expected behavior was a warning for implicit exception-path return unless a value was explicitly returned in the handler or at function end. Reported versions were Pylint 2.4.4, astroid 2.3.3, and Python 3.6.7. These are report observations, not recorded historical CI results."
}
```
