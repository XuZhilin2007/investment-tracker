# OpenBB 研究：可替换的数据基础设施、Point-in-Time 与 Evidence Provenance

> 本文是 investment-tracker 第四轮开源项目研究，只研究 OpenBB。目标不是复制或立即集成 OpenBB，而是回答：如果未来实现 point-in-time Context Reconstruction、Thesis Monitoring 和 Evidence Review，是否存在足够可靠、可追溯、可替换的数据基础设施？

## 0. 研究范围、版本与结论口径

### 0.1 固定版本

- 研究仓库：[OpenBB-finance/OpenBB][repo]
- 固定 commit：[`3e071fcc2cd9f891cac6040ae60296dba76dab46`][commit]
- commit 日期：2026-07-20
- commit 标题：`fix(mcp): support stdio transport on Windows (#7596)`
- 该 commit 中 `openbb_platform/pyproject.toml` 的版本：`4.7.3`
- 官方在线文档补充核对日期：2026-08-12。在线文档会继续变化；凡涉及实现细节，本文以固定 commit 源码为准。

### 0.2 已阅读的本项目上下文

本轮开始前已完整阅读：

- `docs/PRODUCT_VISION_DRAFT.md`
- `docs/research/TRADENOTE_RESEARCH.md`
- `docs/research/TRADENOTE_REVIEW_NOTES.md`
- `docs/research/WEALTHFOLIO_RESEARCH.md`
- `docs/research/GHOSTFOLIO_RESEARCH.md`

本文沿用前三轮形成的候选三层模型：

```text
Financial Reality
Investor Reasoning
Evidence & Review
```

### 0.3 证据等级和措辞

为避免把代码能力、推论和产品主张混在一起，本文使用三种明确标签：

- **事实**：可由固定 commit 的源码、官方 README 或官方文档直接确认。
- **源码推断**：由多个实现细节共同推出，但项目没有以产品承诺的形式明说。
- **对本项目判断**：针对 Investment Tracker 的架构或产品判断，不是 OpenBB 的事实。

“支持历史日期”不等于“支持 point-in-time correctness”。本文将以下概念严格分开：

- **observation time**：数值描述的经济或市场时点；
- **publication time**：信息首次公开的时点；
- **filing time**：申报文件被监管系统接收/公开的时点；
- **fiscal period**：财务事实所属期间；
- **revision time**：历史数值被修订或重述的时点；
- **captured time**：本系统实际取得内容的时点；
- **historical version / vintage**：同一 observation 对应的某个历史版本。

### 0.4 执行摘要

**对本项目判断：**

1. OpenBB 最强的不是某个数据源，而是 `router → standard model → provider fetcher` 这一条可扩展的数据接入边界。它证明“外部供应商可替换、上层接口相对稳定”是可行的。
2. OpenBB 不是通用 point-in-time 数据库。它能返回大量历史数据，也有 SEC `pit_mode` 这样的强局部能力，但缺少跨 provider 的统一 as-of、revision lineage、immutable snapshot 和 replay 契约。
3. 通用 provenance 达到“哪次 OpenBB 调用、哪个 provider、什么参数、何时执行”的级别；原始上游 ID、文档版本、单位/币种/频率、二次加工和质量标记则依模型和 provider 而定。
4. Evidence 不能只保存标准化后的 `value`。至少要把 provider、上游来源、原始标识/URL、各类时间、单位、查询和捕获上下文、转换说明以及不可变快照/哈希一起保存。
5. OpenBB MCP/Workspace 能把标准化数据暴露给 agent，并支持配置式 tool/widget citation；它并不自动把 agent 变成可靠的 Evidence Interpreter，也不提供“缺失值绝不补全”为事实的通用保证。
6. 对 A 股/中文场景，当前公开实现的中国宏观覆盖强于中国证券、公告和中文新闻覆盖。按供应商 symbol 偶尔能查询，不等于具备可商用、可验证、稳定的中国市场数据层。
7. OpenBB 进一步支持三层模型，而不是推翻它：OpenBB 类型能力主要进入 Financial Reality 的外部金融事实入口；Evidence & Review 必须独立承担来源、历史版本、冻结和解释状态。
8. v0.2.0 最值得只验证一个假设时，应选择“用户是否觉得持仓期间的 Evidence Monitoring 有价值”。技术可行性只能做受限验证，用户价值仍是四轮研究后最大的未知数。

---

## 1. OpenBB 的产品和技术定位

### 1.1 它解决什么问题

**事实：** OpenBB README 把 Open Data Platform（ODP）描述为把 proprietary、licensed 和 public data sources 接入下游 AI copilots、research dashboards 等应用的开源工具集，并用“connect once, consume everywhere”概括同一数据接入向 Python、Workspace/Excel、MCP 和 REST API 暴露的方式。[README][repo-readme]

**事实：** OpenBB Workspace 是独立的分析 UI/商业产品面，能够展示数据并承载 AI agents；开源仓库的核心仍是数据接入和接口层，而不是个人投资组合账本。[README][repo-readme]

**对本项目判断：** 四个候选定位不是互斥的，主次如下：

1. **Data Aggregation Layer：最准确。** Provider extension、standard model 和统一调用界面是核心。
2. **Financial Data Platform：准确。** 它不仅聚合，也提供路由、类型、Python/REST/MCP 等消费面。
3. **AI / Agent Infrastructure：是重要出口，不是数据真实性内核。** MCP 把现有接口变成 agent tools。
4. **Research Platform：Workspace 层面成立；开源 ODP 本身更像研究平台的数据底座。**

### 1.2 与前三个项目的根本区别

| 项目 | 主要拥有的状态 | 核心问题 |
| --- | --- | --- |
| TradeNote | 交易日志、交易复盘和用户注释 | 用户如何记录、聚合和复盘交易 |
| Wealthfolio | 账户、资产、活动、持仓和估值 | 用户的金融现实如何被本地重建 |
| Ghostfolio | 账户、订单、SymbolProfile、组合表现 | 组合状态与长期财富管理 |
| OpenBB | provider 接入、标准模型、金融数据查询 | 外部金融事实如何被统一接入和消费 |

**对本项目判断：** OpenBB 主要解决“金融事实获取与标准化”，不拥有用户的投资理由，也不判断一条证据对 thesis 是 supporting 还是 contradicting。它可以给判断提供材料，却不是投资判断系统。

---

## 2. Provider Architecture

这是 OpenBB 对 Investment Tracker 最值得学习的部分。

### 2.1 核心对象和数据流

**事实：** 固定 commit 中的主要角色如下：

| 角色 | 职责 | 主要证据 |
| --- | --- | --- |
| Router | 声明用户可调用的命令，并用 `model="..."` 绑定 standard model | [Equity Router][src-equity-router]、[Price Router][src-price-router]、[News Router][src-news-router] |
| Standard Model | 定义跨 provider 的 canonical query/data 字段 | [standard models 目录][src-standard-models] |
| Provider | 声明名称、credentials 和 `fetcher_dict`，把 standard model 名映射到 fetcher | [Provider][src-provider] |
| Fetcher | 声明 query type、return type，并执行 Transform Query → Extract → Transform Data | [Fetcher][src-fetcher] |
| Registry / RegistryMap | 发现 provider extensions，建立 standard/provider 字段和能力映射 | [Registry][src-registry]、[RegistryMap][src-registry-map] |
| ProviderInterface | 按当前安装的 provider 动态组合 query/result schema 与可选 provider | [ProviderInterface][src-provider-interface] |
| Container | 未显式指定 provider 时，按照 defaults/可用 credentials 选择一个 provider | [Container][src-container] |
| QueryExecutor | 校验 query、取得指定 provider 的 fetcher、注入 credentials 并执行 | [QueryExecutor][src-query-executor] |
| OBBject | 统一包裹 results、provider、warnings、chart 和 extra | [OBBject][src-obbject] |

可把一次调用概括为：

```text
Router command
  → standard model name
  → installed provider map
  → selected provider + fetcher
  → provider query transformation
  → upstream extraction
  → provider data transformation
  → standard fields + provider-specific extra fields
  → OBBject(results, provider, warnings, extra)
```

### 2.2 不同 provider 如何接入

**事实：** Provider extension 通过 Python entry point 注册。一个 provider 是一组 fetchers；每个 fetcher 对应一个 standard model，实现自己的 query 参数扩展、上游请求和返回映射。官方开发文档也把 Fetcher 描述为执行 TET 模式的单元。[Provider Extension 文档][docs-provider-extension] [Architecture Overview][docs-architecture]

