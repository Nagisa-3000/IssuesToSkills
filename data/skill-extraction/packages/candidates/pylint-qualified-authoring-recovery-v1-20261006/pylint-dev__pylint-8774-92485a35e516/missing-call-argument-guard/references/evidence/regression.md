# Historical committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8774:regression",
  "source_id": "pylint-dev/pylint:8774:repair:92485a35e516",
  "available_at": "2023-06-18T14:43:15Z",
  "kind": "historical_regression_assertions",
  "observation": "The functional fixture adds copy.copy() expecting no-value-for-parameter; copy.copy(x=test_dict) without a shallow-copy warning; copy.copy(x=os.environ) expecting shallow-copy-environ; copy.copy(**{\"x\": os.environ}) expecting shallow-copy-environ; copy.copy(**{\"y\": os.environ}) expecting unexpected-keyword-arg; and copy.copy(y=os.environ) expecting no-value-for-parameter plus unexpected-keyword-arg. The expected-output file changes two existing positional shallow-copy-environ confidences from UNDEFINED to HIGH, records HIGH for direct x=os.environ, and INFERENCE for unpacked x. Ordinary argument-diagnostic confidences remain UNDEFINED. These are assertions committed at the historical revision; historical execution status is unknown."
}
```
