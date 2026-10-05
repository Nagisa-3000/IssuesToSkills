# Committed regression

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4612:regression",
  "source_id": "pylint-dev/pylint:4612:repair:93d6c39e8fbb",
  "available_at": "2021-06-23T20:31:17Z",
  "kind": "historical_regression_assertions",
  "observation": "The repair added tests/functional/r/regression/regression_4612_crash_pytest_fixture.py. It disables missing-docstring, consider-using-with and redefined-outer-name, imports pytest, and defines @pytest.fixture function qm_file. Its body assigns `qm_file = open(\"src/test/resources/example_qm_file.csv\").read()` and returns qm_file. This is committed analyzer regression input. Historical execution status is unknown in the supplied core evidence. Later qualification is validation-only provenance, not a backdated historical execution."
}
```
