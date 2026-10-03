# Workflow records → 可使用的 Skill Packages：小样本验证

日期：2026-10-03。范围按用户要求限定为 **2 条现有训练 Episode、2 个
Workflow 包及一个合成代码任务**，没有扩展到全量 83 Workflow，也没有
创建子代理或额外会话。

## 核心修正

旧流程的完成条件只检查 `codex-response.json` 中 Episode、Atomic、Workflow
的结构和证据引用。`universal-resolution-distiller` 把真正包编译放到了
Pattern promotion 之后，导致 JSON 准入被当成 Skill 提取完成。

新流程将包编译纳入强制交付：

```text
evidence → structured IR → evidence validation
         → Workflow package materialization → package validation
         → admitted_candidate → catalog/index → verified package hydration
```

只有 JSON 的结果是 `structured_only` / `materialization_pending`。
`extraction_success`、`admitted` 和 `skill_materialized` 只有在全部 Workflow
包实际存在、文件及引用闭合、内容哈希正确时才为 true。伪造 JSON 中的
`package_validated` 标志不能绕过文件检查。

Episode 是历史证据；Atomic 是 Action reference；Workflow 是本实验的
candidate Agent Skill 单位。图节点、SQLite 和 HNSW 保留为 IR / 索引。
生成包和 eval 定义不代表执行了功能评测，也不代表 promotion。

## Git 与路径

开始时工作区干净，分支为 `main`。重新执行 `git status`、`git log -5
--oneline`、`git rev-parse HEAD`、`git rev-parse origin/main`，并重新
`git fetch origin`。本地和 fetch 后的远端均为：

```text
9abf2a68fca1c0a06cc5b3d1789fbb21da444fed
```

唯一 canonical Skill 根目录继续使用 `data/skill-extraction/packages/`。
元技能保持原址，生成的候选 Workflow 包使用其中的
`candidates/workflows/`。没有复制另一套会漂移的元技能目录，没有修改
2026-10-01 冻结的 20 类原始抽取语料。

实现与实验产物在用户确认后提交并发布到 GitHub `main`；提交及推送前
再次核对远端状态、完整测试和待提交文件的凭据扫描。

## 实际修改

| 层次 | 文件与行为 |
|---|---|
| 元技能 | `universal-resolution-distiller` 强制包生成；`resolution-skill-creator` 区分证据验证、包准入与 promotion；evaluator / lifecycle 规定验证包之后才能注入指导 |
| 新响应协议 | `schemas/codex-change-episode-v3.schema.json` 强制 Workflow 的 `skill_contract`：name、description、applicability probes、failure modes、known limitations；保留 v2 用于历史迁移 |
| 编译器 | `src/arex_skill_graph/skill_packages.py`：确定性渲染 Action/evidence 文档、稳定路径及 ID、manifest/hash、三种 eval、独立验证脚本；拒绝人工修改冲突 |
| 抽取准入 | `experiments/run_codex_issue_episode_extraction.py` 的 `finalize_extraction` 在生成包之前不返回 admitted Episode；拒绝 holdout 和失败的提取进程 |
| 小样本迁移 | `experiments/materialize_candidate_skills.py`：显式训练 allowlist、已验证响应、`--check`、新实验目录；不修改冻结来源 |
| 图/SQLite | graph Workflow 的 `skill_package` 记录 path、version、hash、source IDs、compiler version；新目录默认要求包，SQLite 写入前检查包 |
| Inventory | CLI 默认要求包完整；`--structured-ir-only` 仅审计历史 JSON。新摘要分别统计 IR、package 数量和 package-backed Episode |
| Retrieval | `require_skill_package=True` 过滤无包、deferred、inactive、篡改或陈旧的记录；加载实际 `SKILL.md` 与 Action files。语义 judge 接收同一包 context |
| Pattern 边界 | legacy Pattern compiler 拒绝语义 deferred/rejected 来源；本实验没有生成或晋升 Pattern 包 |

编译器先在临时目录验证，再原子落盘。再次编译必须与所有现有文件完全一致，
包括包内新增的手工文件；发生差异会明确失败并保留原文件。哈希不包含
manifest 本身，避免递归。包引用不会参与源内容哈希，避免重复运行漂移。
完整 Workflow payload 必须与编译时的语义契约一致；改了 Workflow 却继续
引用旧包会被作为 stale package 拒绝。

## 两条训练记录与真实包

| 来源 | Workflow ID | 包路径 | 验证 | Actions |
|---|---|---|---|---:|
| google-gemini/gemini-cli #25357 | `workflow:a1416952c048b7d5` | `data/skill-extraction/packages/candidates/workflows/safely-adapt-provider-endpoint-configuration-9c9708e650cca7f6/` | passed / candidate | 3 |
| Aider-AI/aider #88 | `workflow:b5dccd8edcc90ddd` | `data/skill-extraction/packages/candidates/workflows/adapt-compatible-provider-configuration-and-31690ae4d804c5bf/` | passed / candidate | 3 |

两份包都包含：

```text
<skill-name>/
├── SKILL.md
├── manifest.json
├── references/
│   ├── actions/*.md
│   ├── evidence/*.md
│   ├── workflow.md
│   └── provenance.json
├── evals/
│   ├── activation-cases.json
│   ├── applicability-cases.json
│   └── functional-cases.json
└── scripts/verify_package.py
```

