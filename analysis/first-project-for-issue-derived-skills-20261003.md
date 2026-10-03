**从自身及相似项目历史 Issue 提取 Skill：首个实验项目选择**

调研日期：2026-10-03。**首选 Pylint；先研究 Python 名称绑定、注解/类型检查上下文、推断与 AST 异常处理。历史来源采用 Pylint 自身、Pyflakes 和 Ruff。** Pyflakes 提供同语言的独立检查器实现，Ruff 提供另一套语义分析实现；Ruff 的 Rust 修改应提炼为 Python 语义与诊断验证方法，再适配 Pylint/Astroid。

一些错误来自“词法位置、作用域、求值时间、运行时/类型上下文”混淆。历史修复记录可以帮助 Agent 识别适用条件、定位分析入口，并设计保护正确诊断的对照测试。本轮没有执行 Agent 的 Skill 效果实验，结论是**值得优先检验的选型与机制假设**。

**调查范围与证据强度**

三轮有目的的关键词检索共抓取211个不同issue。本轮检查30个选定PR的实现差异、关联issue及测试差异；检索条件、排序和来源均保留。这是选型调查，不是随机抽样的修复率或“可提取率”估计。搜索正文会命中模板中的规则编号，因此第三轮增加标题限定，并以实际修复链筛选。

14个PR是三个主要项目在2024-01-01前合并的历史种子；13个含原仓库回归测试修改，Pyflakes #750没有新增测试，另用原issue复现程序做了发布版本对照。5个较晚的Pylint修复作为已审阅开发案例；其补丁不得进入后续盲评。其余PR用于比较其他项目。

历史种子的PR与关联issue正文检查了`lastEditedAt`，未发现2024-01-01后的正文编辑。提取时只准使用白名单中的早期正文和固定修复提交；探索数据中的晚期交叉引用、当前README、开发案例和评测补丁不能作为历史知识源。

**选择条件的实际证据**

| 条件 | 实际观察 | 对实验的意义 |
| --- | --- | --- |
| 历史数量与维护 | Pylint已关闭issue 5,113个；历史PR 5,477，近90天合并192个。Pyflakes已关闭issue 495个，历史PR 363，近90天合并42个，主分支最后提交2026-09-30。Ruff历史PR 19,808，近90天合并1,493个 | 有足够历史来源与持续出现的后续问题；有效来源数量须另按修复证据筛选 |
| 重复的问题族 | 作用域、命名表达式、类型注解、TYPE_CHECKING、推断结果处理在不同项目中都有修复记录 | 可研究语义知识与修复步骤迁移，而非仅按接口名字找相似项目 |
| 可验证的历史证据 | 种子PR能追到实现文件、MRE、功能fixture、预期诊断或snapshot | 可形成包含动作、证据、限制及functional eval的Skill Package |
| 初期运行成本 | 已在Python 3.12.3上跑通两组版本对照。Pylint单个复现约0.5秒，Pyflakes约0.06秒 | 方便快速检验；时间仅代表本轮小复现，不代表全套测试或所有历史环境 |
| 相似关系可解释 | Pyflakes逐文件分析Python AST；Pylint使用Astroid推断；Ruff用Rust实现Python语义分析，官方承认借鉴Pyflakes/Pylint等工具 | 要迁移分析方法；规则和测试有传承关系，需检查近重复 |
| 后续任务储备 | 当前Live/verified含29个Pylint任务，可进一步按原始issue日期筛选 | 有公开可复核的任务协议，仍须逐题确认环境与复现 |

PR活动采用此前冻结的2026-10-03调查；Pyflakes维护信息本轮单独查询。90天窗口为2026-07-06至2026-10-03，含采集时已发生的活动。“已关闭issue”包含讨论、重复、未计划等情况，不等同于有效训练episode。

三者中优先以Pylint为目标：其Python实现、Astroid分析入口及功能fixture便于建立修复验证，本轮已有版本对照和后续公开任务池。Pyflakes适合作为同语言的简洁历史来源，本轮尚未建立它的同规模后续评测池；Ruff提供另一套语义实现，将它作为目标还需要建立Rust构建和测试环境。本轮验证过的运行环境与任务筛选证据集中在Pylint，因此这个选择最适合先检验系统机制。

