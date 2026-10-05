**Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-05）**

**尚未全部完成。M0–M3 的主要模块已有实现和工程测试，但完整原生 Skill 包、独立新 Issue 泛化、真实互补组合及排序效果仍待验收。M4 没有合格的训练 Ranker，M5 未联合冻结，M6 正式 SWE 运行数为 0。** 本文依据[当前机器快照 v25](results/pattern-crossbind-ranker-current-status-20261005-v25.json)。旧快照、失败、原始回执与候选版本保留。

| 阶段 | 已实现或已观察到的能力 | 尚缺的验收 |
| --- | --- | --- |
| M0 契约 | Action/Pattern/Task/Plan；输入输出及见证、前提效果、不变量、当前 API/责任绑定、读写冲突、Oracle、来源/包 hash、时间与输入隔离；四项来源内 Action 正例接受；六个分类定义通过 | 完整包功能正反例、独立适配与本次正式 KB 准入 |
| M1 重写 | 按角色、必要效果、不变量和偏序生成当前 DAG；历史 Workflow 不变；删除、替换、重排留来源与理由 | 独立新 Issue 中执行适配、验证必要效果和修复收益 |
| M2 CrossBind | Bind/Cut/Match/Bridge/Compose/Validate；PASS/FAIL/UNKNOWN；状态、前提、冲突、循环、清理与验证闭包；最多两父、四组合 | 独立来源互补动作的真实两父组合及执行效果 |
| M3 prompted Ranker | Workflow/Plan 两处排序；硬门槛、拒绝全部、先探查；受限缺口 Action 补召回与共享预算 | 有用开发集校准及同冻结候选池的排序效果 |
| M4 训练 | 逐 query 时间/身份排除、适用性与效果监督、训练/checkpoint 重载入口 | 有用正负标签、非平局偏好、合格权重与开发校准 |
| M5 冻结 | 冻结与来源校验工具 | KB、题目并集、索引、模型、阈值、预算、协议联合冻结 |
| M6 实验 | 配对修复、模块消融、冻结候选池排序比较入口 | 正式 SWE、模块消融与排序收益尚未运行 |

[最新工程检查](results/published-history-query-and-shared-runtime-engineering-audit-20261005-v1.json)为 **744 passed、20 skipped**，耗时 104.29 秒。实际查询专项 19 passed；当前 privileged copied runtime/boundary 检查 3 passed。完整套件之后仅修正共享运行时测试以加载实际 ELF SONAME，产品源码不变，修正测试已实际运行。lint、格式和 diff 检查通过。跳过不计通过，工程检查不能替代功能或 SWE 效果。

**原生包与功能验收**

Pylint #8120 包由系统直接从已获来源资格的历史证据抽取，含 SKILL.md、Action、证据与 evals。inspect、repair、regressions 和 validate 四项来源内正例均正常结束并获独立上下文复核接受；[最后的 validation v10](results/native-async-lifecycle-validation-terminal-audit-20261005-v10.json)实际执行 9 次模型调用、复核 2 次，保留原 300000 token cap，五项记录检查全 PASS，显式记录并 finish。#1279/#8120 属于同一缺陷簇，不作为两个独立支持。

[activation/applicability 定义 smoke](results/native-async-lifecycle-activation-applicability-definition-audit-20261005-v1.json)为 **6/6**，实际 1 次模型调用，预期标签未提供给模型。它使用同一模型族的独立上下文，human_reviewed=false、independent_model_family=false，不能算独立泛化或开发校准。

三个功能负例已封存原 Task、包 hash 与代码快照并串行启动：已有 async hooks、当前 dispatcher 故障、命令执行不可用。使用统一原 300000 cap、只读运行、真实观察及独立上下文复核。本快照正在执行 q1，尚无终态负例接受结果；不能将已启动计为通过。完整包验收和本次正式 KB 准入仍为未完成。

**Ruff 来源与抽取**