统计：2 candidate Workflow packages，2 验证通过，0 编译失败/延迟，
6 Actions，0 Pattern packages，0 promoted packages。当前 corpus 的规模
仍是 20 类、80 training Episodes、218 Atomic records、83 Workflow records；
本轮只物化上述两个。冻结 inventory 没有新包映射，因此包准入检查会报告
其仍是有效 IR、尚未完成包迁移，不能按历史 `admitted_episodes` 字段宣称
80 次完整 Skill 提取。

## Agent 使用小实验

当前会话先读取生成的 SDK endpoint Skill 及其三个 Action reference，然后
按 `resolve → guard → adapt` 在独立合成代码样例中实现
`functional/endpoint_after.py`。入口是当前任务的 configuration / provider
SDK constructor boundary，测试通过 fake constructor 观察实际参数，
不会发出网络请求，也不需要凭据。

观测维度包括：explicit > environment 的优先级、两 provider 的 environment
选择、保留显式 false / true mode、未配置 endpoint 时保留默认行为、
loopback HTTP、remote HTTP / malformed endpoint 拒绝，以及 unknown
provider 时在构造 SDK 前停止。

| 检查 | 实际结果 |
|---|---|
| 包结构、内容哈希、Action/evidence 闭合 | 2/2 passed |
| 独立脚本，可复制到其他目录执行 | passed；回归测试还验证了 relocated package |
| 重复编译 / `--check` | 同路径、同内容、同 hash；passed |
| SQLite materialization / retrieval / actual package hydration | passed，检索到包并加载了 `SKILL.md` 与 Action files |
| 合成代码修复前，同一组 14 条 oracle | 5 passed，9 failed |
| 当前会话使用包完成修复后 | 14 passed，0 failed |
| 20 个 holdout 的公开 URL / ID 扫描 | 0 identifier leaks；未加载 solution，也未用于生成包 |
| 原始源码仓库 CI / 真正 SDK / end-to-end provider 请求 | 未执行 |
| 独立模型 activation / paired no-skill vs guided / holdout 泛化 | 未执行；没有这些能力提升的结论 |

这不是一个独立盲测：修复由当前会话执行，smoke 脚本重放已记录的适用性
判断与修复结果，没有产生新的模型调用。其作用是证明产物真的以包存在，
能通过索引找到、验证、注入 context，并提供能落实到代码和 oracle 的指导。
包中的训练 eval 定义仍明确为 `not_executed`；合成执行结果保存在独立
`pilot-report.json`，没有篡改编译产物的 lifecycle 状态。

## 验证与复现

起始完整测试：`127 passed`。

修改后完整测试：`142 passed`。新增回归覆盖 JSON-only / 伪造完成标志、
真实包强制准入、幂等及人工修改保护、dry-run、复制后的独立使用、
Action/evidence closure、断链和循环依赖、holdout 拒绝、catalog 映射、
哈希及陈旧包拒绝、deferred serving 拒绝、v3 schema、以及 judge 实际收到
entrypoint 和 Action context。历史 graph/retrieval/evaluation 测试保留。

新增代码通过 Ruff 检查；两个新包及修订的元技能通过 Skill Creator 的
frontmatter/naming quick validator。项目包验证器和包内独立 verifier
均通过。`git diff --check` 通过。

```bash
.venv-linux/bin/python -m pytest -q
.venv-linux/bin/python experiments/run_skill_package_smoke.py
```

只检查选定来源能否重现已写的包：

```bash
.venv-linux/bin/python experiments/materialize_candidate_skills.py \
  --manifest experiments/manifests/agent-core-seven-category-extraction-v2/train-all.json \
  --case-dir data/skill-extraction/agent-core-seven-category-extraction-v2/codex-5.6-sol-contract-v2-20261001/01-provider-interface-adaptation/Aider-AI__aider__88 \
  --case-dir data/skill-extraction/agent-core-seven-category-extraction-v2/codex-5.6-sol-contract-v2-20261001/01-provider-interface-adaptation/google-gemini__gemini-cli__25357 \
  --check
```

机器可读结果位于 `data/skill-extraction/package-materialization-pilot-v1/`：
`package-materialization.json` 为 Workflow → Package 映射，
`training-graph.json` 和 `training-episodes.json` 为本次两条训练的投影，
`pilot-report.json` 保存 package hashes、hydrated Action IDs、检索 trace、
context hash、实际 oracle 结果、holdout audit 和限制。

## 保留的限制

- 未进行 83 Workflow 和 accepted Pattern 的全量迁移；也没有再抽取任何 holdout。
- legacy Pattern packages 保留 v1 契约用于兼容/审计，不能冒充本轮 v2 Workflow
  包，也不会通过新 guided serving path。
- 新提取使用 v3 协议；本轮两个历史 v2 record 采用证据内已有字段和明确的
  compiler defaults 补齐通用适用性/失败分类，没有捏造测试通过或跨项目泛化。
- semantic graph admission / dedup 的旧研究接口仍可处理 IR；active graph
  node 不等于 promoted 或可注入的 Agent Skill，serving 有独立包门槛。
- 本实验没有证明生产 SDK、安全规则在所有环境可用，也没有证明 Agent 效率提升。
