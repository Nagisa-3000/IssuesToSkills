# Public reproduction and intended scope

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6350:body",
  "source_id": "pylint-dev/pylint:6350:repair:cb37ae4fc24a",
  "available_at": "2022-04-15T19:48:44Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter described two files importing os, sys, argparse, random, and math, reproduced without a pylintrc. The command was 'pylint package_name --enable=duplicate-code --ignore-imports=y'. Reported 2.14 output included R0801 for the five identical import lines and unused-import diagnostics. Expected 2.12 output retained unused-import diagnostics but omitted R0801. The report attributed the regression to commit 03cfbf3df1d20ba1bfd445c59f18c906e8dd8a62. These are reported historical observations, not newly executed Skill outcomes."
}
```
