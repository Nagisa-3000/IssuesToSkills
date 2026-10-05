# Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-05）

**目标尚未全部完成。M0–M3 已有实现和契约测试，真实功能、跨项目重写与组合验收仍不完整；M4 尚无合格的训练 Ranker；M5 尚未正式冻结；M6 的正式 SWE 运行仍为 0。**

最新机器快照为 [v13](results/pattern-crossbind-ranker-current-status-20261005-v13.json)。[v12](results/pattern-crossbind-ranker-current-status-20261005-v12.json) 保留时间线恢复完成时的状态。[v11](results/pattern-crossbind-ranker-current-status-20261005-v11.json) 保留资格复验与时间线缺口发现时的状态。[v10](results/pattern-crossbind-ranker-current-status-20261005-v10.json) 保留端口拒绝控制完成时的状态。[v9](results/pattern-crossbind-ranker-current-status-20261005-v9.json) 保留原生验证第二版完成时的状态。[v8](results/pattern-crossbind-ranker-current-status-20261005-v8.json) 保留验证第二版运行前的状态。[v7](results/pattern-crossbind-ranker-current-status-20261005-v7.json) 及更早版本保留当时的状态，不随新结果改写。代码、真实 Action 验收、泛化效果分别统计。

| 阶段 | 已实现或实际完成 | 尚缺的验收 |
| --- | --- | --- |
| M0 | Action/Pattern/Task 契约；输入输出见证；主责任与辅助读写角色绑定；来源/包 hash；工作区内容与权限封存；独立输出复核与状态保存；显式封存状态接续 | 原生编辑、验证 Action 的完整正反例功能验收，跨项目可用性 |
| M1 | 单 Workflow 重写；当前依赖 DAG、必要效果、不变量；历史 Workflow 不变，每项重写保留来源及理由 | 新 Issue 上确认真实 Pattern，执行重写并证明收益 |
| M2 | Bind/Cut/Match/Bridge/Compose/Validate；PASS/FAIL/UNKNOWN；冲突、循环与验证完整性检查；最多两个父 Workflow、四个组合候选 | 真实互补来源的两父组合执行及独立效果验证 |
| M3 | Workflow 与 Plan 两处 prompted 排序；准入失败、拒绝全部、先探查；按缺失角色补召回 Action；共享预算 | 开发集校准及真实效果验证 |
| M4 | 按题时间隔离；修复、别名和复制来源排除；两类候选监督与训练工具；42 条执行观察和 42 条获接受的适用性标签已合并为 84 条观察 | 有效正负适用性监督、有依据的非平局排序偏好、合格训练权重及校准 |
| M5 | 正式冻结和独立评估工具 | KB、题目、模型、预算与验收协议的联合冻结 |
| M6 | 配对修复、模块消融及冻结候选池排序比较入口 | 正式 SWE 配对实验和消融尚未运行 |

## 当前最重要的实验结果

历史开发实验完成 **27/27 分支**，包括 9 个基础 Agent 分支和 18 个冻结 Plan 分支。基础 Agent 修复 **7/9**，Plan 分支修复 **14/18**；逐题看，三个分支的修复结果相同。固定池没有已确认 Pattern、两父 Workflow 的组合或原生 Action 执行记录，指导分支探查后回退。**这没有建立 Skill、重写或 CrossBind 的修复收益。** 原固定代码和结果保留，未用新实现改写原实验。

全部 **42/42 候选/问题组合**已完成适用性提案及独立上下文复核，共 **84 次实际模型调用**；42 个标签全部获接受，全部为 **unrelated**，其中 24 个 Workflow、18 个 Plan。每项检查机制、责任边界、前提、反例、绑定及验证，并引用封存的双侧证据。详见 [完整复核审计](results/historical-applicability-completed-review-audit-20261005-v2.json)。这些是同一模型族的独立上下文判断，明确记录 human_reviewed=false、independent_model_family=false，不是人工或跨模型判定，不建立修复 utility。

[最终监督合并审计](results/historical-dual-supervision-merge-audit-20261005-v11.json)核验每个接受标签的原始证明、完整人口、历史因果对照及所有时间/候选身份。合并仍使用原冻结编译器，验证公开输入、候选、catalog hash 和时间切分保持一致。新数据为 **84 条观察：42 条执行监督 + 42 条适用性监督；40 条训练观察、44 条开发观察**。执行观察的 applicability 继续为未知，不能由操作模式推断；适用性标签也没有被填上执行结果。历史修复和隐藏断言仅供离线标签评估，不进入 Ranker 的公开输入。