**事实：** `Fetcher` 将职责明确分成：

1. `transform_query`：把 canonical query 和 provider-specific query 转成 provider 请求；
2. `extract_data` / `aextract_data`：取得原始响应；
3. `transform_data`：清洗、计算、别名映射并实例化 provider return model。

**源码推断：** 这让 provider 差异集中在 adapter 边界，而不是泄漏到每个业务调用方。但 TET 也意味着结果可能经过相当多处理；“来自某 provider”不等于“上游原始响应原样返回”。

### 2.3 Provider-specific 数据如何进入统一模型

**事实：** Provider query/data model 通常继承 standard model，再增加字段或 alias。`RegistryMap` 依据字段的定义来源区分 standard 和 provider-specific 字段，`ProviderInterface` 再为当前安装组合生成调用签名和返回类型。[RegistryMap][src-registry-map] [ProviderInterface][src-provider-interface]

**事实：** 基础 `Data`/`QueryParams` 允许额外字段；因此标准化并不必然把 provider-specific 字段全部删掉。结果可以同时拥有 canonical 字段和该 provider 的扩展字段。[Data][src-data] [QueryParams][src-query-params]

**事实：** 不被目标 provider 支持的额外 query 参数会被过滤，并通过 warnings 暴露；字段校验失败、空数据和 provider 请求错误则会抛出相应错误或警告。[QueryExecutor][src-query-executor] [Query Parameters 文档][docs-query-params]

**源码推断：** “统一模型”在这里是一个稳定的最小公共表面，不是保证所有 provider 语义完全相同的全球数据字典。上层若只保留 canonical 字段，provider extension 中的 filing date、adjustment、source ID、currency 等关键信息仍可能被下游自己丢失。

### 2.4 上层是否需要知道 provider

**事实：** 用户可以显式传 `provider="..."`；未传时，系统从该命令的默认优先级中选择第一个已安装且 credentials 完整的 provider。用户也可为不同命令配置 provider priority list。[Data Sources 文档][docs-data-sources] [Defaults 文档][docs-defaults]

**事实：** 同一个 standard model 可以由多个 provider 实现。例如 `EquityHistorical` 在固定 commit 中由多个行情 provider 实现，统一入口仍是同一个 router command。[Price Router][src-price-router] [Equity Historical][sm-equity-historical]

**对本项目判断：** 普通展示型页面可以把 provider 选择隐藏在 adapter 内；但 Evidence 创建、回溯和比较不能隐藏。Evidence 必须知道“本次究竟使用了谁、以什么参数和口径”。

### 2.5 失败、缺字段和能力差异如何暴露

**事实：** 差异通过以下方式暴露：

- 命令签名和文档列出 provider-specific 参数和返回字段；
- 非目标 provider 支持的 kwargs 被过滤并进入 warnings；
- canonical 必填字段由 Pydantic 校验；可选缺失字段通常为 `None`；
- provider 可抛出空数据、授权、HTTP、解析或模型校验错误；
- 多 symbol 等场景的局部失败可进入 warnings，具体行为依 fetcher；
- 不存在跨 provider 统一的 completeness、quality score 或 missing-reason 模型。

**源码推断：** 统一的 Python 类型改善了接口可预测性，但并未把“供应商缺数”“原始值确实为空”“字段不适用于该证券”“转换失败”统一编码为可审计状态。

### 2.6 Metadata 是否进入返回结果

**事实：** `OBBject.provider` 保存执行使用的 provider。默认启用 metadata 时，`OBBject.extra["metadata"]` 可包含 route、arguments、timestamp 和 duration；warnings 另有字段。[CommandRunner][src-command-runner] [OBBject][src-obbject]

**事实：** Fetcher 也可返回 `AnnotatedResult(result, metadata)`，其 metadata 会进入 `extra["results_metadata"]`。FRED 会在这里附带 title、units、frequency、notes 等系列元数据；SEC 财务 statement 实现会返回字段来源和验证诊断等丰富信息。[AnnotatedResult][src-annotated-result] [FRED Series][provider-fred-series] [SEC statement schema][provider-sec-statement-readme]

**源码推断：** Metadata 是“可扩展通道”，不是跨 model 强制的 provenance contract。应用若想依赖它，必须为每个 endpoint/provider 建立明确提取规则。

### 2.7 对 canonical research data 边界的借鉴

**对本项目判断：** 值得借鉴的不是复制 OpenBB 全部 standard models，而是以下模式：

1. **内部 canonical 概念与外部 adapter 分离。** Thesis/Evidence 不依赖 FMP、Yahoo 或 SEC 字段名。
2. **canonical 字段只承诺共同语义，provider extras 原样保留在受控命名空间。** 不要为“整齐”而删除 filing/accession/vintage 等信息。
3. **输入和输出都保留 adapter/version 上下文。** 同一个 provider 的映射代码升级也会改变结果。
4. **显式能力表。** 每个 provider 对 price、filing、fundamentals、news、PIT、license 的支持要分别声明，不能只有“支持股票”。
5. **失败可见。** 缺失、不适用、权限不足、解析失败和无数据应是不同状态。
6. **Evidence 路径禁止静默换源。** 展示页面可择优，Evidence 创建必须显式 provider 或记录实际选择。

---

## 3. Asset / Security Symbology

### 3.1 当前实现的事实

**事实：** OpenBB 为 equity、ETF、index、crypto、currency/FX 等建立了不同 router 和 standard models；查询主体通常仍是字符串 `symbol`。典型 search model 的 canonical 返回很薄：

- `EquitySearch`：`symbol`、`name`；
- `EtfSearch`：`symbol`、`name`；
- `IndexSearch`：`symbol`、`name`；
- `CryptoSearch`：`symbol`、`name`；
- 历史行情类通常以 `symbol` 输入，返回 date/OHLC 等。

参见 [EquitySearch][sm-equity-search]、[ETF Search][sm-etf-search]、[Index Search][sm-index-search]、[Crypto Search][sm-crypto-search]。

**事实：** 固定 commit 中没有独立的 mutual fund router、search standard model 或 provider extension。ETF router 的 SEC `nport_disclosure` 可查询美国 ETF 或 mutual fund 的 NPORT-P 披露，但这不是通用基金主数据、净值、持仓和搜索能力。[ETF Router][src-etf-router]

**事实：** `EquityInfo` 比 search 丰富，可包含 CIK、CUSIP、ISIN、LEI、stock exchange、法律名称和总部国家等；但这些字段可为空，且它是 provider 查询结果，不是 OpenBB 自己维护的全局 Security Master。[EquityInfo][sm-equity-info]

**事实：** Core 中存在 ISO 10383 MIC 的 exchange reference 和 country 标准化工具，数据中包含 `XSHG`、`XSHE`、`XHKG` 等 MIC。[exchange_data.json][src-exchange-data] [Exchange utils][src-exchange-utils] [Country utils][src-country-utils]

**事实：** 官方 query 文档明确提醒：同一证券在不同 provider 可能有不同 share-class、exchange suffix 或 global composite 格式，并给出 `brk.b`、`brk-b`、`brk.a:us` 等差异；海外证券通常使用 provider-specific suffix。[Query Parameters 文档][docs-query-params]

### 3.2 Identity 结论

**源码推断：** OpenBB 解决的是“在某个 provider 下用某个 symbol 发起查询”，不是“为现实世界证券分配永久统一 ID”。MIC/ISIN/CIK 等工具和字段提高映射能力，却没有组合成强制、唯一、版本化的 asset master。

**源码推断：** 同一真实证券可能同时拥有：本地 ticker、交易所后缀 symbol、provider internal ID、ISIN、CUSIP、CIK、LEI；不同 share class、dual listing、ADR 和代码复用会让单独 ticker 不足以构成 identity。

### 3.3 与 Wealthfolio / Ghostfolio 的比较

**对本项目判断：** Wealthfolio/Ghostfolio 需要拥有内部 `asset_id`，因为账户活动、持仓和历史记录必须长期指向同一对象。OpenBB 不承担这种生命周期，所以它可以主要以 symbol 为入口。Investment Tracker 更接近前者：

```text
internal asset_id
  ↕
listing identity (MIC + local ticker + validity interval)
  ↕
provider identifiers (provider + provider_symbol/provider_id)
```

这里是语义关系，不是数据库 schema。至少要允许一个资产对应多个 listing、一个 listing 对应多个 provider identifier，并允许映射随时间变化。

### 3.4 A 股、港股、美股的标识限制

