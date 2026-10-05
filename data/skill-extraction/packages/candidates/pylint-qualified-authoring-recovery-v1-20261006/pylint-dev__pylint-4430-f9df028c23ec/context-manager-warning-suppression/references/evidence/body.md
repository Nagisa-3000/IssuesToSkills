# Original reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4430:body",
  "source_id": "pylint-dev/pylint:4430:repair:f9df028c23ec",
  "available_at": "2021-05-02T15:40:43Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report supplied a class whose __enter__ assigns self.fd = open(\"foo\") and whose __exit__ closes self.fd. It reported pylint a.py emitting R1732 in C.__enter__, under pylint 2.8.2, astroid 2.5.6 and Python 3.9.4. It requested suppression in __enter__ and suggested a warning if __exit__ did not release the resource. The missing-cleanup suggestion is not implemented by the supplied fix."
}
```