[精确 Rust 来源资格](qualifications/ruff-5124-exact-rust-native-20261005.json)已经通过版本化 authority 与 canonical loader，限定于一个精确命名历史库测试，保留真实退出码 **0 / 101 / 0**、原 expected snapshot、不可变资源与三组控制。新 fixed tree 精确为 3d56b68f055cc33f189c97630e2cacf41437ef75；保守公开时间为 2023-06-15T19:00:20Z，晚于 pre-2021 训练截止，因此训练明确拒绝。

[首次原生抽取终态审计](results/native-package-classification-and-rust-authoring-terminal-audit-20261005-v1.json)记录 **6 次实际请求，全部 300 秒超时，0 个成功响应、0 个包**。CLI 退出 0 仅说明终态记账完成，不能算抽取成功；缺 usage 的请求费用未知。已准备使用流式响应及 900 秒传输超时重试，保留同一来源资格、输入范围与 24000 输出上限，尚未启动。此前失败和包版本保留。来源资格不能替代 Skill 或 Agent 验收。

**新 Issue 与既有监督**

[Pylint #3666 精确输入与已公开源码](results/historical-query-pylint-3666-published-source-preparation-audit-20261005-v1.json)使用原 opened event，输入时间 2020-06-05T19:22:59Z；Pylint 2.5.0 sdist 于 2020-04-27 已上传，逐项核对 1328 个已发布文件。重放 Git commit 是当前建立的 synthetic identity，没有伪造历史提交时间。实际隔离运行时为 Python 3.8.3、Astroid 2.4.1、Pytest 5.4.1，当前复建，不能描述为报告人的原二进制。

[八项机械控制](results/historical-query-pylint-3666-history-copy-mechanical-controls-audit-20261005-v1.json)全通过：历史 #3604 实际补丁加入下划线字符，修复其自身下划线效果；直接复制后，#3666 数字符号仍解析为 -no-jfly 并失败。数字 message ID、普通连字符、未抑制 checker 与原十项 parser tests 保持。0 次模型调用。这是机械控制，**不是 solver 分支、Skill 功能验收、Ranker 效果标签或 SWE 结果**；缺陷簇、复制来源、当前适用性及独立求解仍待核验。

既有历史开发完成 27/27 分支：基础 Agent **7/9**，两个指导分支合计 **14/18**，九题三个分支逐题结果相同，尚未建立 Skill、重写或组合收益。既有监督为 84 条观察：42 条执行、42 条独立上下文复核接受的适用性标签；适用性全部 unrelated；训练 16 对效果偏好全部 tie，开发 13 对 tie、1 对非 tie。未执行候选没有填失败，没有人工制造偏好或合格 Ranker 权重。

候选文件当前共有 **113 个 SKILL.md，包含历史版本**，Pylint observable v2 批次为 46 个。文件数不代表不同的已验收 Skill，本次 SWE 实验正式 KB 准入仍为 **0**。历史 Issue 人口为 Pylint 5273、Pyflakes 501、Ruff 3582，共 9356；人口存档不代表全部历史完成抽取、资格或功能验收。

主截止严格早于 2024-01-01T00:00:00Z，训练截止严格早于 2021-01-01T00:00:00Z，并逐 query 使用其输入时间，排除自身答案、同修复、重复及复制来源和后来材料。#10034 排除正式评价。所有实际模型调用串行，历史作者只在完成响应且无 sockets/children 后暂时暂停，watchdog 不会恢复到仍存活的工作模型进程中。

代码 c38ace488745f43d282ef85763ed49af853ab378 已独立核对发布到 GitHub main，[公开发布回执](results/github-publication-c38ace4-20261005-v1.json)保留 exact blobs/tree/commit 与 non-force 更新身份。整体目标保持 active、未完成；剩余依赖按完整包与迁移验收 → 有效监督/训练 → 联合冻结 → 正式 SWE 与消融推进。
