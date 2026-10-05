**Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-06）**

**尚未全部完成。M0–M3 有主要实现和工程测试；M4 没有合格的训练 Ranker，M5 未联合冻结，M6 正式 SWE 运行数为 0。** 依据[机器快照 v26](results/pattern-crossbind-ranker-current-status-20261006-v26.json)。旧快照和失败记录保留，不以源码演练替代新 Issue 泛化或 SWE 验收。

| 阶段 | 已实现或已验收 | 尚缺的验收 |
| --- | --- | --- |
| M0 契约 | Action/Pattern/Task/Plan；输入输出、前提效果、不变量、API 与责任绑定、读写冲突、Oracle、来源和包 hash、时间与输入隔离；四项来源内 Action 正例、六个分类定义、三个拒用反例接受 | 完整包独立适配与正式 KB 准入；已接受因果簇与逐题隔离表的协调 |
| M1 重写 | 依据角色、必要效果、不变量和偏序形成当前 DAG；历史 Workflow 不变；删除、替换、重排保留来源和理由 | 独立新 Issue 的执行适配、必要效果和修复收益 |
| M2 CrossBind | Bind/Cut/Match/Bridge/Compose/Validate；PASS/FAIL/UNKNOWN；前提、状态、冲突、循环、清理和验证闭包；最多两父、四组合 | 独立来源互补动作的真实两父组合及效果 |
| M3 prompted Ranker | Workflow/Plan 两处排序；硬门槛、拒绝全部、先探查；受限 Action 补召回和共享预算 | 有用开发校准、同冻结候选池的排序效果 |
| M4 训练 | 逐 query 时间和身份排除；双监督、训练及 checkpoint 重载入口 | 有用正负适用性标签、非平局偏好、合格权重和开发校准 |
| M5 冻结 | 来源核验与冻结工具 | KB、题目并集、索引、模型、阈值、预算和协议联合冻结 |
| M6 实验 | 配对修复、模块消融和冻结候选池排序比较入口 | 正式 SWE 修复、消融和排序收益 |

[工程检查](results/native-authoring-checkpoint-engineering-audit-20261006-v1.json)实际为 **750 passed、20 skipped**，测试耗时 106.77 秒；专项 13 passed，lint、格式和 diff 检查通过。新增 checkpoint 修复将序列化前的 tuple 与 JSON list 按规范化指纹比较，保留对真实协议、证据、模型、来源版本和别名变化的拒绝。旧源码回归为 1 failed、5 passed。此次工程检查 0 次模型调用，不代表功能或 SWE 效果。

**原生包与限定功能验收**

Pylint #8120 原生 Skill 由本系统直接抽取。inspect、repair、regressions、validate 四项来源内正例已被独立上下文复核接受。六个 activation/applicability 定义为 6/6，预期标签未提供给模型。

[功能反例终态 v2](results/native-async-lifecycle-functional-negative-terminal-audit-20261006-v2.json)已接受 **3/3**：已有 async hooks 和 dispatcher 故障均正确拒绝缺失 hooks 修复，机制状态为 CONTRADICTED；执行不可用时维持 UNKNOWN 并拒绝授权修复。三例正常结束、补丁均为 0 字节；原 300000 token cap 保留。q2 仅重做缺失复核，没有重复已有 solver。旧 HTTP429 保留为基础设施失败，不写成语义负标签。

因此，限定的来源内 Action 定义正反例套件已完成。它使用同模型族的独立上下文，没有独立新 Issue 或跨项目效果证据；完整包验收、晋升和本次正式 KB 准入仍未完成。#1279/#8120 保持一个缺陷簇。

**历史人口与跨项目语料**

[Pylint 原生人口终态](results/pylint-native-population-terminal-structural-audit-20261006-v1.json)：1160 条完整修复登记，78 条获来源因果资格；47 个原生候选包均通过生产加载器，31 条已获资格的来源仍延迟抽取。实际请求 288 次：105 成功、27 超时、1 次 HTTP502、155 次 HTTP429；记录到 2825269 tokens，缺 usage 的费用未知。原作者已结束，未重启。31 个延迟来源的修复都晚于训练截止，需要按真实 v7→v8 协议迁移建立新版本，不能忽略协议变化复用旧 checkpoint。

[全部已供给且获资格的跨项目包](results/qualified-native-cross-project-corpus-preparation-audit-20261006-v1.json)为 74 个：Pyflakes 26、Pylint 人口 47、#8120 1，74 个唯一来源均通过资格加载。合并保留 1205 条人口记录，没有任意 top-N 或预设问题族。Ruff 尚未纳入。这不代表全历史完成抽取或正式 KB 已冻结。当前目录有 114 个 SKILL.md，包含历史版本；文件数不代表不同的已验收 Skill。

**Ruff 与独立新 Issue**

Ruff #5124 的来源资格限于一个精确命名 Rust 库测试、原 expected snapshot 和三组因果控制，退出码 0/101/0 保留。修复公开时间 2023-06-15T19:00:20Z，不能用于 pre-2021 训练。首次抽取六次实际请求全部超时，0 包；第一次流式重试因快照漏协议文件，在任何模型调用前失败。[失败审计](results/serial-native-causal-review-and-Ruff-failure-audit-20261006-v1.json)保留这些事实。新版本已补入并校验协议 hash，保持相同来源输入、流式 900 秒和 24000 输出上限，正在串行抽取；启动不能计为成功。

[Pylint #3604/#3666 的第二次因果审查](results/historical-pylint-3604-3666-causal-cluster-terminal-audit-20261006-v2.json)已经通过校验器，并将两者归为同一不完整 MESSAGE_STRING 字符类的连续修复。它们不是文字复制，但不能作为两个独立缺陷支持，#3604 不能作为 #3666 的独立泛化 donor。原精确 opened 输入、已公开 Pylint 2.5.0 源码和八项机械控制保持；机械控制不是 solver 或效果标签。后续监督必须先协调该审查与身份隔离表，不能强行写成独立正例。

既有历史开发 27/27 分支：基础 Agent 7/9、指导分支合计 14/18，九题各分支逐题结果一致。84 条监督中适用性全部 unrelated；训练 16 对效果偏好全部 tie，开发 13 tie、1 非 tie。没有制造缺失候选的失败、正例或非平局偏好，因此不能将现有 checkpoint 重载当作 M4 有效训练完成。

主截止严格早于 2024-01-01T00:00:00Z，训练截止严格早于 2021-01-01T00:00:00Z，并逐题限制在其输入时间以前。排除自身答案、同修复、重复、复制来源、后来的修复和正式评价 #10034。所有实际模型调用串行，凭据仅使用运行时输入和环境。整体目标保持 active；后续按来源与独立适配验收 → 有效监督与训练 → 联合冻结 → 正式 SWE 与消融推进。
