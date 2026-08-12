# Investment Tracker 四轮开源研究综合报告

> 文档性质：基于 TradeNote、Wealthfolio、Ghostfolio、OpenBB 四轮已评审研究的横向综合
>
> 输入基线：`docs/PRODUCT_VISION_DRAFT.md` 与 `docs/research/` 下四轮研究报告、TradeNote Review Notes
>
> 输出目的：重新收敛产品定位、领域边界与 v0.2.0 的单一验证方向
>
> 结论边界：本文不是用户研究、PRD、最终架构或 v0.2.0 完整方案

## 0. 证据口径

本文区分三类陈述：

- **研究事实**：来自四份固定版本开源研究报告对产品、文档和源码的核验。
- **研究支持的判断**：由两个或多个研究事实交叉支持，可作为产品或架构候选，但不等于用户需求已经成立。
- **用户假设**：开源仓库无法验证，必须通过访谈、原型测试或产品实验获得证据。

全文中的 `SUPPORTED_DIRECTION` 表示“现有研究支持继续沿此方向验证或设计”，不表示 PMF、付费意愿或用户采用已经得到证明。

本报告只综合以下已进入仓库的材料，不重新研究四个项目：

- [`PRODUCT_VISION_DRAFT.md`](../PRODUCT_VISION_DRAFT.md)
- [`TRADENOTE_RESEARCH.md`](TRADENOTE_RESEARCH.md)
- [`TRADENOTE_REVIEW_NOTES.md`](TRADENOTE_REVIEW_NOTES.md)
- [`WEALTHFOLIO_RESEARCH.md`](WEALTHFOLIO_RESEARCH.md)
- [`GHOSTFOLIO_RESEARCH.md`](GHOSTFOLIO_RESEARCH.md)
- [`OPENBB_RESEARCH.md`](OPENBB_RESEARCH.md)

---

## 1. Executive Summary

四轮研究后，Investment Tracker 最重要的认识不是“找到了一个没有竞品的功能”，而是确认了三个不同问题不能再混在一起：

```text
Financial Reality：实际发生了什么、现在持有什么、结果如何
Investor Reasoning：用户当时为什么判断、哪些假设和条件支撑判断
Evidence & Review：当时和后来分别看到了什么、来源版本是什么、如何复核
```

TradeNote 证明 Trading Journal 的导入、归并、笔记、标签、截图、规则纪律和行为分析已经相当成熟；Wealthfolio 与 Ghostfolio 共同证明 Account、Asset、Activity/Transaction、Cash、FX、Position、Valuation 和 Performance 是成熟但复杂的 Portfolio Tracking 基础能力；OpenBB 证明 provider abstraction 与 standard model 可以降低外部数据接入成本，却不能自动提供完整的 point-in-time、fact-level provenance 或历史重放。

因此，项目不应把下列事项继续当作核心创新：更完整的交易日志、更多绩效图表、通用 Portfolio Engine、接入多个金融数据源，或让 AI 能调用金融数据。它们可能需要建设，但属于基础设施或行业能力。

四轮研究仍留下一个值得验证、但尚未被用户证明的候选差异：

> 围绕一个长期 `InvestmentCase`，把原始 Thesis、Assumptions、Review Conditions、后续 Evidence、Revisions 和 Final Review 组织成可追踪、可证伪、可回溯的生命周期，并严格区分 Investment Outcome 与 Decision Quality。

其中最有判别力的下一步，不是一次实现完整生命周期，而是只验证：

> **用户是否认为持有期间的 Evidence Monitoring 有持续价值。**

选择它不是因为技术风险最低，而是因为它直接检验产品是否能在买卖之间持续产生价值。如果答案是否定的，围绕自动数据、冻结、AI 分类和完整 Thesis 生命周期的大量建设都应重新评估；如果答案是肯定的，结构化 Thesis、AI 低摩擦澄清和 Freeze + Revision 才有明确的后续验证理由。

### 1.1 原始愿景中得到支持、被削弱、应放弃和仍未验证的部分

| 类别 | 当前综合判断 |
| --- | --- |
| 得到支持 | Financial Reality / Investor Reasoning / Evidence & Review 分层；财务事实与主观判断分离；Position 不等于 InvestmentCase；AI 不是 source of truth；Evidence 需要 provenance、版本和 snapshot；Outcome 与 Decision Quality 应在概念上分离。 |
| 被削弱 | “普通散户”作为统一目标用户；Transaction 作为长期推理中心；单独生成 AI Counter-Thesis；依赖大量已完成交易形成近期 Decision Profile；把降低复盘成本本身当差异。 |
| 应放弃 | `InvestmentRecord = trade + reason` 作为长期中心模型；`Position lifecycle = Case lifecycle`；把当前 MarketData 查询当作历史 Evidence；让 AI 自动判定 Thesis 真伪或给出买卖结论；在价值验证前补齐完整 broker sync、Portfolio Engine 和 Web SaaS。 |
| 仍未验证 | 用户是否愿意写 Thesis 和 Review Conditions；AI 追问是否降低摩擦；Evidence Monitoring 是否值得持续使用；用户是否理解 Freeze、Revision 和 Decision Quality；中文/A 股场景是否形成需求优势；local-first/cloud 偏好与付费意愿。 |

最终定位必须保持克制：研究支持“这是一个有逻辑的候选问题空间”，没有支持“用户一定需要它”或“产品已经形成差异化优势”。

---

## 2. What Each Project Taught Us

### 2.1 TradeNote：Trading Journal 已经成熟，Decision Accountability Loop 仍不完整

TradeNote 最重要的启示不是一份功能清单，而是它同时削弱和保留了原愿景的不同部分。

**研究事实：** broker/CSV import、execution 到 logical trade 的 aggregation、多账户过滤、notes、tags、screenshots、diary、playbook、P&L、MFE、按 setup/mistake/time/duration 等维度分析都已有实际实现。这些已经是通用 Trading Journal 能力。

