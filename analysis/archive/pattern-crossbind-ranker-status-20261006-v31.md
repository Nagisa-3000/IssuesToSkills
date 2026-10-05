**Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-06）**

**尚未全部完成。M0–M3 有主要实现和工程测试；M4 没有合格的训练 Ranker，M5 未联合冻结，M6 正式 SWE 运行数为 0。** 依据[机器快照 v31](results/pattern-crossbind-ranker-current-status-20261006-v31.json)。旧快照和失败记录保留，不以源码演练替代新 Issue 泛化或 SWE 验收。

| 阶段 | 已实现或已验收 | 尚缺的验收 |
| --- | --- | --- |
| M0 契约 | Action/Pattern/Task/Plan；输入输出、前提效果、不变量、API 与责任绑定、读写冲突、Oracle、来源和包 hash、时间与输入隔离；四项来源内 Action 正例、六个分类定义、三个拒用反例接受 | 完整包独立适配与正式 KB 准入；完整语料的因果复核；已有审查现已接入逐题排除 |
| M1 重写 | 依据角色、必要效果、不变量和偏序形成当前 DAG；历史 Workflow 不变；删除、替换、重排保留来源和理由 | 独立新 Issue 的执行适配、必要效果和修复收益 |
| M2 CrossBind | Bind/Cut/Match/Bridge/Compose/Validate；PASS/FAIL/UNKNOWN；前提、状态、冲突、循环、清理和验证闭包；最多两父、四组合 | 独立来源互补动作的真实两父组合及效果 |
| M3 prompted Ranker | Workflow/Plan 两处排序；硬门槛、拒绝全部、先探查；受限 Action 补召回和共享预算 | 有用开发校准、同冻结候选池的排序效果 |
| M4 训练 | 逐 query 时间和身份排除；双监督、训练及 checkpoint 重载入口 | 有用正负适用性标签、非平局偏好、合格权重和开发校准 |
| M5 冻结 | 来源核验与冻结工具 | KB、题目并集、索引、模型、阈值、预算和协议联合冻结 |
| M6 实验 | 配对修复、模块消融和冻结候选池排序比较入口 | 正式 SWE 修复、消融和排序收益 |

此前的 [checkpoint 工程检查](results/native-authoring-checkpoint-engineering-audit-20261006-v1.json)实际为 **750 passed、20 skipped**，测试耗时 106.77 秒；专项 13 passed，lint、格式和 diff 检查通过。新增 checkpoint 修复将序列化前的 tuple 与 JSON list 按规范化指纹比较，保留对真实协议、证据、模型、来源版本和别名变化的拒绝。旧源码回归为 1 failed、5 passed。此次工程检查 0 次模型调用，不代表功能或 SWE 效果。

**原生包与限定功能验收**

Pylint #8120 原生 Skill 由本系统直接抽取。inspect、repair、regressions、validate 四项来源内正例已被独立上下文复核接受。六个 activation/applicability 定义为 6/6，预期标签未提供给模型。

[功能反例终态 v2](results/native-async-lifecycle-functional-negative-terminal-audit-20261006-v2.json)已接受 **3/3**：已有 async hooks 和 dispatcher 故障均正确拒绝缺失 hooks 修复，机制状态为 CONTRADICTED；执行不可用时维持 UNKNOWN 并拒绝授权修复。三例正常结束、补丁均为 0 字节；原 300000 token cap 保留。q2 仅重做缺失复核，没有重复已有 solver。旧 HTTP429 保留为基础设施失败，不写成语义负标签。

因此，限定的来源内 Action 定义正反例套件已完成。它使用同模型族的独立上下文，没有独立新 Issue 或跨项目效果证据；完整包验收、晋升和本次正式 KB 准入仍未完成。#1279/#8120 保持一个缺陷簇。

**历史人口与跨项目语料**

[Pylint 原生人口终态](results/pylint-native-population-terminal-structural-audit-20261006-v1.json)：1160 条完整修复登记，78 条获来源因果资格；47 个原生候选包均通过生产加载器，31 条已获资格的来源仍延迟抽取。实际请求 288 次：105 成功、27 超时、1 次 HTTP502、155 次 HTTP429；记录到 2825269 tokens，缺 usage 的费用未知。原作者已结束，未重启。31 个延迟来源的修复都晚于训练截止，需要按真实 v7→v8 协议迁移建立新版本，不能忽略协议变化复用旧 checkpoint。

