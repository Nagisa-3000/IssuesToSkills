# Agent-core function issue table: extraction and validation status

更新时间：2026-10-01（Asia/Shanghai）

这份状态只针对用户给出的 6 个 harness × 7 个 agent-core 功能类别表。旧的
10 类 universal pilot 仍然保留，但不与本表的结果混报。

## 当前边界

`experiments/manifests/agent-core-function-issue-table-v1.json` 是 42 条原表
issue 的 source-of-truth。每个类别保留一个 untouched repository 作为
leave-one-repository-out holdout，因此训练候选是 35 条、holdout 候选是 7 条。
holdout 行不能进入 ChangeEpisode、Action/Workflow admission 或 Pattern support。

截至本次检查，provider-interface-adaptation 已完成一轮独立替代样本 pilot，
context-budget-and-compaction 已完成精确候选的证据审计并成功抽取 1 条 exact
episode；structured-tool-contract-integrity 的 Qwen #4695 已成功抽取 1/1；
state-continuity-and-resume 已完成种子证据审计，并成功抽取 Hermes #228 exact
episode。credential-resolution-and-authentication 已完成种子证据审计，Hermes
#289 第二次重跑成功抽取 1/1；Qwen #9016 仍因 checkout object 未准备好而未抽取。
effect-control-and-
isolation 的 Hermes #232 已成功抽取 1/1；failure-recovery-and-streaming 的
Qwen #7832 已锁定到 PR #7896 并成功抽取 1/1。其余 exact table rows 仍不能
称为“已完成”。另外，旧 universal pilot 中已经有 4 条与 agent-core
类别高度相关的 verified substitute，已作为显式 supplement 加入统一目录，但不
计入 exact rows 完成率。

## 已完成的证据门禁

### Provider / endpoint 类（独立 pilot，不等同于原表 6 条 exact rows）

原表中有几条 issue 没有可定位的 implementation-bearing resolution，因此 pilot
明确使用了同类别的 verified substitute，并在 manifest 中保留 exact seed 与替代
关系，而不是静默替换。

- train：Aider #88、Hermes #125942、Qwen #11657、Pi #5832，4/4 admitted。
- holdout：Aider #199、Hermes #121359、Qwen #9452、Pi #4558。
- strict oracle qualification：3/4；Qwen #9452 在当前 qualification 环境中
  未通过，不能算 qualified holdout。

这批训练 episode 已经经过
`ChangeEpisode -> semantic Action -> Workflow DAG -> graph -> materialize`
链路，统一目录输出在：

- `data/skill-extraction/provider-endpoint-pilot-20260929-v3/unified-catalog/catalog.sqlite`
- `data/skill-extraction/provider-endpoint-pilot-20260929-v3/unified-catalog/catalog.hnsw`
- `data/skill-extraction/provider-endpoint-pilot-20260929-v3/unified-catalog/training-graph.json`

### Credential / authentication 类（原表 exact rows）

审计输出：
`data/skill-extraction/agent-core-function-issue-table-v1/credential-evidence-audit.json`。

| 原表行 | 当前证据结论 | 处理 |
| --- | --- | --- |
| Pi #9245 | `closed as not planned`，没有 merged implementation | 不抽取，保留为 rejected seed |
| Aider #750 | 文档/提问型 issue；是该类 holdout | 不抽取、不用于训练 |
| Hermes #289 | linked merged PR #295，merge ref `221e4228…`，本地对象可解析；重跑 1/1 admitted | exact train episode |
| Codex #48299 | duplicate，关联的 #48237 仍不是已合并修复 | 不抽取，保留为 unresolved seed |
| Gemini #28337 | stale 后关闭为 not planned，无 implementation PR | 不抽取，保留为 rejected seed |
| Qwen #9016 | linked merged PR #9017，merge ref `fd9c452d…` 已由 API 验证；当前 checkout 尚未包含该 object | train candidate，等待 checkout object 准备 |

所以该类目前是 2/5 train rows 具备实现候选，其中 Hermes #289 已生成
`valid=true`、`admitted=true` 的 exact ChangeEpisode；Qwen #9016 的 merge object
还没有落到 checkout，暂不启动第二条不完整 extraction。Pi #9245、Codex #48299、
Gemini #28337 仍需要同仓库同类的 verified substitute；holdout Aider #750 不能
拿来做代码修复 oracle。

Hermes #289 的 episode 具体提取了三步：诊断 endpoint-specific 与 generic key
的 precedence 冲突、在 CLI 与 shared resolver 两条链上统一顺序、验证 both-keys-set
与 fallback-only 两种环境状态。输出在：
`data/skill-extraction/agent-core-credential-training-v1/codex-train-hermes-windows-luna-rerun/`。