**研究事实：** Satisfaction 可以独立于 P&L 标记是否遵守规则；setup/mistake analytics 可以从长期记录中发现模式。这否定了“现有工具只看盈亏、过程复盘完全空白”的强假设。

**研究支持的判断：** TradeNote 仍未把以下对象连成一个完整闭环：结构化 Thesis、可验证 Assumption、当时 Context、冻结的原始判断、版本化 Revision、后续 Evidence、条件触发和 Final Review。它更擅长回答“我怎样交易、哪些模式赚钱、是否遵守规则”，而不是“当初的假设后来是否得到事实支持”。

所以 TradeNote 留下的差异不是“也做 notes/tags”，而是能否把主观记录升级为有时间边界和证据链的 Decision Accountability Loop。

### 2.2 Wealthfolio：Financial Reality 必须与 Investor Reasoning 分离

Wealthfolio 展示了一套长期金融现实所需的纪律：Account 与 Asset 有独立身份，Activity 是 canonical ledger event，Cash、Fee、Tax、Income、Transfer 和 FX 有明确语义，Position/Holding/Performance 是从事实重建的状态，导入保留 provenance、idempotency 和 review boundary。

它还提供两个关键修正：

1. **Canonical facts 与 derived state 不能混为一谈。** Activity 可以更正，Position、Lot、Valuation 等派生状态应可重建。
2. **Transactions / Holdings 双模式是对证据完整性的诚实表达。** 有完整流水时可以重放；只有持仓快照时，可以开始使用，但不能假装拥有交易级归因。

**研究支持的判断：** `Position` 表达某账户某资产的财务状态，不表达用户为什么持有；同一个 Thesis 可以对应多次买卖和多个账户。`InvestmentRecord = trade + reason` 适合作为 v0.1 的探索模型，但不适合作为长期中心模型。

Wealthfolio 的 local-first 也提供了一项产品原则候选：核心账本由用户拥有、可导出、离线可读写，外部网络能力显式 opt-in。但“local-first 一定更受目标用户欢迎”仍是用户假设。

### 2.3 Ghostfolio：交叉验证稳定原则，也暴露实现选择并不等于领域真理

Ghostfolio 与 Wealthfolio 交叉验证了以下方向：Account 独立于 Asset；经济活动先于 Position；Quote/FX 是独立参考事实；Position/Holding/Performance 是可重算分析状态。

它同时给出了重要反例：

- Portfolio 不一定需要成为持久化实体，也可以只是用户事实加 filters 形成的计算范围；
- Cash 不一定必须复用证券 Activity，同样可以用余额观察表达，但会牺牲事件追溯；
- 有用的财富管理产品不一定已经实现完整 Lot、公司行动和所有绩效算法；
- server-first、多用户、分享、缓存和后台重算会引入大量运行复杂度，但这些复杂度不是新的投资领域。

**研究支持的判断：** Wealthfolio 的具体表结构和 Ghostfolio 的具体服务架构都不是本项目的答案。交叉验证真正稳定的是边界，而不是实现：事实、参考数据、派生状态、用户判断和证据版本应分开。

Ghostfolio 也说明完整 Web SaaS 会过早引入认证、租户隔离、访问控制、缓存、队列、备份、安全更新和可观测性。这些不会验证用户是否需要 Thesis Monitoring，因此当前不应成为核心问题。

### 2.4 OpenBB：数据接入可抽象，Point-in-Time 与 Evidence 仍需由产品负责

OpenBB 最值得借鉴的是：

```text
router → standard model → provider-specific fetcher
```

这个边界使外部 provider 可替换，上层接口相对稳定，并允许 provider extras 和 metadata 继续穿透。它削弱了“需要自己发明金融数据接入框架”的想法。

但 OpenBB 不是通用 point-in-time database：

- 历史 observation date 不等于当时 publication/filing cutoff；
- 财务和宏观历史可能已被 revision/restatement 改写；
- SEC `pit_mode` 是局部强能力，不是跨 provider 契约；
- 通用 provenance 主要到 invocation level，fact-level lineage 不统一；
- 缓存服务于性能和限流，不提供不可变历史 replay；
- agent citation 能力不保证 AI 解释正确或缺失值不被补写。

**研究支持的判断：** Evidence 必须是一个被冻结、可验证的事实包，而不是一个 `value`、URL 或 AI summary。至少需要 source、provider、原始标识、publication/filing/observation/revision/captured time、单位/币种、query、转换说明、snapshot/hash、质量状态，以及与 AI interpretation 分离的原始内容。

对中文/A 股，OpenBB 暴露的现实是：当前中国宏观数据线索强于 A/H 股主数据、法定公告、财务 PIT 和中文新闻。能用某个 provider suffix 查到一只股票，不等于形成稳定、可商用、可验证的数据层。azzE43R5

---

## 3. What Is No Longer Differentiated

以下能力未来可能仍然需要，但应被视为基础设施、行业能力或体验门槛，而不是产品核心差异。

### 3.1 Trading Journal 基础能力

- CSV / broker-specific trade import；
- broker parser / adapter；
- execution 到 logical trade 的 aggregation；
- 多账户筛选；
- notes、tags、screenshots、diary、playbook；
- Satisfaction、process discipline 和 mistake/setup 分类；
- 常规 P&L、MFE/MAE、win rate、profit factor；
- 按时间、symbol、方向、持仓时长、标签做 behavior/performance analysis；
- dashboard、daily view、calendar 和常规月度聚合。

### 3.2 Portfolio Tracking 基础能力

- Account 及 broker/platform metadata；
- 独立 Asset identity 与 provider symbol mapping；
- Transaction/Activity ledger；
- Cash、Fee、Tax、Dividend、Interest 和 Transfer 的财务语义；
- Position/Holding calculation；
- portfolio valuation 和 allocation；
- 多币种、历史 FX 与基准币种换算；
- performance calculation；
- import preview、validation、dedup、idempotency、ImportRun/provenance；
- 从 canonical facts 重建 derived state；
- local-first 或 self-hosted 的隐私友好部署路径。

### 3.3 Financial Data / AI 基础能力

