# Investment Tracker Architecture

> 文档性质：Product Vision 与 Decisions 收敛后的当前架构边界
>
> 当前状态：已接受原则、候选架构与未决问题的分类记录；不是最终系统设计
>
> 正式输入：[`PRODUCT_VISION.md`](PRODUCT_VISION.md)、[`DECISIONS.md`](DECISIONS.md)、[`RESEARCH_SYNTHESIS.md`](research/RESEARCH_SYNTHESIS.md)

## 1. Purpose and Status

本文回答两个问题：

1. 当前已有足够依据约束后续设计的系统职责边界是什么；
2. 哪些领域和技术设计仍必须保持可撤销。

本文不回答最终数据库要有哪些表，也不承诺服务、package、部署或 UI 的最终形态。文中的对象名称用于表达职责和候选概念，不等于已经接受的 schema。

全文使用以下状态：

- **`Accepted Principle`**：已在 [`DECISIONS.md`](DECISIONS.md) 接受、可以约束后续设计的原则；本文只引用，不重新发明。
- **`Candidate Architecture`**：当前研究支持、适合指导下一步实验，但仍可被用户证据或实现反馈改变的结构。
- **`Open Question`**：尚无足够依据作答；不得由候选对象、图示或示例关系暗中固化。

若正文未明确声明某个具体对象关系已经接受，应将其视为候选或未决，而不是默认决定。

## 2. Architectural Principles

以下是本架构必须遵守的 `Accepted Principle`：

1. **Financial Facts 与 Investor Reasoning 分离。** 客观金融事实和用户判断拥有独立身份与生命周期（D-001）。
2. **Account ≠ Asset。** Account 表达所有权、现金、来源和约束边界；Asset 表达可跨账户引用的金融标的身份（D-002）。
3. **Activity / Transaction ≠ Position。** 前者是事件，后者是某一时点和范围内的状态（D-003）。
4. **Position ≠ InvestmentCase。** 财务状态不能自动决定用户判断过程的 identity 或 lifecycle（D-004）。
5. **Source Record ≠ Canonical Event ≠ Derived State。** 来源、规范化事实和计算结果必须在语义上分离（D-005）。
6. **Financial Derived State 应可重建。** 在 canonical facts 和所需 reference facts 足够时，物化或缓存结果不能成为另一套独立真相（D-006）。
7. **Current Market Data ≠ Frozen Evidence。** 后来重新查询的结果不能替代当时实际纳入判断的证据（D-007）。
8. **Evidence Source ≠ Interpretation。** 原始证据与 AI 建议、用户确认和关系分类拥有独立生命周期（D-008）。
9. **AI 不是 source of truth。** AI 只能协助澄清、检索、提取、比较和提出建议（D-009）。
10. **Fact Correction ≠ Reasoning Revision。** 事实更正需要可追溯；认知变化通过 Revision 追加，不能静默覆盖 Original Reasoning（D-010）。
11. **Investment Outcome ≠ Decision Quality。** 盈亏不能自动判定判断过程正确或错误（D-011）。
12. **时间语义保持可区分。** observation、publication、filing / accepted、revision 和 captured time 不能被压成含义不明的单一日期（D-012）。
13. **Internal Asset Identity ≠ Provider Symbol。** 内部资产、listing / market identity 和 provider identifier 必须能够分别演进（D-013）。
14. **Unknown 必须保持 Unknown。** 来源、版本、单位、时间、身份或关系无法可靠确定时，允许 `UNKNOWN` / `UNCLEAR`，不得猜测补全（D-014）。
15. **Checkpoint 不是独立决策样本。** 同一 Case 内的多次复核不能人为扩大 Decision Profile 的样本量（D-015）。
16. **不执行自动交易。** 用户保留最终 Judgment 与 Investment Action（D-016）。

这些原则约束语义，但不决定具体字段、对象基数、接口或存储技术。

## 3. Three-Layer Responsibility Model

**Status:** `Candidate Architecture`

当前使用三层 bounded responsibilities 理解系统：

```text
Financial Reality
Investor Reasoning
Evidence & Review
```

| Responsibility | 回答的问题 | 不负责什么 |
| --- | --- | --- |
| Financial Reality | 实际发生了什么，以及从这些事实可以计算出什么？ | 不解释用户为什么作出判断，不自动创建或关闭 Case。 |
| Investor Reasoning | 用户为什么这样判断，以及判断如何随时间演化？ | 不冒充成交、持仓、价格或其他金融事实。 |
| Evidence & Review | 哪些证据在什么时间、以什么版本进入判断，以及后来如何复核？ | 不把当前查询当作历史快照，不替用户作最终判断。 |

三层模型的约束是职责分离，不是物理分层：

