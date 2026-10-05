**Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-05）**

**尚未全部完成。M0–M3 有代码、接口和工程测试；真实功能与跨项目效果的验收仍不完整。M4 没有合格的训练 Ranker，M5 尚未联合冻结，M6 的正式 SWE 运行数为 0。** 本文依据[当前机器快照 v15](results/pattern-crossbind-ranker-current-status-20261005-v15.json)。旧快照、失败实验和未审阅候选继续保留，源内演练、包准入和正式修复结果分别统计。

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

第四版已在完成成功请求的安全检查点暂停历史作者并启动，执行预算保持 300000 token。快照时仍在运行，尚无终止结果，未记作验证通过。

Ruff #5124 的依赖准备取得实质进展。[精确 Git 依赖恢复](results/ruff-5124-pinned-dependency-recovery-audit-20261005-v3-complete.json)获得原锁定的三个提交；LibCST 从上游取得相同提交，未替换 revision。[离线 vendor 审计](results/ruff-5124-offline-vendor-preparation-audit-20261005-v1.json)核对 310 个原始 registry 包、319 个 vendor 包和 16438 个文件哈希，使用官方 Cargo vendor 归一化，未手工改依赖 manifest。Cargo.lock 与历史 base 源码保持精确一致。

[测试构建预检](results/ruff-5124-host-build-preflight-audit-20261005-v1.json)通过 cargo test --lib --no-run，0 次模型调用、0 个已执行测试。Rust 隔离 harness 及 base／base+regression／fixed 三阶段因果验证仍未完成，尚未抽取或准入新的 Ruff Skill，未确认跨项目 Pattern 或运行两父组合。

本次源码还修复了公共 Git archive 的链接身份：保留 data_filter 的安全检查，重新检查原始目标的包含关系，并保留 contained symlink 的原始 target 文本及末尾分隔符。四项回归覆盖真实 Git tree 身份；此前错误导出和失败准备没有删除。

当前完整工程检查 **636 passed、19 skipped**，耗时 97.86 秒。专项 **40 passed、5 skipped**；修改文件的 Ruff E4/E7/E9/F 与 git diff --check 通过。跳过项不计为通过，工程检查不替代原生功能、迁移或正式 SWE 验收。

历史人口保持 Pylint 5273、Pyflakes 501、Ruff 3582，共 9356 个 Issue。主截止 T=2024-01-01T00:00:00Z，训练截止 τ=2021-01-01T00:00:00Z，均严格排除截止时刻及以后信息；Pylint #10034 继续排除正式评价。已知时间线缺口恢复到独立版本，旧输入与旧结果不改写；仍保留三项权限受限元数据。Pylint 的 78 个合格来源是 changed-test-only 范围。完整人口存档并不等于三项目所有历史经验完成资格复验或功能准入。

后续仍按依赖推进：完成原生包正反例和当前验证；完成 Ruff 的隔离因果对照；由独立真实来源归纳机制并执行单 Workflow 重写、互补两父组合；获得有效适用性及效果监督后训练和校准；联合冻结 M5；最后执行正式 SWE、模块消融与同候选池排序比较。整体目标保持未完成。