- provider abstraction；
- standard financial models；
- provider-specific adapters 与能力表；
- AI/agent 调用金融数据工具；
- tool/widget citation；
- 对财报、新闻、行情、宏观数据的检索和摘要。

“不是差异化”不等于“不做”。它意味着：如果未来需要这些能力，应优先复用成熟概念、库或 provider，并把建设范围限制在核心实验所需的最小集合；不能用工程规模证明产品价值。

---

## 4. Reassessment of Original Product Hypotheses

| # | 原始假设 | 当前状态 | 支持与削弱证据 | 是否仍可能成为核心 | 下一步验证 |
| --- | --- | --- | --- | --- | --- |
| 1 | 从 Trading Performance 转向 Decision Quality | `PARTIALLY_SUPPORTED` | TradeNote 证明 performance/process analytics 已成熟，也用 Satisfaction 触及过程质量；四个项目都未形成 Thesis→Evidence→Review 的正式质量模型。 | 可以作为价值原则，但“用户是否重视”未验证。 | 先做用户验证；评分模型再做技术/概念验证。 |
| 2 | 为普通投资者而非专业短线交易者设计 | `WEAKENED` | TradeNote 确实偏日内交易；但“普通散户”过宽，完全凭感觉的用户可能只想要推荐，不愿复盘。 | 应收窄为已有自主逻辑但方法不成熟的人群。 | `USER_RESEARCH_REQUIRED`。 |
| 3 | AI 主动扮演反方辩手 | `WEAKENED` | 竞品未显示完整 Counter-Thesis；但泛化反对理由容易变成噪音，AI 也不是事实来源。 | 可改为 Socratic / Evidence Assistant，而非独立卖点。 | 先做交互原型和用户测试，再做受控准确性测试。 |
| 4 | 区分 Investment Outcome 与 Decision Quality | `PARTIALLY_SUPPORTED` | TradeNote 已将 Satisfaction 与 P&L 并列，说明概念不是完全空白；但现有系统未正式验证原假设与后续事实。 | 适合作为核心领域原则，不足以单独构成产品。 | 用户理解度验证 + 质量维度定义实验。 |
| 5 | Freeze Decision + 后续事实验证 | `SUPPORTED_DIRECTION` | TradeNote 的可覆盖 notes、Portfolio 工具的事实重算、OpenBB 的 revision/PIT 风险共同说明冻结版本和追加 Revision 的必要性。 | 是建立问责与防止事后包装的关键机制。 | 用户是否在意 Freeze 需验证；snapshot/PIT 做窄技术原型。 |
| 6 | Decision Profile | `WEAKENED` | TradeNote 已有行为模式分析；长期投资的独立 Case 样本太少，checkpoints 不能伪装成独立样本。 | 只能是远期结果，必须显示 sample size/confidence。 | 长期用户研究；当前不要作为 v0.2.0 核心。 |
| 7 | 降低普通投资者复盘成本 | `NOT_DIFFERENTIATED` | 导入、图表、notes、tags、截图、日记和自动分析都已明显降本。 | 仍是体验要求，但不是定位。 | 验证哪一步摩擦最大，以及 AI 是否真的降低它。 |
| 8 | 中文 / A 股场景优化 | `UNVALIDATED_USER_HYPOTHESIS` | 竞品与 OpenBB 的公开覆盖存在缺口，但缺席不等于需求；本地数据、公告、PIT、许可和券商导入反而风险更高。 | 可能形成场景优势，当前不能作为已成立差异。 | 中文/A 股用户研究 + 独立数据可得性 spike。 |

这八项中，研究最强支持的是“分层、冻结和事实/解释边界”；最弱的是“目标用户一定愿意承担结构化复盘成本”。技术可实现与值得做必须继续分开。

---

## 5. Candidate Differentiation

### 5.1 Investment Thesis Lifecycle

候选生命周期为：

```text
InvestmentCase
→ Thesis
→ Assumptions
→ Review Conditions
→ Revisions
→ Final Review
```

**研究支持的部分：** 它比 `Transaction → Note` 更符合一项长期判断跨多次加减仓、多个账户和多年持有的现实；也为 Freeze、Revision 和 Evidence 提供明确容器。

**仍然抽象的部分：** 用户心中的 Case 究竟是一只资产、一轮建仓、跨账户总头寸还是主题；用户愿意结构化到什么程度；“可证伪”是否适合所有投资风格。

**风险：** 如果用户只想保存简短理由，这套生命周期会变成强迫填写的领域仪式。它值得继续研究，但不能先按最完整模型建库。

### 5.2 Thesis Monitoring

持有期间持续发现 supporting、contradicting、unclear evidence，并提醒用户预设的 review condition，是当前最值得验证的候选差异。

**为什么重要：** 长期用户独立交易样本少；如果产品只在 BUY/SELL 时产生价值，使用频率太低。Monitoring 尝试把价值移到持有期间，并为 Final Review 积累当时证据。

**为什么仍危险：** 用户可能不想被持续打扰；一条证据与 Thesis 的关系可能高度主观；数据噪音、AI 误判、通知疲劳和来源成本都可能超过价值。

它不是已验证功能，而是下一阶段最有信息增益的产品实验。

### 5.3 Point-in-Time Decision Accountability

冻结原始理由、当时可知 Context、用户设定的 Review Conditions 和后续 Revisions，可以减少 hindsight bias 与事后移动标准。

**研究支持的部分：** OpenBB 证明当前查询会受到 revision、restatement、provider mapping 和网页变化影响，因此 snapshot 必须真实保存；TradeNote 证明普通可编辑 notes 不具备该语义。

**产品边界：** Point-in-Time 更像信任与审计原则，不一定是用户首先购买的价值。若用户不关心持续复核，严格的 snapshot 只会增加成本。

### 5.4 AI as Socratic / Evidence Assistant

AI 最合适的职责是：澄清模糊 Thesis、提出可验证问题、检索和提取 Evidence、指出不确定性、建议证据关系，并保留 source link。它不应宣布 Thesis 正确/错误或给出买卖建议。