- 不是三个微服务；
- 不是最终数据库 schema；
- 不要求每层对应一个 package；
- 不要求每个候选对象对应一张表；
- 不预设 monolith 或 services；
- 部署、持久化和代码模块边界仍可变化。

三层本身仍是 `Candidate Architecture`。已接受的是它所表达的若干语义边界，而不是这个命名或结构必须永久保留。

## 4. Financial Reality

Financial Reality 负责保存或表达用户、来源确认的金融事实，连接必要的外部参考事实，并提供可追溯、可重建的派生状态。

### 4.1 Canonical Financial Facts

**Status:** `Candidate Architecture`

候选概念包括：

- `Account`；
- `Activity` / `Transaction`；
- 已确认的 cash event，或能力边界明确的 source snapshot；
- import / source identity。

这些概念表达用户或来源确认的金融事实。来源记录进入 canonical facts 前可能需要规范化、复核或拒绝；一条 source record 不保证恰好产生一条 canonical activity。

```text
Source Record
    ↓ normalize / review
Canonical Activity
    ↓ derive with reference facts
Position / Holding / Valuation
```

这是概念流程，不是 importer 接口、表结构或一对一基数。若未来只获得 holdings / balance snapshot，它可以作为诚实的 source fact，但不得声称具有并不存在的交易级归因能力。

### 4.2 Reference Facts

**Status:** `Candidate Architecture`

候选概念包括：

- `Asset`；
- listing / market identity；
- provider mapping；
- Price / Quote；
- FX；
- 在真实需求要求时所需的 market reference 或 corporate action reference。

这些通常来自外部数据源，用于识别标的或计算状态，不等同于用户账户事实。其来源、有效时间、单位、币种、调整口径和不确定性需要按具体用途保留。

```text
Internal Asset
    ↕ map without identity collapse
Listing / Market Identity
    ↕ map without identity collapse
Provider Identifier
```

该关系遵守 D-013，但 Asset / Listing 的最终模型、映射流程和外部标识集合仍未决定。

### 4.3 Derived State

**Status:** `Candidate Architecture`

候选概念包括：

- Position；
- Holding；
- Valuation；
- Allocation；
- Performance；
- Portfolio scope / read model。

这些状态应遵守 D-006：只要 canonical facts、reference facts 和计算口径足够，就应能够重建。缓存或物化可以用于体验和性能，但必须可丢弃、可重算，并能说明计算依据。

本文不设计 Portfolio Engine，也不决定：

- Position 或 Holding 是否物化；
- Portfolio 是否为持久化实体，还是 query / filter scope；
- cash 使用 event ledger、balance snapshot 或受限双模式；
- 成本基础、绩效公式、重算范围和缓存策略。

### 4.4 Accepted Boundaries Within Financial Reality

以下边界是 `Accepted Principle`，但两侧的最终模型仍是候选：

- Account ≠ Asset（D-002）；
- Activity / Transaction ≠ Position（D-003）；
- Source Record ≠ Canonical Event ≠ Derived State（D-005）；
- Internal Asset Identity ≠ Provider Symbol（D-013）；
- Derived State 不应成为独立真相（D-006）。

## 5. Investor Reasoning

Investor Reasoning 负责表达用户的原始判断、前提、复核条件、决定和认知变化。它不由仓位状态自动生成，也不随财务事实更正而被一起覆盖。

### 5.1 Candidate Aggregate and Objects

**Status:** `Candidate Architecture`

候选对象包括：

- `InvestmentCase`：独立 reasoning aggregate 的候选；
- `Thesis`：用户的核心判断；
- `Assumption`：支撑 Thesis、可被检查的前提；
- `ReviewCondition`：触发重新评估的预设条件；
- `Decision`：建立、加仓、减仓、持有、退出或不行动等用户决定；
- `Revision`：对既有判断的追加修订。

`InvestmentCase` 作为独立 aggregate 是候选，而不是已经确定的数据模型。当前可以确定的只有：

- Position 不等于 InvestmentCase（D-004）；
- Financial Facts 与 Investor Reasoning 必须分离（D-001）；
- Original Reasoning 不得被静默覆盖（D-010）；
- Fact Correction 与 Reasoning Revision 必须分离（D-010）。

### 5.2 Open Questions

以下全部是 `Open Question`：

- 一个 Case 是否一对一对应一个 Asset；
- 是否支持一个 Case 覆盖多个 Asset 或主题；
- Case 是否跨 Account，Account 是 context、link 还是 scope；
- 一笔 Activity 是否可以关联或执行多个 Case / Decision；
- 清仓后再次买入是新 Case、恢复旧 Case，还是由用户选择；
- Case 是否可在交易发生前创建；
- Case 何时算结束，以及结束后是否仍可继续 review；
- Position lifecycle 与 Case lifecycle 如何在产品中协调；
- Thesis、Assumption、ReviewCondition、Decision 和 Revision 的最终基数与 ownership。

