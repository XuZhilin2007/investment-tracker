# Investment Tracker Project Context

> 用途：让不了解旧聊天内容的新协作者，仅通过 repository 恢复足够上下文并继续正确推进项目。
>
> 本文不是 README、PRD、研究报告摘要或最终架构。正式产品与工程依据仍以链接文档、代码、测试和 Git history 为准。

## 1. Project Snapshot

| 项目 | 当前状态 |
| --- | --- |
| Project | `Investment Tracker` |
| Current released baseline | 本文当前快照：已发布基线为 `v0.1.0`，Git tag 指向 `129393b`；这是 **Financial Record MVP**，不是最终产品架构 |
| Current stage | **Product Validation Before v0.2.0 Expansion**；即四轮研究和产品收敛后的验证阶段 |
| Internal candidate positioning | **Investment Thesis Monitor + Decision Journal**；尚未经过真实用户验证 |
| One core hypothesis | 用户是否认为持有期间的 Evidence Monitoring 有持续价值？ |
| Immediate next step | User Discovery；问题成立后才进入 Controlled Prototype |

四轮开源研究、正式 Product Vision、Decisions、Architecture 和 Roadmap 已完成。当前不应继续扩大竞品研究，也不应直接开始完整 v0.2.0 工程开发。下一阶段需要的是用户证据，而不是更多功能、数据源或预先重构。

## 2. Why the Project Exists

Investment Tracker 正在验证：

> 已有自主投资逻辑的个人投资者，是否需要一种低摩擦方式，把 Investment Thesis 变成可持续跟踪、可验证、可修订、可回溯的判断过程？

这不是“做一个功能更完整的投资记录软件”。研究已经表明，交易导入、通用日志、绩效图表、Portfolio Tracking、provider abstraction 和 AI 金融数据调用都是成熟能力或基础设施，不能单独构成核心差异。

当前内部候选定位是 **Investment Thesis Monitor + Decision Journal**。它不表示已经形成 PMF，不表示 Monitoring 的价值已经成立，也不表示产品已经拥有完整 Monitoring、Point-in-Time 或市场覆盖能力。

## 3. Candidate User

`UNVALIDATED_USER_HYPOTHESIS`

> 已有一定自主投资逻辑、以中长线或低频波段为主、希望提高判断质量，但缺少稳定结构化跟踪与复核方法的个人投资者。

开源研究没有证明该人群的痛点强度、持续使用意愿、市场规模或付费意愿。主要想让 AI 直接给出买卖答案的用户，与当前方向不匹配；已有成熟研究体系的资深投资者可以提供高质量反馈，但未必是首批采用者。

## 4. Current Core Hypothesis

> **当前单一核心产品假设：用户是否认为持有期间的 Evidence Monitoring 有持续价值？**

如果产品只在 BUY / SELL 时产生价值，中长期和低频投资者的使用频率可能不足。Monitoring 试图在持有期间通过“少遗漏、早复核、保留判断演化”持续产生价值。

这仍没有真实用户证据。当前下一步不是建设完整 Monitoring 产品，而是：

1. 进行 User Discovery，观察真实投资案例、现有流程、遗漏、维护成本和复核行为；
2. 只有问题表现出实际意义时，才用 Controlled Prototype 验证持续行为。

## 5. Current Product and Architecture Understanding

当前以三个责任区域理解问题：

```text
Financial Reality
Investor Reasoning
Evidence & Review
```

整个三层结构是 `Candidate Architecture`，不是最终 schema、服务拆分或部署设计。已接受的是其中若干语义边界，不是每个候选对象、关系或名称。

### 5.1 Financial Reality

回答“实际发生了什么，以及从事实可以计算出什么？”

- canonical facts 候选：`Account`、`Activity` / `Transaction`、已确认的 Cash event 或能力边界明确的 source snapshot；
- reference facts 候选：`Asset`、listing / market identity、provider mapping、Price / FX；
- derived state 候选：`Position`、`Holding`、Valuation、Allocation、Performance 和 Portfolio scope / read model。

