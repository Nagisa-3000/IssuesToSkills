# Agent-core 七类 Skill 检索与适用性评测

更新时间：2026-10-02（Asia/Shanghai）

## 评测边界

- 检索库只由 28 条训练 ChangeEpisode 构建；7 条 holdout 未进入 Episode、Action、Workflow、Pattern 归纳或 graph 构建。
- 第一组输入只使用用户表格中的 `table_note`。
- 第二组输入额外使用公开 GitHub Issue 的标题和正文；没有抓取评论、timeline、关联 PR、commit、patch 或测试。
- LLM judge 只判断返回候选能否作为指导，不执行修复，也不把类别命中当成修复正确性。
- `deferred_by_semantic_judge` 和 `rejected_by_semantic_judge` Pattern 可以作为检索审计证据，但在正式 judge 前被门禁排除，不能被选作指导。
- 本轮没有产生成功/失败执行事件，因此没有进行 feedback、merge、retirement 或 catalog 生命周期变更。

## 实现修正

本轮先修正了三个会使结果失真的问题：

1. holdout manifest 主要只有 `table_note`，原查询构造器忽略该字段，导致空查询或仅类别查询；现在 deterministic retrieval 和 LLM router 都使用 `table_note`。
2. `dense_hnsw` arm 原来误走 Hybrid retriever；现在执行真正的 HNSW vector-only search，并有回归测试。
3. MRR 原来只对命中的 case 求平均，漏召回没有计为 0；现在按全部 case 计算。

另外新增：

- 只抓 Issue title/body 的 holdout evaluation-input 生成器；
- training-only retrieval applicability judge；
- deferred/rejected Pattern guided-use 门禁；
- HNSW/Exact top-k parity、同仓 holdout gold 泄漏计数和完整检索参数记录。

## Catalog 与 Pattern 状态

- 28 training episodes；75 grounded Actions；29 instance Workflows；9 Workflow fragments。
- 7 semantic Pattern contracts：5 个 `candidate_pending_holdout`，2 个 `deferred_by_semantic_judge`。
- 221 embeddings；SQLite 与 HNSW 均已构建。
- Action 安全跨仓合并候选仍为 0；当前复用证据主要位于 Workflow skeleton 与语义 Pattern 层。

## Deterministic retrieval

### 一句话 `table_note`，graph expansion = 1 hop

`top_k=8`，`seed_k=40`。

| arm | Recall@8 | MRR | mean first relevant rank | mean latency ms | context token proxy | mean expanded |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sparse/BM25 | 1.000 | 0.821 | 1.57 | 0.58 | 673 | 0 |
| Dense exact | 0.857 | 0.362 | 3.00（命中 case） | 13.73 | 627 | 0 |
| Dense HNSW | 0.857 | 0.362 | 3.00（命中 case） | 18.64 | 627 | 0 |
| Hybrid exact | 1.000 | 0.702 | 2.29 | 15.01 | 701 | 0 |
| Graph exact, 1 hop | 1.000 | 0.810 | 1.86 | 19.66 | 850 | 93.43 |
| Graph HNSW, 1 hop | 1.000 | 0.810 | 1.86 | 26.49 | 850 | 93.43 |

### 1 hop 与 2 hops

同一组 `table_note` 输入：

| graph setting | Recall@8 | MRR | mean expanded | context token proxy | exact latency ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 hop | 1.000 | 0.810 | 93.43 | 850 | 19.66 |
| 2 hops | 1.000 | 0.667 | 156.86 | 874 | 28.04 |

两跳扩展覆盖了大部分 221-node catalog，排序反而变差；后续默认采用一跳，不再把两跳作为 solve-mode 默认值。

### 补充公开 Issue title/body，graph expansion = 1 hop

| arm | Recall@8 | MRR | mean first relevant rank | mean latency ms |
| --- | ---: | ---: | ---: | ---: |
| Sparse/BM25 | 1.000 | 0.690 | 1.71 | 3.18 |
| Dense exact | 0.857 | 0.571 | 2.33（命中 case） | 14.17 |
| Hybrid exact | 1.000 | 0.768 | 2.43 | 17.75 |
| Graph exact, 1 hop | 1.000 | 0.786 | 1.86 | 22.89 |

Issue 正文改善了 dense/hybrid 的语义排序，但给 sparse 引入了噪声。纯 dense 在两组输入中均漏 1/7，因此当前不能单独作为召回通道；Hybrid 或 Sparse+Graph 更稳妥。

### HNSW 与泄漏检查

- Dense、Hybrid、Graph 三组 Exact/HNSW 在 7/7 case 上 top-8 ID 与顺序完全一致。
- 每个 holdout 的同类别 gold node 中，来自 holdout 自身仓库的数量均为 0。
- HNSW 在此小 catalog 上只验证了近似索引一致性，没有表现出延迟优势；Exact 仍是 correctness oracle。

## LLM applicability judge

模型：`openai/gpt-5.6-sol`。正式结果均使用一跳 graph、Exact dense correctness path，并在 judge 前排除 deferred/rejected Pattern。

### 结果

