# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8719:regression",
  "source_id": "pylint-dev/pylint:8719:repair:6fca82360c67",
  "available_at": "2023-06-13T19:14:21Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed fixtures assert no unspecified-encoding for dictionary mode rb on open; no encoding warning for dictionary mode w and encoding utf-8 on open, io.open and Path.open; bad-open-mode plus unspecified-encoding for dictionary mode 5 on open and io.open; unspecified-encoding for dictionary mode wt and encoding None on open and Path.open; and warnings for Path.write_text/read_text with dictionary encoding None but no warning with utf-8. Expected output marks inferred invalid modes INFERENCE, missing encoding with mode 5 HIGH, and dictionary-derived None encodings INFERENCE. Existing direct bad-open-mode and unspecified-encoding expected confidence changes from UNDEFINED to HIGH. These are historical committed assertions, not evidence of historical execution or executed Skill cases."
}
```
