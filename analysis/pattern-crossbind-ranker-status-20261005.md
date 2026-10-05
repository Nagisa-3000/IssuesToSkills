**Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-05）**

**尚未全部完成。M0–M3 已有实现和工程测试；M0 的完整原生 Skill 包验收、M1 的独立新 Issue 泛化、M2 的真实互补组合和 M3 的排序效果仍待验证。M4 没有合格的训练 Ranker，M5 尚未联合冻结，M6 正式 SWE 运行数为 0。** 本文依据[当前机器快照 v23](results/pattern-crossbind-ranker-current-status-20261005-v23.json)。历史失败、原始回执、旧快照和候选版本均保留；来源资格、来源内 Action 演练、包准入和正式修复分别统计。

| 阶段 | 已实现或已观察到的能力 | 尚缺的验收 |
| --- | --- | --- |
| M0 契约 | Action/Pattern/Task/Plan；输入输出及实际见证；前提、效果、不变量、对象/API 绑定、读写角色、Oracle、来源与包 hash；时间隔离；工作区封存和独立输出复核。Pylint #8120 四项来源内 Action 演练通过，Ruff #5124 的一个精确命名测试来源资格接入完成 | 完整包 activation/applicability/functional 正反案例、独立适配、正式 KB 准入 |
| M1 重写 | Pattern 的角色、必要效果、不变量与偏序生成当前 DAG；删除、替换、重排留理由；历史 Workflow 不变 | 独立新 Issue 中确认机制、执行重写并核验修复收益 |
| M2 CrossBind | Bind/Cut/Match/Bridge/Compose/Validate；PASS/FAIL/UNKNOWN；前提、状态接口、读写冲突、循环、清理及验证闭包；最多两个父 Workflow、四个组合候选 | 独立来源的互补 Action、真实两父组合及其执行效果 |
| M3 prompted Ranker | Workflow 和 Plan 两处排序；硬准入、拒绝全部、先探查；缺失角色的受限 Action 补召回；共享预算 | 有效开发集校准，同冻结候选池的配对排序效果 |
| M4 训练 Ranker | 逐 query 时间隔离；自身修复、重复和复制来源排除；适用性/执行效果监督、训练与 checkpoint 重载入口 | 有用正负标签、非平局训练偏好、合格权重与开发集校准 |
| M5 联合冻结 | 冻结和来源校验工具 | KB、题目、模型、阈值、预算、索引、验收协议联合冻结 |
| M6 正式实验 | 配对修复、模块消融和冻结候选池排序比较入口 | 正式 SWE 与消融尚未运行 |

最新的[完整工程检查](results/native-rust-qualification-engineering-audit-20261005-v1.json)为 **723 passed、19 skipped**，耗时 92.18 秒；Rust 资格专项为 58 passed，lint、格式和 diff 检查通过。跳过项不计为通过。这证明工程检查通过，不能替代包功能、迁移或 SWE 效果验收。

**真实来源内 Action 演练**

Pylint #8120 的包由系统直接从有来源资格的历史证据抽取，含 SKILL.md、Action、证据和 evals。inspect、repair、regressions 三阶段已正常结束并获独立上下文 policy PASS/correct_confirmation/CONFIRMED：实际执行/复核调用分别为 9+2、9+2、7+2；repair 生成 771 字节修复，regressions 增加 902 字节测试。来源 #1279/#8120 属于同一缺陷簇，不作为两个独立支持。

最新[验证 v10](results/native-async-lifecycle-validation-terminal-audit-20261005-v10.json)在不可变代码 832ad2ae5c36a65ae4475c61301c51b307000ef5 上，使用与 v7–v9 相同输入 eeda01d039e04921fab33e0b0b4b11fdb9641175055d6ac560bd282a54029c7a 和原 300000 token 执行上限。实际 9 次执行模型调用、2 次独立上下文复核，219311 model tokens，611.10 秒，0 字节新增 patch。Solver 记录真实 action-result:1 后显式 finish；五项记录检查全部 PASS，独立 policy 为 PASS/correct_confirmation/CONFIRMED，source_validation_case_accepted=true。直接 scope Oracle、精确 focused pytest Oracle 和独立资源审计都有本轮实际见证。

这使四项来源内 Action 定义演练都有接受的正例。**完整包验收、正式 KB 准入、新 Issue 泛化和正式 SWE 仍为未完成。** 复核采用同一模型族的独立上下文，human_reviewed=false、independent_model_family=false。先前 v1–v9 的失败或部分确认仍保留；不能从它们补写 finish 或接受案例。