**候选价值：** 把“我觉得这个行业会变好”转换为可观察假设，可能降低结构化输入门槛。

**风险：** 追问可能增加摩擦；AI 可能诱导用户接受事后包装；分类可能把相关性写成因果。所有关键解释都应是 proposal，原始 Evidence 与用户最终确认必须可见。

### 5.5 Decision Quality ≠ Outcome

这是必要的评价原则：赚钱不自动证明判断正确，亏钱也不自动证明判断错误。

但它目前仍过于抽象。若没有 Frozen Thesis、当时 Context、明确 Assumption 和后续 Evidence，就无法操作化 Decision Quality；若用户不理解或不重视该区别，它也不能单独形成需求。

### 5.6 候选方向的相对判断

| 候选 | 当前价值 | 主要风险 | 综合判断 |
| --- | --- | --- | --- |
| Investment Thesis Lifecycle | 形成产品的长期语义中心 | 结构化摩擦、Case 心智模型未定 | 值得研究，暂不完整实现 |
| Thesis Monitoring | 在持有期间持续产生价值 | 噪音、数据、AI 误判、通知疲劳 | **最值得下一步验证** |
| PIT Decision Accountability | 防止历史被未来信息改写 | 用户可能感知不到，技术与许可成本高 | 作为 Monitoring 的可信性约束 |
| Socratic / Evidence Assistant | 可能降低 Thesis 与 Review 摩擦 | 可能反而增加摩擦或诱导 | 作为交互机制验证，不单独做 AI 产品 |
| Decision Quality ≠ Outcome | 明确产品评价原则 | 抽象、难测、反馈周期长 | 保留原则，后置完整模型 |

---

## 6. Target User Reassessment

### 6.1 三类用户

#### A. 完全凭感觉、主要想知道“买什么”的用户

这类用户可能不主动需要复盘，不愿结构化输入，并倾向于用是否赚钱评价产品。产品若强调 AI，反而可能强化其对推荐和确定答案的期待。当前方向与其核心需求不匹配。

#### B. 已开始形成自主投资逻辑，但方法不成熟的用户

这类用户已有 Thesis 雏形，会做一些基本研究，也明确希望提高判断质量；他们缺少的是结构化记录、条件定义、持有期监控和复盘方法。其现有动机与候选价值最匹配，也有真实材料可用于原型测试。

#### C. 已有成熟投资体系的资深用户

这类用户可能已有自己的模型、文档和工作流，对 AI 错误与数据口径非常敏感。他们可以提供高质量反馈，却未必愿意迁移到本项目的结构或依赖自动分类。

### 6.2 当前 early adopter 候选

**推荐优先验证 B 类：** 已有自主投资逻辑、持有周期以中长线或低频波段为主、愿意改善方法，但尚未形成稳定的 Thesis tracking workflow 的个人投资者。

选择 B 不是因为代码研究证明了他们会采用产品，而是因为：

- A 类与“提高决策质量”的主动需求最弱；
- C 类迁移成本和可信度要求最高；
- B 类既有真实 Thesis，又最可能感受到记录和监控缺口。

这仍是 `UNVALIDATED_USER_HYPOTHESIS`。下一步必须用真实投资案例观察其当前工作流、实际摩擦、持续使用意愿与付费意愿，不能用开源竞品缺少该功能来代替验证。

---

## 7. Three-Layer Domain Model

### 7.1 总体判断

三层模型继续成立，而且四轮研究使边界更清晰：

```text
Evidence & Review
        ↓ supports / challenges / triggers
Investor Reasoning
        ↓ decisions link to, but do not rewrite
Financial Reality
```

这是一组 bounded responsibilities，不是最终数据库表，也不要求三层分别成为独立服务。

### 7.2 Financial Reality

Financial Reality 内部至少应区分三种数据性质。

| 性质 | 候选对象 | 语义 |
| --- | --- | --- |
| Canonical facts | Account；Activity/Transaction；已确认的 Cash event 或 balance snapshot；Import/Source identity | 用户或来源确认后进入账本的金融事实；可更正并保留来源。 |
| Reference facts | Asset/Listing identity；provider mapping；Price/Quote；FX；必要的 corporate action/reference classification | 外部市场与标识事实；有来源、有效时间和口径。 |
| Derived state | Position；Holding；Cash balance（事件模式下）；Valuation；Allocation；Performance；某些 Portfolio scope/read model | 从 canonical/reference facts 计算；应可重建，不是第二套真相。 |

需要保留两个重要例外：

1. 在 Holdings tracking mode 中，用户导入的某日 Position Snapshot 可以是 source fact；系统必须标明它不能支持完整交易级归因。
2. Portfolio 是否持久化取决于是否需要命名、保存、比较或授权稳定范围；Ghostfolio 已证明它也可以只是 derived/query scope。

当前基本可以认为不应混在一起的对象包括：Account 与 Asset、source record 与 canonical activity、Activity 与 Position、Position 与 InvestmentCase、原始金额与换算后的估值、当前 Quote 与冻结 Evidence。

### 7.3 Investor Reasoning

候选对象为：

- `InvestmentCase`：独立 reasoning aggregate；
- `Thesis`：用户对未来或因果关系的核心判断；
- `Assumption`：支撑 Thesis 的可检查前提；
- `ReviewCondition`：需要重新评估的预设条件；
- `Decision`：建立、加仓、减仓、持有、退出或不行动等用户决定；
- `Revision`：追加的新判断，不能静默覆盖原版本。

**当前判断：** `InvestmentCase` 继续作为独立 reasoning aggregate 候选是合理的。它不应被 Position 或 Transaction 拥有，因为它可以在交易前存在、跨多笔 Activity、跨账户延续、清仓后继续复盘。

但以下问题必须保持未定：

- 一个 Case 对一个 Asset，还是可以对多个 Asset/主题；
- Account 是 context/link，还是在某些场景中成为 Case scope；
- 清仓后重新买入默认新建 Case、恢复旧 Case，还是由用户选择；
- 一笔 Activity 是否可以执行多个 Case/Decision；
- Case 是否允许在交易发生前创建；
- Position lifecycle 与 Case lifecycle 在 UI 中如何协调。

