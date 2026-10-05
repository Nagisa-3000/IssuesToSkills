本目录保存完整 98 包机制发现、22 组独立评审、两组证据纠正与补充评审、闭合引用策略更正及最终合并结果。20 组机制接受不等于生成或功能验证了 20 个 Skill。新包、功能验收和正式 SWE 运行均为 0。

original-review 的一个 #5406 原始源包配错到了同 Issue 的后来修复，Ruff 原始 diff 当时未取到。受影响两组的原结论由 corrected-scoped-review 的实际模型响应替换。该响应对两次同 Issue 修复使用了精确来源 packet ID，原先仅允许 Issue evidence ID 的主机验证报错保留在 failure.json；adjudication 中明确记录了闭合引用策略更正，允许已提供的来源 packet ID，不引入任意来源或新证据。

完整纠正后的证据输入可从 original-review/review-input.json 复制，使用 corrected-scoped-review/review-input.json 中 native_historical_evidence 的 7 个同名 packet 覆盖，其他字段保持原值；其 hash 见 identity-correction.json。原始和补充实际请求的完整输入、系统、schema、输入/响应 hash 与实际调用收据均保存。未提交重复的大型请求日志，服务器 ignored tmp 中的原始 transcripts 保留。

全部 57 个参与来源已重新匹配精确 fix、revision 和 available_at。跨机制分组的重叠不自动合并历史因果来源；#5406 两次修复仍只算一个来源组件。full_corpus_causal_review_complete 仍为 false。完整发现生成上下文最晚时间为 2023-06-18T14:43:15Z，不允许用于 pre-2021 的机制选择、训练或开发。