**事实：** 固定 commit 中没有 AkShare、Tushare、Eastmoney、SSE、SZSE 或 HKEX provider extension。存在 MIC 不表示对应交易所的证券搜索、行情、财务和公告已被实现。[Providers 目录][src-providers]

**源码推断：** yfinance/FMP/Intrinio 等全球型 provider 可能接受带 `.SS`、`.SZ`、`.HK` 或自身格式的准确 symbol；是否可查、覆盖哪些字段和历史区间仍由 provider 决定。OpenBB 的通用 search endpoint 并不能替用户保证这些 symbol 被正确发现、去重和映射。

**对本项目判断：** 不能把 symbol suffix 当作资产主键，也不能把“某次查询返回结果”外推为 A/H/美股统一 identity 已解决。进入中国市场前，必须单独验证证券主数据、退市/更名、复权、币种、交易日历和跨市场映射。

---

## 4. Point-in-Time 数据能力

### 4.1 判定标准

**对本项目判断：** 一个接口要可靠回答“2025-03-01 当时能知道什么”，至少要同时满足：

1. 有明确的 publication/filing cutoff，而不只是 observation date；
2. 能选择截止当时可见的 vintage，而不是今天修订后的历史值；
3. 调整、重述、估算、派生等变换可识别；
4. 查询结果及来源可冻结，未来能重放或验证；
5. provider 保留足够历史，并有明确的数据许可和时间语义。

OpenBB 的通用 standard models 没有提供这套统一契约。

### 4.2 分数据类型评估

| 数据类型 | 已有时间语义（事实） | PIT 能力 | 主要缺口 |
| --- | --- | --- | --- |
| Market price | 历史 OHLC 有 observation date/datetime；provider 可扩展 interval、adjustment、actions | **中等，有限条件下可用** | 复权口径、公司行动和纠错会改写历史；无统一 captured_at snapshot/vintage |
| Fundamentals | 常见 period/date/TTM 等依 endpoint/provider | **弱** | 指标可能用今天可得的重述财务；发布时间、计算版本和 source 不统一 |
| Earnings | `report_date`、previous/consensus 等；actual 和 report time 多为 provider extras | **弱** | 历史 consensus/estimate vintage 常不可恢复；“最终实际值”可能在当时尚未知 |
| Financial statements | canonical 有 `period_ending`、`fiscal_period`、`fiscal_year`；SEC 有 opt-in `pit_mode` | **通用弱、SEC 局部较强** | 默认可能是 later-restated；无跨 provider as-of；filing cutoff 和 row-level filing lineage 不统一 |
| Company filings | canonical 有 filing date、type、report URL；SEC extra 有 report date、accession 和文档 URL | **SEC 场景较强** | 通用模型没有 accepted timestamp/report period/source ID；其他市场覆盖不一 |
| Macroeconomic | observation date；calendar 可含 event time、previous/revised/actual；provider metadata 可含频率/单位 | **弱到中等，依 provider** | FRED 通用 series 不暴露 vintage 查询，且删除返回中的 realtime range；修订历史不统一 |
| News | publication datetime、title、author、body/excerpt、URL | **只能做 publication cutoff，不能保证历史版本** | 后续编辑、下架、付费墙、provider 留存变化；无 capture/version/archive 契约 |

### 4.3 Market price 不是天然 PIT 正确

**事实：** `EquityHistorical` canonical fields 是 `date, open, high, low, close, volume, vwap`，没有统一 currency、exchange、adjustment method 或 source 字段。[EquityHistorical][sm-equity-historical]

**事实：** Provider 的复权能力不同：FMP 有 splits-only、splits-and-dividends、unadjusted 等选择；YFinance 暴露 adjustment/actions；Tiingo 同时提供 adjusted OHLC/volume、split 和 dividend 等 provider fields。[FMP Equity Historical][provider-fmp-historical] [YFinance Equity Historical][provider-yf-historical] [Tiingo Equity Historical][provider-tiingo-historical]

**源码推断：** 如果 2027 年回查 2025 年价格而没有保存 adjustment 口径和原始结果，拆股、分红或供应商纠错可能使“同一天的 close”与用户当时看到的不同。市场价格通常比财务数据更接近 PIT，但仍需明确“当时显示价格”还是“后来复权后的可比价格”。

### 4.4 财务和宏观的局部 PIT 能力

**事实：** SEC 的 IncomeStatement、BalanceSheet、CashFlow provider query 都有 `pit_mode` 和 `include_preliminary`。`pit_mode=True` 旨在保留原始 filing vintage，尤其避免用 10-K 中的后来比较数覆盖原 10-Q 季度值；官方源码说明明确把 backtesting、event studies 和 PIT databases 列为适用场景。[SEC Income Statement][provider-sec-income] [SEC Balance Sheet][provider-sec-balance] [SEC Cash Flow][provider-sec-cash] [SEC statement schema][provider-sec-statement-readme]

**事实：** `pit_mode` 默认是 false。默认模式优先跨报表/年度一致性，可能使某个完成季度反映后来 10-K 的重述值；源码文档直接说明这会产生 look-ahead 风险。[SEC statement schema][provider-sec-statement-readme]

**源码推断：** 这是 OpenBB 中非常有价值的 provider-specific PIT 实现，但不是平台级承诺：

- 只适用于 SEC statement provider 的特定模型；
- 没有通用 `as_of=2025-03-01` 参数；
- 调用方仍需依据 filing/publication time 做 cutoff；
- annual/original、8-K preliminary、amendment 和 derived Q4 的语义仍要随 metadata 一起解释；
- 其他 provider 的同名 standard model不因此获得 PIT 性质。

**事实：** FRED `/series/observations` 原始响应带 `realtime_start`/`realtime_end`，但固定 commit 的 `FredSeriesFetcher` 在转换中明确删除这两个字段，standard query 也未暴露 `vintage_date` 或 realtime range。[FRED Series provider][provider-fred-series] [FRED Series standard model][sm-fred-series]

**源码推断：** FRED 本身具备 ALFRED/vintage 体系，并不等于当前 OpenBB `FredSeries` 标准入口保留了该能力。用今天的结果回放过去宏观环境会读到 revised history。

### 4.5 能否回答“2025 年 3 月 1 日当时能知道什么？”

**结论：不能由 OpenBB 通用层可靠、完整地回答。**

**对本项目判断：** 更准确的表述是：OpenBB 可以成为构建该答案的若干 adapter，尤其适合 SEC filings、带明确时间的历史行情和少数 provider-specific PIT 数据；但 Investment Tracker 必须另外实现：

- as-of cutoff 规则；
- publication/filing/accepted time 解析；
- vintage-aware provider capability；
- raw/normalized snapshot 保存；
- 后续 revision 的关联；
- “当时未知”而非空值补全；
- 可重复的 evidence selection policy。

---

## 5. 财务数据修订与 Restatement

### 5.1 财务报表是否可能返回后来重述后的历史值

**事实：会。** SEC statement schema 的设计说明明确表示，默认模式会选择较新的 filing vintage 以增强跨报表和年度一致性，并可能让早期季度显示后来年度文件中的重述比较数。[SEC statement schema][provider-sec-statement-readme]

**事实：** FMP 的 statement provider model 可附加 `filing_date`、`accepted_date`、`reported_currency`、CIK 等，但 standard IncomeStatement/BalanceSheet/CashFlow 只强制 `period_ending`、`fiscal_period`、`fiscal_year`；具体财务科目本身也是 provider 扩展。[IncomeStatement][sm-income] [BalanceSheet][sm-balance] [CashFlow][sm-cash] [FMP Income Statement][provider-fmp-income]

**源码推断：** 即便 provider 返回 filing date，也不能仅凭 `period_ending` 判断某个值何时可知。若供应商用最新重述覆盖历史行，今天查询旧期间仍会看到未来信息。

### 5.2 original filing 与 restatement

**事实：** SEC `pit_mode` 能改变 filing vintage 选择，使季度值来自原 10-Q，而不是后来 10-K comparative；`include_preliminary` 可使特定 8-K preliminary filings 参与选择。statement metadata 还能标记 XBRL source、fallback、imputed、Q4-derived、vintage-corrected 等转换来源和诊断。[SEC statement schema][provider-sec-statement-readme]

**源码推断：** 这比普通标准财务接口强很多，但返回的宽表记录仍不是一个通用 revision ledger。调用方不一定直接得到每个数值完整的 accession、accepted timestamp、原始 XBRL fact 和所有中间版本。要比较 original vs restated，仍需保留两个版本并建立关联。