### Context budget / compaction 类（精确候选 + 显式 supplement）

精确表格 6 条的审计输出在：
`data/skill-extraction/agent-core-function-issue-table-v1/context-evidence-audit.json`。

- Qwen #11894：merged PR #11909、merge ref `398739139…` 本地可解析，Codex
  抽取 1/1 admitted；episode 直接覆盖 input/output 两个 token-limit 映射、调用点、
  regression test 和验证 oracle。
- Hermes #43547：作为 leave-one-repository-out holdout，只审计不抽取。
- Pi #10075、Aider #3493、Codex #16281：关闭状态没有可定位的 merged
  implementation resolution；不能从 closure 生成 episode。
- Gemini #27738：存在多个不相干/未合并关联 PR，审计为
  `ambiguous-linked-resolutions`，不自动选最新 PR。

为获得跨仓训练覆盖，另保留 4 条带完整 before/after/diff/evidence 的旧 pilot
episode（Aider #1842、Hermes #125235、Qwen #12029、Gemini #29080）作为
`context-budget-and-compaction` supplement；它们的原始类别、替代关系和 scope
caveat 写在 `metadata.supplement_provenance` 中，没有被伪装成原表 issue。

### State continuity / resume 类（精确候选证据审计）

审计输出：
`data/skill-extraction/agent-core-function-issue-table-v1/state-evidence-audit.json`。

- Hermes #228 的 issue timeline 混入了多个无关 PR；manifest 已固定首选修复 PR
  #229。该 PR merge commit `56b53bff…` 在本地 checkout 可解析，且改动包含
  `run_agent.py` 和 `tests/test_run_agent.py`；Codex 抽取已 `valid=true`、
  `admitted=true`。episode 提取了“在 turn append 前隔离 caller-owned history”
  与“验证输入 history 不变、返回 history 增长”的两个 grounded Action。
- Pi #10121、Aider #2979、Gemini #29194、Qwen #9573 均为 closed without merged
  resolution；Gemini 的 #29195/#29292 仍是 closed、未合并的候选修复。
- Codex #47761 保留为 leave-one-repository-out holdout，只审计，不进入训练。

当前 summary 是 1 个 implementation-bearing candidate、1 个 holdout、4 个
closed-without-merged-resolution，ambiguous linked resolutions 已通过首选 PR
消解为 0；state 类已获得 1 条 exact admitted episode，但其余 4 个 train row
仍不能从 issue closure 推导出可抽取修复。

### Effect isolation / failure / streaming 与 structured tool 类

Effect/isolation 类现在有一条 exact admitted episode：

- Hermes #232：issue 的 newline bypass 已定位到 PR #233 / merge ref
  `7166647ca1…`。Codex 抽取 1/1 admitted；episode 提取了
  `newline-aware-dangerous-pattern-guard` 和
  `multiline-dangerous-command-regression-coverage`，workflow 为
  `close-multiline-dangerous-command-detection-gap`。实现只增加 `re.DOTALL`
  并保留原有 approval/blocked contract，同时加入 4 个 multiline regression
  tests。
- Pi #9936、Aider #3009、Codex #42184、Gemini #26004、Qwen #10859 当前均
  没有可用的 merged implementation resolution；Qwen #10859 仍是该类别的
  leave-one-repository-out holdout，因此不从 closure 生成 episode。

Failure/streaming 类现在也有一条 exact admitted episode：

- Qwen #7832：issue 明确对应 PR #7896 / merge ref `d7c0d4ca77…`，已修正旧的
  `ddd4659d10…` 错误 ref。Codex 抽取 1/1 admitted；episode 提取了按
  caller-visible progress 分流 retry、request-only continuation、按 attempt
  边界去重 overlap、plain retry 前清理 continuation state 四个 Action，workflow
  为 `recover-a-long-stream-after-a-transport-cut`。
- Hermes #121320：本地修复链在 `13ff15abc5…`，包含 `message_stop` gate、live
  delta streaming 和 streaming tests；Windows Codex 抽取 900 秒超时，Linux
  Codex 则因 `127.0.0.1:15721` Responses stream 断开而失败，暂不计入 admitted。
- Aider #3648、Codex #39988、Gemini #29264 与 Pi #9735 目前只有 closure/
  stale/not-planned 或无法绑定的 implementation 证据；Pi #9735 是该类别
  holdout，不进入训练。

- Qwen #4695：本地 commit `3ce46949c2…` 的 loop-detection change 明确提到
  `#4695` repeated shell inspection loop，并带有 service/test/client 变更。单实例
  Windows Codex 重跑已经完成，`valid=true`、`admitted=true`，并提取出
  normalize / guard / reset / typed-outcome / propagate 五个 grounded Action 及
  一个有阈值与 fail-open 边界的 Workflow。输出在：
  `data/skill-extraction/agent-core-structured-tool-training-v1/codex-train-qwen-windows-luna-single/`。

