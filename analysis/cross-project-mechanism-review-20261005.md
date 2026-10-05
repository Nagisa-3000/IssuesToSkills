# 跨项目机制核查与原生端口验收（2026-10-05）

**尚未确认新的跨项目 Pattern、完成两父 Workflow 组合或证明修复收益。** 本轮建立两个真实端口拒绝边界，并核对值得继续验证的源代码机制。机器证据见 [机制审计](results/cross-project-mechanism-evidence-audit-20261005-v1.json)及[端口审计](results/native-overload-edit-port-controls-audit-20261005-v1.json)。

本轮对三项目完整的已存储历史人口 9356 条记录读取 as-of 标题，再按开发线索检查相关公开报告、修复关系和实际 commit diff。标题线索只用于定位。这不是全体 Issue 的语义处置完成，也不用于正式 benchmark 选题。

| 来源 | 实际修复机制 | 本轮判定与限制 |
| --- | --- | --- |
| Pyflakes #401、#470 | 分别补充 async 函数作用域分类、overload 函数类别，保持同步语义和 runtime gating | 已有同项目两来源 local_template，尚未完成全部功能验收 |
| [Pylint #8120](https://github.com/pylint-dev/pylint/issues/8120) / [PR #8123](https://github.com/pylint-dev/pylint/pull/8123) | 将 async 的 visit/leave 回调接到已有作用域回调，恢复状态边界 | 有机制对应可能，既有资格尝试未获接受，尚未原生归纳及迁移验收；关联 #1279 不能算第二个独立支持 |
| [Ruff #5124](https://github.com/astral-sh/ruff/issues/5124) / [PR #5125](https://github.com/astral-sh/ruff/pull/5125) | AsyncWith 接入已有 With 分支，保持 target/body 语义，同时修改当前 Rust API 和 regression fixtures | 值得进一步核验；Python 的具体 Action 端口不能直接变成 Rust 对象绑定 |
| [Pylint #1126](https://github.com/pylint-dev/pylint/issues/1126) | 将 accessed 属性堆栈改成以真实 class scope 为键的映射 | async 出现在复现中，实际修复并非 async 分类扩展，不能据此并入同机制 |
| [Ruff #4047](https://github.com/astral-sh/ruff/issues/4047) / [PR #4067](https://github.com/astral-sh/ruff/pull/4067) | 汇总 Args、Keyword Args 等文档段的名字集合，再统一判断 missing_args | 与 Pylint #3092 的签名类型证据收集责任不同，不能凭 keyword-only 症状直接交换 Action；另行研究参数文档机制 |

Pylint #8120 已有真实因果尝试，而不是完全没有执行：目标 test_functional[redefined_variable_type] 出现 fail-to-pass；但邻近 regression_newtype_fstring 在原 base 和历史 fixed 都失败，出现由 is_standard_module 的 DeprecationWarning 引发的 astroid-error。原 base、加 regression 的 base 和 fixed 三次退出码均为 1，artifact/issue relationship 标志也未获确认，因此 verified_resolution=false。现有结果、控制题和 warning 策略均保留。下一步应根据 pinned 源码声明校准依赖与来源证明，不能删除失败控制或全局隐藏 warning 来得到资格 PASS。

共同抽象目前是有待核验的假设：异步节点已经进入分析，但同步语义分类或分派遗漏等价变体。迁移仍须证明当前 async 变体能复用对应的普通节点语义、责任边界正确、必要进入/退出动作完整，以及相邻行为保留。类型名或诊断词相似不能建立这些事实。

时间边界保持不变：T=2024-01-01T00:00:00Z，训练截止 τ=2021-01-01T00:00:00Z。Pylint #8120 的实际修复在 2023-01-28、Ruff #5124 在 2023-06-15 公开。它们均不能成为 2021 年之前训练 query 的经验，也不能进入冻在 2021 年的开发目录。较早出现的同 bug 报告不把后来修复的知识回填到过去。

当前历史因果 verifier 仍使用 pytest/JUnit 协议，运行时复制以 Python 及声明的可执行文件为主。传入 cargo 命令后仍附加 pytest 的 JUnit 参数，不构成 Rust harness；工具链出现在服务器上，也不等于存在合格隔离 Rust 环境。需要独立支持 Rust test identities、fixture/snapshot 断言、锁定依赖、运行时封存和三阶段因果对照，之后再进行 native authoring、归纳和组合。当前报告不把未执行的对照填为 PASS。

端口负例隔离了其他条件：只有 input:overload-review 未获满足，角色、前提和已绑定 Oracle 均通过。q1 缺少输入，2 次 solver 调用，刷新指导后拒绝修改；q2 为 post-edit/unvalidated，1 次调用直接拒绝修改。独立上下文复核各 1 次调用，两者均为 policy PASS/correct_refusal，领域状态为 CONTRADICTED。两 checkout 内容和权限一致、均无补丁和编辑记录。它们是同项目、受控输入的定义演练；正确拒绝没有建立修复成功、跨项目泛化或完整功能验收。

下一步验收仍需：编辑/验证正例的全部保留义务；两项候选的真实源资格；有支持的 Pattern 和可绑定互补 Action；真实重写与两父组合；有效适用性及执行效果监督。原冻结池的无关标签和平局结果保持原样，不能用新候选改写旧实验。其后才能训练与校准、联合冻结正式协议，执行配对 SWE 和消融。


## #8120 的后续资格复验与历史时间线缺口

上述 v1 的失败记录继续保留。后续[资格复验 v7](results/pylint-8120-causal-requalification-20261005-v7.json)使用符合历史测试声明的固定依赖，原始 base、base 加回归断言、历史 fixed 的退出码分别为 0、1、0。目标 fixture 从 FAIL 到 PASS，regression_newtype_fstring 邻近控制在三组中均 PASS；没有删除邻近控制或全局抑制警告。

[GitHub 关闭证明](results/pylint-8120-authoritative-closure-proof-20261005-v1.json)独立确认 PR #8123 为 #8120 的实际 closer，修复时间为 2023-01-28T09:29:29Z。#1279 继续保守地属于同一 bug cluster，不能额外增加独立支持。#8120 现已通过限定范围的历史来源资格，尚未证明跨项目机制归纳、当前 Action 绑定或 Skill 迁移成功；它仍不可用于 2021 年以前的训练/开发库。Ruff #5124 的 Rust 因果验证仍未完成。

这次核查发现，#8120 的完整时间线存档遗漏了旧状态快照保留的关闭和改标题事件。[全历史覆盖审计](results/historical-timeline-state-coverage-audit-20261005-v1.json)共发现 2542 个有已知状态/标题事件缺口的 Issue。新的严格读取会标记缺口，保留原存档和输入版本；分页完成及存档 hash 只能证明已存内容，不能独立证明时间线完整。尚未补采这些缺口，不据此扩增 source、Pattern 或正式 KB 的统计。


## 时间线恢复和原生来源定义的后续状态

全部 2542 个已知状态／标题事件缺口已恢复到独立版本，见[恢复审计](results/historical-timeline-coverage-recovery-audit-20261005-v1.json)。全体 9356 个 Issue 的身份、824 个原始文件封印均通过独立复核；旧存档和此前模型输入保持原版本。剩余 3 个 Pylint Issue 的权限受限元数据仍明确保留，不能等同于所有历史事件字段完整。

Pylint #8120 已产出经过独立结构和来源验证的原生 Workflow 包，含 4 个 Action、2 次真实 authoring 调用，仍为 definition_only_not_executed。它尚未与 Pyflakes 或 Ruff 形成可接受的跨项目 Pattern，也没有组成真实两父计划。17 来源／55 Action 的固定[定义快照](results/pylint-native-definition-snapshot-20261005-v13.json)只统计完成、独立验证的定义，不增加功能准入数。

Ruff #5124 首次锁定依赖准备使用精确历史 base，并确认 base/fixed 的 Cargo.lock 相同；GitHub HTTPS 获取历史 LibCST 依赖超时，cargo 退出 101，0 个 vendor 包，失败版本保留。其[准备审计](results/ruff-5124-runtime-preparation-audit-20261005-v1.json)仍明确 historical_artifact_verified=false；需要继续完成 Rust 隔离 harness 和三阶段复现。
