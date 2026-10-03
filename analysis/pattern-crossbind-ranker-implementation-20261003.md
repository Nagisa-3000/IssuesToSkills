# Pattern、CrossBind、Ranker 实现与验收

日期：2026-10-03。实现基线：`1fadfb7fd4c6273c1542e6930aa89cf943ce63f6`。
对照 [模块设计](pattern-crossbind-ranker-design-20261003.md)及其机器路线图逐项审计。
本次交付原生 v4 包、当前绑定与重写、受约束 CrossBind、两阶段排序、时间隔离训练工具和独立修复 runner。
**完成实现和合成验证；未完成完整历史采集、真实监督训练和正式 SWE 效果实验。**

## Action 的输入输出和复用边界

这里的 ActionContract 是本项目的内部契约，不是所有 Agent Skills 的统一标准。
`inputs`、`outputs` 都是必有字段，但可以是空数组；没有产物端口的动作仍必须声明可观察的 `effects`。
例如验证动作输出“目标行为得到验证”的状态，而不必虚构一个文件产物。
每个 Action 还必须有操作语义、owner、前置条件、保留行为、公开 oracle、来源和证据。

Port 的字段为 `name, semantic_role, artifact_kind, language, scope, phase, state, optional`。
连接的两个端口必须在六个语义维度上相容，再由当前证据确认实际含义与接口。
字符串相同只产生候选连接；自然语言语义不由这个检查自动证明。
已知失败拒绝，未知条件只允许探查。

| 可复用的操作语义 | 输入/前提 | 输出/效果 | 每次重新确定的对象 |
| --- | --- | --- | --- |
| 判定某个使用点的类型专用上下文 | 当前 AST、scope、分析阶段 | 带范围和来源的上下文事实 | 当前解析器和 AST API |
| 定位实际负责诊断的入口 | 当前触发路径和源码证据 | owner 与真实接口绑定 | 文件、符号、调用关系 |
| 在 owner 处收窄 guard | 已确认的上下文事实和行为边界 | 目标诊断改变，正常行为保留 | 项目专用判断逻辑 |
| 建立相邻行为验证 | 公开复现和必须保留的行为 | 公开测试观察与 exit code | 测试命令、fixture、断言 |
| 转换或补齐某种分析事实 | 明确的源状态和所需目标状态 | 可供下一动作使用的状态 | 有历史证据支持的 Bridge 实现 |

表中后四类是可研究的复用边界，不能理解为已经拥有完整验证过的通用 Action 库。
提交的合成包只有上下文判定、窄 guard 和相邻验证的两个 realization、六个 Action。
Python 和 Rust 可以共享机制/职责描述；Rust 的具体事实对象不能直接绑定为 Python 对象。
已绑定命令也只来自当前公开 issue、源码或测试。Historical Oracle 保留在原包中，
CurrentOracle 按 action/source-oracle 身份存于 TaskContext；缺少当前绑定或语义检查就不能授权修改。
源码 hash 变化会清除依赖旧证据的事实、绑定、端口和 oracle。

因此目前具备的是**有边界的复用与拒绝能力**。跨时间、跨项目、跨 API 的泛化强度尚无真实任务结果。
建议首先复用具体机制下的动作族，而非只有 analyze/implement/test 的泛化文本步骤。

## 设计要求与代码对应

