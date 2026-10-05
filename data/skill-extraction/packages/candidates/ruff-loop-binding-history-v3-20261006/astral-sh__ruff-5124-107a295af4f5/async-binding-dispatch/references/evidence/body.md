# Public reproduction

```arex-evidence-v4
{
  "id": "astral-sh/ruff:5124:body",
  "source_id": "astral-sh/ruff:5124:repair:107a295af4f5",
  "available_at": "2023-06-15T18:23:11Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter stated that PLW2901 redefined-loop-name panicked on 'async def f():\\n    async with a:\\n        return await b'. The reported command was 'ruff --no-cache --select PLW2901 tasks.py'. The report called it an explicit panic and omitted the backtrace, linking to the rule source. This is a reporter reproduction, not an independently observed historical run."
}
```
