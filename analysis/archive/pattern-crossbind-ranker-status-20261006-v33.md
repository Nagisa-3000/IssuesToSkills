**尚未全部完成。M0–M3 已有核心代码；真实泛化、互补组合和有效排序尚未通过验收，M4–M6 未完成，正式 SWE 运行数仍为 0。**

本次依据见[机器快照 v33](results/pattern-crossbind-ranker-current-status-20261006-v33.json)和[执行归因与机制发现审计](results/guidance-attribution-and-mechanism-discovery-audit-20261006-v1.json)。[历史报告 v32](archive/pattern-crossbind-ranker-status-20261006-v32.md)与旧实验、失败收据均保留。

| 阶段 | 已实现 | 尚未验收 |
| --- | --- | --- |
| M0 | Action/Pattern/Task/Plan 契约、包 hash、来源、时间和输入隔离 | 全包功能验证、全语料因果复核、正式 KB 准入 |
| M1 | 按角色、必要效果与偏序生成当前 DAG；历史 Workflow 不变；变更有来源和理由 | 新 Issue 上的可执行 Pattern 重写与修复收益 |
| M2 | 六阶段 CrossBind、PASS/FAIL/UNKNOWN、前提与验证闭包、冲突/循环检查；最多两父、四组合 | 真正互补的两父 Workflow 组合执行及增量效果 |
| M3 | Workflow/Plan 两处 prompted 排序、硬门槛、拒绝/探查、角色补召回、共同预算 | 有用开发校准及同冻结候选池的排序效果 |
| M4 | 时间隔离、监督/训练/checkpoint 入口；新增执行归因与历史分支真实状态保留 | 有用适用性标签、非平局效用偏好、合格训练 Ranker、开发校准 |
| M5 | 冻结与验证工具 | KB、任务并集、索引、模型、阈值、预算与协议联合冻结 |
| M6 | 配对修复与消融入口 | 正式 SWE 修复、回归损害、成本、模块消融及排序配对比较 |

本次纠正了 #470 小实验的归因。B0 与引导分支均通过限定范围的 23 项独立测试；引导分支在修改代码之前执行了 `drop_guidance`，原因是当前历史计划仅允许探查，且本轮前提探查次数已用完。它随后使用当前公开代码正常求解，tokens 比 B0 多 20.54%。因此，这条结果是“候选曝光后回退的整套分配策略结果”，没有证明历史 Workflow 执行成功、正向适用性或 Skill 修复收益。旧原始结果及旧标签未覆盖，[更正记录](pilots/pyflakes-470-guidance-attribution-20261006-v2/attribution-correction.json)给出新标签的限定范围。

[guidance_attribution.py](../src/arex_skill_graph/guidance_attribution.py)与 [adaptive_runner.py](../src/arex_skill_graph/adaptive_runner.py)现在记录每次请求的真实引导状态、显式回退和 Action 记录所处状态；这些记录本身不建立计划执行。执行标签明确使用 `assigned_candidate_policy`。未带这种归因的旧执行标签保留供审计，但不能进入新的合格效用训练和校准。独立适用性监督仍与执行效用分开。历史监督入口现在保留真实最终公开字节、权限和 TaskContext，并将相关实现纳入实验身份。

#470 的事后输出复核仍未合格。恢复出的内容 hash 和两份被引用文件的 hash 都相同，但执行权限 hash 与原记录不同；原始完整 TaskContext 也没有保留。[预检](pilots/pyflakes-470-guidance-attribution-20261006-v2/mechanical-output-preflight.json)记录了这项缺口。没有启动语义输出复核，没有补造权限、绑定、前提或 CurrentOracle，也没有提升事实、端口或 Workflow 成功状态。

[发现入口](../experiments/discover_native_history_patterns.py)增加了 `--stage discover`：先分析完整语料并检查分组，不自动作者全部包；作者阶段可复用完全相同的发现输入。本次真实发现覆盖全部 98 个已供给原生包，提出 6 个跨项目分组、16 个项目内分组。[发现记录](mechanisms/native-full-corpus-20261006-v1/discovery/discovery-inventory.json)保留完整输入与来源。98 是已供给包数，仍不是 98 个已完成功能验收的 Skill。

独立审阅使用原始生产 diff 与回归断言，核对全部 22 组。最终接受 20 组：5 个跨项目机制、15 个项目内模板；2 组延迟。遗漏不同参数集合的三个修复没有建立统一的语义状态；Boolean 建议的两次修复对未知推断采取了不同回退策略，不能被统一成一条“保留歧义”规则。[合并评审](mechanisms/native-full-corpus-20261006-v1/adjudication/merged-review.json)和[待作者组](mechanisms/native-full-corpus-20261006-v1/adjudication/accepted-authoring-groups.json)均可复核。**本次新生成的 Pattern/Template Skill 包为 0，功能 eval 为 0，正式 KB 准入为 0。**

复审准备曾按 Issue 而非精确 source/fix 查询，混用了 #5406 的两次修复；第一轮也未取到非相邻目录中的 Ruff diff。旧输入、旧评审和失败保留。纠正后逐一验证了 57 个参与来源的 fix、revision 和 available_at，并重新评审受影响的两组。同一 #5406 的两次修复仍只算一个因果来源。补充评审引用了已提供的精确 source packet ID，以区分同 Issue 的重复 evidence ID；闭合引用策略更正单独记录，未增加来源或修改模型的语义判定。

发现加两次评审共 3 次实际串行模型请求，643600 tokens。这三个请求用于发现和复审；本次新机制尚未作者为包，也未执行修复实验。发现的完整生成上下文最晚来源为 2023-06-18T14:43:15Z，不能把它的机制选择或作者包回填到 pre-2021 训练/开发库；训练期和逐题早期 Pattern 需要在对应时间前的完整可用语料上独立发现。

最终工程验证为 **882 passed、20 skipped**；针对性归因/发现/运行器检查为 89 passed、5 skipped，公开状态保留检查为 8 passed；本次修改文件的 lint 与 format 均通过。这些属于工程验证。

下一步先将通过审阅的机制作者为原生候选包并验证来源/功能，再在独立当前任务上建立真实绑定、Pattern DAG 和互补 CrossBind。同时将原始 query evaluator、逐题运行时及控制/评审映射接入统一监督入口，采集有用标签，再完成 Ranker、联合冻结和正式 SWE 实验。现有 84 条旧历史观察、其全部 unrelated 适用性标签和 16 对平局保留；它们未完成 M4。
