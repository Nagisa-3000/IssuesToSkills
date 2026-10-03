**软件生成与自动修复 Agent：代表性顶刊、顶会工作及 Benchmark 调研**

调研日期：2026-10-03。范围以 2024–2026 年的 LLM Agent、软件开发工作流及其训练方法为主。顶刊采用 TSE、TOSEM 口径；顶会包括 ICSE、FSE、ISSTA、ICLR、NeurIPS、ICML、ACL、EMNLP。期刊正式发表、Online First、作者声明已接收，以及尚未核实正式收录的预印本分别标注。

本报告核对了公开出版记录、论文全文或期刊摘要、作者项目及官方数据说明。它是有选择的代表性调研，未复现论文实验。文中历史成绩用于说明评测口径，不代表 2026 年实时排行榜；不同模型、预算、数据版本下的成绩不能作为横向排名。

**主要判断是：仓库级修复以 SWE-bench 系列为主，测试驱动 APR 仍大量采用 Defects4J，短函数生成主要采用 HumanEval/MBPP，而完整软件生成正在转向项目级与行为级评测。** 三类任务输入、定位难度、执行环境和 oracle 不同，必须分开解释。对于 AREX Skill Graph，最有价值的证据是跨项目经验能否在冻结的、未见过目标修复的任务上提高真实修复成功率。

期刊中的代表性工作如下。表中链接指向出版记录或作者论文；“摘要确认”表示 benchmark 已在正式期刊摘要中明确出现，但本次未获得该版本的全部实验配置。

