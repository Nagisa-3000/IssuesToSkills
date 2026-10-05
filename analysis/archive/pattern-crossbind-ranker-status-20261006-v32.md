**尚未全部完成。M0–M3 的核心实现和工程检查已经到位；M1–M3 的真实迁移、互补组合与有效校准未验收，M4–M6 未完成。正式 SWE 运行数为 0。**

最新依据是[机器快照 v32](results/pattern-crossbind-ranker-current-status-20261006-v32.json)和[本次审计](results/original-query-evaluator-and-native-recovery-audit-20261006-v1.json)。既有详细记录保存在[历史报告 v31](archive/pattern-crossbind-ranker-status-20261006-v31.md)，旧失败和旧协议均保留。

| 阶段 | 核心实现 | 仍缺的验收 |
| --- | --- | --- |
| M0 | Action/Pattern/Task/Plan 契约、来源与包 hash、当前绑定、输入输出、前提效果、不变量、时间与输入隔离 | 全包功能验收、完整语料因果审查、正式 KB 准入 |
| M1 | 根据角色、必要效果与偏序重写 DAG；历史 Workflow 不变；变更保留来源和理由 | 独立新 Issue 中可执行适配及修复收益 |
| M2 | 六阶段 CrossBind、PASS/FAIL/UNKNOWN、闭包与冲突/循环检查；最多两父、四组合 | 真正互补的两父组合执行及效果 |
| M3 | Workflow/Plan 两处 prompted 排序、硬门槛、拒绝与探查、补召回、共享预算 | 有用开发校准与同冻结候选池的排序效果 |
| M4 | 逐题时间排除、双监督和训练/checkpoint 入口 | 有用适用性标签、非平局效果偏好、合格训练 Ranker 与开发校准 |
| M5 | 验证和冻结工具 | KB、题目并集、索引、模型、阈值、预算、协议联合冻结 |
| M6 | 配对修复、消融和排序比较入口 | 正式 SWE 运行、修复效果、回归损害、成本及模块收益 |

本次修复了两个实验问题。缺失的公开 Git 来源不再被错误标为“原始输入未恢复”；21 条注册目标始终保留，来源缺口与输入缺口分别记录。已知修复新增显式 evaluator 投影政策：仅允许省略普通文件形式的发布元数据，代码、配置、测试、可执行/符号链接/二进制部分保留，历史回归断言不变；每项省略和原始/投影 hash 都保存。该政策不向 Actor 提供答案，也不覆盖原生 SourceRecord 或来源资格。

新增 [original_query_evaluator.py](../src/arex_skill_graph/original_query_evaluator.py) 从原始 Issue 时间点的公开源码和冻结当前 cohort 验收提交。它重算三阶段控制，绑定来源/测试/运行时及独立评审完整输入与实际调用记录，恢复 evaluator 所有的测试路径，拒绝测试删除、收集变化和运行时漂移。缺口不生成候选失败标签；独立复核缺失时保留机械观测，拒绝效果监督。现有使用修复父版本的 evaluator 保持其原协议。

31 条延迟抽取任务已经终态：71 次串行实际模型请求，23 个新原生包通过生产加载器和来源资格核验，8 条仍延迟。原 75 个加新 23 个，共 **98 个已供给原生包**，并非 98 个已验收或 promoted Skill。新 23 个的修复全部晚于训练截止，不能作为 pre-2021 训练正例。[供给目录](native-corpus/qualified-supplied-cross-project-20261006-v4/references.json)和[新包审计](native-corpus/qualified-deferred-pylint-20261006-v1/completion.json)可直接复核。

当前因果隔离索引覆盖 98 条来源、94 个保守组件，仅 4 条来源完成语义因果复核，full_corpus_causal_review_complete 仍为 false。#3604/#3666 保持同一连续修复簇；新增 #434/#470 复核认定为不同遗漏：前者是作用域查找/装饰器列表识别，后者是 AsyncFunctionDef 排除。[复核原文](causal-reviews/pyflakes-434-470-20261006-v1/review-response.json)只供验证身份，机制和修复正文不进入 Actor 特征。

