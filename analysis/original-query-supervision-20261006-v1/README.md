原始 Issue 监督入口已统一接入；完整 M0–M6 目标仍未完成。

新的 registry 绑定原始 queries 文件、全体登记目标、明确的训练/主截点，以及逐题运行环境、native 修复验证、原始快照控制和独立审查。原始登记没有 cutoff 字段时必须由 registry 明确给出，不能将最新主截点语料回填到早期 query。每次加载重算来源和控制资格，并核对精确文件 hash；旧的 PASS 本身不授予执行或效用标签资格。

宿主准入检查读取私有资格材料，solver 的公共输入与挂载不包含这些材料。solver 与 evaluator 使用同一逐题运行环境。solver 隔离 preflight 后、任何模型请求前核对已冻结的 runtime hash；提交评测在 solver 终止后再次加载私有来源、恢复独立测试并核对控制与独立审查。原始路径不会自动回退到历史修复父版本评测器。

真实登记的分母为 21，原始公开输入为 18。预检 v2 中 #470 合格，7 题旧控制缺少完整来源封存字段，9 题控制未通过，#3737 等待独立审查，3 题原始输入不可用。以上待完成状态均不产生效用失败标签。统一 runner 的 query-population.json 与 study-results.json 保留完整登记分母；候选池只针对有原始输入的题目准备。

首轮预检把 #470 绑定到 submission-evaluator 的运行结果目录，而不是原始 replay 的 cohort/phase 来源，因而记录 controls_missing。v2 已校正到原始来源，逐项匹配既有接受审查的输入和三段实际回执，旧 v1 未覆盖。部分早期控制缺少 production_projection 等字段，未在宿主补写为完整 PASS；正在使用当前实现和原有逐题 runtime 重新运行全部 21 题的控制，仍保留旧记录、#470 审查和 #3737 明确的 metadata 投影记录。

候选准备 v1 在实际 300 秒执行期限到达后终止，已保留终态与最后进度；这不是 solver 或候选的功能失败。v2 仅延长本地准备的执行期限并使用新目录，未因工具观察超时重启进程。候选准备使用本地冻结 embedding、既有 native 包和逐题时间/因果排除，不调用 LLM、不生成修复标签。准备产物与 live-jobs-snapshot.json 的状态不代表 M5 联合冻结。

工程验证为 969 passed、20 skipped，7 个本轮代码/测试文件 lint/format 通过，tested-source-hashes.json 封存最终测试源。合成单元夹具明确使用 synthetic-unit 标记，不能当作真实训练观察、功能修复或模型调用。源代码测试覆盖分母遗漏/重复、输入/别名/簇/修复漂移、私有材料进入 actor 挂载、资格缺口、精确来源变化、旧候选池混用、逐题路由和首请求前的 runtime 拒绝。

CLI 新增：
- experiments/prepare_original_supervision_registry.py，使用 --queries、--query-register、--bindings、--training-cutoff、--main-cutoff 和 --output 封存资格。
- experiments/run_historical_ranker_supervision.py 使用 --original-supervision-registry，原始模式不接受共享 --dependency-root 或旧 --verifications。
- --prepare-only 仅冻结候选；--prepared-dir 与 --candidate-kind plan 用于执行同一候选池。registry 或评测路径变化需要显式新版本。
- 实际外部模型调用必须 --workers 1；缺资格的题目返回 qualification_pending_unrun、live_calls=0、label=null。

本轮新增实际 solver 运行、效用标签和正式 SWE 运行均为 0。#470 既有小实验仍只支持候选曝光后回退的分配策略结果：B0/E1 均通过限定独立测试，E1 在生产修改前放弃历史 guidance，tokens 增加 20.54%，没有证明 Workflow、Pattern、CrossBind 或训练 Ranker 的收益。M4 仍缺有用的时间隔离监督、合格 LLM Ranker 训练及开发校准，M5/M6 仍待完成。