| 工作 | 发表状态 | 方法与任务 | 实际使用的 benchmark / 数据 | 应如何理解结果 |
| --- | --- | --- | --- | --- |
| [SGAgent](https://doi.org/10.1145/3818617) | **TOSEM，2026-05-26 Online First** | Localizer、Suggester、Fixer 协作；从目标仓库构建代码知识图谱；采用 localize–suggest–fix | **SWE-bench Lite**；扩展到漏洞修复时使用 **VUL4J、VJBench**，摘要确认 | Claude 3.5 配置报告 51.3% 修复率，Claude 4 配置报告 60.7%。同时报告文件/函数定位和成本。这里的图是仓库代码关系图，不能直接等同于跨仓库历史修复 Skill 图。 |
| [Agentic Program Repair from Test Failures at Scale](https://doi.org/10.1109/TSE.2026.3696849) | **TSE 52(8)，2026 年 8 月** | Meta Engineering Agent；ReAct 工具循环，结合静态分析、测试反馈、patcher 与 LLM judge | 内部 **TFMB benchmark：123 个真实测试失败，2 个大型 monorepo，15 种语言**；另有 patcher/judge 子评测 | [全文](https://arxiv.org/abs/2507.18755)报告平衡配置 solve rate 42.3%，平均 11.8 次反馈迭代；生产期还统计人工审查与合入。内部任务不具备公共 SWE-bench 的直接可比性。 |
| [ProjectGen / Towards Realistic Project-Level Code Generation…](https://doi.org/10.1145/3817056) | **TOSEM，2026-06-18 Online First** | 语义软件架构树 SSAT；架构设计、骨架生成、代码填充及迭代修正 | **DevBench**；自建 **CodeProjectEval，来自 18 个真实仓库**，摘要确认 | CodeProjectEval 平均每任务 12.7 文件、2,388.6 行代码。摘要中的 52/124、310 是**通过的测试用例数**，不能改写为解决了同样数量的项目。 |
| [Agents4PLC](https://doi.org/10.1109/TSE.2026.3667895) | **TSE 52(5)，2026 年 5 月** | 面向 PLC Structured Text 的规划、编码、验证、调试闭环；引入形式化规范与验证器 | 自建 **可验证 PLC 代码生成 benchmark**：自然语言需求、人工检查的形式化规格、参考代码 | 同时考察编译与形式化验证，oracle 比仅“能运行”更强，但结论受 PLC 领域限制。[公开仓库](https://github.com/Luoji-zju/Agents4PLC_release)区分旧版 23 任务、更新后的 96 任务及另一个 21 任务 High-Fidelity 集；不能把不同版本数量混为正式期刊全部实验规模。 |
| [AdaCoder](https://doi.org/10.1109/TSE.2025.3642621) | **TSE 52(2)，2026 年 2 月正式卷期**；DOI 标识含 2025 | 先直接生成和测试；失败后启用规则调试及自适应规划；研究多 Agent 在不同基础 LLM 上的泛化 | [作者公开数据目录](https://github.com/YXingo/AdaCoder/tree/main/src/datasets)可确认 **HumanEval**；完整正式论文的实验清单未获得 | 属于函数级生成。公开代码不能证明完整正式论文还使用 MBPP、SWE-bench 等数据；也不能仅凭 DOI 中的年份推断 Early Access 日期。 |
| [KGMACG](https://doi.org/10.1145/3842390) | **TOSEM，2026-09-15 Online First** | 组织与规划、知识辅助编码、测试 Agent 协作，面向应用级代码生成 | **3 个工业规模案例：电商、校园安防、股票交易**，摘要确认 | 不是 SWE-bench/HumanEval 标准评测。需要检查需求覆盖率的定义、测试独立性和案例公开程度；“95% 需求覆盖”自身不构成完整正确性的形式化证明。 |
| [HumanEvalComm / Okanagan](https://doi.org/10.1145/3715109) | **TOSEM，2025-01-27 Online First** | 面向含歧义、矛盾或缺失条件的需求，先澄清再生成 | **HumanEvalComm**，从 HumanEval 164 原题构造 **762 个需求变体**，见[全文](https://arxiv.org/abs/2406.00215)表 1 | 除 Pass@1/Test Pass Rate，还测 Communication Rate、Good Question Rate；评估需求沟通，不是仓库修复能力。 |
| [EnvPilot](https://arxiv.org/abs/2609.07357) | **作者在 2026-09-07 预印本页声明 TOSEM 已接收；本次未独立核实正式卷期** | 从历史执行轨迹蒸馏 problem–solution–action 经验；Context-aware Retrieval；环境搭建 | **AES-Bench：112 个真实 GitHub 实例，9 种语言**；初始记忆 **667 条经验** | 报告 75.00% Pass@1；全文说明记忆来源与评测仓库分离。它是经验复用的重要近邻工作，但成功指标是环境搭建，不能称为软件缺陷修复率。 |

会议中的代表性工作如下；表内会议条目均为已核实正式发表的工作。Agentless 是必要的非 Agent 对照；SWE-Gym、SWE-smith、SWE-RL 是训练方法或训练环境，均按实际角色列出。

| 工作 | 顶会 / 年份 | 核心机制 | 论文使用的 benchmark | 关键评测边界 |
| --- | --- | --- | --- | --- |
| [SWE-agent](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html) | **NeurIPS 2024，正式发表** | 为 LM 设计 Agent–Computer Interface：搜索、浏览、编辑、运行测试 | 主实验 **SWE-bench Full 2,294**；消融与分析 **Lite 300**；**HumanEvalFix Python/JavaScript/Java，每语言 164**，见[全文](https://arxiv.org/abs/2405.15793)表 2 与附录 B.8 | 仓库 Issue 修复与函数修复分别评估。工具接口本身是重要变量，不能只比较提示词；函数修复的 3 种语言结果也不能合成一个仓库 resolved rate。 |
| [AutoCodeRover](https://doi.org/10.1145/3650212.3680384) | **ISSTA 2024** | AST/类/方法搜索，迭代上下文获取；有测试时用 spectrum-based fault localization 辅助 | **SWE-bench Full、SWE-bench Lite**，见[全文](https://arxiv.org/abs/2404.05427)实验设置 | 应区分测试辅助定位、不同尝试次数和最终提交的 pass@1；不能把多次尝试的覆盖率作为单次成功率。 |
| [RepairAgent](https://doi.org/10.1109/ICSE55347.2025.00157) | **ICSE 2025** | 有限状态约束的自主修复 Agent；查找修复材料、修改、运行测试 | **Defects4J 835 bugs**：v1.2 的 395 + v2.0 新增的 440，17 个 Java 项目，见[全文](https://arxiv.org/abs/2403.17134) | 正确修复 164 bugs。区分 plausible 和 correct：通过测试后，进一步与开发者补丁做语法或人工语义核验。 |
| [Agentless / Demystifying LLM-Based Software Engineering Agents](https://doi.org/10.1145/3715754) | **FSE 2025；PACMSE 2(FSE)，正式发表** | 固定的定位、修复、补丁验证流水线 | **SWE-bench Lite 300、Verified 500、Lite-S 249**，见[论文](https://arxiv.org/abs/2407.01489) | Lite-S 是作者排除问题描述或参考补丁有问题的实例后得到的子集。PACMSE 是与 FSE 对应的期刊形式 proceedings，不能写成 TOSEM。复杂自主控制或更多角色并非必然胜出，适合作为 Skill 工作的强对照。 |
| [UniDebugger](https://aclanthology.org/2025.emnlp-main.921/) | **EMNLP 2025 主会，正式发表** | 分层多 Agent，联合根因分析与修复；Helper 检索修复参考材料 | **Defects4J 806 active bugs**（v1.2 的 391 + v2.0 新增 415）；**Codeflaws、QuixBugs Java/Python 各 40**；跨模型实验使用 **ConDefects 抽样 600，Java/Python 各 300** | Defects4J 正确修复 197、plausible 286；Codeflaws 的 95% 正确率来自**100 个 plausible patches 抽检**，不等于全量正确修复率。ConDefects 只报 plausible 数。正文对 Codeflaws 写 3902/3982，存在口径不一致；不得替作者默算总量。 |
| [OpenHands](https://iclr.cc/virtual/2025/poster/29831) | **ICLR 2025，正式收录已由会议官网核实** | 通用代码执行、工具与浏览器环境，CodeAct 等 Agent | 软件相关主评测包括 **SWE-bench Lite 300、HumanEvalFix Python 164**；另有 BIRD、ML-Bench 等，整体涵盖 15 类任务，见[作者全文](https://arxiv.org/abs/2407.16741) | 通用平台支持的任务与仓库修复成绩不是同一指标；需要选同一个 Agent 实现、runtime 和模型比较。 |
| [SWE-Gym](https://proceedings.mlr.press/v267/pan25g.html) | **ICML 2025，正式发表** | 训练 SWE Agent 与轨迹 verifier；推理期候选验证 | **训练环境 2,438 个 Python 实例、11 仓库**；另有 **SWE-Gym Lite 230**；正式测试 **SWE-bench Verified 500、Lite 300** | 全文 §3 说明训练仓库与 SWE-bench 仓库分离，提供跨仓库迁移证据。SWE-Gym Lite 是训练/原型子集，不能当作 SWE-bench Lite；训练收益与 best-of-N verifier 的额外推理预算须区分。 |
| [SWE-smith](https://doi.org/10.52202/085713-3239) | **NeurIPS 2025，正式发表** | 通过程序修改、合成故障、PR mirroring 等构建可执行训练任务 | [论文](https://arxiv.org/abs/2504.21798)创建 **50k+ 任务、128 仓库**，最终模型使用 **5,016 条轨迹**训练；测试 **SWE-bench Verified 500、Lite 300、官方 Multilingual 300** | 任务数、实际训练轨迹数和测试分母分开。§3 明确 Multilingual 评测，不能遗漏后误写为仅 Verified。40.2% 是当时 SWE-agent-LM-32B 配置的 Verified 成绩；扩大训练仓库数量本身不能替代完整仓库留出的证明。 |
| [SWE-RL](https://doi.org/10.52202/085713-2629) | **NeurIPS 2025，正式发表** | 使用公开软件演化历史做 RL，改善修复推理 | **SWE-bench Verified 500**；用 **Agentless Mini** scaffold，见[论文](https://arxiv.org/abs/2502.18449) | 历史 PR 用于模型参数训练，附录说明排除 SWE-bench 仓库；这与运行时检索 Skill 不同。不能把它归为“多 Agent 框架优于单 Agent”的证据。 |
| [MetaGPT](https://iclr.cc/virtual/2024/poster/18491) | **ICLR 2024，正式收录已由会议官网核实** | 将产品、设计、工程、测试角色按 SOP 协作 | **HumanEval、MBPP、自建 SoftwareDev** | SoftwareDev 共 70 任务；[作者全文](https://arxiv.org/abs/2308.00352)的主要框架比较随机选 7 个代表任务，附录另有更多设置。人评可执行性/质量与隐藏测试通过率不能等同。 |
| [ChatDev](https://aclanthology.org/2024.acl-long.810/) | **ACL 2024** | 软件公司角色模拟、分阶段通信与调试 | 自建 **SRDD：1,200 个软件需求 prompt，5 大类、40 子类** | 评估完整性、可执行性、任务一致性与成本等。1,200 是需求数据规模，不等于 1,200 个具有独立隐藏测试的仓库修复题。 |
| [MapCoder](https://aclanthology.org/2024.acl-long.269/) | **ACL 2024** | 检索相关例子、规划、编码、调试的角色协作 | **HumanEval、HumanEval-ET、EvalPlus、MBPP、MBPP-ET、APPS、CodeContests、xCodeEval** | 实验使用 HumanEval 164、MBPP 397；APPS 采样 150、CodeContests 165、xCodeEval compact 106。成绩必须连同子集解释。 |
| [USEagent / Unified Software Engineering Agent as AI Software Engineer](https://doi.org/10.1145/3744916.3773202) | **ICSE 2026 研究主轨，2026-04-12 正式发表** | Meta-Agent 动态编排代表工程“工作单元”的 Actions；每个 Action 可独立维护；共享知识用于任务内协作 | **USEbench 主实验 1,271 题**：Verified 500、SWT-bench-Lite 298、REPOCOD-Lite 200、REPOTEST-Lite 173、SWETRY 100，见[作者稿 v2](https://arxiv.org/abs/2506.14683v2)表 1–2 | 混合修复、测试、函数生成与继续完成失败补丁，oracle 不同；33.3% 综合成功率不是 SWE-bench 修复率。表 1 另描述 46 个 feature-development 任务，未计入主实验 1,271 分母。Pass@5 只在抽样 295 题测量。Actions 来自工程设计，并未证明从跨项目历史自动学得 Skill。 |
| [SEAlign](https://doi.org/10.1145/3744916.3764563) | **ICSE 2026 研究主轨，2026-04-12 正式发表** | 高质量工作流轨迹对齐；MCTS 为关键步骤评分，再做偏好优化 | **HumanEvalFix 164、SWE-bench Lite 300、Verified 500**，见[作者稿 v1](https://arxiv.org/abs/2503.18455v1) §5；训练数据排除评测仓库/代码片段 | 评估限制为最多 30 个交互回合或 32k 上下文。改善 instruction following、工具使用和重复循环；收益来自参数对齐，不能归因于运行时 Skill 包或某种文档格式。 |
| [SWE-Debate](https://doi.org/10.1145/3744916.3787810) | **ICSE 2026 研究主轨，2026-04-12 正式发表** | 从当前代码依赖图生成故障传播路径；多角色三轮竞争式辩论；将统一修复计划交给 MCTS 修改 Agent | **SWE-bench Verified 500、Lite 300**，见[作者稿 v1](https://arxiv.org/abs/2507.23348v1) §4.2 | 强调定位推理和计划形成，图源自当前目标仓库；不是历史 Skill 图。辩论轮数、搜索预算和模型须一起固定，不能把更大推理预算的收益归因于 Agent 数量。 |
| [ReinFix / Repair Ingredients Are All You Need](https://doi.org/10.1145/3744916.3764534) | **ICSE 2026 研究主轨，2026-04-12 正式发表** | 推理阶段检索当前程序内部定义；解题阶段按 buggy code + root cause 检索历史 bug-fix pairs，提取修复材料与动作 | **Defects4J v1.2 的 391 active + v2.0 新增 438**；**RWB v1/v2 单函数任务 44/29**。历史检索库为 **TRANSFER 随机 100k pairs**，见[作者稿 v1](https://arxiv.org/abs/2506.23100v1) §4.2–4.5 | **完美故障定位**，最多 3×3×5=45 个候选；仅保留首个 plausible patch，再人工核验正确性。v1.2 报告 146 correct/207 plausible。历史库按 exact match 排除评测样本，不等于整仓库留出或近重复排除。这是历史策略复用的直接强对照，尚不是原生 Skill Package。 |

新增的四项 ICSE 2026 工作均已由 ACM 出版元数据核实正式收录。上述细节对应所链接的公开作者稿：USEagent v2，其余三项 v1；本次未逐字核对出版 Version of Record。作者稿保留旧模板或写“to appear”，不能据此否定已由出版社确认的发表状态；反过来，arXiv 的投稿日期也不能当作会议发表日期。

与“历史经验 → 可复用 Skill”更近的两项 2026 年工作补充如下。它们是 **Findings of ACL 2026 正式论文，非 ACL 主会论文**，与上表主会工作分开；其评测也不直接测仓库 Issue 修复。

| 工作与发表状态 | 复用机制 | 实际实验数据 / 指标 | 对 AREX 的意义与边界 |
| --- | --- | --- | --- |
| [ReMe / Remember Me, Refine Me](https://aclanthology.org/2026.findings-acl.829/)；**Findings of ACL 2026，2026 年 7 月正式发表** | 从成功模式、失败触发条件、对比轨迹蒸馏细粒度经验；按场景适配检索；按使用效用更新或淘汰记忆。经验含 when-to-use、内容、关键词、置信度与 tools | [正式全文](https://aclanthology.org/2026.findings-acl.829.pdf) §4.1：**BFCL-V3 base multi-turn，50 题构建经验 + 150 题评测**；**AppWorld 90 train + 168 test-normal**。报告 **Avg@4 / Pass@4**，分别比较 fixed / dynamic memory | 直接支持研究适用条件、失败经验、检索后适配与记忆生命周期。工具调用及应用操作成功率不能改写为源码修复成功率；动态记忆的任务顺序与测试反馈权限须固定，不能与冻结 catalog 的静态实验混报。 |
| [CodeMEM](https://aclanthology.org/2026.findings-acl.834/)；**Findings of ACL 2026，2026 年 7 月正式发表** | AST 引导维护当前代码上下文；把当前会话历史变为代码中心记忆，检测遗忘和重复引入已修错误 | [正式全文](https://aclanthology.org/2026.findings-acl.834.pdf) §4.1：**CodeIF-Bench L-2：40 个 Python 对话、360 条指令（每对话 9 条）**；**CoderEval：230 个 Python 任务**，扩展为测试反馈驱动的多轮生成。测指令遵循、测试通过及交互轮数 | 解决同仓库、同会话多轮生成的上下文保持。不能直接作为跨项目历史经验迁移的证据；适合用作“仅保留当前会话记忆”的对照。 |

以上各工作的设计能归纳为四条路线：通过 ACI/执行反馈加强自主工具使用；以程序分析和结构化上下文改善定位及修复建议；将职责固定为可控开发流程；通过训练数据、RL、verifier 或历史经验复用改善模型和决策。多 Agent 数量本身并不是一条独立的有效性保证。

benchmark 的任务含义与选用建议如下。数量优先注明论文发布时或本次公开数据版本；动态数据集必须固定 revision 和 instance IDs。

| Benchmark | 任务、语言及规模口径 | Oracle / 常见指标 | 能回答什么问题，以及边界 |
| --- | --- | --- | --- |
| **HumanEval / MBPP** | 需求到短 Python 函数；HumanEval 164。MBPP 的原始、测试、sanitized 子集须分别注明；MapCoder 用 397 | 隐藏单元测试；Pass@k | 检验局部代码生成/反馈修正；不覆盖仓库定位、依赖、跨文件修改、兼容性。 |
| **HumanEval-ET / MBPP-ET / EvalPlus** | 增强上述短函数题的测试覆盖 | 更充分的测试；Pass@k | 减少原测试过弱造成的误判；仍然是函数任务。 |
| **HumanEvalFix** | 从 HumanEval 正确函数注入故障的函数修复任务；[官方 OctoPack](https://github.com/bigcode-project/octopack)支持 6 语言、每语言 164。SWE-agent 论文实际报告 Python/JavaScript/Java，OpenHands 主表用 Python | 单元测试；Pass@k | 输入是有 bug 的函数与测试，区别于从需求生成函数。数据集支持的语言数不等于某论文实际评测的语言数。 |
| **BigCodeBench** | [官方项目](https://github.com/bigcode-project/bigcodebench)：1,140 个强调复杂指令和多库调用的 Python 函数任务；Complete/Instruct 设置不同 | 功能测试；Pass@k | 比 HumanEval 更强调实际库调用；适合作为生成能力补充，但仍不能替代仓库修复。 |
| **APPS / CodeContests / xCodeEval** | 算法与竞赛程序；各论文采样规模差异大 | 输入输出测试、Pass@k | 衡量算法推理与边界条件；真实工程依赖、API 演化、系统集成较弱。 |
| **Defects4J** | 真实 Java 项目、可复现 bug 与测试。RepairAgent 用历史 **835**；UniDebugger 用 **806 active**；ReinFix 用 **391+438=829 active**；[当前官方 README](https://github.com/rjust/defects4j)为 **v3.0.1，854 active + 10 deprecated** | Plausible patches、correct patches、时间/候选预算 | 同名数据不能默认同分母。需固定版本与 bug IDs，并声明 perfect/realistic fault localization、多行/多函数/多文件覆盖及人工正确性核验。 |
| **RWB v1 / v2** | ReinFix 用于较新 bug 的单函数验证；**44 / 29** 题，bug-fixing commits 分别取 2021-10、2023-03 之后，见其全文 §4.2 | 测试通过后人工核验正确补丁 | 时间截断原本针对当时 GPT-3.5/DeepSeek-Coder 的预训练截止日期；不能宣称对所有 2026 模型均无污染。两版是单函数实验，不覆盖完整自主仓库定位。 |
| **QuixBugs / Codeflaws / ConDefects** | 小程序或竞赛故障；QuixBugs 每语言 40。UniDebugger 的 ConDefects 是 **600 抽样（每语言 300）**，并非其原始 **1,254 Java + 1,625 Python** 全集 | 测试通过、人工正确性检查；部分论文只抽检 plausible patches | 对抽样正确性比例报告样本与抽样方式，不能当作所有修复均经人工核验。Codeflaws 在 UniDebugger 正文中的 3902/3982 不一致需保留原文限定。小程序 repair 不能外推为真实仓库维护能力。 |
| **SWE-bench Full / Lite / Verified** | Full **2,294**，Lite **300**，Verified **500**；Python 仓库真实 Issue–PR | 容器化测试；resolved rate；F2P + P2P | 仓库修复标准对照：从 Issue 和修复前代码出发。Verified 人工审核提高可解性，不等于排除预训练污染或所有 oracle 缺陷。 |
| **官方 SWE-bench Multilingual** | **300 题、9 语言**：C/C++/Go/Java/JS/TS/PHP/Ruby/Rust | 与 SWE-bench 兼容的 F2P/P2P | 适合跨语言、跨工具链迁移。官网称 42 仓库，当前 HF card 称 41；本报告不强行统一这一版本差异。 |
| **Multi-SWE-bench** | **NeurIPS 2025**；**1,632 题、7 语言**：Java/TS/JS/Go/Rust/C/C++；另释出 **4,723 训练实例** | 仓库 Issue 测试判定；环境/任务构建 | 与官方 Multilingual 是**两个数据集**。训练 Multi-SWE-RL 与测试 Multi-SWE-bench 也须分开。[论文](https://arxiv.org/abs/2504.02605)、[收录记录](https://doi.org/10.52202/085713-2111)。 |
| **SWE-bench-Live** | **NeurIPS 2025**；论文首发 **1,319 题、93 仓库**，另建 **Lite 300**；Issue 从 2024 年起采集；设计为持续更新 | 可执行 Docker + F2P/P2P；resolved rate | 论文在 Lite 比较全部 Agent–模型组合，再将排名前三组合用于 Full。更适合新时间段和广泛仓库的验证；“Live”需要固定时间快照，不自动保证绝无污染。[论文](https://arxiv.org/abs/2505.23419)、[收录记录](https://doi.org/10.52202/085713-4923)。 |
| **SWE-bench Pro** | **预印本，正式顶会收录未核实**；原论文 **1,865 题、41 仓库**；公开 **731**，另外有 held-out 与 commercial 部分 | 人工核实、增强任务描述、长链条多文件测试评估 | 用于更复杂、长周期工程任务；公开与非公开结果不能混为一个分母。[论文](https://arxiv.org/abs/2509.16941)；本次未独立核实正式顶会收录，不计入已发表顶会方法表。 |
| **SWE-bench Multimodal** | **ICLR 2025**；采用最新公开 v2 口径：官方 2026-09-01 宣布 **480 test**，当前 card 另列 100 dev | 图像相关 Issue + 仓库修改 + 测试 | 补充 UI、渲染、图表等视觉软件域。早期论文摘要写 617、正文写 619，当前 card 描述写 612；这些历史统计不能与 v2 混用。[论文](https://arxiv.org/abs/2410.03859)、[官方 card](https://huggingface.co/datasets/SWE-bench/SWE-bench_Multimodal)。 |
| **CodeIF-Bench / CoderEval（CodeMEM 使用口径）** | [CodeMEM 正式全文](https://aclanthology.org/2026.findings-acl.834.pdf)的 **L-2 子集 40 对话/360 指令、CoderEval Python 230**；后者在本论文中扩展为多轮测试反馈生成 | 指令验证与测试执行；当前轮/会话表现、交互轮数 | 研究代码记忆和多轮生成，输入包含目标函数/项目上下文；不是从 Issue 自主定位的全仓库 repair。论文使用的子集不能改写为完整 CodeIF-Bench 或所有语言的 CoderEval。 |
| **DevBench / CodeProjectEval** | 项目构建/代码生成；ProjectGen 的 CodeProjectEval 源于 **18 个真实仓库** | 编译、项目级执行测试、测试通过数 | 更接近完整软件生成。应额外报告整项目成功率，不能只累加通过用例数。 |
| **SoftwareDev / SRDD** | 软件需求到应用的早期自建集；分别见 MetaGPT/ChatDev | 人工或模型质量评估、可执行性、时间/成本 | 适合考察协作产物和过程；对于功能正确性，独立可执行 oracle 比主观评分更有解释力。 |
| **AES-Bench** | 112 GitHub 实例、9 语言；软件环境搭建 | Pass@1、成本、步数 | 检验经验复用如何帮助配置依赖并运行项目，不能当作补丁修复 benchmark。 |
| **PLC benchmark** | Structured Text 需求到代码与规格；版本见 Agents4PLC | 编译、形式化验证、综合成功率 | 适合有形式化规范的领域任务；形式化正确性仍然相对于给定规范与环境假设。 |
| **TFMB internal benchmark** | Meta 内部 123 真实测试失败，15 语言 | 解决率、错误率、成本/时延；生产审查和合入 | 体现工业适用性，但外部难复现，也不能与公共测试集百分比直接竞争。 |
| **USEbench** | [ICSE 2026 正式论文](https://doi.org/10.1145/3744916.3773202)的统一工程评测；主实验 **1,271**，五部分分别 **500/298/200/173/100**，具体见方法表；另描述 46 个 feature-development 任务 | Repair/code generation 用 test-suite pass；regression testing 用 patch coverage；REPOTEST 用 code coverage | 考察动态识别任务与组合 Actions。同一底层仓库或 Issue 可派生不同任务；不是 1,271 个独立修复题。应分别报告各子任务指标，不能只用混合总体成功率证明修复或功能完整性。 |
| **ProgramBench** | **预印本，正式顶会收录未核实**；[2026-05 论文](https://arxiv.org/abs/2605.03546)，**200 任务**；[官网](https://programbench.com/)本次所见更新日期 2026-09-28。给定可执行程序和文档，从头重建代码与 build script | 独立行为测试，由 agent-driven fuzzing 构建；完全 solved 与 ≥95% tests 分开 | 最新完整软件构建方向的重要补充。不是一般自然语言需求，也不是 Issue 修复；本次未核实顶会收录。 |

SWE-bench 规模与定义采用[官方仓库](https://github.com/SWE-bench/SWE-bench)及 [Full](https://huggingface.co/datasets/SWE-bench/SWE-bench)、[Lite](https://huggingface.co/datasets/SWE-bench/SWE-bench_Lite)、[Verified](https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified)、[Multilingual](https://huggingface.co/datasets/SWE-bench/SWE-bench_Multilingual) 数据说明。官方 Multilingual 的任务与局限还见[介绍页](https://www.swebench.com/multilingual.html)。

从这些实验可以得到几项更有用的判断。

**“生成了补丁”与“修复成功”之间，需要独立验证。** RepairAgent 区分 plausible/correct，工程 Agent 使用静态分析、测试、judge 和人工审查，Agents4PLC 使用形式化验证。仅有输出文件、JSON、Skill 文档、能编译或 Agent 自称完成，都不构成功能成功。即使隐藏测试通过，也不能保证覆盖全部需求。

**论文中的 Pass@1 不一定意味着只调用模型一次。** 一个 Agent 的一次完整运行可以包含搜索、规划、多轮代码修改、测试反馈和多个内部候选。应报告整条轨迹的 token、工具调用、候选数、时限和费用。Pass@k、多次运行后取最好结果、verifier 的 best-of-N，以及单次运行 resolved rate 必须区分。

同名框架也可能被评测论文改写。例如 SWE-bench-Live 论文说明，其 Agentless 实现省掉 regression-testing reranking，定位与修复阶段都仅生成一个样本。因此该结果不能直接等同于 FSE 论文的完整 Agentless 配置；引用“相同 Agent 的不同 benchmark 分数”时也必须核对 scaffold。

**定位信息和测试权限会改变任务难度。** 已知 faulty function/line 的 APR、提供触发测试的 repair、从 Issue 在整个仓库自主定位，属于不同实验条件。由 evaluator 保留的目标补丁和隐藏测试，不能成为 Agent 或 Skill 提取器的输入。Agent 自己生成的测试可以提供反馈，但不能作为最终独立成功 oracle。

**最新研究更重视环境、跨仓库迁移和长链条工程。** Live、Multilingual、Pro 增加新仓库、新语言和任务复杂度；ProjectGen、ProgramBench 增加架构与完整项目构建要求。一个在 HumanEval 上很强的多 Agent 系统，仍可能在依赖配置、API 兼容、跨文件修改和真实回归测试上失败。

**经验复用、当前仓库知识与工程 Action 抽象应分别比较。** 仅把它们都称为 knowledge/memory/skill，会掩盖真正的贡献与泄漏边界。

| 复用对象 | 代表工作与可确认的证据 | AREX 应如何建立差异 |
| --- | --- | --- |
| 当前仓库代码关系、依赖与定义 | SGAgent、SWE-Debate、ReinFix 内部 ingredients；用于理解目标代码和定位 | 作为目标上下文的一部分固定；不能把仓库代码图带来的收益算成跨项目历史 Skill 收益。 |
| 人工设计的可组合工程工作单元 | USEagent Actions；Meta-Agent 自配置流程，Action 可独立维护 | 区分“预置 Actions 能执行”与“从历史经验自动生成了有效 Actions”。历史蒸馏及门控需要单独对照和证据。 |
| 历史 buggy/fixed code 与修复根因 | ReinFix 的 TRANSFER 100k 检索、UniDebugger 的 Helper 修复材料检索 | 是最直接的 RAG 对照。要证明 Skill 抽象的价值，应从同一历史池比较原始案例检索与抽象 Skill，而非只与无检索 Agent 比较。 |
| 历史执行轨迹中的程序性经验 | EnvPilot 的 problem–solution–action；ReMe 的场景条件、成功/失败/对比经验与淘汰机制 | 支持研究经验抽象、适用性和生命周期，但任务域分别是环境搭建与工具/应用操作。必须在修复任务重新验证。 |
| 当前会话中已经验证的代码与交互历史 | CodeMEM 的 AST 上下文与会话记忆 | 对照任务内记忆与跨任务历史 catalog，避免把上下文压缩收益误认为跨项目泛化。 |
| 模型参数中的历史知识与行为 | SWE-Gym、SWE-RL、SEAlign；训练轨迹或 PR、关键步骤/偏好对齐 | 与运行时检索包是不同干预，应固定模型版本，并将 post-training 与 Skill 注入拆成可检验变量。 |

AREX 的设计是从跨仓库历史 Issue/PR 与验证轨迹**直接生成可使用的原生 Skill Package**（`SKILL.md`、Action、Evidence、references 等文件），再从这些文件派生图与检索索引。它最接近“历史案例 RAG + 程序性经验蒸馏 + 可组合 Action”，而非仅当前仓库代码图。已有论文能说明这些机制值得研究，但不能直接证明 Markdown 格式或把 JSON 编译成文档能提高修复率。需要验证：从历史材料直接生成的适用条件与动作是否可信；在新任务中检索、门控和执行是否正确；最后是否确实提高独立 oracle 判定的修复成功率。

历史样本本身也应区分 **plausible / correct / unknown**：来源 PR 已合并、历史测试通过、人工语义正确是不同证据强度。Skill 的 Evidence 应保留来源和验证范围；结构 validator、路径可解析和文件可加载仅能检查交付结构，不能证明动作语义正确或可泛化。

**数据时间截断、样本去重与整仓库留出，保证的是不同层级。** ReinFix 的 exact-match 排除降低直接复制测试样本的风险，尚不能证明近重复修复或同仓库知识没有进入检索；SWE-Gym、SWE-RL、SEAlign 明确排除评测仓库，EnvPilot 也按仓库名分离历史记忆与 AES-Bench，提供了更接近跨项目迁移的设计依据。RWB 的时间窗口仅相对于论文使用的模型；Live 或“最新数据”的日期也必须相对于模型训练截止日重新审计，不能统称绝无污染。

针对 AREX Skill Graph，建议下一阶段采用以下实验设计。这是研究建议，本次调研没有执行新的 Agent benchmark。

| 要回答的问题 | 优先数据 | 对照及评价 |
| --- | --- | --- |
| Skill 注入是否提高仓库 Issue 修复能力？ | **固定 SWE-bench Verified/Lite 子集**用于与既有论文对照；补充 **Live 或 Pro 的固定公开快照**检验新任务 | 同一模型、Agent harness、工具权限、实例与预算；**无复用 / 原始 bug-fix pair 或轨迹 RAG / 从同一历史池直接生成的原生 Skill Package** 三组配对比较。匹配检索候选数和注入长度；JSON/IR 摘要可作为额外表示对照。 |
| 是否跨语言、跨项目迁移？ | 官方 **Multilingual** 或 **Multi-SWE-bench**，按语言与仓库分层选题 | 完整留出目标仓库；训练、蒸馏、合并和选择阈值不使用测试目标修复。分别报告同仓库、跨仓库和跨语言成绩。 |
| Action、适用性门控和验证梯是否有效？ | 与当前业务类别一致的小型真实 Issue/PR holdout；必要时用 Defects4J 做机制实验 | 去掉 applicability gate、去掉 Action references、去掉图扩展，逐项消融。修复成功以独立测试/人工语义核验判断。 |
| 是否真的复用了经验？ | 冻结 Skill catalog 后的新任务 | 记录命中的 Skill ID、版本/hash、使用的 Actions、适用性决策与执行轨迹；分析不适用 Skill 导致的误用及成功修复的证据链。 |

最小可行试验可以先做固定的 20–50 个实例和上述三组对照。20 题中单题变化就是 5 个百分点，只适合验证链路与发现失败模式，无法凭一次结果作广泛 SOTA 声明。正式报告应给出配对差异、置信区间，保留多次运行的随机性与失败原因。

Skill 包、图、检索参数和模型配置应在测试前冻结，保存可复现的 manifest 与 hash。另做在线学习实验时，应独立报告任务顺序、记忆更新时点、可见反馈和固定/动态 catalog，不把前一题隐藏答案写入后续静态评测。目标修复、目标 PR diff、隐藏测试和测试集上的反馈不能进入当前测试批次的 Skill 蒸馏或晋升；线上持续学习应按批次或时间段重新划分评测。URL/ID 去重之外，还应检查同一 PR/commit 的别名、近重复代码以及同一故障的衍生任务。跨项目泛化要求留出整个项目，而非仅留出同项目的某个 Issue。

最终至少同时报告：resolved rate；F2P 修复与 P2P 回归结果；环境搭建失败和补丁无效分别计数；在线 token、费用、时延及工具/测试调用；离线 Skill 蒸馏、验证、索引构建成本及按复用次数摊销的成本；Skill 误触发率和错误适用率；跨仓库、跨语言、问题类别分层成绩。环境失败属于端到端失败，同时应单独分析，避免把环境质量问题归因于 Skill 推理，也避免将其从分母删除以抬高成绩。

原生 Skill 文件可生成、validator 可通过、references 可加载、图索引可检索，以及小型构造实验，都只能证明交付与使用链路成立。要发表“经验提取与 Skill 复用改善软件修复”的研究结论，仍需上述真实任务、独立 oracle、无目标修复泄漏、同预算的 Agent 对照实验；Action 的实现、工具权限或预算若变化，也须作为单独变量记录。

建议优先精读 **ReinFix、USEagent、EnvPilot、ReMe、Agentless、SGAgent**：分别对应历史修复材料检索、可组合工程 Actions、跨项目轨迹经验、细粒度程序性记忆、强流水线基线、当前代码图与修复建议。研究训练与跨仓库迁移时再读 **SWE-Gym、SEAlign、SWE-RL、SWE-smith**；受控 APR 设计参考 **RepairAgent、UniDebugger**。面向完整软件生成时再加入 **ProjectGen、MetaGPT、ChatDev、ProgramBench**。这种阅读顺序最接近本项目的贡献与需要补足的实验。

本次核实的主要限制：部分最新期刊工作只取得出版社元数据及实验摘要，已在表中注明；AdaCoder 的完整 benchmark 清单及最初 Early Access 日期未独立核实；EnvPilot 采用作者“已接收”声明，未将其写成已核实正式卷期；四项新增 ICSE 2026 工作的正式发表由出版社记录确认，但具体实验依据公开作者稿，未逐字核对出版终稿；Pro、ProgramBench 的正式顶会收录未独立核实。官方 Multilingual、Multimodal 的网页/数据版本存在数量差异，UniDebugger 对 Codeflaws 的原文统计也不一致，本报告保留并提示口径。所有数值均来自上述公开来源，本次没有自行复现实验或编制新的模型排行榜。

核查来源优先级为 **出版社/正式 proceedings 或 ACL Anthology → 对应版本全文 → 作者官方数据与仓库**。会议表中的 DOI、NeurIPS/PMLR 页面用于确认正式收录；arXiv 链接用于取得论文内容，不能仅以 arXiv 条目推断同行评审。发表状态与当前模型榜单是两件事：论文正式发表并不使其历史结果成为 2026-10-03 的最新 SOTA。