| 设计要求 | 实现 | 本次证据/限制 |
| --- | --- | --- |
| 原生包是权威，JSON 只是投影 | pattern_contracts、direct_skill_extraction、skill_packages | v4 文件发布、完整性/拷贝验证；原 v3 测试通过 |
| 多来源 Pattern 与独立支持 | PatternContract.validate_support、extract_native_pattern | 重复 issue/fix/cluster/copy 支持拒绝；角色/effect/source 闭包 |
| 按证据归纳机制 | native-extract、native-pattern、抽取 metaskill 的 v4 协议 | 可以调用原生作者接口或 defer；本次仅离线作者协议回放 |
| Action 端口、状态与 current owner | action_contracts、task_context | 具体语言、scope、phase、state；真实 Python 符号/接口检查 |
| Pattern 重写与不变量 | workflow_rewriter | required effects、替代、已满足/不适用省略、可选分支与当前偏序 |
| 语义 cut/splice 与替换 | crossbind | 联合前提闭包、两个父来源、substitute、边界状态、sourced Bridge |
| 冲突及验证/清理闭包 | plan_validation | 真实 alias 对齐、读写顺序、cycle、cleanup、validate、父不变量 |
| 三态授权与当前 oracle | plan_validation、guidance_renderer | PASS 只是预期计划相容；UNKNOWN 是 probe_only；绑定过期重新探查 |
| 同级召回与 role gap 补召回 | retrieval、adaptive_guidance | 先限 admissible IDs；关闭无条件 type priority；Pattern 独立召回 |
| 一致的神经编码器 | embeddings、store | 本地 Transformer；模型 inventory/长度/维数一致；在线编码计入模型预算 |
| Workflow 与 Plan 两阶段 Ranker | workflow_ranker | 七个分项证据、ID 和硬门槛检查、顺序扰动、拒绝/abstain |
| 渐进加载和统一预算 | adaptive_budget、guidance_renderer | 默认 300k 模型 token、60 调用、120 工具、30 分钟、6k 历史 token、两根包 |
| 每个 query 的时间候选库 | temporal_ranker_data、build_temporal_workflow_ranker_dataset | t_q 前来源、自身/fix/cluster/alias/copy 隔离，开发库冻结 |
| 有依据的监督及 ties | SupervisionLabel、execution_label_from_run、pair_preferences | 审阅不能伪称执行；结果标签需已结束的独立验收和候选使用记录 |
| 真实训练和重载 | ranker_training、train_workflow_ranker | 本地 Transformer＋排序/适用性头；可选 backbone/LoRA；开发拒绝校准 |
| 固定 solver、隐藏答案隔离 | adaptive_runner、sandbox_tool、原 runner 的 --adaptive-spec | 同一 broker loop；Linux namespace/chroot、网络隔离；验收最后读私有材料 |
| E0–E3 和共享池比较 | eval_pattern_crossbind_ranker | 有共享当前观察/计划池的 prompted/trained 两分支 CLI 集成验证 |
| 独立分母、配对与成本 | experiment_metrics | failures 保留、issue/cluster 计数、cluster bootstrap、nDCG、预算原始记录 |
| 正式数据/模型/预算冻结 | evaluator 配置 hash 和只读 KB | 已实现工具；未完成全历史总体和正式题目冻结 |
| 正式泛化与模块收益 | v2/M6 实验仍待执行 | 当前没有真实 SWE 成功率、召回准确率或回归损害结论 |

历史包不可变；TaskWorkflowPlan 只属于当前运行，不回写正式知识库。
临时 DAG 表示条件性预计效果；执行观察和独立验收另存，不能把计划 PASS 当作修复成功。

## 可复现的小实验

安装开发与本地训练依赖后，在 Linux/WSL 仓库目录运行：

```bash
python -m pip install -e '.[dev,ranker]'
python -m pytest -q
python experiments/run_adaptive_contract_smoke.py --output-dir /tmp/arex-adaptive-smoke-new
```

输出目录必须是新的版本目录，避免覆盖包和 checkpoint。
Linux 必须支持 user/mount/PID/network namespaces；runner 在缺少隔离能力时拒绝运行。
正式项目的依赖先准备在隔离的 virtualenv，通过 `--dependency-root` 只读挂载；solver 工具不使用宿主凭据或网络安装。

本次完整测试 **198 passed / 13.35 秒**。Ruff 的 E4/E7/E9/F 检查通过。
[实测记录](results/adaptive-contract-synthetic-smoke-20261003.json)和
[自包含合成包](../tests/fixtures/adaptive-v4/type-context-pattern/SKILL.md)已提交，可拷贝后运行其中的 verifier。

| 小实验观察 | 实测 |
| --- | --- |
| 原生包 | 2 Workflow、6 Action、1 Pattern；18 个包文件；拷贝完整性 PASS |
| 两来源 CrossBind | PASS，保留两个父 Workflow；没有声称结构验证等于行为成功 |
| E0 / E1 / E2 | 都能召回、生成并选取当前计划 |
| E2 历史指导用量 | 2,726 个 cl100k_base token，默认上限 6,000 |
| E3 | 正确 abstain；微型训练结果未达到接受要求，拒绝后不复活邻居 |
| 真正的本地参数训练 | 2 training queries、1 development query、2 pairs；训练并重载 checkpoint |
| 三轮训练 loss | 1.6932 → 1.6696 → 1.6502 |
| 隔离 solver 的公开复现 | 修复前 exit 1，修复后 exit 0 |
| solver 停止后的独立验收 | true；原始 checkout 未改变 |
| live LLM / 正式 SWE 调用 | 0 / 0 |

该结果使用合成历史、合成审阅标签、离线排序/修复请求回放和随机初始化的微型 Transformer。
修复内容预写在回放请求中；没有证明模型自主找到补丁，也不能估计任何模块对修复率的因果收益。
合成包位于 tests/fixtures，不准入正式历史库；eval 定义保持 not_executed。

## 工具使用