偏好仍为 **30 对：训练 16 对全部平局；开发 13 对平局、1 对非平局**。没有把未执行候选标失败，没有制造优先级来训练，没有新合格 Ranker 权重。该候选池支持拒绝错误经验的监督，尚不提供选择有效修复经验的充分信号。需要先获得真实可适用、可适配的经验和效果差异，再训练排序。v10 合并器误读终止字段而退出的版本保留，0 次模型调用；v11 已实际编译成功，耗时 326.34 秒，0 次合并模型调用。

## 原生 Action 闭环的实际边界

原生包仍为 Pyflakes 的两来源 **local_template**，不是跨项目 Pattern，未晋升正式 KB。overload-inspect 四场景已完成独立复核：[v5 审计](results/native-overload-independent-functional-review-audit-20261005-v5.json)。q0 的五项 authored checks 全部 PASS，确认一个只读、修改前的 overload-review；已有 async-aware gate、其他装饰器机制及执行不可用三个边界均拒绝确认。不可用场景的领域状态仍为 UNKNOWN。这证明诊断输出及拒绝边界，不能证明修复或泛化。

编辑场景的前三次真实准入各用 1 次模型调用，并因多余未来检查、嵌套 argv、拼接符号名被拒绝；全部版本保留，没有由 host 过滤字段或填 PASS。第四版实际用 **8 次模型调用**修改两个文件，产生 **1695 字节 patch 和 1 个 overload-change 记录**。公开探针的语义输出和 3 个定向测试提供了当前范围内的支持，但 solver 随后耗尽共享 token 预算，未正常结束，不能计为已完成修复。

独立复核在单独 checkout 精确重放实际 patch，并核对内容和权限封印。旧的修改前事实、绑定、端口与语义检查按锚点变化失效。两版输出复核共 **4 次实际调用**，均确认异步分类扩展、新增回归覆盖和 post-edit/unvalidated 输出端口；普通函数行为与相邻诊断有支持，编辑 Oracle、运行时兼容性和下游语义仍为 UNKNOWN。完整 policy 未获接受：第一版缺少执行时的认证输入并发生引用协议失败；第二版保留了 correct_confirmation 与 UNKNOWN domain_state 的矛盾响应。没有改判或删除失败结果。见 [v1 审计](results/native-overload-edit-output-review-audit-20261005-v1.json) 和 [v2 输入上下文审计](results/native-overload-edit-output-review-audit-20261005-v2-input-context.json)。

评估 CLI 现在保存独立复核后的 Task，并把执行时的认证输入与修改后状态分开、使用不同的证据命名空间。只有接受的记录复核才能产生当前输出事实；存在输出端口不能代替未完成的功能 Oracle。

验证 Action 的第一版真实 grounding 完成后，在工具启动前失败：solver 重新导出 pinned Git base，不能接续实际封存的修改后内容。其原始调用 metadata 在未处理异常前未写出，该限制已单独记录：[bootstrap 失败审计](results/native-overload-validation-bootstrap-failure-audit-20261005-v1.json)。未执行验证命令，0 个验证 Action 记录，不能统计为验证通过。

新增**显式接续**入口只允许一致、未陈旧的执行封印，并复制精确公开内容与权限，排除 Git metadata、拒绝外部链接并复验复制期间变化。正式入口的默认 pinned-base 行为保持原样。真实封存输入的[确定性交接对照](results/native-overload-validation-state-transfer-control-20261005-v1.json)通过：默认入口仍拒绝修改后的 checkout，显式入口的封印与实际执行记录一致。该对照为 0 次模型调用，不能当作 Action 功能验收。native 验证第二版已实际完成：**5 次模型调用、1 个真实验证记录、solver 正常结束、0 字节新增 patch**。两个绑定命令分别真实执行、退出码均为 0、未超时；公开目标和非 overload 控制通过，受影响的 type-annotation 模块 **24 项测试通过**，工作区封印保持不变。见 [真实执行审计](results/native-overload-validation-exercise-audit-20261005-v2.json)。

其[独立复核](results/native-overload-validation-independent-review-audit-20261005-v2.json)实际用 **2 次调用**，确认 public-validation-observed、async-target-behavior-correct、overload-suite 和 outcomes-recorded 输出；运行时兼容性、下游语义及完整 target-and-controls Oracle 仍为 UNKNOWN。policy verdict 为 **PASS / correct_refusal**：Agent 正确保留未知、拒绝重复修改和过度确认。领域状态仍为 UNKNOWN，**完整功能验收仍未通过，包未晋升**。这建立了同项目定义演练中的诊断→编辑→只读验证状态传递及拒绝边界，未建立新 Issue 泛化、跨项目迁移或 SWE 效果。

