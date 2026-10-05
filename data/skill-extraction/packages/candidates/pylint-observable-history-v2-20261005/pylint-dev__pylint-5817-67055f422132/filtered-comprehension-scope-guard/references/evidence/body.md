# Original public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5817:body",
  "source_id": "pylint-dev/pylint:5817:repair:67055f422132",
  "available_at": "2022-02-17T13:07:36Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied a function with try: some_list = [e for e in (1, 2, 3) if e], followed by except Exception as e: pass. Running 'pylint used_before_assignment.py -E' reportedly produced E0601 at 3:45 on the filter name. The expected behavior was no error because the comprehension and handler bindings have different scopes. Reported versions were Pylint 2.12.2, astroid 2.9.3, Python 3.9.0. This is reported output, not an independently observed historical test run."
}
```
