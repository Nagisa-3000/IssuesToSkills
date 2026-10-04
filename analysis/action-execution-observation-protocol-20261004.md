# Action 执行观察协议（开发阶段）

计划中的 output 表示预期产物；它不能充当实际执行后的 PortValue。
新增的 record_action_observation 记录实际工具结果或当前工作区文件，保留模型所声明的输出及其证据，供 solver 停止后的功能评估器检查。

调用必须提供 action_id、当前 context_revision、summary，以及 outputs。每个 output 有 port_name、observation_ids 和 artifact_paths。端口必须来自已经交付的原生 Action，不能在调用中重写角色、阶段或状态。工具结果必须由当前 broker 实际产生；不存在的结果、计划本身、另一条输出声明都不能成为证据。文件须位于公开快照内，并满足现有文件大小限制。记录保存实际 argv、exit code、output、文件哈希和原生契约哈希；失败结果原样保留。

每条记录标为 semantic_validation=unreviewed。该接口不会更新 TaskContext 的 facts、checks 或 port_values，不会证明 Action 前置条件、效果、preserves 或修复成功。独立功能评估仍须检查正例、负例、UNKNOWN 分支、真实改动和实际 Oracle 结果；只有记录到文件不算通过。

solver 提供稳定的 observation_id 和产生结果时的 context_revision。历史输出可能参与前后对照，评估器必须检查引用的阶段和新鲜性。代码修改后，日志中可继续引用此前交付的 Action 定义；这不恢复旧计划的编辑授权。

原生功能开发可显式传入 recordable_actions，但必须使用固定选择模式。所有契约仍须与 ResourcePolicy 内的作者包逐字段一致，根包和读取预算正常计费；结果明确标记 explicit_functional_action_catalog。此入口只授权记录，不能由此宣称正式 KB 准入或正式 SWE 结果。

当前仍待完成：依据具体功能案例独立判断记录的语义，将通过复验的实际端口接入当前 grounding，以及完整 Action 正例、负例和 UNKNOWN 功能评估。M4/M5/M6 不因日志接口上线而完成。