21 条历史注册目标中，19 条精确 opened 输入、18 条输入前公开 Git 源已恢复；#419/#422 仍是输入缺口，#3604 仍是 archive 读取失败造成的源码缺口。[98 包的逐题目录](history-query-recovery/pre2021-public-query-temporal-catalogs-20261006-v2/completion.json)保留全部注册分母。#395 无时间合格历史 Skill，不能制造正例。

原生公开 Git 控制有 **8 项机械 PASS、10 项未合格、1 项源码缺口、2 项输入缺口**。另一个显式政策下，#3737 仅排除 ChangeLog/CONTRIBUTORS 发布元数据后机械通过；该结果单独计数，不能改写原生控制。新增 #3798 原生控制仍未合格。[三个目标的控制](controls/pre2021-targeted-public-git-replay-20261006-v1/completion.json)保留实际失败。

#470 的原始查询回放已由独立上下文接受其限定测试范围：1 个 F2P、22 个 PTP，仍缺一个后来原生 PTP。新评估器的真实私有控制为：空提交失败，已知修复通过，均收集 23 项测试。这是 evaluator 校验，solver 分支与效果标签均为 0，不是 Skill 迁移成功。[独立评审](controls/pyflakes-470-original-replay-independent-review-20261006-v1/review.json)和[实际控制](controls/pyflakes-470-original-query-evaluator-20261006-v1/completion.json)均已保存。

原始输入配对小实验已经终态：B0 与 E1 都修复 #470，独立 evaluator 的 23 项冻结测试全部通过。B0 消耗 130735 tokens、13 次模型请求；E1 消耗 157592 tokens、16 次请求，tokens 增加 **20.54%**。两者预算相同，均使用输入前公开 Git、相同 runtime 和模型，29 次实际请求全部串行。指导分支保留一项 validation Action 输出记录；语义仍为 unreviewed，没有自动提升为已验证 Action 或上下文事实。[完整终态审计](pilots/pyflakes-470-original-input-20261006-v1/terminal-audit.json)、[基础分支](pilots/pyflakes-470-original-input-20261006-v1/B0/run.json)、[指导分支](pilots/pyflakes-470-original-input-20261006-v1/E1/run.json)、[冻结协议](pilots/pyflakes-470-original-input-20261006-v1/study-identity.json)可复核。

这个单题试验产生 1 条限于新 evaluator 协议的效果观测，模式为 probe_only；适用性标签与排序偏好新增均为 0。它证明指导输入、独立修复与验收能跑通，没有证明修复收益。guidance_runs 为 0、review rounds 为 0，本次不验收 Pattern 重写、CrossBind、检索/Ranker 排序或 M1 的完整适配。当前生产改动由 Agent 按 async AST 问题形成，未照搬 #434 的作用域查找/装饰器列表修复；该归因仍需独立 Action 复核。


最新完整工程回归为 **872 passed、20 skipped，106.68 秒**；专项 **62 passed**，lint 和格式通过，六个代码/测试文件的测试时 hash 均保存。[完整 receipt](results/original-query-evaluator-full-20261006-v1/result.json)不代表泛化或 SWE 效果。

此前 84 条适用性监督全部 unrelated、16 对训练效果偏好全部 tie；旧九题的三个分支逐题结果一致。因此合格训练 Ranker、M5 联合冻结和 M6 正式实验仍未完成。主截止严格早于 2024-01-01T00:00:00Z，训练截止严格早于 2021-01-01T00:00:00Z，且逐题限制在原始输入时间以前；#10034、自身答案、同一修复/缺陷簇、重复与复制来源保持排除。

目标保持 active。后续验收依次需要实际 Action 迁移/拒绝复核、跨项目 Pattern 与互补组合、有用时间隔离监督与 Ranker、联合冻结以及正式 SWE/消融。