因此 structured-tool 类现在有 1 条 exact admitted episode；其余 5 条 exact row
仍只完成候选/审计或尚未抽取，不得据此宣称整类完成。

已有的 provisional substitute 仍然可用于结构分析：Hermes #123989（effect
isolation）、Qwen #12683（structured permission aggregation）、Gemini #28339
（failure classification）、Qwen #12047（state continuity）。它们来自先前
admitted-and-verified episode 文件，并通过显式 supplement provenance 进入 composed
catalog，不替换 exact table rows。

## 统一系统入口

现在不再为每一类各自维护一套 graph 逻辑，统一入口为：

1. `experiments/audit_issue_seed_evidence.py`：读取 manifest，检查 issue 状态、
   timeline 关联 PR、merged ref 和 local object。关闭状态本身不等于 resolution；
   多个交叉引用 PR 且没有明确首选关联时输出 `ambiguous-linked-resolutions`。
2. `experiments/run_codex_issue_episode_extraction.py`：以 pinned implementation
   ref 和 checkout 为边界，按修正后的
   `data/skill-extraction/packages/universal-resolution-distiller/SKILL.md`
   抽取 ChangeEpisode。没有 before/after、实现、调用点和验证 oracle 时拒绝。
3. `experiments/build_agent_core_catalog.py`：只接受 manifest 中的
   `train_candidate` episode，构建一个跨类别的
   `Action -> Workflow -> Pattern` graph，物化 SQLite，并可生成 HNSW。
4. `experiments/audit_action_factorization.py`：审计跨仓 Action 是否能安全复用，
   同时把可复用的 Workflow-role skeleton 与真正可复用的 Action 分开。
5. `experiments/summarize_guided_agent_comparison.py`：对 holdout 做 paired
   no-skill/guided 的 correctness、token、耗时和 leakage 汇总。

## Action 复用与粒度验证

对当前跨类别 composed catalog（provider 4 条训练 episode、context 的 1 条 exact
加 4 条 supplement、credential 的 Hermes #289 exact episode、structured 的 Qwen
#4695 exact episode、state 的 Hermes #228 exact episode、effect 的 Hermes #232
exact episode、failure 的 Qwen #7832 exact episode，以及其余 verified supplements）
运行结果：

- grounded Action：58；Workflow：21；可检索的 workflow fragment：9。
- 跨仓 Action pair：1144；`safe-reuse-candidate`：0。
- 当前总目录中的 18 个 training episode 包含 6 个原表 exact row episode 和 12 个
  显式标注 provenance 的 supplement；不能把 18/42 解读为 42 条 exact row 已完成。
- 当前已 admission 的 6 条 exact row 是：Qwen #11894（context）、Hermes #289
  （credential）、Qwen #4695（structured tool）、Hermes #228（state）、Hermes
  #232（effect/isolation）和 Qwen #7832（failure/streaming）。provider 的 4 条以及其余目录项仍是显式
  supplement，不改变原表 42 行的完成口径。
- 已经被多个仓库共同支持的 Action：0。
- 相同 finite verb 但 semantic owner 不同的 pair：77。
- Workflow-role skeleton：9 个，其中 5 个在同一类别跨仓重复，7 个是跨类别的
  通用骨架；代表性片段包括 `establish-contract -> reconcile`、
  `reconcile -> implement`、`implement -> validate`，以及 structured-tool 的
  `normalize -> guard -> reset -> map -> propagate`。
- 只有 1 个 Action 触发 split-review 信号；它是 Hermes 的 persisted-route
  resolver。该信号只要求人工检查，不会自动拆分，因为当前证据仍显示一个主要
  postcondition 和一个验证契约。

审计文件：
`data/skill-extraction/agent-core-composed-v1/unified-catalog-with-structured-state-effect-failure-credential/action-factorization-audit.json`。

工作流片段已经以低置信、不可直接执行的 workflow node 写入 SQLite/HNSW；它们只
保存角色序列、支持仓库/类别和原始 occurrences，不把具体 Action 自动绑定成同一
个实现。当前 composed catalog 的物化统计是 58 Action、21 实例 Workflow、9
fragment、7 个类别 Pattern 节点、153 个检索 embedding：
`data/skill-extraction/agent-core-composed-v1/unified-catalog-with-structured-state-effect-failure-credential/catalog.sqlite`。

