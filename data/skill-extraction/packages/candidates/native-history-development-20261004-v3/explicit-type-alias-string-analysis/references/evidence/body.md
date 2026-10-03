# Reported reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:671:body",
  "source_id": "PyCQA/pyflakes:671",
  "available_at": "2022-01-20T19:25:35Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used pyflakes 2.4.0 with Python 3.8.6 on Linux. Their example imported os.PathLike and imported TypeAlias conditionally from typing for Python >= 3.10 or typing_extensions otherwise. PathLikeStr: TypeAlias = \"PathLike[str]\" produced foo.py:2:1 'os.PathLike' imported but unused. A comparison with \"PathLike[str]\" as function parameter and return annotations produced no output. These are reported historical observations, not execution by this package."
}
```