### 5.3 宏观 revision

**事实：** `EconomicCalendar` canonical model 有 `previous`、`revised`、`actual`，可表达某次事件附近的修订状态；它还可包含 source、currency 和 unit。[EconomicCalendar][sm-economic-calendar]

**事实：** 一般 `EconomicIndicators` 只有 observation date、symbol/country/value，单位和频率可能来自 provider extras；FRED Series 的 realtime range 在当前转换中被删除。[EconomicIndicators][sm-economic-indicators] [FRED Series provider][provider-fred-series]

**源码推断：** `revised` 字段是一次事件的修订提示，不是完整 vintage history。没有 `value valid_from/valid_to` 或 vintage query，就无法保证重建某天用户看到的 CPI/GDP/就业值。

### 5.4 Hindsight bias 风险

**对本项目判断：** 如果 Context Reconstruction 只按 observation/fiscal period 过滤，至少会产生五种后见偏差：

1. 把后来重述的季度收入或毛利率当作当时已知；
2. 把后来发布的年报 comparative 当成原季报内容；
3. 把后来修订的宏观数据当作当时经济环境；
4. 把今天存活、可访问的新闻集合当作当时所有/唯一新闻；
5. 用后复权价格替代用户当时屏幕上的名义价格而未说明。

因此 Context Reconstruction 必须表达“不确定是否为当时版本”，而不是仅返回一个看似精确的历史数值。

---

## 6. News / Filings / Documents

### 6.1 News

**事实：** 固定 commit 中 CompanyNews 可由 Benzinga、FMP、Intrinio、Tiingo、TMX、YFinance 等 provider 实现；WorldNews 另有自己的 provider 组合。具体 provider 可安装、移除，覆盖和授权各自不同。[Providers 目录][src-providers] [Company News 文档][docs-company-news]

**事实：** `CompanyNews` canonical fields 包括：

- `date`（文章发布日期时间）；
- `title`；
- `author`；
- `excerpt`；
- `body`；
- `images`；
- `url`；
- `symbols`。

其中 author/body/excerpt 等可以为空，canonical model 没有强制 `source`、provider article ID、updated time、language 或 version。[CompanyNews][sm-company-news]

**源码推断：** Provider extras 可能补充 source、ID、channels、updated time 等，但不存在跨 provider 一致保证。URL 是验证入口，不是内容冻结：旧文章可能编辑、下架、迁移、加入付费墙或被 provider 移出历史窗口。

### 6.2 Company filings

**事实：** `CompanyFilings` canonical fields 只有 `filing_date`、`report_type`、`report_url`；symbol 是 query，不是每行强制字段。[CompanyFilings][sm-company-filings]

**事实：** SEC provider 显著扩展了该模型，包括 report date、accession number、primary document、complete submission URL、detail URL 和 XBRL flags 等；`HtmFile` 等 endpoint 还能抓取指定 SEC HTML 文档正文。[SEC CompanyFilings][provider-sec-filings] [SEC HtmFile][provider-sec-htm]

**事实：** SEC 官方提供 submissions、XBRL API、daily/quarterly indexes 和历史 archives；同时要求声明自动化客户端并遵守 fair-access 限速。OpenBB connector 不改变这些上游约束。[SEC Developer Resources][sec-developer]

**源码推断：** 对美国上市公司，SEC accession + 官方 URL + filing/accepted time 是目前研究中最接近稳定、可验证 Evidence 的组合。对非 SEC 市场，通用 CompanyFilings model 本身不足以保证 report period、原始 identifier、正文、修订关系或永久可访问性。

### 6.3 Evidence，不只是 AI summary

**对本项目判断：** 新闻或 filing 被 AI 总结前，应先形成可验证 Evidence：

```text
upstream document identity
+ provider identity
+ publication/filing/captured time
+ original excerpt or immutable snapshot/hash
+ normalized fields
+ AI interpretation (separate, revisable)
```

仅保存 title + URL + summary 不够：URL 可能变化，summary 无法证明原文，且后来无法判断模型当时引用了哪个版本。

---

## 7. Provenance

### 7.1 OpenBB 通用返回能够回答什么

| 问题 | 通用层现状 | 评价 |
| --- | --- | --- |
| 来自哪个 OpenBB provider？ | `OBBject.provider` 明确记录 | **较好**，前提是下游保存它 |
| 对应哪个原始数据源？ | provider 名可见；上游 dataset/source/ID/URL 依模型和 provider | **不统一** |
| 查询时间？ | 默认 metadata 可含命令执行 timestamp | **有，但不是持久快照** |
| 数据观察时间？ | price/macro 等模型通常有 date/datetime | **依模型较好**，但 date 的业务含义仍要确认 |
| 发布/filing/revision 时间？ | news/filing/少数 provider 有；standard model 不统一 | **不足** |
| 单位？ | 一些 canonical/provider metadata 有；财务 statement 不统一 | **不足** |
| 币种？ | quote/calendar/部分 statement extras 有；HistoricalPrice canonical 没有 | **不足** |
| 数据频率？ | query interval 或 provider metadata 常有 | **可推知但不统一落在结果** |
| 是否经过 OpenBB 标准化？ | 由调用 route/model 可知，但没有每行统一标记 | **隐含** |
| 是否经过 provider 二次加工？ | provider code 可审计，少数 metadata 标出 derived/imputed | **通常不显式** |
| 质量/缺失标记？ | warnings、validation error、SEC diagnostics 局部存在 | **无统一 contract** |

**事实：** `CommandRunner` 在 metadata 开启时记录 arguments、route、timestamp 和 duration；OBBject 单独记录 provider 和 warnings。[CommandRunner][src-command-runner]

**事实：** `AnnotatedResult` 允许 provider 返回自定义 metadata，但没有规定每个 provider 必须提供统一的 source、unit、currency、revision 或 quality 字段。[AnnotatedResult][src-annotated-result]

**源码推断：** OpenBB 的 provenance 达到 **invocation-level lineage**：能知道调用了什么 OpenBB 命令、实际用了哪个 provider、传了哪些参数、何时完成。它还没有达到通用 **fact-level lineage**：每个数值来自哪个原始记录、在什么版本首次/最后有效、经过哪些转换。

### 7.2 标准化与上游来源之间的断点

**事实：** Provider fetcher 可以执行 alias mapping、单位/类型转换、排序、复权、宽表 pivot、季度值推导、imputation 和 validation。SEC statement 是最明显的例子，FRED Series 也会把动态 series value 列组织为结果并删除 realtime 字段。[SEC statement schema][provider-sec-statement-readme] [FRED Series provider][provider-fred-series]

**源码推断：** 仅保存 standard result 可能无法重建以下内容：

- 原始 provider payload；
- provider API endpoint 与上游 dataset version；
- 当时使用的字段 alias/mapping 版本；
- 某个值是直接报告、换算、复权、推导还是填补；
- 被 standardization 忽略或下游投影掉的 provider extras；
- 返回为空的真实原因。

### 7.3 Evidence 至少应保存的 provenance 语义

**对本项目判断：** Evidence 的最低语义不是一个值，而是一个“可验证事实包”。至少需要：

- **identity**：稳定的 `evidence_id`；
- **subject**：关联的 internal asset/issuer/thesis，不直接以 provider symbol 代替；
- **type**：price、metric、filing、news、macro、user observation 等；
- **original content**：原始值、原文摘录，或指向不可变 raw snapshot 的引用；
- **upstream source**：原始机构/出版物/数据集，而不只写 OpenBB；
- **adapter/provider**：OpenBB provider、endpoint/route、provider identifier；
- **time semantics**：observation period、publication/filing/accepted/revision time、captured_at；未知必须保持未知；
- **measurement context**：currency、unit、scale、frequency、period type、adjustment basis；
- **raw identity**：accession/article/dataset/series ID、canonical URL；
- **capture integrity**：raw/normalized snapshot hash、content type、抓取状态；
- **transformation context**：standard model、provider mapping/adapter version、query、派生/复权/填补说明；
- **quality context**：缺失、部分成功、冲突、估算、preliminary、restated、provider warning；
- **interpretation state**：尚未解释、AI 建议、人已确认、需复核；解释与事实内容分离。

这不是数据库 schema；关键是这些语义不能在“先存一个 value，以后再补”时被恢复。

---

## 8. 与本项目最相关的 Standard Models

### 8.1 模型对比

下表中的 canonical fields 只列研究关键字段，不代表完整 provider 返回。