现有研究支持“分开”，不支持直接选择最终基数或数据库 schema。

### 7.4 Evidence & Review

候选对象为：

- `Evidence`：有来源、版本、时间和完整性信息的事实包；
- `ContextSnapshot`：某次 Decision 当时实际可见 Evidence 与关键现实事实的冻结集合；
- `Checkpoint`：持有期间围绕 Thesis 的阶段复核；
- `OutcomeReview`：结束后对原 Thesis、过程和实际 outcome 的回顾；
- `DecisionProfile`：样本足够后的长期模式读模型，当前应后置。

这一层不能简单并入 MarketData，原因是：

- Evidence 不只包含价格，还包含 filing、news、macro、用户观察和文档；
- MarketData 的当前查询结果会修订，Evidence 需要冻结版本；
- Evidence 需要 publication、filing、observation、revision、captured time；
- Evidence 需要说明它为何被选入某次判断；
- 同一 source fact 可以被多个 Thesis/Checkpoint 引用；
- AI interpretation 和用户确认有自己的 revision 状态，不能改写 source fact。

### 7.5 Evidence 的最低语义

Evidence 至少应保留：subject、type、original value/content、upstream source、provider/adapter、raw identifier/URL、time semantics、unit/currency/frequency/adjustment、query 与 mapping version、quality/warnings、captured snapshot/hash，以及独立的 interpretation state。

未知 publication time、revision 或单位必须保持未知。AI 不得为了生成完整叙事而补成事实。

---

## 8. High-Confidence Domain Boundaries

以下原则已有较强交叉证据，可作为未来 `DECISIONS.md` 的候选输入，但本轮不直接修改该文件。

1. **Account ≠ Asset。** Account 是所有权、现金和限制边界；Asset 是可跨账户引用的金融标的身份。
2. **Provider/Broker ≠ Account。** Provider 是数据或连接来源，不能替代用户真实账户身份。
3. **Source record ≠ Canonical Activity ≠ Derived State。** 一条来源记录可映射为多个领域事件；Position、Valuation、Performance 应从事实重建。
4. **Transaction / Activity ≠ Position。** 前者是发生过的事件，后者是某时点状态。
5. **Position ≠ InvestmentCase。** 财务状态不能承担用户判断的身份和生命周期。
6. **Financial Fact ≠ Investor Reasoning。** 修正成交或资产映射不能静默改写用户原始理由。
7. **MarketData / Current Query ≠ Frozen Evidence。** 历史查询可能因复权、重述、provider 或网页变化而改变。
8. **Evidence Source Fact ≠ AI Interpretation。** AI 只提出提取、关联和分类建议；原始来源和用户确认独立保存。
9. **Investment Outcome ≠ Decision Quality。** 盈亏是结果约束，不是对判断过程的自动判决。
10. **Fact correction ≠ Reasoning revision。** 财务事实可以更正；用户判断通过追加 Revision 演化，不能原地重写历史。
11. **Provider symbol ≠ Internal Asset Identity。** 内部 Asset、listing identity 和 provider identifiers 应可分别演进。
12. **Observation time ≠ Publication/Filing time ≠ Captured time。** PIT 语义不能压成一个日期。
13. **Portfolio 不必天然是持久化实体。** 只有稳定命名、比较、授权或目标场景出现时才需要决定。
14. **Web/多用户/队列是横切运行能力，不是第四个投资领域。** 当前无需为它改变三层模型。
15. **Checkpoint 数量 ≠ 独立决策样本量。** Decision Profile 必须按独立 Case、样本量和置信度表达。

---

## 9. Remaining Unknowns

以下问题不能通过继续阅读更多开源代码仓库得到答案。除少数同时需要技术 spike 的问题外，均应标记为 `USER_RESEARCH_REQUIRED`。

| 未知问题 | 为什么现有研究不能回答 | 所需验证 |
| --- | --- | --- |
| 用户是否愿意写 Thesis | 仓库只能证明结构可实现，不能证明使用动机 | `USER_RESEARCH_REQUIRED` |
| 用户是否愿意定义 invalidation / review conditions | 可能减少 hindsight，也可能显著增加摩擦 | `USER_RESEARCH_REQUIRED` |
| AI 提问降低还是增加摩擦 | AI 能生成问题不等于问题有帮助 | `USER_RESEARCH_REQUIRED` + 交互原型 |
| Evidence Monitoring 是否有持续价值 | 四轮研究没有目标用户使用证据 | `USER_RESEARCH_REQUIRED` + 产品实验 |
| 多高频率的 monitoring 才不烦 | 取决于持有周期、信息类型和个人偏好 | `USER_RESEARCH_REQUIRED` |
| 用户是否愿意确认 AI evidence classification | 需要观察真实复核行为，而不是询问抽象态度 | `USER_RESEARCH_REQUIRED` |
| 用户是否理解 Decision Quality | 概念上合理不代表用户会采用或付费 | `USER_RESEARCH_REQUIRED` |
| InvestmentCase 的真实心智模型 | Case 可能是资产、仓位周期、账户头寸或主题 | `USER_RESEARCH_REQUIRED`，使用真实投资史 |
| 清仓再买是否为新 Case | Position 生命周期无法替用户决定 | `USER_RESEARCH_REQUIRED` |
| 中文/A 股用户的真实导入条件 | 不同券商、账单、截图和历史完整度差异大 | `USER_RESEARCH_REQUIRED` + 数据样本审计 |
| 用户是否愿意付费 | 开源实现和技术可行性均不能证明 | `USER_RESEARCH_REQUIRED` |
| local-first / cloud 的信任偏好 | 两种成熟实现都存在，偏好依用户与场景 | `USER_RESEARCH_REQUIRED` |
| 哪类 Evidence 最值得提醒 | filing、指标、新闻、价格事件的价值与噪音不同 | `USER_RESEARCH_REQUIRED` |
| Freeze + Revision 是否被重视 | 它可能是后台可信性要求，而非可感知价值 | `USER_RESEARCH_REQUIRED` |