[全部已供给且获资格的跨项目包](results/qualified-native-cross-project-corpus-preparation-audit-20261006-v3.json)为 75 个：Pyflakes 26、Pylint 人口 47、#8120 1、Ruff 1，75 个唯一来源 ID 均通过资格加载。合并保留原 1205 条人口记录并追加一条 Ruff 来源，共 1206 条，没有任意 top-N 或预设问题族。这不代表全历史完成抽取或正式 KB 已冻结。上次 v27 目录统计为 115 个 SKILL.md，包含历史版本；文件数不代表不同的已验收 Skill。

**Ruff 与独立新 Issue**

Ruff #5124 的来源资格限于一个精确命名 Rust 库测试、原 expected snapshot 和三组因果控制，退出码 0/101/0 保留。修复公开时间 2023-06-15T19:00:20Z，不能用于 pre-2021 训练。首次抽取六次实际请求全部超时，0 包；第一次流式重试因快照漏协议文件，在任何模型调用前失败。[失败审计](results/serial-native-causal-review-and-Ruff-failure-audit-20261006-v1.json)保留这些事实。[新版本终态](results/qualified-Ruff-native-package-authoring-terminal-audit-20261006-v3.json)已补入并校验协议 hash，保持相同来源输入、流式 900 秒和 24000 输出上限；实际 1 次模型调用生成 1 个原生 Workflow 包，生产加载器和来源资格均通过。功能 evals 仍未执行，不代表 Agent、跨项目或 SWE 修复效果。

