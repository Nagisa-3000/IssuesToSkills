# Reported overload contrast

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:470:body",
  "source_id": "PyCQA/pyflakes:470:repair:ee1eb0670a47",
  "available_at": "2019-09-23T09:05:30Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter states that synchronous overloads work since #435 but async ones do not. The reproduction imports overload from typing and defines two decorated synchronous f declarations followed by an undecorated implementation, then two decorated async g declarations followed by an undecorated async implementation. The reported command is 'python -m pyflakes .'. Reported output is \"18:1 redefinition of unused 'g' from line 14\" and \"22:1 redefinition of unused 'g' from line 18\". This is reported behavior, not an independently executed authored Skill reproduction."
}
```
