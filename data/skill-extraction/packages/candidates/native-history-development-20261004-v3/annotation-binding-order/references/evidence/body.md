# Reported reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:728:body",
  "source_id": "PyCQA/pyflakes:728",
  "available_at": "2022-09-08T20:06:47Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter showed `pyflakes /dev/stdin <<< 'x = x'` producing `/dev/stdin:1:5: undefined name 'x'`, while `pyflakes /dev/stdin <<< 'x: int = x'` produced no diagnostic. These are reported historical console observations, not commands executed by this package."
}
```
