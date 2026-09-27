# Modified files — this extraction run

本 run 只创建/修改以下目标目录内的分析产物；没有修改 `hermes-agent` 源码、历史 commit 或其他 agent run。

## 本 run 新建文件（完整路径）

- `/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/agent-runs/hermes-independent-2026/evidence.md`
- `/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/agent-runs/hermes-independent-2026/cases.json`
- `/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/agent-runs/hermes-independent-2026/atomic-skills.md`
- `/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/agent-runs/hermes-independent-2026/workflow-skill.md`
- `/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/agent-runs/hermes-independent-2026/promotion-decision.md`
- `/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/agent-runs/hermes-independent-2026/modified-files.md`

## 被分析的真实 Hermes commit 修改文件（仅记录，不在本 run 修改）

### Case 1 — `f92006ce1cda1a40249fa4d5dd9c663f70a9de8d`

- `run_agent.py`
- `tests/run_agent/test_compression_feasibility.py`

### Case 2 — `35a0803a3b64a0b43e49dbbc809c4986be3ae331`

- `hermes_cli/config.py`
- `scripts/release.py`
- `tests/tools/test_delegate_summary_budget.py`
- `tools/credential_files.py`
- `tools/delegate_tool.py`

### Case 3 — `903b9bf1873fa52daf9d0000c83ac7ffeb28fc4a` + `09138852500bc02062008a565942c0c9176b2fc3`

- `agent/tool_executor.py`
- `agent/turn_usage.py`
- `tools/delegate_tool_results.py`
- `tests/agent/test_sequential_deadline_delegate_exempt.py`
- `tests/tools/test_delegate_summary_budget.py`

### Case 4 — `76381e2a8e3a21fbbd0a192b4b5f7356a7ca47b8`

- `agent/context_compressor.py`
- `cli-config.yaml.example`
- `hermes_cli/config.py`
- `tests/agent/test_compression_small_ctx_threshold_floor.py`
- `tests/agent/test_context_compressor.py`
- `tests/run_agent/test_infinite_compaction_loop.py`

### Explicitly analyzed but excluded from selected cases

- `agent/display.py`, `run_agent.py`, `tests/test_context_pressure.py` in `15cfd2082083099bff7e6d7f61544f802ad06170` — display/telemetry mechanism.
- `agent/tool_executor.py`, `tests/agent/test_sequential_deadline_delegate_exempt.py` in Case 3 — deadline exemption is recorded as adjacent liveness evidence, not selected as a separate capacity case.
- `tools/delegate_tool.py` and related files in `6e369a37622be1785c94640663752cdb655a1f2a` — worker concurrency capacity.
- Files in `c68091c04`, `40051c2a1`, `3f7e0fd07` — compression concurrency/generation ownership.