来源记录、canonical event 与 derived state 必须在语义上分离。派生状态在事实和计算口径足够时应可重建，不应成为另一套真相。

### 5.2 Investor Reasoning

回答“用户为什么这样判断，以及判断如何演化？”

候选对象包括 `InvestmentCase`、`Thesis`、`Assumption`、`ReviewCondition`、`Decision` 和 `Revision`。`InvestmentCase` 是独立 reasoning aggregate 的候选，但它的 cardinality、Asset / Account 范围和 lifecycle 都未决定。

### 5.3 Evidence & Review

回答“当时和后来分别出现了什么 Evidence，以及它如何影响复核？”

候选对象包括 `Evidence`、`ContextSnapshot`、`Checkpoint`、`OutcomeReview`，以及远期的 `DecisionProfile`。Evidence source、AI interpretation 和用户确认必须分离；同一 Case 的多个 Checkpoint 不是多个独立决策样本。

完整候选架构和 Open Questions 见 [`ARCHITECTURE.md`](ARCHITECTURE.md)。

## 6. Accepted Principles

以下是后续工作必须遵守的压缩边界；详细定义和 `Not Decided Yet` 以 [`DECISIONS.md`](DECISIONS.md) 为准：

- Financial Fact ≠ Investor Reasoning；
- Account ≠ Asset；
- Activity / Transaction ≠ Position；
- Position ≠ InvestmentCase；
- Source Record ≠ Canonical Event ≠ Derived State；
- Financial Derived State 原则上应可重建；
- Current Market Data ≠ Frozen Evidence；
- Evidence Source ≠ Interpretation；
- AI ≠ Source of Truth；
- Fact Correction ≠ Reasoning Revision；
- Investment Outcome ≠ Decision Quality；
- observation、publication / filing、revision 与 captured time 语义不可混写；
- Internal Asset Identity ≠ Provider Symbol；
- Unknown must remain unknown；
- Checkpoints ≠ Independent Decision Samples；
- No Automated Trading。

这些原则不决定最终对象名称、数据库 schema、对象基数、UI、provider、部署或存储技术。

## 7. AI Boundary

> **AI is a Socratic and Evidence Assistant, not an Investment Advisor and not the source of truth.**

AI 可以澄清、提问、检索、提取、比较、暴露 uncertainty、建议 Evidence relationship 和生成草稿。

AI 不得创造金融事实、填补 unknown、自动宣布 Thesis 对错、把 summary 当作原始 Evidence、代替用户作最终投资判断或执行交易。AI 输出是 proposal / interpretation / extraction / draft；用户保留最终 Judgment 与 Action。

## 8. Point-in-Time and Evidence Lessons

- historical data 不等于 point-in-time correct data；
- observation time 不等于 publication / filing / revision / captured time；
- Current Query 不能替代 Frozen Evidence；
- provider metadata、symbol、mapping、历史数值和网页内容可能变化；
- 进入历史判断的关键 Evidence 必须保留足以追溯当时状态的来源与时间上下文；
- version 或其他语义不可获得时必须保持 unknown；
- AI summary 不能替代 Evidence source；
- OpenBB 是研究对象，不是已选择的 dependency。

PIT、provenance、revision 和 snapshot 是可信实验的约束，但当前不应扩张成通用数据平台。

## 9. What Four Research Rounds Changed

- **TradeNote：** import、notes、tags、绩效和 process analytics 已经成熟；“更多 Trading Journal 功能”不是差异。
- **Wealthfolio：** Account / Asset / Activity / canonical facts / derived state 的 Financial Reality 边界更加清晰。
- **Ghostfolio：** 交叉验证了稳定领域边界，也证明 Portfolio persistence、Cash 表达和具体实现不是唯一真理；Web SaaS 会带来大量横切复杂度。
- **OpenBB：** provider abstraction 可以复用，但 PIT、provenance、revision 和 Evidence Snapshot 仍需产品自己负责。

