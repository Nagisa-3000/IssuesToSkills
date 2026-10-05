# 历史 Python 3.7 兼容运行时

使用 Pyflakes 2.0–2.2 公开发行包声明的 Python 3.7 支持，处理已观察的 Python 3.12 Constant AST 不兼容。实际构建 CPython 3.7.17、安装 pytest 6.2.5，并在无网络的 namespace-copy 沙箱中验证 Python/pytest 版本、Num AST 和 /opt/venv 前缀。运行时按当前执行时间记录，不声称在原始 Issue 输入时已发布该补丁版本。

官方 HTTPS 下载与实测源码 hash 已记录；实测 hash 不等于独立认证历史校验和。保留首次使用非特权执行器的预检失败，以及 uv venv 写 version_info 而复制器要求 version 字段的失败；第二版使用 CPython 标准 venv 格式通过。这里没有重放修复效用结果。#507 的公开 Python 3.8 语法需要相应运行时，不能用 Python 3.7 结果替代。
