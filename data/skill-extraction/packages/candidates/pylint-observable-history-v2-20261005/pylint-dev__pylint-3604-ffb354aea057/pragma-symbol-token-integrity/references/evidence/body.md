# Reported fragmentation and numeric workaround

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3604:body",
  "source_id": "pylint-dev/pylint:3604:repair:ffb354aea057",
  "available_at": "2020-05-11T15:28:48Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter described regression from pylint 2.4.4 to 2.5.0. A pocketlint message named found-_-in-module-class failed to disable symbolically: E0012 bad-option-value appeared for 'found-' and '-in-module-class', and W9902 warnings remained. Replacing the symbol with W9902 produced no output in the reported reproduction. The reported environment was pylint 2.5.0, astroid 2.4.1 and Python 3.7.7. These are reported observations, not executed Skill outcomes."
}
```