最终结论：不再以更多记录功能、更多图表、更多数据源或 AI 能调用金融数据作为核心差异。历史细节见 [`RESEARCH_SYNTHESIS.md`](research/RESEARCH_SYNTHESIS.md)，无需重新进行相同开源研究。

## 10. Current v0.1.0 Engineering Baseline

以下内容已根据当前 code、tests、Git tag 和目录核对：

- Python 项目，入口是 `main.py`；当前入口只初始化本地数据库并输出路径；
- 源码位于 `src/records/` 与 `src/storage/`；`reviews/` 和 `integrations/` 当前只有占位文件；
- 使用 Python 标准库 `sqlite3` 做本地持久化，默认数据库为 `data/investment_tracker.db`，路径固定相对 repository root；
- schema version 为 `1`，当前表是 `investment_records`，并为 `trade_date` 和 `symbol` 建索引；
- 核心模型是 monolithic `InvestmentRecord`，同时保存交易事实、reasoning 和 review 字段，并使用 `Action`、`Market`、`AssetType`、`StrategyType` 枚举；
- 金额字段使用 `Decimal`，在 SQLite 中按文本保存，避免二进制浮点误差；
- repository 当前实现 initialize、add、list、get 和 update；没有 delete 实现；
- tests 使用标准库 `unittest` 和临时 SQLite 数据库，当前共 11 项；
- `.gitignore` 忽略 `.vscode/`、Python cache，以及 `data/*.db`、`*.db-shm`、`*.db-wal`；本地数据库不得进入 Git；
- `requirements.txt` 当前只有 `packaging`、`setuptools`、`wheel`，现有运行代码没有第三方 runtime import。

常用命令：

```bash
python main.py
python -m unittest discover -s tests -v
```

运行前应激活可用 Python 环境；若 `python` 不在 `PATH`，使用当前工作区配置的 Python executable 执行同样的模块命令。

README 目前仍主要反映早期 MVP，可能滞后于正式 Product Vision、Roadmap 或当前实现。涉及产品状态时以正式 docs 为准，涉及实现行为时以 code 和 tests 为准。README 的已知差异应在明确的文档维护任务中修复，不要在无关任务中顺手修改；具体差异应以 repository 当时实际内容为准。

### 10.1 v0.1 Amount Semantics

当前代码和 tests 明确保证：

- `amount` 是历史成交金额；有 broker / source 金额时保留该事实；
- 未传入 `amount` 时，只在创建记录时用 `price * quantity` 填入历史金额；
- `fee` 独立保存，不自动并入 `amount`；
- `calculated_amount` 始终按当前 `price * quantity` 动态计算，用于比较和校验；
- 后续修改 price / quantity 不会静默重写已有历史 `amount`。

`InvestmentRecord` 是 v0.1 Financial Record MVP 的 monolithic model。它不是最终 schema，但也不应在没有验证需求阻塞时被推倒重写。

## 11. Current Roadmap

当前路径由证据解锁，而不是线性版本承诺：

```text
User Discovery
    ↓
Problem appears meaningful?
    ├─ No → revisit product hypothesis
    └─ Yes
         ↓
Controlled Prototype
         ↓
Repeated user value?
    ├─ No → simplify or change
    └─ Yes
         ↓
choose exactly one next hypothesis
```

当前不承诺传统的 `v0.2 → v0.3 → v0.4` 功能扩张。详细 gate、信号和退出标准见 [`ROADMAP.md`](ROADMAP.md)。

## 12. Controlled Prototype Boundary

只有 User Discovery 表明问题实际存在，才进入 Stage 2。受控原型保持很窄：