### 9.1 当前最大的技术未知

在目标市场和许可条件下，能否对一组足够有用的 Evidence 持续保存正确的 point-in-time、provenance、revision 和 snapshot 语义，同时把噪音与成本控制在可接受范围。

OpenBB 已证明窄范围技术原型可行，尤其是 SEC filing + 单一明确指标；它没有证明任意市场、任意 Thesis、全自动分类可行。对 A/H 股，这个未知更大。

### 9.2 当前最大的用户未知

目标用户是否认为持有期间的 Evidence Monitoring 带来的“少遗漏、早复核、保留判断演化”足以抵消设置 Thesis、确认证据和处理提醒的持续摩擦。

这是下一阶段首先应回答的问题。

---

## 10. Reinterpretation of v0.1.0

v0.1.0 不应被描述为失败，也不需要被否定。更准确的重新定位是：

> 一个用于验证交易事实、SQLite persistence、Decimal 金额语义和基础 repository 的 Financial Record MVP。

### 10.1 继续有价值的部分

- 已发布、可运行、可测试的产品基线；
- SQLite 本地持久化经验；
- Decimal 金额处理，避免用二进制浮点表达金融金额；
- repository 边界和基础测试；
- 对交易事实、增删改查和迁移成本的真实工程反馈；
- 为后续区分 Financial Reality 与 Reasoning 提供了可观察的现状，而不是纸面模型。

### 10.2 临时 monolithic model

当前 `InvestmentRecord` 把 trade、reason、context、thesis、risk、exit/review 等候选概念放在同一记录中。这在 v0.1 用于验证端到端持久化是合理的，但长期会产生：

- 成交事实纠错与历史判断改写共用更新路径；
- 一项 Thesis 跨多笔交易时重复或丢失理由；
- 缺少 Account、稳定 Asset、Currency 和 provenance；
- Position、Outcome 和 Decision 无法形成独立生命周期；
- BUY/SELL 之外的收入、费用、转账和公司行动难以扩展。

这些是未来可重构的边界，不是要求现在立即推倒的缺陷清单。

### 10.3 为什么不推倒重来

1. SQLite、Decimal、repository 和测试仍可服务未来任何方向。
2. 下一阶段的核心未知是用户价值，不是最终 schema；现在重构会把候选模型过早固化。
3. InvestmentCase 的基数、Account 关系、Cash 表达、Portfolio 持久化和 Evidence 自动化都还未确定。
4. 窄范围产品实验可以使用最小适配或独立实验数据，不需要先迁移完整账本。

### 10.4 为什么也不应立即重构

当前重构不会回答用户是否需要 Evidence Monitoring，反而可能投入 Account、Portfolio、broker sync、PIT 数据平台等大量基础设施。只有当产品实验确认需要哪些最小领域合同时，才应为对应边界制定增量迁移方案。

---

## 11. One Core Hypothesis for v0.2.0

### 11.1 五个候选的风险比较

| 候选 | 用户价值风险 | 技术风险 | 数据依赖 | 实现复杂度 | 过早建设基础设施风险 | 获得真实反馈的难易 |
| --- | --- | --- | --- | --- | --- | --- |
| A. 用户愿意结构化记录 Thesis | 高：可能只愿写自由文本 | 低 | 低 | 低到中 | 低 | 容易，但只能验证输入意愿 |
| B. AI 能低摩擦形成可证伪 Thesis | 高：追问可能更烦或诱导 | 中：质量、可控性、来源标记 | 低 | 中 | 中 | 较容易，但依赖用户本就关心 Thesis |
| C. 持有期间 Evidence Monitoring 有持续价值 | **最高且最关键**：价值可能小于噪音 | 中到高，但可用窄范围/人工方式压缩 | 中到高；依市场与 Evidence 类型 | 中；不应扩展为数据平台 | **高，若追求全市场自动化** | **最有判别力**，可观察回访、确认和行动 |
| D. 用户重视 Freeze + Revision | 中：可能只在出错后才感知 | 低到中：snapshot/versioning | 低到中 | 低到中 | 中 | 反馈周期较长，容易得到礼貌性认可 |
| E. 用户理解并重视 Decision Quality ≠ Outcome | 高：概念抽象 | 中：质量维度难定义 | 需长期 outcome/evidence | 中到高 | 中 | 慢，容易停留在态度而非行为 |

### 11.2 选择 C

如果 v0.2.0 只能验证一个假设，选择：

> **C. 用户是否认为持有期间的 Evidence Monitoring 有持续价值。**

原因不是 C 最容易，而是它最接近产品能否从“交易记录工具”升级为“Thesis lifecycle system”的分水岭。

- 如果 C 不成立，A/B 可能只是更复杂的写笔记方式，D 可能只是用户无感的审计机制，E 也缺少持续事实基础。
- 如果 C 成立，A 是建立监控对象的必要输入，B 是降低输入摩擦的后续机制，D 是保持可信性的必要边界，E 是长期复盘目标。

实验中仍需要一条最小 Thesis 和一个可识别 Review 目标，但它们只是测试 C 的必要脚手架，不应把 A、B、D、E 同时宣称为已验证目标。

### 11.3 “验证阶段不做”清单

为了让用户价值验证优先于完整基础设施建设，本阶段明确不做：

