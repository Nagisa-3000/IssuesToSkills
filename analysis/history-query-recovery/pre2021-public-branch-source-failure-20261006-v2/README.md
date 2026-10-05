# 公共 Git 源恢复的失败与诊断

第一版在扫描前因 TaskContext.root 是字符串而退出，实际归档请求 0；已修正 Path 转换并增加真实 CLI 集成测试。第二版全部 18 个归档请求返回 HTTP 403，21/21 目标保留，0 个 Git query。

对同一 publisher 地址的限长 Range 探查：Python 默认 User-Agent 返回 Cloudflare 1010；项目已有 AREX historical-input-audit 标识返回 206 和 gzip magic。恢复入口现使用这一已有审计标识，并增加完整 gzip 流计数和 hash 测试。探查成功本身不构成公开 head 证明；新版本的真实扫描结果另存，不覆盖本失败记录。基础设施和来源缺口不产生候选失败标签。