任何实现实验都不得将其局部简化悄悄升级为长期 cardinality 决定。

## 6. Evidence & Review

Evidence & Review 负责保存进入判断的证据边界、证据时间和版本语义，以及用户后来如何复核原判断。

### 6.1 Candidate Objects

**Status:** `Candidate Architecture`

候选对象包括：

- `Evidence`：具有可追溯来源、内容和时间语义，并在来源提供或合规允许时保留版本、snapshot / hash 与完整性信息的事实包；不可获得的信息保持 unknown；
- `ContextSnapshot`：某次 Decision 或 Checkpoint 中实际被系统捕获并纳入判断的 Evidence 集合；
- `Checkpoint`：在某一时点对 InvestmentCase 的阶段性复核；
- `OutcomeReview`：比较冻结判断、后来证据和金融结果的复盘；
- `DecisionProfile`：样本充分时才可能形成的远期读模型，目前不进入实现范围。

### 6.2 Evidence Is Not Market Data

**Status:** `Accepted Principle`

Evidence 可以引用行情、指标、filing、news、宏观数据、文档或用户观察，但它不等于 MarketData。当前查询可能受到复权、restatement、revision、provider mapping、网页变化或权限变化影响，因此：

```text
Current Query Result ≠ Frozen Evidence
```

动态查询可以服务当前视图，不能静默改写旧 ContextSnapshot。具体 snapshot 内容、存储格式和保留范围仍是 `Open Question`。

### 6.3 Evidence Source and Interpretation

**Status:** `Accepted Principle`

原始 Evidence 与以下解释必须拥有独立生命周期：

- AI interpretation / extraction；
- user confirmation；
- relevant / not relevant；
- supporting / contradicting / unclear。

关系分类是可复核解释，不是证据自身属性或不可变真相。解释变化不得覆盖原始值、原文、来源标识或历史确认。

### 6.4 Time Semantics

**Status:** `Accepted Principle`

在具体 Evidence 类型需要时，至少保持以下含义可区分：

- observation time；
- publication time；
- filing / accepted time；
- revision time；
- captured time。

并非每类 Evidence 都必须强行拥有所有时间；缺失或来源不提供的时间应保持 unknown。最终字段、时区、精度和 cutoff 规则仍是 `Open Question`。

### 6.5 ContextSnapshot Boundary

**Status:** `Candidate Architecture`

`ContextSnapshot` 表达：

> 某次 Decision 或 Checkpoint 中，实际被系统捕获并纳入判断的 Evidence 集合。

它不声称完整重建“当时所有可知信息”，也不能用后来查询到的内容填补当时未捕获的空白。它应能明确表达缺失、冲突、无权限和未知，并遵守 D-014。

## 7. External Data Adapter Boundary

**Status:** `Candidate Architecture`

当可信实验确实需要外部数据时，可以使用薄 adapter 隔离应用语义与 provider-specific 语义：

```text
Application / Domain
        ↓
Canonical Research Query
        ↓
Provider Adapter
        ↓
External Data Source
```

对于普通 current-view query，以下 provider / query metadata 可按实际用途保留：

- provider identity；
- query context；
- provider extras；
- source identifier；
- warnings / quality state；
- capture time。

对于会形成 Frozen Evidence 的 capture，必须至少保留足以追溯当时状态的来源与时间上下文。provider extras、source identifier、warnings、版本、snapshot / hash，以及单位、币种、时间语义和转换说明等信息，在可获得且合规允许时保留；不可获得的信息保持 unknown。

边界限制：

- 当前没有决定使用 OpenBB 或任何特定 provider；
- OpenBB 是研究依据，不是已选技术栈；
- 当前不设计完整 provider framework；
- 产品验证里只允许为一个受控来源建立实验所需的薄 adapter；
- provider abstraction 是基础能力，不是产品差异；
- adapter 的存在不证明来源具备 PIT、完整 provenance、许可或长期可用性。

## 8. AI Boundary

**Role boundaries:** `Accepted Principle`

**Workflow placement:** `Candidate Architecture`

AI 位于用户主导的 reasoning / review workflow 中，可以调用受控的 Evidence / Data Tools：

```text
User
  ↓
Reasoning / Review Workflow
  ↓
AI Assistant
  ↓
Evidence / Data Tools
```

该图只表达候选调用方向，不决定 package、process、service、database 或 deployment topology。

这不改变以下边界：

```text
AI ≠ Financial Fact
AI ≠ Evidence Source
AI ≠ Final Investment Judgment
AI ≠ Trade Executor
```

AI 输出应被保存和展示为 proposal、interpretation、extraction 或 draft。需要进入用户判断链的分类和结论由用户确认；证据不足时 AI 必须允许 unknown / unclear，而不是补写完整叙事。