- **完整 broker sync**：不会提高对 Evidence Monitoring 价值的判别力，却带来长期适配和安全成本；
- **完整 Portfolio Engine**：一项真实持仓和最小上下文足以实验，不需要先实现全面估值；
- **Web multi-user SaaS**：认证、隔离、队列和运维会掩盖核心反馈；
- **全市场 news**：噪音、授权和去重问题会使实验变成新闻平台建设；
- **任意 Thesis 自动理解**：先限制一个明确 Thesis/指标，避免把模型泛化能力当价值；
- **全自动 AI 判断**：AI 只建议 `SUPPORTING` / `CONTRADICTING` / `UNCLEAR`，用户最终确认；
- **自动买卖建议**：偏离 Thinking Assistant 边界，也无法验证 C；
- **完整 A 股数据平台**：当前主数据、公告、财务 PIT 和许可均未解决，范围会吞没实验；
- **Decision Profile**：独立样本量和长期周期都不支持当前生成；
- **月报/年报**：属于后续汇总形式，不是持有期单条 Evidence 是否有用；
- **大量图表**：视觉分析不能代替“该证据是否改变复核”的反馈；
- **完整 OpenBB 集成**：可直接使用一个受控来源或薄 adapter，避免将平台接入当成果。

这份清单不是长期产品否决表。它只说明在验证 C 时，建设范围必须服从信息增益。

### 11.4 允许的最小验证边界

不定义完整 v0.2.0，只给出保证实验可信所需的边界：一个真实持仓、一个用户已有 Thesis、一个明确指标或一类 filing、人工或半自动挑选 Evidence、展示原值/原文和来源、AI 只给关系建议、用户确认相关性以及是否需要复核。

需要观察的是持续行为：用户是否回来查看、是否认为提醒减少遗漏、是否愿意确认/纠正、是否调整 confidence 或触发 review。数据抓取数量和 AI 生成字数不是成功证据。

---

## 12. Technical Research vs User Research

| 问题 | 当前证据 | 下一步 |
| --- | --- | --- |
| Account 应独立于 Transaction | Wealthfolio 与 Ghostfolio 交叉支持 | 进入架构候选；暂不为实验做全量重构 |
| Asset 应独立于 Account | 两个 Portfolio 项目均支持，OpenBB 进一步显示 provider symbol 不稳定 | 进入架构候选；未来设计内部 identity/mapping |
| Source record、canonical event、derived state 应分离 | TradeNote、Wealthfolio、Ghostfolio 均提供正反例 | 进入高置信原则 |
| Position 是否等于 InvestmentCase | 两个 Portfolio 项目都显示 Position 是派生状态 | 明确不等同；具体 links 交给用户研究 |
| Portfolio 是否必须持久化 | Wealthfolio 持久化，Ghostfolio 作为 scope | 保持未定，等真实命名/分享需求 |
| PIT 数据是否完全可得 | OpenBB 表明仅局部成立，SEC 较强、中国较弱 | 做窄技术 spike，不建设通用 PIT 平台 |
| Evidence Snapshot 是否需要自存 | provider 修订、网页变化、缓存过期和 mapping 升级共同支持 | 进入架构候选；实验只保存最小可信 snapshot |
| Provider abstraction 是否可行 | OpenBB 已充分证明 | 借鉴模式，不重新发明完整框架 |
| A/H 股主数据、公告、财务 PIT 是否可用 | OpenBB 公开实现显示明显缺口 | 独立技术/许可 spike，不能以查询成功替代覆盖验证 |
| 用户是否愿意写 Thesis | 开源项目无法回答 | `USER_RESEARCH_REQUIRED` |
| 用户是否愿意定义 Review Conditions | 没有用户证据 | `USER_RESEARCH_REQUIRED` |
| AI 澄清是否降低摩擦 | 技术上可生成，价值和诱导风险未知 | 交互原型 + 真实任务观察 |
| Evidence Monitoring 是否有价值 | 没有用户证据；只是最有判别力方向 | 产品实验，v0.2.0 单一假设 |
| monitoring 频率多高合适 | 代码研究无法回答 | 真实持仓纵向测试 |
| 用户是否确认 AI classification | 代码只能实现状态 | 观察实际接受、修改、忽略比例 |
| 用户是否理解 Outcome / Decision Quality | 概念受支持，采用未知 | 使用真实盈亏反例做访谈/可用性测试 |
| InvestmentCase 是一个还是多个 Asset | 现有仓库没有目标用户心智模型 | 基于真实投资史的 contextual inquiry |
| 清仓再买是否新 Case | Position 不能给答案 | 用户研究，并保留可撤销设计 |
| local-first 还是 cloud | Wealthfolio 与 Ghostfolio 分别证明两者可行 | 信任/协作概念测试，不由技术偏好决定 |
| 用户是否愿意付费 | 无任何开源研究证据 | 价值访谈、试用行为和后续付费实验 |

该表的目的，是阻止下一阶段继续用代码仓库回答用户问题。技术研究应收缩到会阻塞可信实验的窄问题；其余未知必须进入真实用户与产品验证。

---

## 13. Inputs for Final Project Docs

本节只整理后续正式文档应该吸收什么，不在本轮创建或修改这些文件。

### 13.1 `PRODUCT_VISION.md`

建议写入：

- 收窄后的问题：帮助已有自主逻辑的个人投资者持续澄清、跟踪和复核 Investment Thesis；
- AI 是 Socratic / Evidence Assistant，不是 Investment Advisor；
- Investment Outcome 与 Decision Quality 分离；
- 候选价值分布在形成 Thesis、持有期 Monitoring、结束后 Review 三个时点；
- 中文/A 股只是待验证场景，不是已成立优势；
- 明确所有用户价值与付费结论仍未验证。

### 13.2 `DECISIONS.md`

建议写入高置信边界：

- Account ≠ Asset；Transaction ≠ Position；Position ≠ InvestmentCase；
- source record ≠ canonical event ≠ derived state；
- Financial Fact ≠ Investor Reasoning；
- Current MarketData ≠ Frozen Evidence；
- AI interpretation ≠ source of truth；
- Outcome ≠ Decision Quality；
- observation/publication/filing/revision/captured time 分离；
- fact correction 与 reasoning revision 分离。

只记录真正定案的原则；Case 基数、Portfolio 持久化、Cash 表达和部署模式应继续保持未定。

### 13.3 `ARCHITECTURE.md`

可以描述的候选架构：三层 bounded responsibilities；Financial Reality 内的 canonical/reference/derived 分层；external provider adapter；Evidence Snapshot/provenance；Reasoning Revision 与用户确认边界。