[Pylint #3604/#3666 的第二次因果审查](results/historical-pylint-3604-3666-causal-cluster-terminal-audit-20261006-v2.json)已经通过校验器，并将两者归为同一不完整 MESSAGE_STRING 字符类的连续修复。它们不是文字复制，但不能作为两个独立缺陷支持，#3604 不能作为 #3666 的独立泛化 donor。原精确 opened 输入、已公开 Pylint 2.5.0 源码和八项机械控制保持；机械控制不是 solver 或效果标签。该审查现已接入验证专用隔离索引；#3604 不能作为 #3666 的独立正例或候选来源。

既有历史开发 27/27 分支：基础 Agent 7/9、指导分支合计 14/18，九题各分支逐题结果一致。84 条监督中适用性全部 unrelated；训练 16 对效果偏好全部 tie，开发 13 tie、1 非 tie。没有制造缺失候选的失败、正例或非平局偏好，因此不能将现有 checkpoint 重载当作 M4 有效训练完成。

主截止严格早于 2024-01-01T00:00:00Z，训练截止严格早于 2021-01-01T00:00:00Z，并逐题限制在其输入时间以前。排除自身答案、同修复、重复、复制来源、后来的修复和正式评价 #10034。所有实际模型调用串行，凭据仅使用运行时输入和环境。整体目标保持 active；后续按来源与独立适配验收 → 有效监督与训练 → 联合冻结 → 正式 SWE 与消融推进。

[全部 31 个延迟来源的恢复准备](results/pylint-qualified-deferred-protocol-recovery-preparation-audit-20261006-v3.json)已逐项核对 Issue 与 fix 双重身份、历史来源和证据指纹不变，保留真实 v7→v8 协议变化并使用新输出版本。批次已串行启动，遇重复 HTTP429 停止后续调用；31 个来源均晚于训练截止，不能用作 pre-2021 训练正例。恢复启动不计抽取成功。

代码与此前审计已非强制发布：[1426c19](https://github.com/Nagisa-3000/IssuesToSkills/commit/1426c19d5b4747c24dbdf6ee34c07ec1dea0fba4)，795 个范围内 blob SHA 与 mode 已独立核对。

**已完成的因果隔离接入**

[本次审计](results/historical-causal-isolation-integration-audit-20261006-v1.json)保存真实 #3666 查询的排除证据：原输入时间保持 2020-06-05T19:22:59Z，候选由 15 减为 14，#3604 被明确拒绝，32 个历史包文件字节未变。历史包及 SourceRecord 保持不可变；验证专用索引只包含身份关系、来源指纹与审查 hash，不包含 reviewer 的机制或修复正文。

隔离规则覆盖历史候选准入、训练/开发簇切分、适用性评审准备和复用、冻结 Plan 池身份以及 Pattern 独立来源计数。新实验须显式提供 --causal-isolation；变更隔离输入会拒绝复用旧池或旧评审人口，不能悄悄改写已完成的标签。既有无索引记录保留其原始协议。

本次修改后的完整工程检查为 **765 passed、20 skipped（112.10 秒）**；相关专项 **95 passed（44.80 秒）**，lint 与 diff 检查通过。此前失败和路径错误记录保留。检查没有调用模型，没有新增效果标签，也没有正式 SWE 运行。

[当前隔离索引](isolation/historical-causal-isolation-20261006-v1.json)覆盖 75 条来源记录，形成 71 个保守身份组件，只有 #3604/#3666 两个 Issue 经过语义因果审查。共享 fix、原生别名和复制来源的机械合并不等于全语料独立审查，full_corpus_causal_review_complete 仍为 false。M1 独立适配、M2 两父互补执行、M3 有效校准、M4 合格训练 Ranker、M5 联合冻结与 M6 正式 SWE 仍未验收。整体目标保持 active。


**本次补齐的原始历史查询与当前源码控制**

[原始输入与版本控制审计](results/original-history-query-recovery-and-current-source-controls-audit-20261006-v1.json)涵盖现有 75 个合格供给包中全部 21 个 pre-2021 来源，没有任意 top-N 或预设问题族。这 21 条只对应 20 个保守身份组件，不代表 20 个经过独立语义审查的缺陷。

已从 GH Archive 原始公开 opened 事件恢复 **19/21** 个输入，并为全部 19 个选定输入前已发布的稳定 sdist，校验包大小、SHA256、Git blob 和 mode。Pyflakes #419/#422 没有找到精确 opened 事件，保留为缺口。完整原始输入、资格及版本记录见[查询工件说明](history-query-recovery/pre2021-original-inputs-20261006-v1/README.md)。合成 Git commit 使用真实创建时间，不回填历史日期；当前 PyPI 观察不能证明已经被删除的历史发行版。

本次五个新增恢复/选择源码及测试文件的完整工程检查为 **786 passed、20 skipped（140.20 秒）**；发布前逐个 SHA256 确认其与测试时字节一致。此前 750/765 的检查分别对应 checkpoint 修复和因果隔离接入，保留各自审计。

Pyflakes #574 使用 2020-08-16 原始问题与更早发布的 2.2.0 sdist。原历史生产补丁虽然可以应用，但调用该版本不存在的 AnnotationState，出现 NameError；原失败控制保留，不能据此赋予候选失败标签。三个历史 PTP 测试在 2.2.0 不存在，明确列为缺口。

单独的 evaluator 控制版本将历史注解状态映射到当前 Boolean API，显式处理首个类型参数并恢复元数据后的状态。未修改历史回归断言、SourceRecord 或公开 TaskContext。控制前冻结当前可收集的 41 项测试：原有 37 项与新增回归 4 项，其中 F2P 2、当前 PTP 39。三阶段公开 MRE 退出码为 1/1/0，测试退出码为 0/1/0；修复后 41 项通过，另五个首参数、元数据名称、属性入口和状态恢复边界探查通过。

这个结果仅是**版本专用机械控制通过**，独立复核仍未完成；适配后的已知修复属于 evaluator，不能提供给 planner、Ranker 或 solver。#486 的后续 AnnotationState 修复晚于 #574 输入，不能作为该问题的历史 donor/Bridge。控制脚本首次保存 diff 时假设快照含 .git 而失败；新版本改为比较源码字节，旧尝试保留。

本次新增实际模型调用、solver 分支、效用标签和正式 SWE 运行均为 **0**。M1 独立新 Issue 适配、M2 两父互补执行、M3 有用排序校准、M4 合格训练 Ranker、M5 联合冻结与 M6 正式 SWE 仍未通过验收。


**原始重放控制与逐题时间目录的补齐**

[本次审计](results/original-replay-controls-and-temporal-catalog-preparation-audit-20261006-v1.json)新增版本化 evaluator 重放控制实现。控制在原始公开源码上先冻结测试集合，再执行已知修复，验证相同运行时、F2P、PTP、原有测试保留和来源字节未变；这些控制不替换原生 SourceRecord，不向 planner、Ranker 或 solver 提供已知答案。

原生 F2P/PTP 的测试名称可以重叠：同一个既有测试可能扩展断言后成为回归 F2P。因此当前实现保存交集，并要求匹配测试体 AST 或精确参数化 fixture 的变化见证；无见证的原有 passing→failed 仍拒绝。修正后完整工程测试为 **808 passed、20 skipped（109.14 秒）**，专项 53 passed，lint 和格式通过。这些是工程检查，不代表独立迁移或 SWE 成功。

[旧协议全部控制](controls/pre2021-original-release-replay-20261006-v1/README.md)保留 21/21 注册目标，其中 19 条有恢复输入：2 个机械 PASS、13 个控制未合格、4 个旧交集检查导致的执行缺口、2 个原始输入缺口。不得把资格缺口写成候选失败标签；两项 PASS 也尚未独立验收。修正协议已启动新的 21 条控制，机器快照只记录有时间戳的进度，不将其写成终态。

[19 份逐输入时间目录](history-query-recovery/pre2021-temporal-catalogs-20261006-v1/README.md)已完整生成：统一校验全部 75 个已供应原生包后，按每个问题输入时间和因果排除规则重建候选。最早 #395 无合格历史；#574 有 16 个时间合格包。仅证明准入，不代表相关性、绑定、排序或修复效果。75 个供应包仍不是完整历史普查。

[Python 3.7 实际沙箱预检](controls/historical-python37-runtime-20261006-v2/README.md)通过，保留非特权执行器和 uv venv 配置格式的两次失败。#507 的公开复现需要 Python 3.8 语法，另已开始对应兼容解释器构建。解释器补丁版本与执行时间均按当前真实时间记录；不能据此回填历史发布证明。部分发行包缺少 master 上的代码或测试，仍需恢复有公开时间证据的 pre-input Git 源码。

控制和目录准备没有调用模型、运行 solver 或生成效用标签。既有 31 条 Pylint 原生包作者任务继续串行运行，进度单独记录；全部来源晚于训练截点，不作为 pre-2021 Ranker 正例。M1 独立迁移、M2 互补组合、M3 有效校准、M4 训练 Ranker、M5 联合冻结和 M6 正式 SWE 仍未验收，整体目标未完成。


**公开 Git 基线恢复与修正控制终态（v31）**

[本次实际审计](results/public-branch-source-and-corrected-replay-preparation-audit-20261006-v1.json)将修正协议的发行版控制更新为终态：21/21 保留，19 条原始查询，2 项机械 PASS、17 项未合格、2 项原始输入缺口；完整独立重放接受仍为 0。结果见[修正协议控制](controls/pre2021-original-release-replay-20261006-v2/README.md)。已知修复仍仅供 evaluator，任何来源、补丁或环境缺口不产生候选失败标签。

已补充共享原始输入校验和公开 Git 源恢复模块：以稳定仓库数字 ID、明确分支、严格 pre-input 时间和官方 GH Archive 原始 PushEvent 证明公开 head；核对 commit/blob 字节与 mode 后只复制该 head，depth-1 checkout 不包含后来对象。公开索引只定位小时，不能代替原事件证明，也不宣称完整 push 历史。[冻结定位工件](history-query-recovery/pre2021-public-branch-locator-20261006-v1/README.md)保存全部 1819 条相关仓库定位行及 18 个小时，不使用任意 top-N。

第一版在扫描前遇到 str/Path 错误，第二版 18/18 归档请求被 HTTP403 拒绝，均保留。限长诊断证实既有审计 User-Agent 可访问相同 publisher 地址，现已修正请求标识并补充完整压缩流 hash/计数测试；[旧失败和诊断](history-query-recovery/pre2021-public-branch-source-failure-20261006-v2/README.md)不覆盖。v31 只保存带时间戳的新版真实进度，不能把 live 扫描或已验证 Push 投影算成已接受修复。

[Python 3.8 copied namespace 预检](controls/historical-python38-runtime-20261006-v1/README.md)已通过。另按原始 Pylint 输入的 astroid/Python 报告准备兼容 runtime，并记录实际依赖约束与失败。原始版本报告仍是未观察的声明，#3468 的兼容 runtime 使用支持的 3.7 而报告为 3.6，#3798 的 astroid 为待源 requirements 核实的推断，不能宣称精确复现原用户环境。公开 Git query 与对应运行时尚需独立 replay 控制与验收。

最新完整工程检查为 **832 passed、20 skipped（149.09 秒）**；专项 **71 passed（3.85 秒）**，五个改动文件 lint、格式和 diff 检查通过。代码字节与工程 receipt 的 SHA256 一致。本次源码恢复、runtime 准备和工程检查新增模型请求、solver 分支、效用标签、正式 SWE runs 均为 0；已有原生作者仍串行运行，其进度单独保存，全部 31 个来源晚于训练截止。

M1 独立迁移、M2 真正互补的两父组合、M3 有效排序校准、M4 合格训练 Ranker、M5 联合冻结和 M6 正式 SWE 与消融仍未验收。整体目标保持 active，没有因工程测试或准备工作改成完成。