| 当前源码模型 | 关键 canonical fields | 时间/单位/source | 直接作为 Evidence？ | 标准化或只取 canonical 后的风险 |
| --- | --- | --- | --- | --- |
| `EquityHistorical` | date, OHLC, volume, vwap | 有 observation date；无统一 currency、exchange、adjustment、source | **条件性可用** | provider 的 adjustment/actions/adjusted fields 可能被忽略 |
| `EquitySearch` | symbol, name | 无 identity validity、MIC、country 强制字段 | **不可作为事实证据**；只适合发现候选 | provider-specific exchange/type/ID 可能不在 canonical 中 |
| `EquityInfo` | symbol/name、CIK/CUSIP/ISIN/LEI、stock_exchange、行业和地址等 | `latest_filing_date` 等少数字段；无 identity version | **可作参考事实，需 provider/capture** | 多数 identifier 可空，无法替代内部 asset master |
| `IncomeStatement` | period_ending, fiscal_period, fiscal_year | 标准层无 filing/publication time、currency、unit；财务科目由 provider 扩展 | **不可直接无条件使用** | 容易丢失 filing date、reported currency、PIT/restatement 语义 |
| `BalanceSheet` | 同上 | 同上 | **不可直接无条件使用** | 同上；瞬时值和 filing vintage 仍需区分 |
| `CashFlow` | 同上 | 同上 | **不可直接无条件使用** | 季度/累计/derived Q4 等含义容易被压平 |
| `CalendarEarnings` | report_date, symbol, name, eps_previous, eps_consensus | 有 report date；无 canonical estimate vintage/source | **仅作事件线索** | actual、time-of-day、currency、updated time 常是 extras；历史 consensus 可能已改 |
| `CompanyNews` | publication datetime, title, author, excerpt/body, URL, symbols | 有 publication time/URL；无 canonical source、updated/version/language | **可形成 Evidence 候选** | 原文版本和 provider article ID 不保证；正文可空 |
| `CompanyFilings` | filing_date, report_type, report_url | 有 filing date/URL；无 canonical report period/accession/accepted time/source | **SEC provider 条件下较适合** | 只取 canonical 会丢 SEC accession、complete submission、report date 等 |
| `EconomicCalendar` | event datetime, country/category/event, source, currency/unit, consensus/previous/revised/actual | 时间和测量语义相对丰富 | **可作事件 Evidence 候选** | revised 是当前记录中的字段，不等于完整 revision history |
| `EconomicIndicators` | date, symbol_root/symbol, country, value | frequency 是 query；unit/scale 常为 provider extras | **条件性可用** | 缺 publication/revision/vintage；series definition 易丢 |
| `FredSeries` | date；series values 是动态列 | metadata 可有 title/unit/frequency/notes；realtime range 被删除 | **不适合直接做 PIT Evidence** | 明确丢失 FRED realtime/vintage 字段 |

模型源码见 [standard models 目录][src-standard-models]，重点包括 [EquityHistorical][sm-equity-historical]、[EquityInfo][sm-equity-info]、[IncomeStatement][sm-income]、[CompanyNews][sm-company-news]、[CompanyFilings][sm-company-filings] 和 [EconomicCalendar][sm-economic-calendar]。

### 8.2 Provider mapping 的真实含义

**事实：** Provider return model 继承 standard data model，使用 aliases 和 validator 把上游字段转换成 canonical 名，同时可以保留额外字段。例如不同历史行情 provider 对复权字段有不同扩展，FMP statement 增加 filing/accepted/currency 等信息，SEC filings 增加 accession 和文档 URL。[FMP Equity Historical][provider-fmp-historical] [FMP Income Statement][provider-fmp-income] [SEC CompanyFilings][provider-sec-filings]

**源码推断：** Standard model 最适合作为“查询和最低字段互操作层”，不适合作为 Evidence 的完整持久模型。尤其财务 statement 的 canonical 基类只规定期间键，真正科目和 provenance 大量留在 provider model 中。

### 8.3 哪些信息算“丢失”

需要区分两种情况：

1. **OpenBB 转换时明确丢失。** 例如 FRED Series 删除 `realtime_start`/`realtime_end`。
2. **OpenBB 仍返回 extras，但下游只使用 canonical projection 时丢失。** 例如 SEC accession、FMP accepted date、YFinance actions、Tiingo adjusted fields。

**对本项目判断：** Adapter ingestion 时应同时保存：canonical projection、provider extras、raw snapshot/reference。否则“接口中曾经有”对几年后的审计没有帮助。

---

## 9. Provider 差异与 fallback 风险

### 9.1 OpenBB 的 fallback 到底是什么

**事实：** 未显式指定 provider 时，`Container` 会按 command defaults 或 provider priority list，选择第一个已安装且具备所需 credentials 的 provider。若无自定义配置，顺序来自当前命令可用 provider 的默认列表。[Container][src-container] [Defaults 文档][docs-defaults]

**事实：** 一旦 provider 被选择，`QueryExecutor` 就取得该 provider 对应的 fetcher 并执行；固定 commit 中没有“Provider A 请求报错或返回空后，自动执行 Provider B”的通用重试链。[QueryExecutor][src-query-executor]

**结论：** OpenBB 有的是 **pre-execution provider selection/fallback**，不是 **post-failure data failover**。官方资料有时把前者简称 fallback，二者不可混同。

### 9.2 即使自行 failover，也会有哪些风险

**事实与源码推断：** 两个 provider 即使实现同一个 standard model，仍可能不同：

- symbol 和 exchange suffix；
- 价格 adjustment method、交易时段和 timezone；
- 财务科目映射、季度累计拆分和 restatement 选择；
- earnings consensus 的采样时点和贡献者集合；
- news 的发布时间、抓取版本和正文权限；
- macro source、seasonal adjustment、unit/scale；
- 历史覆盖、空值、延迟和授权等级。

**事实：** OpenBB 的 provider-specific query/data schema 正是为了暴露这些差异，而不是宣称它们不存在。[Standardization 文档][docs-standardization]

### 9.3 对 Investment Tracker 的结论

```text
Evidence ≠ value

Evidence = value/content
         + upstream source
         + provider
         + original metadata
         + time semantics
         + captured_at
         + immutable snapshot/hash
         + transformation/quality context
```

**对本项目判断：** Evidence 创建不得静默 failover。如果确实重试 Provider B，应产生可见的 capture attempt 记录，并把最终 provider 放入 Evidence；若 A/B 值冲突，应保留冲突而不是“选一个看起来合理的”。

---

## 10. Caching / Historical Replay

### 10.1 缓存现状

**事实：** 固定 commit 没有一个覆盖全部 ODP 查询、以 Evidence 为目标的统一结果缓存。缓存是 provider/endpoint 自主实现的。例如：

- SEC statement 暴露 `use_cache`，用于短时复用 provider 侧处理结果；
- SEC CompanyFilings 使用 HTTP cache 机制并有到期策略；
- EconDB 等 provider 在部分 endpoint 使用自己的时效缓存；
- FRED 的 rate limiter/response cache 使用短 TTL，并按请求 URL 组织，API key 会被排除在安全日志/键处理之外的相应路径中。

参见 [SEC Income Statement][provider-sec-income]、[SEC CompanyFilings][provider-sec-filings]、[FRED rate limiter][provider-fred-cache]。

**源码推断：** 这些缓存目标是速度、限流和稳定性，不是历史审计。它们没有形成统一的：

- cache key contract（provider + endpoint + normalized query + credential tier + adapter version）；
- immutable content address；
- retention policy；
- revision chain；
- 用户可调用的 replay/snapshot API。

### 10.2 后来修订的数据会怎样

**源码推断：** 缓存过期后，重新请求会取得 provider 当时的新响应。若 provider 改写历史、OpenBB mapping 改版、权限等级改变或 symbol 映射变化，旧结果不会因曾被短期缓存而自动可恢复。

**事实：** `OBBject.extra.metadata.timestamp` 是该次执行的时间；OpenBB 不会仅因为生成了 OBBject 就自动把完整响应长期持久化为不可变 artifact。[CommandRunner][src-command-runner]

### 10.3 是否支持 historical replay

**结论：** 通用层没有“重放用户当初看到的同一结果”的能力。个别上游源本身有 archives/vintages，不等于 OpenBB 已为所有 provider 提供统一 replay。

**对本项目判断：** Investment Tracker 必须自行保存关键 Evidence Snapshot，原因包括：