应保持未定的内容：最终数据库 schema、InvestmentCase 基数、一个或多个 Asset、Account ownership、Transaction 分摊、Portfolio 是否实体、Cash event 或 balance、local-first/cloud、OpenBB 是否集成、服务拆分。

### 13.4 `ROADMAP.md`

下一阶段应围绕单一假设 C 组织：先做用户问题发现与受控原型，再决定是否开发；技术工作只覆盖可信 Evidence 所需的最小来源、snapshot 和展示。完整 broker sync、Portfolio Engine、Web SaaS、A 股全数据与 Decision Profile 不进入当前阶段。

### 13.5 `PROJECT_CONTEXT.md`

新任务最需要知道：

- v0.1.0 是已发布的 Financial Record MVP，不是失败版本；
- 四轮研究已完成，不应重复抓取同一项目；
- 当前最大用户未知是 Evidence Monitoring 的价值/摩擦；
- 当前最大技术未知是窄范围 PIT/provenance 在目标市场的可持续性；
- 三层模型是候选边界，不是最终 schema；
- 不得把竞品缺失写成用户需求，也不得把技术可行写成值得做。

### 13.6 `AGENTS.md`

建议 Codex 长期遵守：

- 明确区分事实、研究支持的判断和用户假设；
- 不用更多开源代码研究替代用户研究；
- 不在价值验证前扩大 v0.2.0 范围；
- 不把成熟基础设施描述成产品差异；
- 不让 AI 输出成为金融事实或买卖建议；
- 不静默丢失 provenance、PIT、unknown 和 revision；
- 不未经决策修改既有发布、数据库或领域模型；
- 任何架构提案都标明可撤销假设和验证依据。

### 13.7 推荐的文档组织顺序

先完成 `PRODUCT_VISION.md` 和少量真正定案的 `DECISIONS.md`，再写仅描述候选与未决项的 `ARCHITECTURE.md`；`ROADMAP.md` 围绕单一产品实验；`PROJECT_CONTEXT.md` 与 `AGENTS.md` 最后固化协作上下文和防偏航约束。不要用 Architecture 先行替代产品决策。

---

## 14. Candidate Product Positioning

### 14.1 Investment Thesis Monitor + Decision Journal

- **强调：** 持有期间 Monitoring 与完整 Decision Journal 的结合。
- **隐藏：** Financial Reality、PIT 和 Evidence provenance 等底层可信性工作。
- **可能误导：** “Monitor” 容易让用户以为覆盖所有新闻和自动判断 Thesis 状态。
- **当前适用性：** 最适合作为内部工作定位，但必须附带“受控 Evidence、用户最终确认、非投资建议”的边界。

### 14.2 A system that helps self-directed investors turn investment ideas into trackable, falsifiable and reviewable theses.

- **强调：** 从模糊 idea 到可追踪、可证伪、可复核 Thesis 的转化。
- **隐藏：** 持有期 Evidence Monitoring 与真实交易/持仓连接。
- **可能误导：** 可能被理解为一次性的 AI 写作或 Thesis 生成工具。
- **当前适用性：** 适合作为内部产品结果描述，尤其适合指导 Socratic workflow；不宜单独替代产品类别。

### 14.3 Point-in-Time Investment Decision Review System

- **强调：** Freeze、当时可知信息、Revision 和 Outcome/Decision Quality 分离。
- **隐藏：** 持有期间的持续价值与低摩擦输入。
- **可能误导：** 容易显得像审计工具，或让用户误以为任意历史 Context 都能被完整还原。
- **当前适用性：** 适合作为内部可信性原则，不适合作为当前首选产品定位。

**综合建议：** 当前内部定位采用第一项，产品结果陈述参考第二项，第三项作为设计原则。暂不改项目名，也不对外宣称完整 Monitoring、PIT 覆盖或用户价值已经验证。

---

## 15. Final Recommendations

1. **停止用功能缺口定义创新。** Notes、tags、broker import、绩效、portfolio、provider abstraction 和 AI tool use 都按成熟能力处理。
2. **保留三层模型，但只固化边界。** Financial Reality、Investor Reasoning、Evidence & Review 成立；表结构、服务拆分和 Case 基数仍保持可撤销。
3. **把 InvestmentCase 保留为独立 reasoning aggregate 候选。** 不再以 Transaction 或 Position 作为长期中心，也不在用户研究前决定一对一/多对多关系。
4. **收窄 early adopter。** 优先验证已经有自主投资逻辑、但缺少结构化跟踪与复核方法的人，而不是笼统的“普通散户”。
5. **v0.2.0 只验证 Evidence Monitoring 的用户价值。** 使用窄来源、真实 Thesis、原始证据可见、AI 建议和用户确认；不以抓取量、自动化率或图表数量衡量成功。
6. **把 Freeze/PIT/provenance 当可信实验的约束，不当作先行平台项目。** 只实现实验所需的最小 snapshot，未知保持未知。
7. **让 AI 职责继续收缩。** AI 澄清、检索、提取和建议；用户确认，source fact 独立，禁止自动买卖结论。
8. **保留 v0.1.0。** 将它视为 Financial Record MVP，在核心假设得到反馈前不推倒、不大规模重构。
9. **将中文/A 股拆成用户机会与技术现实两条验证线。** 竞品缺席不证明需求；数据缺口也不应迫使当前建设完整平台。
10. **下一轮证据必须来自真实用户行为。** 重点观察 Thesis 输入、Evidence 复核、提醒噪音、回访频率、confidence/review 变化和付费意愿，而不是继续扩大开源仓库样本。

四轮研究后的产品问题可以最终收敛为：

> 不是“怎样做一个更完整的 Investment Tracker”，而是“已有自主投资逻辑的人，是否愿意使用一个有来源、有时间边界、可修订但不可静默改写的系统，在持有期间持续检查自己的 Thesis”。

在这个问题获得真实用户证据之前，所有候选定位、领域模型和 AI 工作流都应保持可撤销。
