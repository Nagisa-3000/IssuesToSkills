**Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-05）**

**尚未全部完成。M0–M3 有代码、接口和工程测试；真实功能与跨项目效果的验收仍不完整。M4 没有合格的训练 Ranker，M5 尚未联合冻结，M6 的正式 SWE 运行数为 0。** 本文依据[当前机器快照 v20](results/pattern-crossbind-ranker-current-status-20261005-v20.json)。旧快照、失败实验和未审阅候选继续保留，源内演练、包准入和正式修复结果分别统计。

| 阶段 | 已有实现或已验证能力 | 尚缺的验收 |
| --- | --- | --- |
| M0 契约 | Action/Pattern/Task/Plan；输入输出与实际见证；当前主责任、辅助读写角色与 Oracle 绑定；来源和包 hash；时间边界；工作区内容/权限封存；独立输出复核；实际状态保存与接续 | 原生包全部 activation/applicability/functional 案例，跨项目适配与正式 KB 准入 |
| M1 重写 | 根据 Pattern 角色、必要效果、不变量及偏序生成当前 DAG；删除、替换和重排保留理由；历史 Workflow 不变 | 在独立新 Issue 中确认 Pattern，执行重写并核验修复收益 |
| M2 CrossBind | Bind/Cut/Match/Bridge/Compose/Validate；PASS/FAIL/UNKNOWN；缺前提、错误状态、读写冲突、循环及验证闭包检查；最多两个父 Workflow、四个组合候选 | 有独立来源支持的互补 Action，以及真实两父组合的执行与效果验证 |
| M3 prompted Ranker | 原 Workflow 和当前 Plan 两处排序；硬准入失败、拒绝全部、先探查；按缺失角色补召回 Action；共享预算 | 有效开发集校准，以及同冻结候选池中的配对排序效果 |
| M4 训练 | 逐 query 时间隔离；自身修复、重复和复制来源排除；适用性/执行效果监督；训练与 checkpoint 重载工具 | 可用正负适用性标签、非平局效果偏好、合格权重与开发集校准 |
| M5 冻结 | 冻结和来源校验工具 | KB、题目并集、模型、阈值、预算、索引和验收协议联合冻结 |
| M6 实验 | 配对修复、模块消融及冻结候选池 Ranker 比较入口 | 正式 SWE 配对实验和消融尚未运行 |

现有[历史配对开发实验](results/pattern-crossbind-ranker-current-status-20261005-v14.json)完成 27/27 分支：基础 Agent 7/9，两个指导分支合计 14/18。9 道题的三个分支逐题结果相同，未建立 Skill、重写或组合的修复收益。原固定候选池和代码继续保留，新候选不回填原实验。

[监督合并审计](results/historical-dual-supervision-merge-audit-20261005-v11.json)记录 84 条观察：42 条执行、42 条独立上下文复核后获接受的适用性标签；40 条训练、44 条开发。适用性标签全部 unrelated。训练的 16 对效果偏好全部平局；开发为 13 对平局、1 对非平局。未执行候选没有被填成失败，没有人为制造优先级，没有新的合格 Ranker 权重。复核仍是同一模型族的独立上下文判断，human_reviewed=false、independent_model_family=false。

Pylint #8120 的来源已通过有限范围的历史因果资格；原生包是系统直接抽取的 SKILL.md、Action、证据和 evals 资源，不进入正式 KB。当前完成的是来源内定义演练：inspect 实际 9 次执行调用、2 次独立复核；repair 为 9+2，生成 771 字节修复；regressions 为 7+2，增加 902 字节测试。三阶段都正常结束、有真实记录，并获 policy PASS/correct_confirmation/CONFIRMED。实际修复只补齐 async 进入/退出生命周期；回归增加独立 async 函数与方法，保留原有十个正例诊断。

验证失败全部保留。第一版遇到只读 pytest cache 错误并耗尽预算，未完成记录；第二版通过 subprocess wrapper 运行测试并产生记录，但独立 guard 拒绝缺少直接精确 argv 的 Oracle 见证；第三版两个直接 Oracle 都通过，独立领域判断为 CONFIRMED，但 policy 为 UNKNOWN，因为预算结束前没有 Action 完成记录。

第三版还暴露了真实系统问题：[观测身份修复审计](results/resumed-observation-identity-fix-audit-20261005-v1.json)。接续运行从零复用 current:probe:3，覆盖了先前被 suite 绑定及 Oracle 引用的证据。工作区未变，绑定却失效，solver 因此反复探查。新实现从保留的 probe、broker 观测和 Action 记录身份继续编号，避免覆盖旧见证；实际代码变化仍按原规则使证据失效，Oracle 接受 guard 没有放宽。回归先复现失败，再通过两项接续对照；新记录仍 unreviewed，失败输出不晋升事实。