## 新增端口拒绝边界与共同机制核查

两个此前只准备、未执行的编辑端口负例已实际完成：[执行与独立复核审计](results/native-overload-edit-port-controls-audit-20261005-v1.json)。复用真实 grounding 的角色、前提和 Oracle，在精确一致的独立公开 checkout 上只改变输入端口并取消相应连接确认。两场景执行前仅 input:overload-review 为 UNKNOWN，其余准入条件为 PASS。

q1 缺输入，实际用 2 次模型调用，刷新指导后拒绝修改；q2 的输出为 post-edit/unvalidated，实际用 1 次调用直接拒绝修改。两者 solver 正常结束、补丁均为 0 字节、编辑 Action 记录均为 0，内容与权限封印保持一致。独立上下文复核各用 1 次调用，两者 policy 都为 PASS/correct_refusal，领域状态都为 CONTRADICTED：原缺陷仍在，正确拒绝没有修复问题。这补上端口拒绝边界，未完成编辑正例全部保留义务、整个功能 suite、新问题泛化或 SWE 验收。supervisor 已结束，历史作者原 PID/start ticks 恢复并独立核实为运行状态；全部模型请求继续串行。

[共同机制核查](cross-project-mechanism-review-20261005.md)从完整 9356 条已存储记录的 as-of 标题定位开发线索，再读取报告、修复关系及实际 diff。Pylint #8120 补上 async 进入/退出回调，Ruff #5124 补上 AsyncWith 分类分支，值得进一步资格复现与归纳。Pylint #1126 修复作用域映射，Ruff #4047 修复文档参数集合合并，不能仅凭 async/keyword-only 症状混入同一机制。

两项 2023 年修复不能进入 2021 年训练截止之前的 query/catalog。Ruff 还缺合格 Rust 因果验证 harness 与完整隔离运行环境。没有生成或确认新跨项目 Pattern，没有执行新两父组合，也没有新训练 checkpoint。

v10 固定审阅快照包含 9 个 Pylint 来源、9 个通过原生结构/来源验证的包和 27 个 Action 定义；完成来源的实际 authoring 调用为 21。全为 definition_only_not_executed、没有 Pattern、没有正式 KB 准入；之后仍在抽取的结果不计入该固定快照。见 [证据审计](results/cross-project-mechanism-evidence-audit-20261005-v1.json)。

## 历史证据资格修复和时间线完整性纠正

Pylint #8120 已完成新的独立[因果资格复验](results/pylint-8120-causal-requalification-20261005-v7.json)，旧失败版本未改写。历史 requirements_test_min.txt 固定 astroid==2.13.3 和 pytest~=7.2；旧环境的 astroid 2.15.8 超过项目上界，pytest 8.4.2 也不满足测试范围。新环境使用固定 Python 3.10.18、astroid 2.13.3、pytest 7.2.1 及记录了 wheel hash 的依赖，三组运行的隔离 runtime hash 完全相同。

| 对照 | 退出码 | redefined_variable_type | regression_newtype_fstring |
| --- | --- | --- | --- |
| 原始 base | 0 | PASS | PASS |
| base 加历史回归测试 | 1 | FAIL | PASS |
| 历史 fixed | 0 | PASS | PASS |

测试选择器保持不变，邻近控制保留，未全局忽略警告。得到 1 个 fail-to-pass 功能测试身份和 2 个 original-base pass-to-pass 身份；这是每组 2 个功能 fixture 的有限范围，不是整项目验证。

[权威关闭证据](results/pylint-8120-authoritative-closure-proof-20261005-v1.json)确认 PR #8123 于 2023-01-28 合并后自动关闭 #8120。公开修复时间继续为 2023-01-28T09:29:29Z；2026 年的复验只作为来源资格证明，不能倒填为历史执行或纳入 2021 年之前的查询。该次复验 0 次模型调用、0 次 solver 修复、0 次正式 SWE 运行；尚未建立跨项目 Pattern 或迁移收益。

核查还发现 #8120 的旧完整时间线缓存缺少原状态快照保存的关闭和改标题事件。新增 state_title_coverage_gaps 将独立的 pre-cutoff 状态/标题事件与严格读取的时间线交叉核对；缺失记录产生明确 metadata gap，缺少整条 Issue 时间线也不再因 manifest 存在而视为完整。已有 PR 提及保持原关系，不补造事件 ID、关闭证明或修复结论；旧页和固定模型输入保持不变。

