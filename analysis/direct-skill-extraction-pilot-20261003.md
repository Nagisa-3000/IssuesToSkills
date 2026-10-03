# 直接提取 Skill：实现与真实小实验

截至 2026-10-03，默认链路已改为：

```text
Issue / PR / commit evidence
  → 模型直接编写完整 Skill 文件包
  → host 原样落盘、校验闭环与内容 hash
  → 从已验证 Markdown 派生 Episode / Action / Workflow 索引
  → graph / SQLite / HNSW
  → 加载真实 Skill 和 references 到 Agent context
```

新抽取不再先让模型输出 candidate_atomics、candidate_workflows 或 candidate_patterns
JSON，再把这些记录渲染成 Markdown。包里的 provenance 和 eval JSON 是审计信息与
评测定义；它们不替代可读的动作和工作流。Codex 的 `--json` 仅用于 CLI 事件日志，
新流程不传语义 JSON 的 `--output-schema`。

## 实现边界

- Codex 和 HTTP 抽取入口默认请求原生多文件文本包；显式支持 defer 和多个 Workflow 包。
- 发布器保存模型文件正文，额外添加 manifest/hash 和独立完整性验证脚本。
- 包必须包含 SKILL.md、历史 Episode、Workflow、Action/evidence 卡、provenance，及三类 eval。
- 先验证整个响应，再发布。拒绝残缺包、悬空引用、依赖环、非法路径、凭据及覆盖冲突。
- 图、目录、摘要、inventory 和治理入口从已验证文件读取；目录重建不改写作者正文。
- `universal-resolution-distiller`、`resolution-skill-creator`、生命周期治理已按直接编写修订。
- 历史 JSON 编译保留为显式迁移入口；历史 IR 不自动变成已完成 Skill。

实现见 [发布与投影模块](../src/arex_skill_graph/direct_skill_extraction.py)、
[Codex 抽取入口](../experiments/run_codex_issue_episode_extraction.py) 和
[直接文件协议](../data/skill-extraction/packages/universal-resolution-distiller/references/direct-skill-output-protocol.md)。

## 真实模型抽取

训练源为 google-gemini/gemini-cli 的 #25357，固定提交
`cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45`。只使用该提交、选定父提交、
实现/测试/调用点证据；未读取旧 candidate JSON 或持出解答。该例是已验证替代样本，
保留原始 manifest 的 seed/provenance 信息，不冒充原种子问题。

模型是 `openai/gpt-6.1-sol`，CLI 0.144.6，read-only sandbox，未绕过 sandbox。
三个尝试分别是 Linux DNS/网络失败、Windows 对 UNC 读取受限后的合理 defer、
以及独立 Windows 暂存 checkout 上的成功抽取。前两次没有包进入目录。

暂存 checkout 保留固定提交和父提交的缓存对象，所有变更文件完整；与原仓库的
选定 diff 按字节一致，hash 见 staging-report。暂存是稀疏的，未缓存的无关文件未
包含，没有安装依赖或执行历史测试。相关限制已进入模型的证据说明和成品 Skill。

生成的 [Skill 入口](../data/skill-extraction/packages/candidates/workflows/provider-endpoint-boundary-fcedf90eb77c/SKILL.md)
解决共享 provider SDK 构造边界中的 endpoint 覆盖、优先级、URL 检查和模式默认值。
包含 4 个 Action、8 张 evidence 卡、19 个模型编写文件；host 添加 2 个完整性文件。
模型编写的 19 个文件与响应正文逐字节一致。保留 5 个 activation、6 个 applicability、
4 个 functional case，全部标记 `not_executed`。

CLI 报告输入 302,740 token（其中缓存 254,464），输出 10,190 token。
这是整个多步抽取轨迹的累计统计，不是一次提示的长度；本次不估算费用。

## 验证结果

| 检查 | 实际结果 |
| --- | --- |
| 完整 Skill 结构、引用闭环、hash | 通过 |
| 原生响应与发布文件一致 | 19/19 文件逐字节一致 |
| 复制到独立目录，无 AREX 依赖的 verifier | 通过 |
| graph / SQLite | 4 Action、1 Workflow、4 WorkflowStep；另有 1 个不可服务的结构 Pattern 审计节点，共 10 节点 |
| exact 与 HNSW 检索 | 均返回同一个包支撑的 Workflow |
| 实际 context 加载 | 4 个 Action 与 Workflow/evidence references，33,475 字符 |
| 重建索引是否修改包 | 没有，原文件及 hash 保持一致 |
| inventory / Episode admission | 通过；持出 URL/ID 泄漏检查为 0 |
| 回归测试 | 157 项通过，包含 15 项新增行为检查 |
| 修改的 Meta-skill | 3 项 quick_validate 通过 |

这证明直接作者文件 → 校验 → 索引 → 检索 → context 的交付链路成立。
本次未执行历史源码测试、生成的 functional eval 或独立持出修复，不提供修复率、
迁移成功率或 SOTA 结论，也没有晋升任何 Pattern。HTTP 入口做了行为集成检查，
本次真实抽取使用的是 Codex CLI。

## 复核

无需模型、凭据或原始 checkout，即可重放冻结的真实抽取产物：

```bash
.venv-linux/bin/python experiments/run_direct_skill_smoke.py --output /tmp/arex-direct-replay
```

新模型抽取仍需可读的固定源 checkout 和已配置 CLI；每轮使用空的新输出目录。
原始成功响应、prompt、CLI 事件、校验和派生 Episode 位于
`data/skill-extraction/direct-skill-pilot-20261003/extraction-staged/`。
所有 JSON 图/目录文件均为验证后的派生数据。

[机器报告](../data/skill-extraction/direct-skill-pilot-20261003/pilot-report.json)、
[交付/检索验证报告](../data/skill-extraction/direct-skill-pilot-20261003/verification/verification-report.json)、
[inventory 校验](../data/skill-extraction/direct-skill-pilot-20261003/extraction-validation.json)
记录具体 hash、命中 ID、统计和边界。软件修复研究的正式 benchmark 与下一阶段
对照设计见 [顶刊/顶会调研](agent-software-repair-benchmark-survey-20261003.md)。