模型、provider、prompt、置信度表达、确认粒度和自动化程度均为 `Open Question`。

## 9. Conceptual Cross-Layer Relationships

**Status:** `Candidate Architecture`

下列关系只用于讨论职责协作，不是最终 schema、foreign key、API 或 cardinality：

```text
Activity
    → may EXECUTE a Decision

InvestmentCase
    → may contain or REFERENCE Thesis

Evidence
    → may SUPPORT / CONTRADICT / be UNCLEAR relative to Thesis

ReviewCondition
    → may TRIGGER_REVIEW

Checkpoint
    → reviews an InvestmentCase at a point in time

ContextSnapshot
    → captures Evidence actually used at a Decision / Checkpoint

OutcomeReview
    → compares frozen reasoning, later Evidence and financial outcome
```

`EXECUTES`、`SCOPED_TO`、`SUPPORTS`、`CONTRADICTS`、`TRIGGERS_REVIEW` 和 `REFERENCES` 都是 conceptual relation labels。它们不决定方向性、必选性、多重性或持久化实现。

## 10. Cross-Cutting Concerns

以下是横切运行能力，不是第四个投资领域：

- authentication；
- permissions；
- multi-user tenancy；
- cache；
- background jobs；
- backups；
- observability；
- rate limits；
- secrets；
- data retention；
- compliance / data licensing。

当前不提前建设完整的 production-grade authentication、multi-user tenancy、background jobs、observability 等平台基础设施；这些横切能力不应反向决定三层职责、服务数量或数据库选择。

但是，如果受控实验实际触及外部数据、API credentials、真实用户数据或持久化，则必须满足与实验范围相称的最小 secrets handling、access / privacy protection、data retention、compliance / data licensing 和必要安全约束。本文不因此设计完整安全架构。

## 11. What Is Explicitly Not Decided

以下全部保持 `Open Question`：

### Domain and Data

- InvestmentCase 的真实心智模型、Asset / Account 关系与所有 cardinality；
- Case 创建、清仓再买、结束和复盘的生命周期规则；
- Activity 与 Case / Decision 的关联与分摊方式；
- Portfolio 是否为持久化实体；
- cash 的 event、balance snapshot 或受限双模式；
- Source Record 保存粒度、原文件保留、去重和 ImportRun；
- Asset / Listing 模型、identity merge / split 和 provider mapping；
- Evidence、ContextSnapshot、Checkpoint、OutcomeReview 与 Revision 的最终模型；
- snapshot 内容、hash、许可、保留范围和 citation 展示；
- derived state、绩效、成本基础、重算和缓存策略；
- 最终数据库 schema 和迁移方案。

### Product and External Data

- Evidence Monitoring 是否有持续用户价值、合适内容和频率；
- 是否以 A 股、H 股、美股或其他市场作为首发范围；
- 是否使用 OpenBB 或任何特定 provider；
- provider 覆盖、PIT 能力、数据许可和长期成本；
- AI 模型、provider、工作流与自动化程度。

### Runtime and Deployment

- local-first、cloud、self-hosted 或 hybrid；
- desktop、web 或 hybrid 产品形态；
- SQLite 是否长期保留；
- 是否需要 PostgreSQL 等服务器数据库；
- monolith、modular monolith 或 services；
- package、process、queue 和 deployment topology。

不得因为 Wealthfolio、Ghostfolio 或 OpenBB 采用某种技术栈，就默认选择相同实现。

## 12. Relationship to v0.1.0

v0.1.0 的 `InvestmentRecord` 是 Financial Record MVP 中用于验证交易事实、SQLite persistence、Decimal 金额语义和基础 repository 的 monolithic model。

它：

- 不是最终领域模型；
- 也不是需要立即废弃的错误设计；
- 可以继续作为已发布、可运行、可测试的工程基线；
- 不应仅因研究产生了更完整的候选模型就被大规模重构。

下一阶段只有在产品实验确实需要新的领域边界时，才为被阻塞的能力做最小增量拆分。例如，实验要求一个 Case 跨多笔 Activity、Evidence 独立持久化、Account / Asset identity 支持真实导入，或 Revision 拥有独立生命周期时，才设计对应的最小迁移。

本文不制定 migration，也不要求先重构 Financial Reality 才能开始用户验证。

## 13. Architecture Evolution Rule

每项架构演进都应说明：

1. 它服务于哪个已观察到的用户需求或可信实验；
2. 当前模型具体阻塞了什么；
3. 可以完成验证的最小新边界是什么；
4. 哪些 cardinality、存储和部署选择仍可撤销；
5. 如何保留 provenance、unknown、revision 和既有数据语义。

不得用竞品规模、技术可行性、未来可能需要或模型看起来更完整，替代产品证据。

> **Architecture follows validated product needs. Candidate models must remain reversible until user evidence justifies stronger commitments.**