[全部 9356 条记录的覆盖审计](results/historical-timeline-state-coverage-audit-20261005-v1.json)发现 2542 个 Issue 有这类缺口：Pylint 2088、Pyflakes 54、Ruff 400。Issue 身份普查数量未变，但分页完成与 hash 通过不证明事件完整。旧审计中这类元数据完整性的表述需按新结果限定；这些缺口仍待补采、复核并建立新的输入版本。已有独立因果证明与有限测试资格单独记录，不能由元数据缺口推断修复无效，也不能将缺口当成合格历史经验。

v11 的[独立定义快照](results/pylint-native-definition-snapshot-20261005-v12.json)包含 12 个完成的 Pylint 来源、12 个通过原生结构/来源验证的包、38 个 Action 定义和 26 次完成来源的实际 authoring 调用。均为 definition_only_not_executed；0 个跨项目 Pattern、0 个正式 KB 准入。正在生成的输出和未审阅的包继续保留在服务器，未批量发布。

## 工程检查、数据范围与剩余验收

当前最终实现完整测试 **570 passed、19 skipped**，耗时 126.37 秒；新增时间线检查及相关定向测试 **20 passed**。此前接续及相关定向测试的 **52 passed、5 skipped** 记录保留。修改文件的 Ruff E4/E7/E9/F 与 git diff --check 通过。跳过项不计为通过，工程检查不能替代泛化、修复效果或 SWE 验收。

历史范围保持 Pylint 5273、Pyflakes 501、Ruff 3582，共 **9356 个 Issue**。主截止 T=2024-01-01T00:00:00Z，训练截止 τ=2021-01-01T00:00:00Z，均为严格时间边界。已暴露的 Pylint #10034 继续排除正式评价。

Pylint 资格流程已处理 1160 个规范化候选，得到 78 个 verified 来源，资格范围是修改测试，不能描述为整项目完整验证。针对全体合格来源的抽取不设预定族或任意 top-N。结构合法的包继续属于 definition_only_not_executed。未审阅的 pyflakes-mechanism-history-v5、Pylint authoring 输出与全部失败版本保留，未批量提交或自动纳入正式 KB。

剩余工作是：完成原生编辑/验证的真实正反例；核验 Pyflakes/Pylint/Ruff 的共同机制与互补 Action，并执行真实两父组合；获得有效适用性和效果监督后训练、校准；最后联合冻结 KB、模型、题目、预算和验收协议，执行正式 SWE 配对及模块/Ranker 消融。目标仍未完成。


## 全量已知时间线缺口恢复与实际定义验收（后续 v12）

[独立恢复审计](results/historical-timeline-coverage-recovery-audit-20261005-v1.json)已完成。原始 824 个文件的哈希封印与原始内容核对通过，三项目 Issue 身份总数仍为 9356。新数据版本没有改写原始普查、旧时间线页或此前冻结模型输入。

| 项目 | 已知缺口目标 Issue | 第一版补采后仍缺 | 显式状态视图补采后仍缺 |
| --- | --- | --- | --- |
| Pyflakes | 54 | 39 | 0 |
| Ruff | 400 | 198 | 0 |
| Pylint | 2088 | 1143 | 0 |
| 合计 | 2542 | 1380 | 0 |

第一版确实完成了全部目标，但 unfiltered API 响应仍遗漏部分已知事件，不能因此宣称事件完整。独立小批量探针能观察到真实事件 ID，第二版针对残留缺口加入显式 CLOSED_EVENT／REOPENED_EVENT／RENAMED_TITLE_EVENT 视图，并保持完整分页。两版结果都保留；第一版 53 次 API 请求，第二版 102 次，独立视图探针 2 次。全部为 GitHub 元数据请求，0 次恢复模型调用、0 次正式 SWE 运行。

独立审计逐条核对人口身份、原始文件、保留的旧事件 ID、新事件及严格截止时间。Pylint #8120 的实际关闭事件与合格修复 PR #8123 再次吻合。仍有 3 个 Pylint Issue 带权限受限事件元数据，不能宣称所有历史字段完整。另有 43 个未补采旧记录中的 PR resolution 字段发生在截止之后；恢复版本的默认读取现在强制严格投影，学习输入中这些未来字段全部隐藏。此修复没有回写旧冻结输入或模型结果。