第四版已实际结束：[终止审计](results/native-async-lifecycle-validation-terminal-audit-20261005-v4.json)。6 次执行调用、2 次独立复核，保持原 300000 token 执行预算。两个直接 Oracle 退出码均为 0；新记录为 action-result:1，两个直接见证为 public:observation:8 和 public:observation:9，未覆盖旧证据。五项记录检查全部 PASS，独立 policy 为 PASS/correct_confirmation/CONFIRMED，0 字节新增 patch。记录之后的下一次请求被预算预检拒绝，实际用量为 174458；solver_ended=false、source_validation_case_accepted=false。记录的复核通过没有被改写成正常 finish 或完整来源验收。下一步需限制重复观测进入模型上下文，保留完整封存轨迹和原预算。它仍是来源内定义演练；activation/applicability 全案例、新 Issue 泛化及跨项目组合未完成。历史作者已恢复，并以原 PID/start ticks 核实为运行状态。

第五版真实验证已经结束：[终止审计](results/native-async-lifecycle-validation-terminal-audit-20261005-v5.json)。使用与第四版完全相同的验证输入，保留原 300000 token 执行上限；实际 7 次执行调用、1 次独立复核，206843 token，0 字节新增 patch。两条直接 Oracle 均退出 0，scope Oracle 又被重复执行一次；Solver 在记录 Action 前被预算预检阻止，native_action_records=0、solver_ended=false。独立 policy 为 UNKNOWN/unresolved/CONFIRMED：实际九例行为和保留控制得到确认，完成记录仍未建立。没有将领域确认、命令成功或 CLI 退出 0 当作完整验收。首次监督启动在模型请求之前遇到缩进错误，失败回执已保留，修正并语法检查后重启；最终历史作者以原 PID/start ticks 核对为运行状态，监督 lease 已结束。

新增[模型上下文紧凑视图审计](results/compact-solver-context-engineering-audit-20261005-v1.json)对应修复已发布：完整 broker 结果、原 TaskContext 和独立审查输入继续封存；Solver 接收旧 Probe 与 Action 重复见证的身份、哈希、命令结果及必要摘录，没有自动 finish、事实晋升或 Oracle 放宽。相同 145000 token 的模拟协议对照中，父提交在记录后被预算预检阻止，新实现正常 finish，原失败见证仍 unreviewed。第四版末尾数据帧的共同协议测量中，请求的 UTF-8 保守 token 预留估计从 129653 降到 115328，低于当时原剩余预算 125542。第五版真实负结果说明此压缩仍不足以确保整个运行完成；需要进一步减少保留上下文重放，并向 Solver 明确区分本次已经取得的直接 Oracle 见证与此前尝试。后续保留原预算、完整证据和独立门槛，包准入、泛化与正式 SWE 仍未完成。

第六版真实验证已结束：[v6 审计](results/native-async-lifecycle-validation-terminal-audit-20261005-v6.json)。与 v5 相同输入、原 300000 token 上限；8 次执行调用、2 次独立复核，204803 token，1 条 Action，正常 finish，0 字节新增 patch。但补充命令使用 runpy.run_path(..., run_name='__main__')，被探查脚本的 SystemExit 提前结束，后续资源哈希、sentinel 和 warning 检查未执行，stdout 为空。Solver 仍声称它们已完成；独立 policy 为 FAIL/unsupported_confirmation/UNKNOWN。两个直接 Oracle 退出 0 不足以补齐这些义务，来源验收不接受。

第七版使用新输入明确要求独立只读资源审计，不能当作同输入压缩对照：[v7 审计](results/native-async-lifecycle-validation-terminal-audit-20261005-v7.json)。代码为 196ae46、原上限 300000；8 次执行调用、1 次独立复核，206254 token。九例行为、实际回归、资源哈希、sentinel 缺席及 warning 配置均获确认；下一次模型请求在预算预检被拒绝，0 条 Action、未 finish。独立 policy 为 UNKNOWN/unresolved/CONFIRMED，来源验收仍不接受，不能从领域确认自动生成记录或结束任务。两次 supervisor/watchdog 都已 terminal，历史作者已核对原 PID/start ticks 并恢复。

[本轮进程见证日志工程审计](results/solver-run-process-journal-engineering-audit-20261005-v1.json)记录 current_run 视图：仅本轮实际 broker 结果、精确 argv、最新执行、失败覆盖旧成功、工作区变化后见证 stale。passed_process 只证明进程执行结果；完整 Task 与轨迹、原 300000 上限和独立 Oracle guard 保留。相同合成输入、145000 cap 的协议对照从一次请求后拒绝变为三次请求后记录并显式 finish，129076 用量；实际 LLM 调用和实际命令执行都是 0，记录仍 unreviewed。v7 的真实负结果仍需通过实际请求几何分析与更有针对性的模型投影解决，新的分页证据 reader 随后通过工程验证，真实完整来源验收尚未完成。