1. provider 历史值会修订；
2. 新闻和网页会编辑或消失；
3. OpenBB/provider mapping 会升级；
4. 数据权限或订阅可能终止；
5. fallback/provider priority 会变化；
6. 只有本系统知道哪条内容实际进入了当时的用户判断。

建议冻结“原始响应或合规允许保存的最小原文 + canonical projection + provider extras + capture manifest + hash”。保存范围仍须受各数据许可约束。

---

## 11. AI / Agent / MCP / Workspace

### 11.1 AI 获得什么

**事实：** 固定 commit 的 `openbb-mcp-server` 以 FastAPI app/OpenAPI routes 为基础，把 OpenBB API 分类暴露为 MCP tools/resources，支持 `stdio`、SSE 和 streamable HTTP，并可按 session 发现、启用或禁用工具类别。[MCP Server README][src-mcp-readme]

**源码推断：** 对普通 OpenBB endpoint，agent 取得的是 route 的序列化输出，即 standard/provider result + OBBject wrapper metadata，而不是 provider 原始 HTTP payload。除非某个 endpoint 本身返回原始文档/数据，或自定义 route 明确暴露 raw 内容。

### 11.2 Citation 能力

**事实：** OpenBB Workspace 可以把 MCP tool 与 widget 精确匹配，并为 tool response 生成匹配 citation；配置要求 `mcp_server` 和 `tool_id` 一一对应。[Matching widget to MCP tool][workspace-mcp-citation]

**事实：** 自定义 Workspace agent 也可以使用 OpenBB AI SDK 主动构造并流式发送 citations，把回答关联到 widget/数据源和输入参数。[Highlight widget citations][workspace-agent-citation]

**源码推断：** 这是“支持 citation 的 UI/协议”，不是“任何模型结论自动具有正确来源”。是否引用、引用粒度、引用是否指向原始文档、tool response 是否已丢失 vintage，仍取决于 endpoint、widget 配置和 agent 实现。

### 11.3 事实、解释和缺失值

**事实：** OpenBB standard/provider models 区分 typed data fields 和 metadata/warnings，但没有一个通用 agent output schema 强制每句话标注 `FACT`/`INTERPRETATION`，也没有跨模型机制保证 LLM 不把 `None`、缺字段或无结果补全成事实。

**对本项目判断：** MCP 只降低“AI 调用可靠工具”的接入成本，不解决：

- source-of-truth 边界；
- point-in-time 数据正确性；
- prompt injection/错误文档；
- narrative causal claim 的证据充分性；
- missing/unknown 的守恒；
- supporting/contradicting 的最终责任。

因此 OpenBB 可作为 Evidence Interpreter 的工具层，但不能作为解释结论的真实性担保。

---

## 12. 数据许可与商业化边界

### 12.1 两种许可证必须分开

**事实：** OpenBB 仓库代码使用 AGPLv3；完整条款以固定 commit 的 LICENSE 为准。[LICENSE][repo-license]

**事实：** 官方 provider 文档明确说明 OpenBB 不托管或提供数据，而是提供 connectors；不同 provider 是可独立安装/移除的 extension，许多需要 API key，既有 free 也有 paid provider。[Providers 文档][docs-providers]

因此必须分开：

```text
OpenBB 软件许可证
≠
每个上游金融数据/文档/新闻的访问、存储、展示和再分发许可
```

### 12.2 免费不等于可商业再分发

**事实：** FRED API 条款明确提示部分 series 由第三方拥有并受版权限制，FRED 提供访问不覆盖数据所有者的限制。[FRED API Terms][fred-terms]

**事实：** yfinance 项目声明其工具用于 research/education，并提醒 Yahoo Finance API/data 的权利受 Yahoo 条款约束、面向 personal use；OpenBB 安装 `openbb-yfinance` 不会改变该上游条件。[yfinance README][yfinance-readme]

**事实：** SEC 提供公开 filings、XBRL API 和 archives，但自动访问仍要遵守 SEC 的 fair-access 与客户端声明要求。[SEC Developer Resources][sec-developer]

**源码推断：** “无需 API key”“公开网页可访问”“OpenBB 标为 Free”都不能单独证明允许把数据缓存多年、展示给付费用户、批量导出或再分发正文。

### 12.3 商业 provider

**事实：** Intrinio、TradingEconomics 等在 OpenBB provider 清单中标为 paid；FMP、Tiingo 等虽可能有 free key，也由其套餐决定 endpoint、速率和用途。[Providers 文档][docs-providers]

**对本项目判断：** 商业产品需要逐 provider、逐数据类型建立许可矩阵，至少核对：

- server-side use 与 end-user display；
- derived data；
- raw data redistribution/export；
- caching/retention；
- news/full-text storage；
- AI training/context usage；
- attribution；
- 地域和用户数量；
- 订阅终止后的历史证据保留。

**非法律结论：** 本轮公开资料足以确认“必须分开审查”，不足以给出所有 provider 的商业可用性结论。OpenBB 的存在绝不等于可以把所有 provider 数据直接提供给自己的用户。

---

## 13. 中文 / A 股 / 港股场景

### 13.1 分项结论

| 场景 | 固定 commit 可见能力 | 结论与限制 |
| --- | --- | --- |
| A 股证券搜索 | 通用 equity search；无中国本地证券主数据 provider | 未发现可靠的 A 股全市场发现/去重承诺 |
| A 股行情 | 全球 provider 可能接受 provider-specific suffix；OpenBB 文档说明海外 symbol 常依 provider 格式 | 可做逐 provider 探索，不能据此认定覆盖、复权和商业质量达标 |
| 港股 | 同样可能通过 `.HK` 或 provider 自有 symbol 查询 | 缺统一搜索、主数据、公司行动和覆盖 SLA 证据 |
| 中国公司财务 | FMP/YFinance/Intrinio 等全球 provider 可能按其覆盖返回 | 标准模型可接，但公开实现未证明 A/H 股财务完整性、口径、filing time 和 restatement lineage |
| 中国公告 | 固定 provider 列表中无 SSE/SZSE/HKEX 公告 connector | **明显缺口**；SEC 能力不能外推到中国市场 |
| 中文新闻 | 有全球/公司新闻 providers，但无中文本地新闻标准或中文来源覆盖承诺 | 可能搜到关于中国的英文/多语新闻，不等于中文新闻证据层 |
| 中国宏观 | EconDB、IMF、OECD、ECB/TradingEconomics 等存在中国 series/country 能力；EconDB fixtures 可见来自中国国家统计局等 source 的 series | 是当前相对可行的一块，但 revision vintage、许可和更新可靠性仍需逐 series 验证 |
| Symbol/exchange mapping | MIC 数据含 XSHG/XSHE/XHKG；provider 格式各异 | Reference list 不是 Security Master，也不证明 endpoint coverage |

参见 [Providers 目录][src-providers]、[Query Parameters 文档][docs-query-params]、[exchange_data.json][src-exchange-data] 和 [EconDB helpers][provider-econdb-helpers]。

### 13.2 为什么不能以“名义支持 China”下结论

**源码推断：** 中国市场商业可用性至少还取决于：

- 搜索能否覆盖上市、退市、北交所、不同 share class；
- symbol 和 MIC 是否可长期稳定映射；
- 前/后复权和公司行动是否完整；
- 财务报告采用何种会计口径、币种和季度累计规则；
- 公告是否来自法定披露源，是否有原文和发布时间；
- 中文新闻授权、正文、去重和修订；
- 交易日历、停牌和价格限制；
- 供应商在中国网络和合规环境中的稳定性；
- 商业展示、缓存和再分发许可。

**对本项目判断：** OpenBB 对中国宏观可以作为 adapter 候选；A/H 股的证券主数据、公告、财务 PIT 和中文新闻仍应视为未解决。若 v0.2.0 依赖这些能力，技术风险会掩盖产品价值验证。

---

## 14. 对 Evidence & Review 层的启示

### 14.1 Evidence

**对本项目判断：** 一个可靠 Evidence 应表达四件不同的事：

1. **现实发生/被发布了什么**：原始值、原文、文件或事件；
2. **我们何时、通过谁看到它**：provider、query、captured_at；
3. **它描述哪个时段和哪个版本**：observation/fiscal/publication/revision/vintage；
4. **我们如何解释它**：相关性和 supporting/contradicting 建议，且可被用户修改。

Evidence 需要前述 `evidence_id`、subject/asset、type、original value/excerpt、source、provider、各类时间、measurement context、raw ID/URL、hash/snapshot 和 interpretation status。缺失字段不能由 AI 猜测补齐。

### 14.2 ContextSnapshot