- 每个实验实例一个用户、一个真实 `InvestmentCase`；
- 一条真实 `Thesis`；
- 一个指标或一类 filing；
- 一个受控 Evidence 来源；
- 人工或半自动 capture；
- 原值 / 原文、source 和 captured time 可见；
- 按来源能力保留必要时间和版本语义，不可获得的保持 unknown；
- AI 只建议 relation；
- 用户确认相关性、relationship 和是否需要 review。

同一窄原型可以在少量候选用户上重复，以获得跨用户行为证据，但不能借此扩大功能范围。

## 13. Explicitly Deferred Work

当前不得擅自开始：

- 完整 broker sync 或全面 Financial Reality 重构；
- 完整 Portfolio Engine；
- production-grade Web multi-user SaaS；
- 完整 OpenBB integration 或通用 provider framework；
- A 股完整数据平台、全市场新闻；
- OCR 自动化；
- Decision Profile、月报 / 年报；
- complex performance、tax / lot / corporate actions；
- 全自动 Evidence classification；
- 自动交易。

其中自动交易是长期边界，不只是 deferred。最小安全、隐私、secrets、访问控制、许可和数据保留义务不能以“deferred”为由忽略。

## 14. Open Questions

以下问题没有定案，未来协作者不得从候选架构或竞品实现中猜答案：

- `InvestmentCase` 是单资产、多资产还是主题；是否跨 Account；
- Activity 与 Case / Decision 的 cardinality；
- 清仓再买是新 Case、恢复旧 Case，还是由用户选择；Case 如何开始和结束；
- Portfolio 是否需要持久化实体；
- Cash 使用 event、balance snapshot 还是受限双模式；
- Evidence、ContextSnapshot、Revision 和 review 对象的最终模型；
- Asset / Listing / provider mapping 的最终模型；
- 最终 schema 和 migration；
- local-first、cloud、self-hosted 或 hybrid；
- desktop、web 或 hybrid；
- SQLite 是否长期保留；
- 是否使用 OpenBB 或任何特定 provider；
- 是否以 A 股首发；
- Evidence Monitoring 是否有真实用户价值、合适内容与频率；
- 用户是否愿意结构化 Thesis、确认 AI 建议、持续使用和付费。

## 15. When Refactoring Is Allowed

> **Refactor in response to validated product needs, not architectural curiosity.**

只有可信实验被当前模型具体阻塞时，才做解除阻塞所需的最小增量修改，例如真实 Case 必须跨多笔 Activity、Evidence 必须独立持久化、Account / Asset identity 阻塞真实导入、Revision history 必须独立，或 ContextSnapshot 是可信实验的必要条件。

`ARCHITECTURE.md` 中存在更完整的候选模型，不构成主动重构 v0.1 的授权。

## 16. Source of Truth and Reading Order

新协作者推荐按以下顺序恢复项目：

1. [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)
2. [`PRODUCT_VISION.md`](PRODUCT_VISION.md)
3. [`DECISIONS.md`](DECISIONS.md)
4. [`ROADMAP.md`](ROADMAP.md)
5. [`ARCHITECTURE.md`](ARCHITECTURE.md)
6. [`RESEARCH_SYNTHESIS.md`](research/RESEARCH_SYNTHESIS.md)

只有需要历史研究依据时，才读取 `docs/research/` 下的单项目报告和 [`PRODUCT_VISION_DRAFT.md`](PRODUCT_VISION_DRAFT.md)。不要默认重新研究 TradeNote、Wealthfolio、Ghostfolio 或 OpenBB。

实现问题进一步读取 README、source、tests 和 Git history。旧聊天不是唯一 source of truth；repository 中的 code、tests、docs 与 Git history 共同构成项目长期记录。

> **Maintenance rule:** `PROJECT_CONTEXT.md` 是当前项目状态的 handoff snapshot，不是 append-only history。当 Product Vision、Accepted Decisions、Roadmap / current stage、Architecture 中转为正式决定的重要边界或 released engineering baseline 发生实质变化时，应同步更新本文；旧状态由 Git history、历史 docs 和 release / tag 保留，不要把历代过期状态不断追加到本文。