新增[只读公共证据 reader 工程审计](results/public-evidence-reader-engineering-audit-20261005-v1.json)：read_public_evidence 仅按现有 Task anchor 或本轮实际 broker ID 读取；分页上限 4000 字符，可从完整存储的 JSON 字段选择子值。未知 ID、主机路径、非法分页/JSON pointer 和不完整 JSON 选择会被拒绝。读操作不执行命令、不推进 Task revision、不建立新 Oracle 见证、不提升事实或 Action；保留的 anchor 表示也可能已经是摘录。当前 public_problem、事实、绑定、端口和 Oracle 保留完整值；仅重复 broker 元数据、旧输出和解释投影压缩，普通 Probe 元数据保留原兼容性。使用完全相同的 v7 最终 Task/轨迹测量，原保守预留 99261 超过剩余 93746；新值 84388 可以发出该次请求。0 次真实 LLM/命令调用，未推断后续记录、finish 或来源验收。首次工程 lint、错误测试路径、新测试控制错误以及完整检查发现的普通 Probe 兼容性失败都保留；修复后专项和完整检查通过。下一步为相同 v7 输入的真实串行复验。

Ruff #5124 的依赖准备取得实质进展。[精确 Git 依赖恢复](results/ruff-5124-pinned-dependency-recovery-audit-20261005-v3-complete.json)获得原锁定的三个提交；LibCST 从上游取得相同提交，未替换 revision。[离线 vendor 审计](results/ruff-5124-offline-vendor-preparation-audit-20261005-v1.json)核对 310 个原始 registry 包、319 个 vendor 包和 16438 个文件哈希，使用官方 Cargo vendor 归一化，未手工改依赖 manifest。Cargo.lock 与历史 base 源码保持精确一致。

[测试构建预检](results/ruff-5124-host-build-preflight-audit-20261005-v1.json)原先仅证明编译。本轮[隔离历史因果资格](results/ruff-5124-isolated-causal-qualification-audit-20261005-v1.json)进一步完成三组精确控制：base 执行 1 项命名 Rust 测试并通过；base+新 fixture 保留原 expected snapshot，执行 1 项测试、退出 101，实际触发原始 “not a With, For, or AsyncFor” panic；精确 fixed tree 执行同一项测试并通过。原 Cargo.lock、Rust 1.74.1、319 个 vendor 包和工作区/保护资源封存保持一致，未重新生成 snapshot；INSTA_UPDATE=no、INSTA_FORCE_PASS=0、INSTA_WORKSPACE_ROOT=/workspace。四版准备/基础设施尝试及失败全部保留。此资格限定于一个历史库回归测试，0 次 LLM 调用；尚未由系统抽取或准入新的 Ruff Skill，未确认跨项目 Pattern 或接受两父组合。两个来源修复均在 2023 年，不符合 pre-2021 Ranker 训练截止。

本次源码还修复了公共 Git archive 的链接身份：保留 data_filter 的安全检查，重新检查原始目标的包含关系，并保留 contained symlink 的原始 target 文本及末尾分隔符。四项回归覆盖真实 Git tree 身份；此前错误导出和失败准备没有删除。

当前完整工程检查 **678 passed、19 skipped**，测试耗时 120.79 秒。专项 **93 passed、5 skipped**；修改文件的 Ruff E4/E7/E9/F 与 git diff --check 通过。跳过项不计为通过，工程检查不替代原生功能、迁移或正式 SWE 验收。

历史人口保持 Pylint 5273、Pyflakes 501、Ruff 3582，共 9356 个 Issue。主截止 T=2024-01-01T00:00:00Z，训练截止 τ=2021-01-01T00:00:00Z，均严格排除截止时刻及以后信息；Pylint #10034 继续排除正式评价。已知时间线缺口恢复到独立版本，旧输入与旧结果不改写；仍保留三项权限受限元数据。Pylint 的 78 个合格来源是 changed-test-only 范围。完整人口存档并不等于三项目所有历史经验完成资格复验或功能准入。

后续仍按依赖推进：完成原生包正反例和当前验证；由已限定资格的 Ruff 来源通过系统抽取和验收原生包；由独立真实来源归纳机制并执行单 Workflow 重写、互补两父组合；获得有效适用性及效果监督后训练和校准；联合冻结 M5；最后执行正式 SWE、模块消融与同候选池排序比较。整体目标保持未完成。
