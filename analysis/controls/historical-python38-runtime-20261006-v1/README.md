# Python 3.8 历史兼容运行时

原始 Pyflakes #483/#507 输入明确涉及 Python 3.8，#507 使用 positional-only 语法。本版在当前时间构建 CPython 3.8.20、安装 pytest 6.2.5；已在特权 broker 的 copied namespace 中实际执行语法、Constant AST、SSL、ctypes 和 /opt/venv 检查，退出码 0。

解释器源码来自 python.org HTTPS，保存测量 SHA256；没有独立认证旧 checksum。运行时不回填历史日期，也不宣称该补丁版本在原 query 时已经发布。这里只是执行环境准备，没有历史修复或 Skill 泛化验收。