**对本项目判断：** ContextSnapshot 必须是一个真实冻结动作，而不是保存一组未来会重新执行的 queries。它至少应固定：

- 截止时间和 timezone；
- 当时实际选中的 Evidence 集合及版本；
- 关键 market/portfolio facts 的快照值；
- 选择和过滤规则版本；
- provider/capture failures 与 unknowns；
- snapshot/hash，使后续修订不会改写原决策上下文。

动态查询可以用于“当前视图”，不能替代历史判断的 ContextSnapshot。

### 14.3 Checkpoint 与 OutcomeReview

**对本项目判断：**

- **Checkpoint** 是某时点对 Thesis 的定期复核：关联新 Evidence、运行确定性规则、保存 AI 建议和用户确认；它不是行情缓存。
- **OutcomeReview** 是结果发生后的回顾：比较原 Thesis、当时 ContextSnapshot、后续 Checkpoints 和实际 outcome，区分“决策过程质量”与“结果好坏”。
- 后续修订应新增 revision/更正关系，不能覆盖旧 Evidence，否则 OutcomeReview 会失去审计意义。

### 14.4 与 Financial Reality 的链接

**对本项目判断：** Evidence 可以引用 Financial Reality 中已存在的 asset、position、transaction、price observation；也必须能引用不属于组合账本的外部 filing、news、macro series 和用户手工观察。引用不等于复制所有对象职责。

---

## 15. AI Evidence Interpreter 的安全边界

### 15.1 AI 可以安全承担的工作

在来源和输出约束充分时，AI 可以：

- 从已捕获文档中提取候选 claims、数字、管理层解释和段落位置；
- 把 provider-specific 字段映射为用户可读说明，但同时展示原字段和单位；
- 为 Thesis 检索和排序可能相关的 Evidence；
- 比较多期数字并生成可复核的差异描述；
- 建议 `SUPPORTING`、`CONTRADICTING`、`UNCLEAR`、`NOT_RELEVANT`；
- 指出证据冲突、缺失的时间语义和需要用户澄清的问题；
- 生成 Checkpoint 草稿和反方问题。

### 15.2 必须展示原始数据或文档的判断

以下内容不能只给 AI 结论：

- 影响 thesis 状态的关键财务指标；
- filing 中管理层对变化原因的陈述；
- 会计口径、非 GAAP 调整、restatement/preliminary；
- 新闻中的事实指控、预测和转述；
- provider 冲突或缺失值；
- 触发用户行动的重大 Evidence。

界面至少要能回到原值/摘录、source、URL/ID、时间、单位、provider 和 capture version。

### 15.3 自动分类与规则化

**对本项目判断：**

- **规则适合**：用户已定义明确阈值且输入语义稳定，例如“同口径季度毛利率同比下降超过 200bp”。规则输出应是“条件已触发”，不直接等于 thesis 被证伪。
- **AI 适合建议**：管理层解释、竞争格局、行业变化和多证据综合。这些应默认是 proposal。
- **必须保留 `UNCLEAR`**：期间/币种/单位不明、PIT 不可靠、来源冲突、只有二手转述、因果关系不足、行业定义漂移、关键文档缺失。
- **用户最终确认**：用户在看到 Evidence 和建议后确认 Checkpoint 的相关性及状态；系统保存 AI 建议、用户决定和差异，而不覆盖其历史。

**结论：** AI 是 evidence selection/extraction/interpretation assistant；source of truth 是被冻结且可验证的 Evidence，最终 investment reasoning 归用户。

---

## 16. 重新评价 Thesis Monitoring 的可行性

假设 Thesis 是：

> 未来两年公司毛利率会持续改善。

系统监控新季度财报、毛利率变化、公司解释和行业变化。

### 16.1 一条受控工作流

```text
用户定义 Thesis 与衡量口径
  ↓
检测新 filing（以 filing/publication time 为准）
  ↓
冻结原文与 statement Evidence
  ↓
确定性计算 gross margin 与可比期变化
  ↓
AI 提取管理层解释、寻找行业 Evidence
  ↓
规则触发 + AI 分类建议
  ↓
用户复核并冻结 Checkpoint
```

### 16.2 分维度评估

| 维度 | 评估 | 说明 |
| --- | --- | --- |
| 数据可得性 | **美国大中型上市公司：中高；全球/中国：低到中** | SEC statements/filings 很有价值；行业指标和中国本地披露不是通用覆盖 |
| 时间边界 | **中低** | filing date 可用，SEC `pit_mode` 局部可用；跨 provider publication/revision/as-of 不统一 |
| Provenance | **调用级中等，事实级不均匀** | provider/query/timestamp 可保留；原始 fact、unit、mapping、revision 需自建 |
| 自动化难度 | **数值监控中等；叙事/行业高** | 毛利率公式简单，科目映射、期间可比、重述、行业定义不简单 |
| AI 误判风险 | **数值描述中；原因/分类高** | AI 易把相关性写成因果、把一次季度波动解释为长期趋势 |
| 商业数据成本 | **SEC 低，新闻/全球财务/行业数据不确定到高** | 许可、正文、历史留存和再分发需要逐 provider 采购/审查 |

### 16.3 毛利率看似简单但需要的语义

**对本项目判断：** 自动计算前至少要固定：

- gross profit 是直接报告还是 revenue - cost of revenue；
- GAAP/IFRS、reported/adjusted；
- 单季还是 YTD，财年日历；
- currency/unit/scale；
- original filing 还是 latest restated；
- filing/publication cutoff；
- 同行业 benchmark 的定义和版本。

数字规则可以判断“按该口径，指标变化了多少”，不能自动证明“未来两年持续改善”或“变化由某个管理层原因导致”。

### 16.4 综合结论

**对本项目判断：** OpenBB 类型的数据层足以支撑一个 **窄范围、强来源约束、用户复核** 的 Thesis Monitoring 原型，例如先限于 SEC 美国公司、一个财务指标、一类 filing。它不足以直接支撑“任意市场、任意 thesis、全自动给出真值分类”的产品。

OpenBB 解决了 provider adapter 的大量机械成本，但最关键的产品/领域成本仍在：Thesis 到可观测条件的映射、PIT capture、Evidence provenance、解释边界和用户 review workflow。

---

## 17. 四轮研究后重新评价三层模型

### 17.1 三层模型仍然成立

```text
Financial Reality
  accounts / transactions / positions / assets / market observations

Investor Reasoning
  decision / thesis / assumptions / invalidation conditions / revisions

Evidence & Review
  captured evidence / context snapshot / checkpoint / outcome review
```

**对本项目判断：** OpenBB 没有要求增加第四层，反而让第三层独立的理由更强：外部数据查询的“当前值”与“进入某次判断的历史版本”是不同对象。

### 17.2 Evidence & Review 为什么值得独立

- Financial Reality 关心“账户和市场现在/某时发生了什么”；
- Evidence 关心“哪一个来源的哪个版本，在何时被看到，并如何与某个 thesis 相关”；
- 同一 market value 可以被多个 Checkpoint 引用；
- 同一外部 filing/news 并不属于用户账户账本；
- Evidence 有 capture、citation、revision、interpretation 和 review 生命周期，MarketData 通常没有。

### 17.3 已经比较清楚的边界

1. **Financial Reality 拥有内部 asset identity。** Provider symbol 只是映射。
2. **Investor Reasoning 拥有 Thesis 和用户判断。** OpenBB/AI 不拥有。
3. **Evidence & Review 拥有来源和历史版本。** 不能把当前 provider query 当历史 snapshot。
4. **外部数据 adapter 可替换，已冻结 Evidence 不应随 adapter 切换而改变。**
5. **事实与解释分离。** AI 建议和用户确认都引用同一 Evidence，但不改写原始内容。
6. **结果与过程质量分离。** OutcomeReview 需要看到当时 ContextSnapshot，而非后见数据。

### 17.4 仍需用户研究的问题

技术研究无法回答：

- 用户是否愿意在持仓期间持续回看 Thesis；
- 哪种 Evidence 才值得打扰，用户能承受多少噪音；
- 用户是否理解/在意 source、PIT、restatement 和 freeze；
- 用户会不会确认/纠正 AI 分类；
- Checkpoint 的适当频率和触发方式；
- 用户更需要财务指标、filing、news 还是价格/组合事件；
- 中文用户能否接受初期只覆盖受控市场/来源；
- Evidence Monitoring 是否改变决策质量，而非只增加信息焦虑。

---

## 18. 对 v0.2.0 的启示：只验证一个核心产品假设