| holdout | judge | selected guidance | rank | confidence | 结论 |
| --- | --- | --- | ---: | ---: | --- |
| Pi #5823 provider/model | reject | — | — | 0.94（table-note run） | 当前可用 Workflow 处理 client/endpoint/request boundary，不覆盖 provider-qualified model lookup；deferred provider Pattern 不允许使用。 |
| Aider #750 API key | reject | — | — | 0.98 | 实际是 shell-specific 环境变量文档问题，不是凭据 precedence/fallback 运行时缺陷。 |
| Hermes #43547 compaction | applicable | `pattern:8105d8c0f3d9ec16` — Repair budget decisions at their policy boundary | 1（完整 Issue）；6（table-note） | 0.94 / 0.78 | Pattern 能把共享 context window、output reservation 和 stricter threshold 归到正确 policy boundary。仍为 `candidate_pending_holdout`，尚未晋级。 |
| Codex #47761 resume/worktree | reject | — | — | 0.99 | 缺失 workspace/worktree identity 与 session eligibility filtering Skill；现有 resume Pattern 处理 state ownership，不处理 session discovery。 |
| Gemini #29308 JSON.parse | reject | — | — | 0.99 | 需要 malformed tool-argument parsing/error-conversion contract；现有 structured Pattern 明确不覆盖 malformed-content sanitization。 |
| Qwen #10859 shell guard | reject | — | — | 0.96 | 需要 command/path policy classification、auditability 和 diagnostics；现有 effect Pattern 是“扩权但保留限制”，因果边界不同。 |
| Pi #9735 premature stream | applicable | `workflow:bca58288062025eb` — recover-recognized-premature-stream-termination | 6 | 0.90 / 0.93 | Workflow 的“窄化地补充 retry classifier + stream-iteration regression”可以迁移，但必须绑定目标 proxy 的稳定错误表示，不能复制 Gemini 的具体错误码。 |

两组输入最终都批准 2/7：一个跨仓 Pattern 和一个跨仓 Workflow；其余 5/7 明确拒绝，不会因为类别或关键词相似而强行使用 Skill。

### 门禁发现

门禁实现前的 smoke run 表明，LLM 可能把 `deferred_by_semantic_judge` provider Pattern 判为当前 holdout 可用。正式 runner 现已在 LLM judge 前排除 deferred/rejected Pattern，并重跑全部 7 case。正式结果中：

- 共排除 12 个进入 top-8 的 deferred Pattern hit；
- 没有 deferred/rejected Pattern 被选中；
- `candidate_pending_holdout` Pattern 仍允许进入 holdout 验证，但不会因此自动晋级。

### API 使用

| input | calls | prompt tokens | completion tokens | total tokens | mean judge time |
| --- | ---: | ---: | ---: | ---: | ---: |
| table-note | 7 | 92,201 | 2,253 | 94,454 | 8.95 s |
| Issue title/body | 7 | 92,934 | 2,921 | 95,855 | 10.09 s |

API key 只通过进程环境变量传入，不在 artifact、manifest 或报告中持久化。

## 当前可得结论

1. **Category retrieval 不是 applicability。** 7/7 类别召回并不意味着 7/7 都有可用 Skill；LLM judge 最终只批准 2/7。
2. **Pattern 有一次真实的跨仓泛化信号。** context budget Pattern 在 Hermes holdout 上得到因果一致的批准，但仍需实际 agent patch 与隐藏 oracle 才能晋级。
3. **Workflow 可以比过度抽象的 Pattern 更有用。** failure/streaming 的统一 Pattern 被语义 judge defer，但一个具体 Workflow 能迁移到另一仓库，同时保留“不复制具体错误码”的约束。
4. **拒绝也是有效结果。** provider lookup、worktree session filtering、malformed JSON、shell guard 与文档问题暴露了当前 catalog 的真实覆盖缺口。
5. **图扩展应受限。** 一跳有帮助，两跳过宽；Pattern 类型优先级和 provisional lifecycle 仍需要在后续排序/serving policy 中继续校准。

## 下一阶段

只对 LLM judge 已批准的两条 holdout 进入 paired agent validation：

1. Hermes #43547：no-skill vs context Pattern-guided。
2. Pi #9735：no-skill vs premature-stream-recovery Workflow-guided。

两条实验都应：

- 使用相同 checkout、相同 issue input、相同模型与时间限制；
- 对 guided arm 只暴露 training-only 检索结果与 judge 批准的 contract；
- 在 agent 完成后才揭示 solution/reference tests；
- 独立评估 correctness、scope precision、maintainability/style、validation quality、tokens 和 wall time；
- 只有执行成功/失败证据产生后，才进入 feedback、revision/merge/quarantine/retirement。

对其余 5 条 holdout 不应强行做 guided arm；它们应记录为 coverage gap，等待新的训练证据或新的 Skill contract。

## 主要 artifact

- `experiments/manifests/agent-core-seven-category-extraction-v2/holdouts-evaluation-input.json`
- `data/skill-extraction/agent-core-seven-category-extraction-v2/catalog-contract-v2-20261001/holdout-retrieval-evaluation-hops1.json`
- `data/skill-extraction/agent-core-seven-category-extraction-v2/catalog-contract-v2-20261001/holdout-retrieval-evaluation.json`
- `data/skill-extraction/agent-core-seven-category-extraction-v2/catalog-contract-v2-20261001/holdout-retrieval-evaluation-enriched.json`
- `data/skill-extraction/agent-core-seven-category-extraction-v2/catalog-contract-v2-20261001/holdout-retrieval-applicability.json`
- `data/skill-extraction/agent-core-seven-category-extraction-v2/catalog-contract-v2-20261001/holdout-retrieval-applicability-enriched.json`