新 corpus 路径为 tmp/temporal-history-census-v3-explicit-state-20261005。它需要新的、可追踪的 evidence review 才能服务新的学习输入，尚未自动纳入正式 KB，也不改写原有 78 个来源的有限资格范围。

Pylint #8120 的原生抽取第二版完成：2 次模型调用、1 个结构及来源验证通过的 Package、4 个 Action，第一次格式协议失败保留。其输入公开时间仍为 2023-01-28，不能进入 2021 年之前的训练查询。该包没有功能执行或正式 KB 准入。

[固定定义快照 v13](results/pylint-native-definition-snapshot-20261005-v13.json)独立核验 17 个完成来源、17 个包、55 个 Action，完成来源的实际 authoring 调用为 36；全部为 definition_only_not_executed。#3763 和 #4238 共享同一修复，未算独立 Pattern 支持。该快照不含随后仍在生成的输出，未批量发布未审阅候选。

Ruff #5124 从正确的历史 base c811213302f76c255da89d374bd8ab42f3b223e5 开始准备，而非使用旧的 2023 年底通用 build source。base 和 fixed 的 Cargo.lock 完全相同，SHA 为 1ca9ffb06f2bc561a5e009a62c52f9c72f6120b02d718f299d8107dc4fa3f6b7。首次 vendor 下载因历史 LibCST Git 依赖的 GitHub HTTPS 连接超时退出 101，锁文件未改动、0 个 vendor 包。见[失败与准备审计](results/ruff-5124-runtime-preparation-audit-20261005-v1.json)。隔离 Rust harness 与三组因果对照仍未完成，不将这次准备计为历史来源资格或 Skill 验收。

本轮最终代码完整测试为 **583 passed、19 skipped，127.26 秒**；相关定向测试 **36 passed**，Ruff E4/E7/E9/F 与 git diff --check 通过。原有各版本的工程、失败和实验证据保留。工程检查及元数据恢复不建立 Skill 修复收益：M0–M3 仍缺完整真实功能、重写和两父组合验收；M4 没有合格训练 Ranker；M5 未联合冻结；M6 正式 SWE 运行仍为 0。

## 无 artifact 端口的真实执行见证及新的 Pylint 验收准备

独立检查发现一个 M0 的真实接口缺口：#8120 原生候选的四个 Action 使用 evidence predicates，均未声明 artifact 输出端口，但旧记录器与复核器都强制至少一个 PortValue。这使合法的诊断、编辑与验证动作无法留下可复核执行记录。仅生成 ActionContract 或通过包结构检查不能发现这一运行时缺口。

现在有 artifact 端口的记录继续使用 `arex-action-observation-v3`。没有声明 artifact 端口的 Action 使用 v4，显式提交 `outputs=[]`、`observation_ids` 和 `artifact_paths`，至少一个见证必须来自真实 broker 结果或当前文件。v4 保存闭合的 `execution_evidence_refs`，继续核查 Action／包／契约身份、当前工作区内容及权限封印。声明了必需端口的 Action 不得使用该入口绕过输出契约。记录阶段仍不建立语义事实，独立复核才可记录 PASS／FAIL／UNKNOWN；validate 的 PASS 仍要求绑定命令实际在当前封存工作区通过。没有修改候选包来添加虚构端口。

新准备器为 #8120 构建九个公开作用域例子：独立 async 函数／方法及同步对应物、独立类、同一 async／sync 作用域，以及类／模块中的真实类型变更。四类控制分别是历史缺失 hooks、已修好 hooks、hooks 存在但 dispatcher 被控制性破坏，以及执行不可用。初版因拒绝合法封闭符号链接而失败；第二版独立 Git 树核查发现遗漏 `tests/.pylint_primer_tests/.gitkeep`，已保留并拒绝使用。第三版强制保留全部公开文件、比较源码与导出快照封印，并进行真实 namespace-copy 行为校准，审计时仍在运行。

串行模型作业等待实际校准成功，再在历史作者新响应的完成检查点暂停它，核查无 socket／子进程后运行原生诊断及独立上下文复核；watchdog 与 finally 负责恢复历史作者。审计时该作业尚未执行模型请求，不能计入 Action 功能成功。第三版准备成功也只会建立公开测试控制，不能替代模型真实执行和独立效果验收。

新增核心接口与校准测试后，完整工程测试为 **616 passed，19 skipped，105.04 秒**。详见 [协议审计](results/native-effect-only-action-protocol-audit-20261005-v1.json)。没有新增已确认 Pattern、双父组合执行、合格训练 Ranker、KB 晋升或正式 SWE 运行。M0–M6 的整体目标仍未完成。