原生发布/抽取采用 `<name>/SKILL.md` 与 references/evals/scripts 自包含目录。
`native-publish` 接收外部作者的 FILE bundle；`native-extract` 接收 source records 与历史证据，
使用已配置 provider 直接作者文件。`native-pattern` 从两个或更多合格包归纳或 defer。
正文不由宿主模板从 candidate JSON 生成。

```bash
python -m arex_skill_graph.cli native-publish \
  --cutoff 2024-01-01T00:00:00Z --sources sources.json \
  --response authored-bundle.txt --output native-packages-v1
python -m arex_skill_graph.cli native-index \
  --cutoff 2024-01-01T00:00:00Z \
  --references native-packages-v1/extraction-inventory-v4.json \
  --db catalog-v4.sqlite --embedding-model /path/to/pinned-local-model
python -m arex_skill_graph.cli adaptive-plan \
  --cutoff 2024-01-01T00:00:00Z \
  --references native-packages-v1/extraction-inventory-v4.json \
  --db catalog-v4.sqlite --embedding-model /path/to/pinned-local-model \
  --task-context public-task.json --arm E2 --ground-with-model \
  --model configured-model --base-url https://provider.example/v1 \
  --output task-plan-v1.json
```

建库和查询必须用相同的已冻结 embedding；不传 embedding-model 时显式使用旧 feature-hash 基线。
provider 凭据只从指定的运行时环境变量读取，不写入包、命令、报告或 checkpoint。
以上域名和路径是使用格式示例。

历史 query 文件的每项包含 `task, bug_cluster_id, fix_id` 及可选 aliases/copied_from/exposed；
`task` 是仅公开信息的 TaskContext。标签使用 evidence_review 或经过独立执行的 execution；
不能把没有运行的候选标成修复失败。

```bash
python experiments/build_temporal_workflow_ranker_dataset.py \
  --queries historical-public-queries.json --references historical-references.json \
  --labels verified-labels.json --training-cutoff <tau-before-T> \
  --main-cutoff 2024-01-01T00:00:00Z --output ranker-dataset-v1.json
python experiments/train_workflow_ranker.py \
  --dataset ranker-dataset-v1.json --model /path/to/pinned-local-model \
  --output ranker-checkpoint-v1
python experiments/eval_pattern_crossbind_ranker.py \
  --tasks public-tasks-with-evaluator-locators.json --references frozen-references.json \
  --db catalog-v4.sqlite --cutoff 2024-01-01T00:00:00Z \
  --mode solver --arm E2 --model configured-model \
  --base-url https://provider.example/v1 --output e2-results-v1.json
```

固定共享池格式为 `{task_id: {task: <TaskContext>, plans: [<TaskWorkflowPlan>]}}`。
`--mode shared-pool --pool ... --checkpoint ...` 分别执行 prompted/trained 排序和独立 solver 分支。
离线协议回放支持数组，或 `{task_id: {arm: [responses]}}`，避免两个分支响应数不同导致串用。
`--ranking-labels` 在排序和 solver 结束后读取，用于 nDCG；私有 evaluator 也直到 solver 停止才读。
原 `run_cross_project_holdout_agent_eval.py --adaptive-spec ...` 可转接这个新 runner；旧路径只作兼容。

## 尚未达成的实验验收

| 阶段 | 状态 |
| --- | --- |
| M0–M3 | 实现并通过契约/合成集成验收；语义结论仍依赖有证据的审阅与实际 probe |
| M4 | 时间数据、真实训练和拒绝校准工具可用；只有合成训练，缺真实历史监督与正式 checkpoint |
| M5 | 未完成；全历史总体、合格 SWE 题并集、模型/超参/阈值/预算等尚未冻结 |
| M6 | 未执行正式修复；共享池仅做协议集成验证 |

继续保持 Pylint、Pyflakes、Ruff **2024-01-01T00:00:00Z 之前的全部历史普查范围**，
不能将该范围换成两条 fixture 或任意 top-N 历史。
当前没有经完成性审计的正式 N，也不能以旧的 300 次资源算例代表新模块实验总量。

训练首版 pairwise 监督比较独立验收通过频率或有证据的适用等级，保留 ties/replicates/采样概率。
成本与回归记录已保存；完整的损害/成本效用权重和拒绝政策仍需真实历史开发数据校准并冻结。
LoRA 代码提供显式 capability 错误，本次未安装 peft、未执行 LoRA；不声称该分支已实测。
正式实验还需基于公开输入预定泛化分层、独立覆盖/适用标签及各 benchmark 的官方验收协议。
模型预训练是否见过公开题不可由时间目录排除，应按 v2 的限制报告。
