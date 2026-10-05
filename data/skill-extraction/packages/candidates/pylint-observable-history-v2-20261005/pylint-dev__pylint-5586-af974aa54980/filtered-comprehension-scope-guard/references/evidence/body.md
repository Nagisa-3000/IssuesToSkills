# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5586:body",
  "source_id": "pylint-dev/pylint:5586:repair:af974aa54980",
  "available_at": "2021-12-22T04:38:35Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report ran `pylint a.py` on a function whose try block printed `value for value in range(1 / 0) if isinstance(value, int)` and whose except ZeroDivisionError block assigned `value = 1`. It reported E0601 at the filter reference and expected no message. The reporter stated that found_nodes included the exception-handler assignment and raised filtering in to_consume() as a possible responsibility, not an implemented solution. The report attributed the regression to bd55b27d41542e3ca1f031f986b6151f6cac457f in unreleased 2.13.0 development."
}
```
