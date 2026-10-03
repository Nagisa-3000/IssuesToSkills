**SWE-bench 常用变种的项目清单与维护活跃度筛选**

调研快照：2026-10-03。核对 10 个公开数据源、18 个 split 入口，得到 1096 个原始仓库身份，GitHub 别名/大小写归一后为 **1087 个项目**。其中 **73 个项目**同时通过本轮维护、历史 PR、近期合并、许可与相似对照门槛。

[完整分基准项目名单与全量筛选表](swebench-project-inventory-20261003.md)；[机器可读筛选结果](data/swebench-projects-20261003/project-selection.json)；[前沿修复 Agent 论文与 benchmark 调研](agent-software-repair-benchmark-survey-20261003.md)。下文推荐池是人工功能组门控后的已核实子集，不是宣称其余项目没有相似替代。

**覆盖范围和项目数量**

Full、Lite、Verified 是当前最常见的论文/榜单对照；另覆盖官方 Multilingual、Multimodal，较新的 Live 系列、Pro、独立 Multi-SWE-bench 和 SWE-rebench。HF 下载量快照保留在 dataset-snapshots.json，仅辅助解释使用范围，不等于独立使用人数或论文引用次数。

| 数据源 / split（固定版本） | 原始任务行数 | 不同任务ID | 发布仓库身份数 | 归一项目数 | 口径 |
| --- | ---: | ---: | ---: | ---: | --- |
| [Full/test](https://huggingface.co/datasets/SWE-bench/SWE-bench/tree/c6fe717fd7a4c3ac1daa4055a4fd082c6a1d28a2) | 2294 | 2294 | 12 | 12 | 原版公开 test |
| [Lite/test](https://huggingface.co/datasets/SWE-bench/SWE-bench_Lite/tree/b0dde1093fe417d83b7184254edf8199c1f0dff5) | 300 | 300 | 12 | 12 | 原版精简 test |
| [Verified/test](https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified/tree/78f471bf655a3137b2e8a75af1501690ec009ec3) | 500 | 500 | 12 | 12 | 人工核验 test |
| [Multilingual/test](https://huggingface.co/datasets/SWE-bench/SWE-bench_Multilingual/tree/846e647b9f33c0b51b739d005d13d85493c9af09) | 300 | 300 | 41 | 41 | 官方 9 语言，与 ByteDance 的 Multi-SWE-bench 不同 |
| [Multimodal/test](https://huggingface.co/datasets/SWE-bench/SWE-bench_Multimodal/tree/4e6662d51c48e475f7f346e4fa09a6f8b31fcaa5) | 480 | 480 | 11 | 11 | 当前 v2；不沿用早期 617/619 的规模 |
| [Multimodal/dev](https://huggingface.co/datasets/SWE-bench/SWE-bench_Multimodal/tree/4e6662d51c48e475f7f346e4fa09a6f8b31fcaa5) | 100 | 100 | 5 | 5 | 开发集，单列 |
| [Live/full](https://huggingface.co/datasets/SWE-bench-Live/SWE-bench-Live/tree/b51a86422e10cfd403beb4773e5a2947953e36ec) | 1888 | 1887 | 223 | 221 | 动态 full；1888行有1个重复ID |
| [Live/test](https://huggingface.co/datasets/SWE-bench-Live/SWE-bench-Live/tree/b51a86422e10cfd403beb4773e5a2947953e36ec) | 1000 | 1000 | 156 | 155 | 公开 test |
| [Live/lite](https://huggingface.co/datasets/SWE-bench-Live/SWE-bench-Live/tree/b51a86422e10cfd403beb4773e5a2947953e36ec) | 300 | 300 | 70 | 70 | 冻结 lite |
| [Live/verified](https://huggingface.co/datasets/SWE-bench-Live/SWE-bench-Live/tree/b51a86422e10cfd403beb4773e5a2947953e36ec) | 500 | 499 | 100 | 100 | 500行有1个重复ID；与原版 Verified 不同 |
| [Live-MultiLang/all-public](https://huggingface.co/datasets/SWE-bench-Live/MultiLang/tree/3638632e8153a10ca422c1022bed79023084b5c9) | 1077 | 1077 | 431 | 429 | 8个语言split合并后的项目集合 |
| [Pro/default](https://huggingface.co/datasets/ScaleAI/SWE-bench_Pro/tree/2d52cb3df914a3fcf80c7f66738b3a88ae37fc50) | 642 | 642 | 11 | 11 | 2026-09-22 V2；公开11项目 |
| [Pro/hard](https://huggingface.co/datasets/ScaleAI/SWE-bench_Pro/tree/2d52cb3df914a3fcf80c7f66738b3a88ae37fc50) | 51 | 51 | 11 | 11 | V2 HARD子集，不新增项目 |
| [Pro/v1](https://huggingface.co/datasets/ScaleAI/SWE-bench_Pro/tree/2d52cb3df914a3fcf80c7f66738b3a88ae37fc50) | 731 | 731 | 11 | 11 | 保留的原始公开版731题；非当前default |
| [Multi-SWE-bench/released-7-languages](https://huggingface.co/datasets/ByteDance-Seed/Multi-SWE-bench/tree/56ff018c04a38e27ada1e9d0a6d5839a51f88f0d) | — | — | 39 | 39 | 39个JSONL文件身份；论文1632题未在本轮重数 |
| [Multi-SWE-bench/kotlin-additional-files](https://huggingface.co/datasets/ByteDance-Seed/Multi-SWE-bench/tree/56ff018c04a38e27ada1e9d0a6d5839a51f88f0d) | — | — | 8 | 8 | 当前包新增文件，单列；不冒充原论文7语言实验 |
| [Multi-SWE-bench/python-additional-files](https://huggingface.co/datasets/ByteDance-Seed/Multi-SWE-bench/tree/56ff018c04a38e27ada1e9d0a6d5839a51f88f0d) | 500 | 500 | 12 | 12 | 当前包另有500行Python文件，单列 |
| [SWE-rebench-leaderboard/test](https://huggingface.co/datasets/nebius/SWE-rebench-leaderboard/tree/34d5a58864acf91613740a09ec5d205228dcfa39) | 860 | 860 | 413 | 411 | HF公开test快照；2026-07 Harbor另有111题，不混入本表 |

各行项目集合有重叠，不能直接相加；同一项目在不同 benchmark 中的题目也不一定相同。Pro 论文整体的41项目包含其他划分，当前公开 HF 仅11项目，本轮不编造私有/未公开项目名单。SWE-rebench 的大规模训练/构建语料与公开 leaderboard 分开；只统计后者。Lite-S 等原版子集不作为新增项目来源，本轮没有单独复算其每项目题量。

**筛选口径**

历史 PR ≥1,000；2026-07-06 至 2026-10-03（查询时已发生的90个日历日）合并 PR ≥20；主分支最新提交也在此窗口；项目公开、未归档/禁用；许可得到 GitHub 标准许可识别或实际文件复核；至少存在另一个公开、许可可接受且主分支近期更新的相似项目。对照项目不必达到主池1,000 PR门槛，也不必属于 benchmark，分别标注。

PR 总量用 GitHub pullRequests.totalCount，包含打开、关闭及合并 PR，避免把 issues_count 当 PR。近期使用单一 `merged:YYYY-MM-DD..YYYY-MM-DD` / `created:...` 区间。每个查询返回的日期样本逐项验证，保存90天最多25个合并PR、90天新增和365天合并各1个验证样本。各批次 observed_at 保留，统计是查询时快照。

GitHub 日期查询按 UTC 日历日期；2026-10-03 只包含采集时已发生的活动，不代表当天结束后的完整计数。

Bot/非Bot作者只作最多25条样本描述，不当作全季比例。近期主分支提交及合并活动不等于所有PR都是缺陷修复；真正的 Skill 源仍需另行筛选实现、测试与验证证据。GitHub 的 NOASSERTION/null 表示识别不足，不自动等同于非开源。

**原版12个项目：基准题量与当前筛选**

| 项目 | Full | Lite | Verified | 历史PR | 90天合并PR | 当前结论 / 相似项目 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [astropy/astropy](https://github.com/astropy/astropy) | 95 | 6 | 22 | 13,645 | 281 | 推荐；[sunpy/sunpy](https://github.com/sunpy/sunpy) |
| [django/django](https://github.com/django/django) | 850 | 114 | 231 | 21,979 | 178 | 推荐；[Kludex/starlette](https://github.com/Kludex/starlette), [fastapi/fastapi](https://github.com/fastapi/fastapi), [pallets/flask](https://github.com/pallets/flask) |
| [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) | 184 | 23 | 34 | 20,930 | 234 | 推荐；[bokeh/bokeh](https://github.com/bokeh/bokeh), [has2k1/plotnine](https://github.com/has2k1/plotnine), [mwaskom/seaborn](https://github.com/mwaskom/seaborn) |
| [mwaskom/seaborn](https://github.com/mwaskom/seaborn) | 22 | 4 | 2 | 1,227 | 1 | 维护中；近90天合并PR未达20；[bokeh/bokeh](https://github.com/bokeh/bokeh), [has2k1/plotnine](https://github.com/has2k1/plotnine), [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) |
| [pallets/flask](https://github.com/pallets/flask) | 11 | 3 | 1 | 2,910 | 3 | 维护中；近90天合并PR未达20；[Kludex/starlette](https://github.com/Kludex/starlette), [django/django](https://github.com/django/django), [fastapi/fastapi](https://github.com/fastapi/fastapi) |
| [psf/requests](https://github.com/psf/requests) | 44 | 6 | 8 | 3,095 | 14 | 维护中；近90天合并PR未达20；[urllib3/urllib3](https://github.com/urllib3/urllib3) |
| [pydata/xarray](https://github.com/pydata/xarray) | 110 | 5 | 22 | 5,549 | 105 | 推荐；[Kotlin/dataframe](https://github.com/Kotlin/dataframe), [pandas-dev/pandas](https://github.com/pandas-dev/pandas), [pola-rs/polars](https://github.com/pola-rs/polars) |
| [pylint-dev/pylint](https://github.com/pylint-dev/pylint) | 57 | 6 | 10 | 5,477 | 192 | 推荐；[astral-sh/ruff](https://github.com/astral-sh/ruff) |
| [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | 119 | 17 | 19 | 7,542 | 152 | 推荐；[jestjs/jest](https://github.com/jestjs/jest) |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | 229 | 23 | 32 | 21,564 | 233 | 推荐；[catboost/catboost](https://github.com/catboost/catboost), [dmlc/xgboost](https://github.com/dmlc/xgboost), [lightgbm-org/LightGBM](https://github.com/lightgbm-org/LightGBM) |
| [sphinx-doc/sphinx](https://github.com/sphinx-doc/sphinx) | 187 | 16 | 44 | 6,872 | 4 | 维护中；近90天合并PR未达20；[facebook/docusaurus](https://github.com/facebook/docusaurus) |
| [sympy/sympy](https://github.com/sympy/sympy) | 386 | 77 | 75 | 15,779 | 149 | 维护/PR/许可通过；相似对照未核实 |

**已核实推荐项目与相似对照**

下表按功能组列出通过全部主池门槛的 benchmark 项目。对照列表仅保留通过公开性、许可与近期主分支检查的项目；其中一些是库的组件对照、跨语言类比、共享依赖或分叉关系，边界在每行说明。相似性由官方项目描述与人工功能比较支持，尚未进行跨项目修复实验。

| 功能组 | 入选benchmark项目（历史PR / 90天合并PR） | 组内可用项目（含源项目） | 比较范围与限制 |
| --- | --- | --- | --- |
| Python Web 框架 | [django/django](https://github.com/django/django) (21,979 / 178); [Kludex/starlette](https://github.com/Kludex/starlette) (2,170 / 95) | [django/django](https://github.com/django/django), [pallets/flask](https://github.com/pallets/flask), [fastapi/fastapi](https://github.com/fastapi/fastapi)（池外）, [Kludex/starlette](https://github.com/Kludex/starlette) | 路由、中间件、请求响应与兼容性；Django 包含 ORM/admin；Flask、FastAPI、Starlette 的架构与同步/异步约定不同。 |
| Python HTTP 客户端 | [urllib3/urllib3](https://github.com/urllib3/urllib3) (2,718 / 60) | [psf/requests](https://github.com/psf/requests), [urllib3/urllib3](https://github.com/urllib3/urllib3) | URL、代理、重试、超时、连接管理；HTTPX 支持异步；urllib3 更接近底层连接池，不能直接迁移全部 API。 |
| 表格与标记数组 | [pandas-dev/pandas](https://github.com/pandas-dev/pandas) (39,141 / 1015); [pola-rs/polars](https://github.com/pola-rs/polars) (16,273 / 780); [pydata/xarray](https://github.com/pydata/xarray) (5,549 / 105); [Kotlin/dataframe](https://github.com/Kotlin/dataframe) (1,094 / 88) | [pandas-dev/pandas](https://github.com/pandas-dev/pandas), [pola-rs/polars](https://github.com/pola-rs/polars), [pydata/xarray](https://github.com/pydata/xarray), [Kotlin/dataframe](https://github.com/Kotlin/dataframe) | 索引、类型、空值、序列化与数据对齐；xarray 面向 N 维；Polars、pandas 与 JVM DataFrame 的执行模型不同。 |
| 天文科学计算 | [astropy/astropy](https://github.com/astropy/astropy) (13,645 / 281); [sunpy/sunpy](https://github.com/sunpy/sunpy) (6,536 / 56) | [astropy/astropy](https://github.com/astropy/astropy), [sunpy/sunpy](https://github.com/sunpy/sunpy) | 单位、坐标、时间与科学数据 I/O；SunPy 依赖 Astropy；太阳物理与通用天文库的领域假设不同，需检查共享依赖和近重复。 |
| 可视化与图表 | [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) (20,930 / 234); [vega/altair](https://github.com/vega/altair) (1,808 / 35) | [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib), [mwaskom/seaborn](https://github.com/mwaskom/seaborn), [vega/altair](https://github.com/vega/altair), [bokeh/bokeh](https://github.com/bokeh/bokeh)（池外）, [plotly/plotly.py](https://github.com/plotly/plotly.py)（池外）, [has2k1/plotnine](https://github.com/has2k1/plotnine)（池外） | 坐标轴、尺度、图例、数据转换、渲染回归；命令式、声明式、浏览器渲染与统计绘图的 oracle 不同；Seaborn 依赖 Matplotlib。 |
| 机器学习估计器 | [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) (21,564 / 233) | [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn), [dmlc/xgboost](https://github.com/dmlc/xgboost)（池外）, [lightgbm-org/LightGBM](https://github.com/lightgbm-org/LightGBM)（池外）, [catboost/catboost](https://github.com/catboost/catboost)（池外） | 输入类型、特征/标签形状、参数校验、模型持久化；后三者偏树模型；不能视为 sklearn 全部算法的替代。 |
| 文档构建 | [facebook/docusaurus](https://github.com/facebook/docusaurus) (7,463 / 196) | [sphinx-doc/sphinx](https://github.com/sphinx-doc/sphinx), [facebook/docusaurus](https://github.com/facebook/docusaurus) | 交叉引用、构建、插件、主题、文档兼容性；reStructuredText、Markdown、MDX 及 Python/JS 工具链不同。 |
| 静态站点生成 | [gohugoio/hugo](https://github.com/gohugoio/hugo) (6,882 / 133); [facebook/docusaurus](https://github.com/facebook/docusaurus) (7,463 / 196) | [gohugoio/hugo](https://github.com/gohugoio/hugo), [jekyll/jekyll](https://github.com/jekyll/jekyll), [facebook/docusaurus](https://github.com/facebook/docusaurus) | 模板、内容路由、资源路径与增量构建；面向博客与面向产品文档的默认约定不同；语言和模板系统不同。 |
| Python 静态检查 | [pylint-dev/pylint](https://github.com/pylint-dev/pylint) (5,477 / 192); [astral-sh/ruff](https://github.com/astral-sh/ruff) (19,808 / 1493) | [pylint-dev/pylint](https://github.com/pylint-dev/pylint), [astral-sh/ruff](https://github.com/astral-sh/ruff) | 诊断规则、语法分析、配置、误报与兼容性；Ruff 用 Rust 实现；三者规则编号、插件与类型推断深度不同。 |
| Python 格式化 | [astral-sh/ruff](https://github.com/astral-sh/ruff) (19,808 / 1493); [psf/black](https://github.com/psf/black) (2,498 / 97) | [astral-sh/ruff](https://github.com/astral-sh/ruff), [psf/black](https://github.com/psf/black) | 格式稳定性、注释、语法版本、幂等性；格式风格及异常语法处理不完全一致。 |
| 测试框架 | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) (7,542 / 152); [jestjs/jest](https://github.com/jestjs/jest) (8,067 / 103) | [pytest-dev/pytest](https://github.com/pytest-dev/pytest), [jestjs/jest](https://github.com/jestjs/jest) | 测试发现、fixture/钩子、隔离、失败报告；Jest 是跨语言对照；nose2 不具备 pytest 完整插件生态。 |
| Python 依赖和项目管理 | [astral-sh/uv](https://github.com/astral-sh/uv) (12,657 / 1276); [python-poetry/poetry](https://github.com/python-poetry/poetry) (3,594 / 61); [pdm-project/pdm](https://github.com/pdm-project/pdm) (1,454 / 59) | [astral-sh/uv](https://github.com/astral-sh/uv), [python-poetry/poetry](https://github.com/python-poetry/poetry), [pdm-project/pdm](https://github.com/pdm-project/pdm), [pypa/pip](https://github.com/pypa/pip)（池外） | 依赖解析、锁文件、安装、环境与平台标记；pip 不管理完整项目；uv 是 Rust 实现，锁文件格式和 resolver 行为不同。 |
| JavaScript HTTP 框架 | [expressjs/express](https://github.com/expressjs/express) (2,676 / 23); [fastify/fastify](https://github.com/fastify/fastify) (4,389 / 102); [honojs/hono](https://github.com/honojs/hono) (2,855 / 157) | [expressjs/express](https://github.com/expressjs/express), [fastify/fastify](https://github.com/fastify/fastify), [honojs/hono](https://github.com/honojs/hono), [koajs/koa](https://github.com/koajs/koa)（池外） | 路由、中间件、错误处理、HTTP 语义；运行时、插件约定和 Web Standards API 不同。 |
| Go Web 与服务框架 | [zeromicro/go-zero](https://github.com/zeromicro/go-zero) (3,710 / 61) | [gin-gonic/gin](https://github.com/gin-gonic/gin), [zeromicro/go-zero](https://github.com/zeromicro/go-zero) | HTTP 路由、服务配置、错误与边界处理；go-zero、Kratos 还包含更完整的微服务治理。 |
| Rust HTTP 框架 | [tokio-rs/axum](https://github.com/tokio-rs/axum) (2,022 / 59) | [tokio-rs/axum](https://github.com/tokio-rs/axum), [actix/actix-web](https://github.com/actix/actix-web)（池外） | 路由、extractor、状态、响应与异步错误；共享 Rust HTTP 生态但 trait 和运行时约束不同。 |
| RPC 与微服务 | [grpc/grpc-go](https://github.com/grpc/grpc-go) (6,401 / 152); [apache/dubbo](https://github.com/apache/dubbo) (8,655 / 23) | [grpc/grpc-go](https://github.com/grpc/grpc-go), [connectrpc/connect-go](https://github.com/connectrpc/connect-go)（池外）, [apache/dubbo](https://github.com/apache/dubbo) | 协议、序列化、客户端配置、超时与重试；Dubbo 是跨语言/跨协议对照；Connect 支持的协议与 gRPC 原生实现不同。 |
| JVM JSON 序列化 | [FasterXML/jackson-databind](https://github.com/FasterXML/jackson-databind) (2,137 / 94); [google/gson](https://github.com/google/gson) (1,337 / 44); [alibaba/fastjson2](https://github.com/alibaba/fastjson2) (1,838 / 36) | [FasterXML/jackson-databind](https://github.com/FasterXML/jackson-databind), [FasterXML/jackson-core](https://github.com/FasterXML/jackson-core), [google/gson](https://github.com/google/gson), [alibaba/fastjson2](https://github.com/alibaba/fastjson2) | JSON、类型映射、空值、流式解析与兼容性；Jackson Core 是基础组件，不是完整 databind 的独立替代；版本与安全契约需固定。 |
| C++ JSON 库 | [nlohmann/json](https://github.com/nlohmann/json) (1,911 / 246); [simdjson/simdjson](https://github.com/simdjson/simdjson) (1,744 / 81) | [nlohmann/json](https://github.com/nlohmann/json), [simdjson/simdjson](https://github.com/simdjson/simdjson) | 解析、数字/Unicode、错误、序列化与内存边界；DOM、流式、on-demand 与 SIMD 假设不同；性能结论不能由功能相似推出。 |
| C++ 字符串格式化 | [fmtlib/fmt](https://github.com/fmtlib/fmt) (1,923 / 56) | [fmtlib/fmt](https://github.com/fmtlib/fmt), [abseil/abseil-cpp](https://github.com/abseil/abseil-cpp)（池外） | 格式字符串、类型、数值格式与兼容性；Abseil 是组件集合，比较范围限定在字符串格式化组件。 |
| JavaScript HTTP 客户端 | [axios/axios](https://github.com/axios/axios) (2,835 / 95) | [axios/axios](https://github.com/axios/axios), [sindresorhus/ky](https://github.com/sindresorhus/ky)（池外） | 请求配置、URL、取消、错误与重试；Ky 基于 Fetch；Axios 的 adapter 和配置模型不同。 |
| Web UI 框架 | [vuejs/core](https://github.com/vuejs/core) (6,853 / 353); [sveltejs/svelte](https://github.com/sveltejs/svelte) (8,615 / 159); [preactjs/preact](https://github.com/preactjs/preact) (2,970 / 98) | [vuejs/core](https://github.com/vuejs/core), [sveltejs/svelte](https://github.com/sveltejs/svelte), [preactjs/preact](https://github.com/preactjs/preact), [react/react](https://github.com/react/react)（池外） | 组件生命周期、状态、DOM、SSR 与渲染；编译期与运行时模型不同；Preact 与 React 接近，不能把其兼容性推广至 Vue/Svelte。 |
| React 组件库 | [mui/material-ui](https://github.com/mui/material-ui) (27,319 / 380); [carbon-design-system/carbon](https://github.com/carbon-design-system/carbon) (11,419 / 453); [grommet/grommet](https://github.com/grommet/grommet) (4,403 / 79) | [mui/material-ui](https://github.com/mui/material-ui), [carbon-design-system/carbon](https://github.com/carbon-design-system/carbon), [grommet/grommet](https://github.com/grommet/grommet), [chakra-ui/chakra-ui](https://github.com/chakra-ui/chakra-ui)（池外）, [ant-design/ant-design](https://github.com/ant-design/ant-design)（池外） | 可访问性、焦点、表单、主题、受控状态与视觉回归；设计系统、样式与默认交互不同，需独立视觉及行为 oracle。 |
| 语法高亮 | [highlightjs/highlight.js](https://github.com/highlightjs/highlight.js) (2,273 / 97) | [PrismJS/prism](https://github.com/PrismJS/prism), [highlightjs/highlight.js](https://github.com/highlightjs/highlight.js) | 语法边界、嵌套语言、转义与输出稳定性；语法定义和语言自动检测机制不同。 |
| JavaScript 静态检查 | [eslint/eslint](https://github.com/eslint/eslint) (8,954 / 157); [biomejs/biome](https://github.com/biomejs/biome) (7,257 / 689) | [eslint/eslint](https://github.com/eslint/eslint), [biomejs/biome](https://github.com/biomejs/biome) | AST、规则、配置、诊断与修复；Biome 是 Rust 工具链，ESLint 插件兼容性不是默认成立。 |
| Web 代码格式化 | [prettier/prettier](https://github.com/prettier/prettier) (12,400 / 375); [biomejs/biome](https://github.com/biomejs/biome) (7,257 / 689) | [prettier/prettier](https://github.com/prettier/prettier), [biomejs/biome](https://github.com/biomejs/biome) | 语法、注释、格式稳定性与幂等性；支持语法、配置与风格不同。 |
| 浏览器质量评测 | [GoogleChrome/lighthouse](https://github.com/GoogleChrome/lighthouse) (6,693 / 49) | [GoogleChrome/lighthouse](https://github.com/GoogleChrome/lighthouse), [sitespeedio/sitespeed.io](https://github.com/sitespeedio/sitespeed.io)（池外） | 导航、性能指标、页面评测和浏览器环境；工具可能共享浏览器或 Lighthouse 依赖；相似性不证明独立工程实现。 |
| 浏览器地图 | [openlayers/openlayers](https://github.com/openlayers/openlayers) (10,531 / 64); [maplibre/maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) (6,359 / 510) | [openlayers/openlayers](https://github.com/openlayers/openlayers), [maplibre/maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) | 坐标投影、瓦片、交互、资源载入与渲染；渲染器、投影支持和地图样式不同。 |
| 日志与可观测数据管道 | [fluent/fluentd](https://github.com/fluent/fluentd) (2,652 / 85); [fluent/fluent-bit](https://github.com/fluent/fluent-bit) (6,423 / 271) | [fluent/fluentd](https://github.com/fluent/fluentd), [fluent/fluent-bit](https://github.com/fluent/fluent-bit), [vectordotdev/vector](https://github.com/vectordotdev/vector)（池外） | 输入/输出插件、解析、缓冲、重试与配置；语言、吞吐架构与插件生态不同。 |
| 键值与缓存服务 | [redis/redis](https://github.com/redis/redis) (8,336 / 187); [valkey-io/valkey](https://github.com/valkey-io/valkey) (3,184 / 342) | [redis/redis](https://github.com/redis/redis), [valkey-io/valkey](https://github.com/valkey-io/valkey) | 协议、命令、过期、复制、兼容性；Valkey 源于 Redis；必须标记分叉关系，排除共享修复与近重复。 |
| 指标与时序系统 | [prometheus/prometheus](https://github.com/prometheus/prometheus) (12,545 / 425) | [prometheus/prometheus](https://github.com/prometheus/prometheus), [VictoriaMetrics/VictoriaMetrics](https://github.com/VictoriaMetrics/VictoriaMetrics)（池外） | 查询、采集、时间边界、存储与配置；VictoriaMetrics 提供兼容接口但存储和部署不同。 |
| 配置与部署自动化 | [ansible/ansible](https://github.com/ansible/ansible) (53,772 / 172) | [ansible/ansible](https://github.com/ansible/ansible), [saltstack/salt](https://github.com/saltstack/salt)（池外）, [pyinfra-dev/pyinfra](https://github.com/pyinfra-dev/pyinfra) | 幂等性、远端执行、inventory、模块与错误恢复；代理模型、描述语言及命令执行方式不同。 |
| 社区论坛 | [NodeBB/NodeBB](https://github.com/NodeBB/NodeBB) (6,130 / 363) | [NodeBB/NodeBB](https://github.com/NodeBB/NodeBB), [discourse/discourse](https://github.com/discourse/discourse)（池外）, [flarum/framework](https://github.com/flarum/framework)（池外） | 权限、通知、插件、搜索、分页与兼容性；Node.js、Ruby、PHP 技术栈不同，功能相似不保证补丁可直接迁移。 |
| 音乐服务器 | [navidrome/navidrome](https://github.com/navidrome/navidrome) (3,281 / 207) | [navidrome/navidrome](https://github.com/navidrome/navidrome), [ampache/ampache](https://github.com/ampache/ampache)（池外） | 媒体扫描、元数据、播放接口、权限与存储；Go 与 PHP 架构不同；需固定兼容协议及元数据契约。 |
| API 开发客户端 | [Kong/insomnia](https://github.com/Kong/insomnia) (5,498 / 231); [usebruno/bruno](https://github.com/usebruno/bruno) (4,377 / 448) | [Kong/insomnia](https://github.com/Kong/insomnia), [usebruno/bruno](https://github.com/usebruno/bruno) | 请求定义、环境、导入导出、认证与响应展示；存储、脚本和同步方式不同；实验必须使用无凭据或 mock 环境。 |
| 漏洞扫描工具 | [future-architect/vuls](https://github.com/future-architect/vuls) (1,990 / 36) | [future-architect/vuls](https://github.com/future-architect/vuls), [aquasecurity/trivy](https://github.com/aquasecurity/trivy)（池外） | 版本识别、漏洞匹配、报告与兼容性；数据源、覆盖目标、依赖扫描模型与时效不同。 |
| 数据工作流编排 | [PrefectHQ/prefect](https://github.com/PrefectHQ/prefect) (15,213 / 402) | [dagster-io/dagster](https://github.com/dagster-io/dagster), [PrefectHQ/prefect](https://github.com/PrefectHQ/prefect), [apache/airflow](https://github.com/apache/airflow)（池外） | 调度、依赖、重试、状态、资源与持久化；数据资产与任务模型不同，部署成本较高。 |
| 模型载入与推理 | [huggingface/transformers](https://github.com/huggingface/transformers) (28,932 / 907); [ollama/ollama](https://github.com/ollama/ollama) (7,020 / 253) | [huggingface/transformers](https://github.com/huggingface/transformers), [ollama/ollama](https://github.com/ollama/ollama), [vllm-project/vllm](https://github.com/vllm-project/vllm)（池外）, [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)（池外） | 模型配置、tokenizer、缓存、推理 API 与数值边界；库与服务、Python 与 C++/Go 不同；GPU/模型资源成本需要另行验证。 |
| 代码修复 Agent 工具 | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) (11,942 / 571) | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands), [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent)（池外） | 工具调用、运行环境、编辑、轨迹和验证；框架及模型预算不同；功能相似不构成其修复能力的排名。 |
| 分析型数据库 | [apache/druid](https://github.com/apache/druid) (15,049 / 650); [ClickHouse/ClickHouse](https://github.com/ClickHouse/ClickHouse) (90,391 / 8540); [duckdb/duckdb](https://github.com/duckdb/duckdb) (14,630 / 1433) | [apache/druid](https://github.com/apache/druid), [ClickHouse/ClickHouse](https://github.com/ClickHouse/ClickHouse), [duckdb/duckdb](https://github.com/duckdb/duckdb) | SQL、聚合、类型、时间、查询规划与数据 I/O；分布式服务与嵌入式引擎不同；部署及性能不能混比。 |
| 图像载入与处理 | [python-pillow/Pillow](https://github.com/python-pillow/Pillow) (6,405 / 236) | [python-pillow/Pillow](https://github.com/python-pillow/Pillow), [imageio/imageio](https://github.com/imageio/imageio)（池外） | 格式、像素类型、编码解码、边界与回归；scikit-image 包含更广泛的算法，比较范围限定在共享图像处理/I-O 能力。 |
| JSON 命令行处理 | [jqlang/jq](https://github.com/jqlang/jq) (1,219 / 25) | [jqlang/jq](https://github.com/jqlang/jq), [itchyny/gojq](https://github.com/itchyny/gojq)（池外） | 查询语法、数字、Unicode、流式输入与错误；gojq 实现 jq 兼容语言；差异与兼容版本须固定。 |
| Rust 异步运行时 | [tokio-rs/tokio](https://github.com/tokio-rs/tokio) (5,023 / 180) | [tokio-rs/tokio](https://github.com/tokio-rs/tokio), [smol-rs/smol](https://github.com/smol-rs/smol)（池外） | 任务、I/O、定时器、取消和运行时边界；运行时架构、库生态和 trait 约束不同。 |
| Rust 参数解析 | [clap-rs/clap](https://github.com/clap-rs/clap) (3,079 / 33) | [clap-rs/clap](https://github.com/clap-rs/clap), [pacak/bpaf](https://github.com/pacak/bpaf)（池外） | 参数、默认值、校验、帮助和错误信息；derive/parser 模型不同，不共享同一参数契约。 |
| 基础设施访问网关 | [gravitational/teleport](https://github.com/gravitational/teleport) (55,082 / 1018) | [gravitational/teleport](https://github.com/gravitational/teleport), [warp-tech/warpgate](https://github.com/warp-tech/warpgate)（池外） | 身份、SSH/数据库访问、代理、权限与审计；部署、协议覆盖和认证系统不同，测试应使用隔离环境。 |
| 加密邮件 Web 客户端 | [tutao/tutanota](https://github.com/tutao/tutanota) (4,045 / 135) | [tutao/tutanota](https://github.com/tutao/tutanota), [ProtonMail/WebClients](https://github.com/ProtonMail/WebClients) | 邮件、联系人、日历、加密状态与客户端 UI；后台协议不同；Proton 公开仓库没有 PR，不能作为本轮历史 PR 源。 |

**全部项目的筛选分布**

| 状态 | 项目数 |
| --- | ---: |
| 维护/PR/许可通过；相似对照未核实 | 445 |
| 历史PR未达1000 | 388 |
| 主分支近期维护未达门槛 | 12 |
| 维护中；近90天合并PR未达20 | 53 |
| 已归档/禁用 | 12 |
| 推荐 | 73 |
| 许可证待复核 | 102 |
| 当前许可不满足本轮开源条件 | 2 |

每个项目在上表只计一个首要状态；可能同时存在其他不足。`维护/PR/许可通过；相似对照未核实` 不是判定它不存在同类项目。未达本轮20个合并PR门槛的成熟库也不等于停止维护；完整表保留其真实量及提交日期。

**值得单独标注的情况**

- `scratchfoundation/scratch-gui` 当前已归档，历史出现在 Multimodal 不保证今天仍适合作为维护中的 PR 源。
- `ProtonMail/WebClients` 主分支仍有更新，但公开 PR 总量为0；当前公开镜像不满足本轮 PR 源门槛。
- `hashicorp/terraform` 当前许可为 BUSL-1.1，`flipt-io/flipt` 当前为 FCL-1.0-MIT，本轮不把来源可见/未来开源当成当前的开源许可。
- `redis/redis` 当前 Redis 8+ 有 AGPLv3 选项；`valkey-io/valkey` 为BSD项目。两者存在分叉关系，需审查近重复修复。
- Sphinx、SymPy、Matplotlib、jq、Zstandard、MapLibre、Pillow、JavaParser 等已核对实际许可文件；结果和固定提交链接见 manual-license-decisions.json。

优先从 HTTP 客户端、表格/数组、Web、JSON、静态检查、文档构建等明确功能组选择项目。核心12项目提供既有论文对照；多语言与真实应用扩展提供不同语言和工程域。大型数据库、深度学习和基础设施网关的环境成本更高，本次项目活跃度不证明其修复评测更容易。

若用于 AREX 下一阶段，按整个项目留出评测目标，冻结历史截止日及源PR列表；共享依赖、分叉与相同修复别名要做近重复检查。当前调研未向提取器或 catalog 导入 benchmark 的目标补丁或测试，也未执行新的修复率实验。

**来源与复核**

数据版本和公开 metadata：[dataset-snapshots.json](data/swebench-projects-20261003/dataset-snapshots.json)。逐文件项目统计、SHA及文件首部身份检查：[benchmark-project-census.json](data/swebench-projects-20261003/benchmark-project-census.json)。维护/PR证据：[github-repositories.json](data/swebench-projects-20261003/github-repositories.json)、[github-pr-activity.json](data/swebench-projects-20261003/github-pr-activity.json)。相似组及限制：[similarity-groups.json](data/swebench-projects-20261003/similarity-groups.json)。

独立 REST 日期区间复核：[rest-date-range-crosscheck.json](data/swebench-projects-20261003/rest-date-range-crosscheck.json)。离线数据审核与文件哈希：[data-audit.json](data/swebench-projects-20261003/data-audit.json)。[审核脚本](scripts/audit_swebench_project_data.py)不访问网络；可用外部缓存复验完整下载文件的官方哈希。

固定版本完整 Parquet/单文件 Python JSONL 用官方 LFS SHA-256 或 Git blob SHA-1 验证；大型多仓 JSONL 只读取固定版本实际首部，并与官方文件索引的 org/repo 身份交叉匹配，不声称完整内容hash已重新验证。原始问题/补丁/执行日志不进入本报告数据目录；外部缓存不纳入提交。

采集脚本：[项目普查](scripts/swebench_project_census.py)、[GitHub活动](scripts/swebench_repository_screening.py)、[报告和门控](scripts/build_swebench_project_report.py)。脚本使用公开 HTTP 与已登录的 GitHub CLI；API凭据由CLI处理，不读取、打印或写入报告。普查需要 duckdb==1.4.0，当前采集使用 WSL + Windows HTTP；跨平台运行需提供适合本机的HTTP/CLI路径。

在仓库根目录用 Python 3.12 离线重建报告并审核：

```bash
python analysis/scripts/build_swebench_project_report.py --data analysis/data/swebench-projects-20261003 --analysis analysis
python analysis/scripts/audit_swebench_project_data.py --data analysis/data/swebench-projects-20261003 --analysis analysis
```

第二条命令可加 `--cache <外部缓存目录>`，独立复验已完整下载文件的实际哈希；不提供缓存时仅核对记录及官方索引，不声称重读了原始完整文件。

当前公开性/维护性评估对应2026-10-03，不替代 benchmark 历史 base_commit 的环境或许可。部分未来/迁移到其他平台的版本、未公开 Pro 划分、未正式说明评测角色的新增语言文件分别标注；本报告不宣称遍历所有曾存在的衍生变种。