v10 使用的[本轮小命令输出保留](results/public-command-working-set-engineering-audit-20261005-v1.json)将完整实际小输出投影到有界窗口，保留身份、哈希、失败状态和过期标记，不建立新读取事件、见证或事实。相较 v9，v10 少两次全文重读，执行调用从 10 降至 9，model tokens 少 16635，并完成显式 finish。每版本仅一次随机运行，不能据此宣称统计因果收益；同帧证据投影实际增加 479–2399 字节，不能称为 prompt 压缩。

**Ruff 的精确历史来源资格**

[规范来源资格报告](qualifications/ruff-5124-exact-rust-native-20261005.json)和[整合审计](results/ruff-5124-exact-native-qualification-integration-audit-20261005-v1.json)限定于 Ruff #5124 的一个精确命名 Rust 库测试。原始 Issue closing event 指向 PR #5125、修复 107a295af4f51dce1e78dcbfd234b2a3ad99a00f，保守公开可用时间为 2023-06-15T19:00:20Z。资格通过生产 versioned authority 与 canonical loader，保留原始退出码 **0 / 101 / 0**，没有归一化为 Python 的 0 / 1 / 0。

整合时发现旧 fixed 构建源码存在三项无关字节差异：两个 CRLF fixture 的换行和一个 symlink target 文本。旧结果保留为该命名测试的有界观察；不能再称旧 fixed 整个文件系统与历史 tree 精确一致。v5 从精确 base 重建，仅按原始字节替换四项历史修改；逐项核对 3300 个 Git 路径、mode 和 blob，fixed tree 精确为 3d56b68f055cc33f189c97630e2cacf41437ef75。

新 fixed 源码在原 Cargo.lock、Rust 1.74.1、319 个已核对 vendor 包下离线 frozen 构建成功，并新增三次真实隔离执行：base 通过；base+regression 保留原 expected snapshot，退出 101 且触发原始 “not a With, For, or AsyncFor” panic；fixed 通过。三个控制各执行一项精确测试，资源封存不变，INSTA_UPDATE=no、INSTA_FORCE_PASS=0；0 次模型调用。规范资格 fingerprint 为 f43ca31c3d921211b124f5f8c8554db29cddb7bd2c6c6015b6248ff53c371249。

此来源可用时间晚于 pre-2021 Ranker 训练截止，训练加载明确拒绝。**尚未由系统抽取及完整验收 Ruff 原生 Skill，尚未确认跨项目 Pattern 或接受两父组合。** 来源因果资格只覆盖该命名测试。

**已有开发结果与监督**

[历史配对开发实验](results/pattern-crossbind-ranker-current-status-20261005-v14.json)完成 27/27 分支：基础 Agent 7/9，两个指导分支合计 14/18。九题三个分支逐题结果相同，未建立 Skill、重写或组合的修复收益。旧候选池和结果冻结保留，新候选不回填。

[监督合并审计](results/historical-dual-supervision-merge-audit-20261005-v11.json)共有 84 条观察：42 条执行、42 条获独立上下文复核接受的适用性标签；训练 40、开发 44。适用性全部 unrelated；训练 16 对效果偏好全部平局，开发 13 对平局、1 对非平局。未执行候选没有填为失败；没有人为制造偏好或新的合格 Ranker 权重。

候选文件共有 **112 个 SKILL.md，包含历史版本**，其中当前 Pylint observable v2 批次为 44 个。112 不是不同的已验证 Skill 数，正式准入为 **0**。历史 Issue 人口是 Pylint 5273、Pyflakes 501、Ruff 3582，总计 9356；人口存档不表示全部历史经验完成抽取、资格或功能验收。

[Pylint #3666 原始输入溯源](results/historical-query-pylint-3666-opened-input-audit-20261005-v1.json)恢复了公开 opened event；query 保守时间为 2020-06-05T19:22:59Z，候选 #3604 修复可用于 2020-05-14T17:04:40Z，时间顺序符合训练要求。缺陷/复制身份、候选完整功能、相关性及效果标签尚待核验；仅时间合法不能赋予正标签。

**时间边界与后续依赖**

主截止严格早于 2024-01-01T00:00:00Z，训练截止严格早于 2021-01-01T00:00:00Z。每条训练 query 再使用其自身输入时间，排除自身答案、同修复、重复及复制来源和后来可用的材料。Pylint #10034 排除正式评价。原历史作者保持已有进程，真实模型调用串行；不另启作者或并行模型。

下一步按依赖完成：原生包 activation/applicability/functional 正反案例；从精确 qualified Ruff 来源进行系统原生抽取及验收；独立新 Issue 的重写和互补两父执行；有效时间隔离监督、训练与开发校准；M5 联合冻结；M6 正式 SWE、模块消融及同候选池排序比较。当前整体目标保持 active、未完成。