**本项目与相似项目的历史修复**

| 历史issue | 关联修复及日期 | 实际动作与测试 | 可提炼的知识 |
| --- | --- | --- | --- |
| [Pylint #6136](https://github.com/pylint-dev/pylint/issues/6136)：`for x in x`同名变量误报未使用 | [PR #6154](https://github.com/pylint-dev/pylint/pull/6154)，2022-04-03 | 修改`variables.py`，功能fixture覆盖推导式目标与外部变量 | 同一标识符不等于同一次绑定，需检查所属作用域 |
| [Pyflakes #633](https://github.com/PyCQA/pyflakes/issues/633)：生成器海象表达式变量在外部报未定义 | [PR #698](https://github.com/PyCQA/pyflakes/pull/698)，2022-05-30 | 引入NamedExprAssignment，越过生成器作用域绑定到外部；新增嵌套测试 | PEP572的绑定规则不同于普通推导式目标 |
| [Ruff #9230](https://github.com/astral-sh/ruff/issues/9230)：类体海象表达式与推导式误报F821 | [PR #9248](https://github.com/astral-sh/ruff/pull/9248)，2023-12-22 | 将“在NamedExpr内”细化为“当前表达式是否是其target”；新增fixture/snapshot | 应判断节点的结构角色，而非仅判断祖先类型 |
| [Pylint #8252](https://github.com/pylint-dev/pylint/issues/8252)：容器非首位命名表达式误报 | [PR #8253](https://github.com/pylint-dev/pylint/pull/8253)，2023-02-11 | 修改容器检查；新增ternary/walrus fixture | 检查求值顺序。原测试注明某些邻近输入仍有漏报，Skill须保留限制 |
| [Pyflakes #617](https://github.com/PyCQA/pyflakes/issues/617)：给导入变量添加注解触发F811 | [PR #619](https://github.com/PyCQA/pyflakes/pull/619)，2021-03-24 | Annotation.redefines返回False，新增测试 | 只有注解的语句不等于重新定义 |
| [Pyflakes #728](https://github.com/PyCQA/pyflakes/issues/728)：AnnAssign遮蔽未定义名称检查 | [PR #729](https://github.com/PyCQA/pyflakes/pull/729)，2022-09-08 | 调整遍历顺序，新增`x: int = x`必须报错的测试 | 注解/赋值目标和值表达式应分别处理，不能将所有注解免检 |
| [Pyflakes #749](https://github.com/PyCQA/pyflakes/issues/749)：内部类前向注解误报 | [PR #750](https://github.com/PyCQA/pyflakes/pull/750)，2022-11-27 | 修改延迟/最终作用域检查；未新增测试。本轮重建复现，2.5.0报错、3.1.0通过 | 检查时机与作用域完成状态；发布版本对照不是单独隔离该PR的因果测试 |
| [Pyflakes #764](https://github.com/PyCQA/pyflakes/issues/764)：外部注解名称在内部赋值导致崩溃 | [PR #765](https://github.com/PyCQA/pyflakes/pull/765)，2023-01-31 | 修复used状态结构；测试要求保留未定义/未使用诊断 | 消除崩溃时应同时保留正确诊断 |
| [Ruff #7879](https://github.com/astral-sh/ruff/issues/7879)：Annotated推导式误报F821 | [PR #7885](https://github.com/astral-sh/ruff/pull/7885)，2023-10-10 | 修复注解内绑定/引用访问；新增推导式及命名表达式测试 | 注解上下文可能仍包含表达式和局部绑定 |
| [Ruff #6030](https://github.com/astral-sh/ruff/issues/6030)：future annotations下Literal字符串被当名称 | [PR #6032](https://github.com/astral-sh/ruff/pull/6032)，2023-07-24 | 加入Literal语义上下文保护；新增F821测试 | `Literal["ns"]`里的字符串是值，不是待解析名称 |
| [Pylint #8696](https://github.com/pylint-dev/pylint/issues/8696)：TYPE_CHECKING内导入触发unused-variable | [PR #8713](https://github.com/pylint-dev/pylint/pull/8713)，2023-06-06 | 加入类型检查块条件；新增配置相关fixture | 类型用途的导入与运行时变量检查应区分 |
| [Pylint #8198](https://github.com/pylint-dev/pylint/issues/8198)：TYPE_CHECKING相关先使用后赋值漏报 | [PR #8431](https://github.com/pylint-dev/pylint/pull/8431)，2023-04-15 | 维护类型检查作用域；fixture要求块外datetime.now()保留诊断 | 不能泛化为“TYPE_CHECKING相关名称全部免报” |
| [Ruff #8427](https://github.com/astral-sh/ruff/issues/8427)：未识别typing_extensions.TYPE_CHECKING | [PR #8429](https://github.com/astral-sh/ruff/pull/8429)，2023-11-09 | 按typing provider解析导入符号；修改多个fixture/snapshot | 先识别模块来源和别名，再判断上下文 |
| [Ruff #8441](https://github.com/astral-sh/ruff/issues/8441)：解包赋值漏报F841 | [PR #8489](https://github.com/astral-sh/ruff/pull/8489)，2023-11-05 | 增加unpacked assignment检测和preview分支测试 | 绑定种类、规则模式与版本都是适用条件 |

这些来源共享语言语义，使用不同的数据结构和分析阶段。最适合抽取的是“识别绑定/上下文 → 核实求值和提供方 → 定位分析入口 → 修改条件 → 保留反例”。历史路径是证据与定位线索；修改须适配目标base_commit的Astroid版本和接口。

**较晚的issue仍出现相关问题**

下列补丁已审阅，只作为开发/提示设计/harness材料，不能再充当盲评。表中的迁移关系是待Agent实验检验的机制假设。

| 后续Pylint issue | 修复 | 历史方法可能指导的检查 | 边界 |
| --- | --- | --- | --- |
| [#9391](https://github.com/pylint-dev/pylint/issues/9391)，2024-01-26：内部函数返回类型误报 | [#10275](https://github.com/pylint-dev/pylint/pull/10275)，2025-03-18 | 区分模块词法行号与内部函数创建/调用时的求值，检查frame和作用域 | 原新增测试承认外层函数在类声明前调用仍有漏报，不能无条件抑制 |
| [#9780](https://github.com/pylint-dev/pylint/issues/9780)，2024-07-08：回移assert_never行为不同 | [#9782](https://github.com/pylint-dev/pylint/pull/9782)，2024-07-12 | 识别typing_extensions、Python版本条件及路径终止语义；Ruff的provider修复可提供检查清单 | 原问题涉及Python3.10/3.12差异，本轮未完成两解释器完整对照 |
| [#10028](https://github.com/pylint-dev/pylint/issues/10028)，2024-10-16：TYPE_CHECKING内函数定义漏报 | [#10034](https://github.com/pylint-dev/pylint/pull/10034)，2024-11-04 | 从导入扩展到函数/类定义，检查块外使用、nonlocal和顺序 | 原讨论说明直接扩展旧修复会造成其他项目误报，需要正反例及primer |
| [#10208](https://github.com/pylint-dev/pylint/issues/10208)，2025-01-29：变量组成合法协议返回值仍报错 | [#10209](https://github.com/pylint-dev/pylint/pull/10209)，2025-01-30 | 区分语法形态Name与推断后的值类型，检查是否仅处理Call而遗漏Name | 属推断扩展与harness案例，不是作用域Skill已有收益的证明 |
| [#10334](https://github.com/pylint-dev/pylint/issues/10334)，2025-04-10：Slice装饰器导致崩溃 | [#10350](https://github.com/pylint-dev/pylint/pull/10350)，2025-05-01 | 访问推断结果属性前核验实际类型，避免跳过所有检查 | 应保留not-callable等正确诊断；属鲁棒性扩展 |

同项目旧错误、相似项目语义实现及较晚的新组合支持迁移假设。是否带来更多正确修复、更少误改或更低成本，必须通过等预算Agent对照回答。

**实际版本对照**

独立外部目录安装固定版本，关闭本机Pylint配置、持久缓存及无关诊断。两Pylint版本共享`astroid==3.3.8`和其他固定依赖，未修改产品环境或依赖。

| 案例 | 旧版本 | 较新版本 | 结论 |
| --- | --- | --- | --- |
| Pylint #10208合法返回值复现 | 3.3.4：E0313、exit2 | 3.3.5：无诊断、exit0 | 误报可稳定观测 |
| 邻近非法返回值：kwargs改为None | 3.3.4：E0313、exit2 | 3.3.5：E0313、exit2 | 真正非法输入仍被识别，能防止“直接关闭检查”骗过评测 |
| Pyflakes #749前向注解复现 | 2.5.0：InnerModel2未定义、exit1 | 3.1.0：无诊断、exit0 | 相似项目案例可重建为确定性功能测试 |

这是行为与评测可行性验证，没有调用修复Agent或计算Skill提升率；也未重跑全部30个PR的完整原始测试套件。

**其他候选的比较**

| 项目组 | 检查过的修复 | 有利条件 | 第一轮成本或混淆 |
| --- | --- | --- | --- |
| xarray ← pandas、Polars | [xarray #7917](https://github.com/pydata/xarray/pull/7917)：空数组reindex保留float32；[#6389](https://github.com/pydata/xarray/pull/6389)：保留attrs/encoding；[pandas #39759](https://github.com/pandas-dev/pandas/pull/39759)：dt64/td64重索引避免整数化 | dtype、缺失值、元数据不变量适合提炼；可作为第二组 | xarray直接依赖pandas/NumPy，须分辨独立迁移与底层依赖修复；Dask、flox、Zarr、I/O进一步增加环境差异 |
| Gson ← Jackson、Fastjson2 | [Gson #2731](https://github.com/google/gson/pull/2731)：nullSafe幂等；[#2158](https://github.com/google/gson/pull/2158)：数值转换；[Fastjson2 #1452](https://github.com/alibaba/fastjson2/pull/1452)：泛型接口无父类时NPE；[Jackson #4857](https://github.com/FasterXML/jackson-databind/pull/4857)：EnumSet/default typing | 同为Java JSON库，类型、空值、适配器规则可验证，独立性较清楚 | Gson官方声明维护模式。Multilingual九题全早于2024，不能用2024历史知识评测；新样本还混有发布、OSGi/JDK和咨询，需另建目标集 |
| Fastify ← Express、Hono | [Fastify #5742](https://github.com/fastify/fastify/pull/5742)：Content-Type大小写；[#5892](https://github.com/fastify/fastify/pull/5892)：Host缺失；[#5920](https://github.com/fastify/fastify/pull/5920)：locked ReadableStream；[Express #5603](https://github.com/expressjs/express/pull/5603)：正则命名组 | HTTP语义、缺省值和流生命周期可形成Skills，Node测试便利 | Express案例通过path-to-regexp升级修复；部分Fastify问题落在插件/协议/TS类型，需更细地核对跨项目方法对应层次 |

维护模式不表示停止维护，依赖关系也不表示不可迁移。以上是本轮目标与证据下的实验顺序，其他项目的抽取成功率尚未系统测量。

**建议冻结的第一轮实验**

历史知识截止日采用2024-01-01：Ruff此前已有可用修复和测试积累，Pylint Live有足够后续issue。这个边界在开始Agent效果实验前确定。探索时也核对过2025边界：

- Live/verified的29个Pylint任务中，13个PR在2025年提交，但仅7题的所有关联issue均在2025年后创建，排除两个Pyreverse题后只有5题。
- 2024边界下有28个原始issue日期候选，排除Pyreverse后26个；再排除文档、新语法检查、文件统计和已审阅gold的三个重叠开发题，得到**20个未读取gold diff的元数据候选**。
- 这不是20个已合格盲评题。须逐题复现base_commit失败、验证测试能区分修复、检查issue输入没有答案及近重复，再冻结最终清单。任务和固定base_commit见[实验清单](data/first-project-issue-study-20261003/experiment-selection.json)。

任务池固定为[SWE-bench-Live/SWE-bench-Live](https://huggingface.co/datasets/SWE-bench-Live/SWE-bench-Live/tree/b51a86422e10cfd403beb4773e5a2947953e36ec)，revision为`b51a86422e10cfd403beb4773e5a2947953e36ec`，default配置的verified split。20个候选的base_commit已逐个与这个冻结数据集的元数据比对，全部一致；此检查确认任务身份，不代替失败/通过测试资格审核。

第一批可从14个历史种子提炼3—5个有边界的Skill族，再扩充来源。建议先做：

1. **绑定来源与所属作用域**：区分推导式target、命名表达式target、外部容器和nonlocal，核实PEP572与求值顺序。
2. **注解角色与检查时机**：区分值、类型、Literal、只有注解的名称、实际赋值与延迟求值，设计相邻输入的反例。
3. **类型提供方与运行路径**：先解析typing/typing_extensions及别名，再区分类型用途和块外运行时用途，保留应报错路径。

20个候选并非都属于这三个族。正式冻结时应标记各题的适用族，并保留一部分不适用任务检查错误激活；推断和AST鲁棒性可在后续增加有历史证据支持的Skill族。

各族应生成可注入context的Skill Package：`SKILL.md`、actions/evidence、workflow/provenance和activation/applicability/functional evals。正文包含触发线索、不适用情形、步骤、版本适配要求和停止条件。开发案例只用于开发验证，不得伪装为盲测。

一个特别适合验证AREX的例子：#8713消除TYPE_CHECKING导入的unused-variable误报；#8431要求块外运行时使用继续报告used-before-assignment。关键词相似，诊断方向不同。适用条件和workflow应保留这种区别，eval要求正反例都正确；合并成“遇到TYPE_CHECKING就跳过检查”的记录会有害。

冻结同一模型版本、工具集合、token及调用轮数预算，按任务配对运行：

| 条件 | 要回答的问题 |
| --- | --- |
| 无Skill baseline | 原有Agent能力 |
| 原始历史证据检索，预算匹配 | 加入历史信息本身的作用 |
| 仅自身项目Skill | 本项目经验的作用 |
| 仅相似项目Skill | 独立检验跨项目迁移 |
| 自身+相似项目Skill | 相似来源对自身来源的增量 |

主比较是“自身+相似”相对“仅自身”，以及相对“原始证据检索”。Ruff/Pyflakes规则有传承关系，须排除相同复现、同一跨仓库bug、复制测试和共享修复，必要时做逐个donor消融。

报告真实任务成功率、保留原有测试/诊断、错误激活与误改、token/工具调用/时间成本及逐题配对结果。适用与不适用任务分组报告，不能只报有收益的任务。若baseline接近全解，关注成本和误改，再扩展复杂作用域/推断任务；20题pilot不能支持宽泛统计结论。公开题目是否被模型训练见过也无法由这个时间边界保证。

**材料与复核**

- [探索issue](data/first-project-issue-study-20261003/exploratory-issues.json)、[关联修复检索](data/first-project-issue-study-20261003/targeted-issues.json)、[标题限定检索](data/first-project-issue-study-20261003/focused-issues.json)。
- [30个PR的实现/测试证据](data/first-project-issue-study-20261003/reviewed-repair-evidence.json)、[历史正文编辑审核](data/first-project-issue-study-20261003/historical-text-edit-audit.json)。
- [固定提交的项目文档](data/first-project-issue-study-20261003/repository-documents.json)、[Pyflakes维护复核](data/first-project-issue-study-20261003/pyflakes-maintenance.json)。文档保存前去除可识别凭据字面值。
- [任务元数据](data/first-project-issue-study-20261003/benchmark-candidates.json)、[原始issue日期](data/first-project-issue-study-20261003/pylint-benchmark-pr-metadata.json)、[实验来源与候选清单](data/first-project-issue-study-20261003/experiment-selection.json)。
- [版本对照结果](data/first-project-issue-study-20261003/reproducer-qualification.json)、[复现脚本](scripts/qualify_first_project_reproducers.py)、[PR证据采集](scripts/collect_reviewed_repair_evidence.py)、[检索脚本](scripts/research_issue_skill_suitability.py)。
- [数据审核及文件哈希](data/first-project-issue-study-20261003/data-audit.json)：检查历史时间边界、候选与已审阅补丁的互斥、冻结提交一致性及复现对照；三个研究脚本通过Ruff检查。

外部复现库没有进入仓库或修改产品依赖。GitHub CLI在内部处理凭据，正文与patch先脱敏再输出/保存。未执行新修复Agent实验，未向生产提取器/catalog导入开发或评测补丁。