当前证据支持的原因判断是：Workflow 的控制流角色可以抽象复用，但 Action
不能仅因都叫 `adapt` / `reconcile` / `validate` 就合并。不同仓库的这些动作通常
有不同的 semantic owner、pre-state、post-state 和 validation oracle；如果强行
合并，检索得到的参数看似相似，却不能保证替换到目标仓库后仍满足状态契约。

因此暂时应该复用两层：

- 复用 Workflow skeleton：`diagnose/establish-contract -> reconcile/adapt ->
  validate/repair`，节点上保留条件、anti-goal 和 stop condition。
- 复用 Action 只有在 semantic owner、finite operation、pre/post state 和 oracle
  全部一致时才允许；否则保留为不同 Action，由同一 skeleton 的不同实例承载。

当前扩展后的审计仍没有出现“同 owner、同 operation 但 contract 字段不同”的
pair；因此目前没有证据说明需要普遍把 Action 再拆小。唯一的 split-review 仍是
一个复合描述信号，需检查是否存在独立 postcondition/oracle，而不是自动拆分。更
准确的结论是：先复用 Workflow skeleton；只有未来出现同 owner/operation、而
pre/post/oracle 差异稳定重复时，才考虑把 Action 拆成更小的契约单元。

检索环境已用 HNSW 与 SQLite 重新验证：structured-tool 查询命中
`break_syntactically_varied_read_only_shell_loop`，state 查询命中
`resume-from-history-with-caller-state-isolation`，provider 查询命中
`adapt-session-resume-to-a-versioned-provider-route`，failure 查询命中
`recover-a-long-stream-after-a-transport-cut`，effect 查询命中
`close-multiline-dangerous-command-detection-gap`，credential 查询命中
`repair-provider-specific-credential-precedence-with-fallback`；这些查询的 closure
`unresolved` 均为空。为此修正了候选 Pattern 的 closure 门禁：没有 mandatory
action 的未晋级 Pattern 仍可被检索，但不再伪报“没有 declared steps”；只有已
声明 mandatory action 却缺失图边时才报告 unresolved。

代码与 catalog 回归验证：`PYTHONPATH=. ./.venv-linux/bin/pytest -q`，73 tests
全部通过。

## 未抽取 holdout 的 token 对比

使用 provider pilot 中未进入训练抽取的 Aider #199 做一次 paired comparison：
`data/skill-extraction/provider-endpoint-pilot-20260929-v3/agent-eval-aider-v2/holdout-token-comparison.json`。

| 指标 | no-skill | guided | guided - no-skill |
| --- | ---: | ---: | ---: |
| visible test | pass | pass | correctness tie |
| input tokens | 297,881 | 555,345 | +257,464（+86.4%） |
| output tokens | 3,724 | 4,507 | +783（+21.0%） |
| wall time | 163.26s | 249.55s | +86.29s（+52.9%） |

两个 arm 都没有编辑 visible tests，solution ref 都隐藏，leakage gate 通过。这个
样本说明当前 guided prompt/catalog 的成本收益还没有被证明；它不是“skill 一定
有害”的统计结论，因为只有一个 paired holdout，后续必须在更多类别、更多仓库
上复现。

## 当前可复现实验入口与下一步顺序

统一训练 manifest：
`experiments/manifests/agent-core-composed-training-v1.json`。

类别 supplement 的 provenance 适配器：
`experiments/prepare_context_budget_substitutes.py`、
`experiments/prepare_agent_core_substitutes.py`；统一 catalog 入口：
`experiments/build_agent_core_catalog.py`。

1. 等 Qwen checkout 补齐 #9017 merge object，再用当前支持的 Codex model 抽取
   Qwen #9016；Hermes #289 已完成，不再重复运行。失败必须记录为 checkout 或
   model blocker，而不是生成空 episode。
2. 为 credential 类的 Pi、Codex、Gemini 三个 rejected seed 搜索同仓库的
   implementation-bearing substitute，且保留原表 issue 为 holdout/负证据，不替换
   source-of-truth。
3. 对 state 其余 4 个 train row、structured-tool 其余 5 个 row，以及
   effect-isolation/failure-recovery 中尚未获得 implementation-bearing resolution
   的 exact table rows 继续做 evidence audit。现有 Qwen/Hermes/Gemini substitute 只能作为
   provisional coverage，不能替换精确表格审计。
4. 对 Hermes #43547 holdout 或其他未抽取 holdout 增加第二组 no-skill/guided
   paired comparison；当前 Aider #199 结果只是一组方向性样本。
5. Pattern 只在同类别跨仓 Workflow、精确 evidence 和 holdout 都通过后晋级；当前
   composed catalog 的 6 个 Pattern 都保持 `insufficient-structural-support` 或
   candidate 状态，没有被提升为强制共享 Action。