### 18.1 推荐选择 C

> **C. 用户是否觉得持仓期间的 Evidence Monitoring 有价值。**

**理由：**

1. TradeNote 已说明日志/复盘可用，但不能证明用户会持续维护可证伪 Thesis。
2. Wealthfolio/Ghostfolio 已说明 Financial Reality 可构建，但不能证明增加 Evidence 层产生用户价值。
3. OpenBB 已说明外部事实接入在技术上可行，却同时暴露 PIT、provenance、许可和中国覆盖成本。
4. 如果用户不需要持续 Evidence Monitoring，A/B/D 的结构化、AI 辅助和 freeze 机制即使技术漂亮，也难成为核心产品。
5. 如果用户确实需要它，A、B、D 才分别成为 onboarding、低摩擦输入和信任/复盘机制的后续假设。

### 18.2 技术可行性与用户需求必须分开

**技术可行性：部分成立，但只能在窄范围内。** 可用 SEC filing + 一个明确指标 + snapshot + source link 做出可信原型；跨市场、全新闻、完整 PIT 和自动解释尚未成立。

**用户需求：未被四轮开源研究验证。** 开源项目说明别人如何实现数据、账本和日志，不说明目标用户愿不愿意在持仓期间消费、确认并依赖 Evidence Monitoring。

### 18.3 最小验证形态，而不是完整 v0.2.0 设计

**对本项目判断：** 为避免技术建设吞没产品验证，可以用一个非常受控的实验：

- 用户选择一项真实持仓和一条已有 Thesis；
- 只监控一个明确指标或一类 filing；
- 允许人工/半自动选择 Evidence，确保 PIT 和来源可信；
- 展示原值/原文、来源与 captured time；
- AI 只给 supporting/contradicting/unclear 建议；
- 用户确认是否相关、是否改变 confidence/next action；
- 观察用户是否持续回来、是否减少遗漏、是否认为噪音值得。

这验证的是 C，不是以“大量自动抓数已完成”冒充需求成立。

---

## 19. 最终研究判断

### A. 最值得学习的架构思想

`router + standard model + provider-specific fetcher/extension`：把稳定的调用语义与可替换的外部数据源分开，同时允许 provider extras 和 metadata 穿透。

### B. 能否真正提供 point-in-time 数据

不能作为通用保证。SEC `pit_mode` 是很强的局部实现，filings/历史价格也可构成部分 PIT 基础；跨 provider 的 as-of、vintage、revision、snapshot 和 replay 仍缺失。

### C. Provenance 程度

调用级 provenance 中等偏好：provider、route、arguments、timestamp、warnings 可得；事实级 provenance 不统一，原始记录、单位/币种、revision、加工链和质量状态依 provider/model。

### D. 为什么 Evidence Snapshot 仍要自存

Provider 会修订历史，网页会变化，缓存会过期，mapping 会升级，权限会改变；OpenBB 没有保存“这位用户当时真正看到的那个版本”。

### E. AI Evidence Interpreter 的边界

AI 可检索、提取、比较、解释并建议分类；关键数字和叙述必须回链原始 Evidence，规则只报告条件触发，`UNCLEAR` 必须可保留，用户最终确认。

### F. A 股 / 中文数据现实

中国宏观有若干可用 provider 线索；A/H 股主数据、公告、财务 PIT 和中文新闻没有形成稳定、统一、可商用的公开能力。Symbol suffix 可查询不等于覆盖达标。

### G. 三层模型

仍成立且边界更清晰。OpenBB 类型数据主要服务 Financial Reality 的外部事实入口；Evidence & Review 独立保存来源、版本、快照和解释状态。

### H. v0.2.0 最值得验证的假设

选择 C：用户是否觉得持仓期间的 Evidence Monitoring 有价值。技术上先做窄范围可信原型；用户是否需要它仍是首要未知。

---

## 参考资料

以下源码链接全部固定到研究 commit；在线文档用于解释公开接口和产品行为，已记录核对日期。

[repo]: https://github.com/OpenBB-finance/OpenBB
[commit]: https://github.com/OpenBB-finance/OpenBB/commit/3e071fcc2cd9f891cac6040ae60296dba76dab46
[repo-readme]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/README.md
[repo-license]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/LICENSE
[src-provider]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/abstract/provider.py
[src-fetcher]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/abstract/fetcher.py
[src-data]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/abstract/data.py
[src-query-params]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/abstract/query_params.py
[src-annotated-result]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/abstract/annotated_result.py
[src-registry]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/registry.py
[src-registry-map]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/registry_map.py
[src-provider-interface]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/app/provider_interface.py
[src-container]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/app/static/container.py
[src-query-executor]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/query_executor.py
[src-obbject]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/app/model/obbject.py
[src-command-runner]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/app/command_runner.py
[src-equity-router]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/extensions/equity/openbb_equity/equity_router.py
[src-price-router]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/extensions/equity/openbb_equity/price/price_router.py
[src-news-router]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/extensions/news/openbb_news/news_router.py
[src-etf-router]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/extensions/etf/openbb_etf/etf_router.py
[src-standard-models]: https://github.com/OpenBB-finance/OpenBB/tree/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models
[src-providers]: https://github.com/OpenBB-finance/OpenBB/tree/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers
[src-exchange-data]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/utils/exchange_data.json
[src-exchange-utils]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/utils/exchange_utils.py
[src-country-utils]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/utils/country_utils.py
[sm-equity-historical]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/equity_historical.py
[sm-equity-search]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/equity_search.py
[sm-equity-info]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/equity_info.py
[sm-etf-search]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/etf_search.py
[sm-index-search]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/index_search.py
[sm-crypto-search]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/crypto_search.py
[sm-income]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/income_statement.py
[sm-balance]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/balance_sheet.py
[sm-cash]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/cash_flow.py
[sm-company-news]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/company_news.py
[sm-company-filings]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/company_filings.py
[sm-economic-calendar]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/economic_calendar.py
[sm-economic-indicators]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/economic_indicators.py
[sm-fred-series]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/core/openbb_core/provider/standard_models/fred_series.py
[provider-fmp-historical]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/fmp/openbb_fmp/models/equity_historical.py
[provider-yf-historical]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/yfinance/openbb_yfinance/models/equity_historical.py
[provider-tiingo-historical]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/tiingo/openbb_tiingo/models/equity_historical.py
[provider-fmp-income]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/fmp/openbb_fmp/models/income_statement.py
[provider-sec-income]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/sec/openbb_sec/models/income_statement.py
[provider-sec-balance]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/sec/openbb_sec/models/balance_sheet.py
[provider-sec-cash]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/sec/openbb_sec/models/cash_flow.py
[provider-sec-statement-readme]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/sec/openbb_sec/utils/STATEMENT_SCHEMA_README.md
[provider-fred-series]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/fred/openbb_fred/models/series.py
[provider-fred-cache]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/fred/openbb_fred/utils/rate_limiter.py
[provider-sec-filings]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/sec/openbb_sec/models/company_filings.py
[provider-sec-htm]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/sec/openbb_sec/models/htm_file.py
[provider-econdb-helpers]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/providers/econdb/openbb_econdb/utils/helpers.py
[src-mcp-readme]: https://github.com/OpenBB-finance/OpenBB/blob/3e071fcc2cd9f891cac6040ae60296dba76dab46/openbb_platform/extensions/mcp_server/README.md
[docs-architecture]: https://docs.openbb.co/odp/python/developer/architecture_overview
[docs-provider-extension]: https://docs.openbb.co/odp/python/developer/extension_types/provider
[docs-standardization]: https://docs.openbb.co/odp/python/developer/standardization
[docs-data-sources]: https://docs.openbb.co/odp/cli/data-sources
[docs-defaults]: https://docs.openbb.co/odp/python/settings/user_settings/defaults
[docs-query-params]: https://docs.openbb.co/odp/python/basic_usage/query_parameters
[docs-providers]: https://docs.openbb.co/odp/python/extensions/providers
[docs-company-news]: https://docs.openbb.co/odp/python/reference/news/company
[workspace-mcp-citation]: https://docs.openbb.co/workspace/developers/widget-configuration/matching-widget-to-mcp-tool
[workspace-agent-citation]: https://docs.openbb.co/workspace/developers/ai-features/highlight-widget-citations
[sec-developer]: https://www.sec.gov/about/developer-resources
[fred-terms]: https://fred.stlouisfed.org/docs/api/terms_of_use.html
[yfinance-readme]: https://github.com/ranaroussi/yfinance
