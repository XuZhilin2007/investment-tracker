# Investment Tracker Roadmap

> 文档性质：Product Vision 收敛后的产品验证路线
>
> 当前状态：v0.2.0 扩展前的条件式验证计划；不是功能愿望清单或版本承诺
>
> 正式输入：[`PRODUCT_VISION.md`](PRODUCT_VISION.md)、[`DECISIONS.md`](DECISIONS.md)、[`ARCHITECTURE.md`](ARCHITECTURE.md)

## 1. Purpose

Roadmap 的目的不是预先安排越来越完整的功能，而是：

> 通过最小实验减少下一阶段最大的未知。

当前最大未知不是最终 schema、Portfolio Engine 或数据覆盖，而是目标用户是否从持有期间的 Thesis / Evidence Monitoring 中获得足以抵消设置、确认和提醒摩擦的持续价值。

因此，每一阶段都必须由真实证据解锁；技术工作只服务于可信实验。未经阶段证据，不承诺 `v0.2 → v0.3 → v0.4` 的线性扩张。

## 2. Current Stage — Product Validation Before v0.2.0 Expansion

项目当前处于 **Product Validation Before v0.2.0 Expansion**，不直接进入完整 v0.2.0 工程开发。

当前需要先回答：

- 用户是否愿意在持有期间持续查看与 Thesis 相关的 Evidence；
- Monitoring 是否发现了用户本来可能遗漏的信息；
- 提醒是否值得，什么频率不会产生噪音；
- 用户是否愿意确认或纠正 AI 的 relevance / relationship 建议；
- Evidence 是否会触发真实 review，而不只是被阅读；
- review 是否改变 confidence、reasoning、ReviewCondition 或 Decision；
- 哪类 Evidence 最有价值；
- 用户是否愿意承担维护 Case 和 Thesis 的持续成本。

这意味着当前阶段的成果是关于问题与行为的证据，不是功能数量、数据抓取量或代码规模。

## 3. Core Validation Hypothesis

当前唯一核心假设是：

> **用户是否认为持有期间的 Evidence Monitoring 有持续价值？**

这是从 Product Vision 中选出的单一验证焦点，因为它决定 Investment Tracker 能否在交易之间持续产生价值。

实验需要一条最小 Thesis、一个真实 Case、可信 Evidence 和必要的用户确认，但这些只是验证该假设的脚手架。本阶段不同时宣称验证：

- 完整 Investment Thesis Lifecycle；
- AI 能自动形成高质量 Thesis；
- Freeze + Revision 本身构成用户购买理由；
- Decision Quality 模型已经可操作；
- 大规模数据接入已经可行。

## 4. Candidate Early Adopter

**Status:** `UNVALIDATED_USER_HYPOTHESIS`

当前候选 early adopter 是：

> 已有自主投资逻辑、以中长线或低频波段为主，但缺少稳定 Thesis tracking workflow 的个人投资者。

选择这一人群只表示其现有行为与候选问题更可能匹配，不表示痛点、采用、持续使用或付费意愿已经得到证明。

当前不优先面向：

- 主要希望 AI 直接给出买卖结论、不愿维护自身判断过程的用户；
- 已有成熟专业研究体系、迁移成本和数据要求很高的用户。

后者仍可作为高质量研究参与者，但不能用专家认可替代目标用户行为证据。

## 5. Stage 1 — User Discovery

### 5.1 Goal

用少量真实用户和真实历史投资案例，确认问题是否存在、当前替代流程是什么，以及 Monitoring 的潜在价值是否足以进入原型实验。

不以“你觉得这个功能好不好”作为主要问题。优先请用户回到一项真实投资，展示当时材料、后续行为、遗漏和复核过程。

### 5.2 Questions to Investigate

- 用户现在如何形成并记录投资理由；
- 买入后是否重新检查理由，通常在什么事件后检查；
- 当前使用哪些工具、信息源和提醒方式；
- 哪类信息最容易遗漏，遗漏造成了什么后果；
- 用户不复盘或中断跟踪的真实原因；
- 用户会不会主动定义 Review / Invalidation Conditions；
- 什么提醒会有帮助，什么提醒会令人厌烦；
- 在真实投资史中，Case 对用户而言是一只资产、一轮持仓、跨账户判断、主题还是其他对象；
- 清仓再买、加减仓和跨账户持有时，用户是否认为判断仍属于同一 Case；
- 用户是否在意 Original Reasoning 被冻结，以及何时认为需要 Revision；
- 用户是否愿意确认或纠正 Evidence relation；
- 用户是否理解并重视 Outcome 与 Decision Quality 的区别；
- 用户是否愿意持续使用并为该流程付费。

访谈中用户声称愿意付费只能作为探索性线索，不能视为付费意愿已经得到验证；后续仍需用真实试用、替代行为或实际付费实验验证。

### 5.3 Evidence to Capture

- 用户实际使用的笔记、表格、收藏、提醒或研究材料；
- 一项真实 Case 的时间线；
- 用户曾遗漏的信息及其后果；
- 一次真实观点变化及其原因；
- 用户当前流程中的维护成本和放弃点；
- 用户对提醒、AI 建议和人工确认的实际反应，而不只是抽象态度。

### 5.4 Gate to Stage 2

只有观察到以下组合，才进入 Controlled Prototype：

- 多个访谈或任务中出现真实的持有期跟踪缺口；
- 用户能指出 Monitoring 可能避免的具体遗漏或延迟复核；
- 至少部分目标用户愿意用一个真实 Case 参与持续实验；
- 最小 Thesis / Evidence 确认成本看起来可承受；
- 在候选 early adopter 的真实行为中，没有形成“主要只需要买卖结论或一次性笔记、不愿维护判断过程”的占主导模式。

若问题不明显、维护成本压倒价值，或 early adopter 假设不成立，则不开发完整原型；应回到 Product Vision，收窄用户、问题或价值假设。

## 6. Stage 2 — Controlled Prototype

### 6.1 Entry Condition

仅在 Stage 1 表明 Evidence Monitoring 问题具有实际意义后进入。

### 6.2 Allowed Scope

原型只允许包含：

- 每个受控实验实例只围绕一个用户的一个真实 `InvestmentCase`；同一窄原型可以在少量候选用户上重复使用，以获得跨用户的行为证据，但不得因此扩展功能范围；
- 一条真实 `Thesis`；
- 一个明确指标或一类 filing；
- 一个受控 Evidence 来源；
- 人工或半自动 Evidence capture；
- 可见的原始值 / 原文、source 和 captured time；
- 按来源能力保留必要的 observation / publication / filing / revision time；
- AI 提供关系建议，而不是最终分类；
- 用户确认：
  - relevant / not relevant；
  - supporting / contradicting / unclear；
  - 是否需要 review。

为了保持实验可信：

- Current Query 不能替代 Frozen Evidence；
- 原始 Evidence 与 AI interpretation、用户确认分离；
- 不可获得的来源、版本、时间或关系保持 unknown；
- AI 不提供最终投资判断或买卖执行；
- 用户能够回到原始来源复核建议。

### 6.3 What the Prototype Tests

原型只测试：用户在一段真实持有期中，是否反复认为 Evidence Monitoring 有用，并愿意完成必要的查看、确认和 review。

它不测试：

- 数据抓取规模；
- provider 数量；
- 全市场覆盖；
- 全自动 classification；
- 完整 Portfolio / Thesis Lifecycle；
- 最终 UI 或部署形态。

## 7. Behavioral Signals

当前不设置缺乏基线的精确 KPI。先观察 qualitative / behavioral signals，并保留样本量、观察周期和 Case 相关性。

### 7.1 Positive Signals

- 用户愿意在初次演示后继续回来查看；
- 用户指出系统发现了自己本来会遗漏的具体信息；
- 用户会确认、纠正或解释 AI 建议，而不是完全忽略；
- Evidence 触发了真实 Thesis review；
- review 改变了 confidence、reasoning、ReviewCondition 或后续 Decision；
- 用户能区分有用 Evidence 与噪音，并帮助收敛频率；
- 用户希望加入第二个真实 Case；
- 用户主动要求更多 Evidence 类型；
- 用户愿意持续使用，而不只是评价“概念很好”；
- 用户愿意讨论试用后的付费或替代现有工具的条件。

### 7.2 Negative Signals

- 用户只想获得买卖结论；
- Evidence 大量被忽略，且没有后续复核行为；
- 设置或维护 Thesis 的成本过高；
- 提醒频率或内容产生明显噪音；
- AI classification 没有帮助，纠正它反而增加负担；
- 用户仍只以价格涨跌评价所有 Evidence 和判断；
- 用户不愿持续维护 Case；
- 用户不关心遗漏，也没有可观察的持有期复核任务；
- 人工 / 半自动实验已经足够表明该流程没有持续价值。

正向信号不因单次礼貌性认可而成立；负向信号也不因单个错误提醒自动否定方向。判断应基于真实行为、重复出现和具体上下文。

## 8. Technical Spikes Allowed

技术 spike 只能解决会阻塞可信实验的窄问题，必须事先写明实验用途、停止条件和可丢弃边界。

允许的候选 spike：

- SEC filing 加一个明确指标的 PIT / snapshot 可行性；
- 一个最小 Evidence provenance model；
- 为一个受控来源建立薄 provider adapter；
- 审计一个真实 Brokerage CSV / statement 样本，以确认实验所需的最小事实。

每个 spike 必须满足：

- 直接服务 Stage 1 或 Stage 2；
- 只覆盖一个受控来源、市场或 Evidence 类型；
- 能显示原始内容、来源、时间和 warning / unknown；
- 不预设长期 provider、schema 或 deployment；
- 在获得答案后停止，不自动演化为生产平台。

不得扩张为：

- 完整数据平台；
- 完整 provider framework 或 OpenBB integration；
- 全 A 股覆盖工程；
- 通用 PIT / historical replay 平台。

## 9. Explicitly Deferred Work

当前验证阶段明确不先做：

- 完整 broker sync；
- 全面 Financial Reality 重构；
- 完整 Portfolio Engine；
- Web multi-user SaaS；
- 完整 / production-grade authentication、permissions、multi-user 用户系统；
- 完整 OpenBB integration；
- A 股完整数据层；
- 全市场新闻；
- OCR 自动化；
- Decision Profile；
- 月报 / 年报；
- 复杂 performance；
- tax / lot；
- corporate actions；
- 全自动 AI Evidence classification；
- 自动交易。

部分能力长期可能需要，但“以后可能需要”不是当前建设依据。它们只能在新的验证假设或已验证产品需求明确要求时重新进入范围。

即使这些生产级能力 deferred，如果受控实验处理真实用户数据、API credentials 或受许可约束的数据，仍必须实施与实验规模相称的最小安全、隐私、访问控制、数据保留与许可约束。

自动交易不仅 deferred，还是长期产品边界：Investment Tracker 不执行自动交易（D-016）。

## 10. Conditional Next Steps

Roadmap 采用条件路径：

```text
User Discovery
    ↓
Evidence Monitoring problem appears meaningful?
    ├─ No
    │   → revisit Product Vision, target user or problem framing
    │
    └─ Yes
        ↓
Controlled Prototype
        ↓
Users repeatedly find it valuable?
        ├─ No
        │   → simplify or change the hypothesis; do not scale infrastructure
        │
        └─ Yes
            ↓
Choose exactly one next hypothesis:
            - structured Thesis input
            - AI Socratic clarification
            - Freeze + Revision
            - narrow data automation
```

“Yes” 不是一次访谈赞同或一次成功提醒，而是重复行为证据。进入下一轮时只选择一个最需要降低的不确定性，不把四个候选同时变成功能计划。

可能的分支含义：

- **问题不存在：** 回看目标用户和 Product Vision，不用更多工程挽救假设；
- **问题存在但原型无价值：** 检查 Evidence 类型、频率、Thesis setup 或交互摩擦，并决定简化还是停止；
- **价值存在但数据不可持续：** 只验证一个更窄来源或人工服务边界，不直接建设完整数据平台；
- **价值重复出现：** 基于最主要的新阻塞，选择下一项产品假设并定义新的退出标准。

## 11. When Architecture Refactoring Becomes Justified

四轮研究得出了更清晰的候选领域模型，但这本身不授权重构 v0.1.0。只有真实验证需求被当前模型阻塞时，才允许为该能力设计最小增量迁移。

候选触发条件包括：

- 一个真实 Case 必须跨多笔 Activity；
- Evidence 必须拥有独立持久化和生命周期，才能完成受控实验；
- Account / Asset identity 阻塞真实数据导入或复核；
- Revision history 必须独立存在，才能避免覆盖 Original Reasoning；
- Current Query 无法满足可信实验，必须保存最小 ContextSnapshot；
- 已验证的计算需求要求某项 Derived State 可重建。

每次重构前必须回答：

1. 哪个已观察到的用户行为或实验要求它；
2. v0.1.0 当前具体阻塞什么；
3. 哪个最小边界足以解除阻塞；
4. 哪些候选关系仍不需要决定；
5. 如何保留现有数据、provenance、unknown 和 revision 语义。

> **Refactor in response to validated product needs, not architectural curiosity.**

## 12. Relationship to v0.1.0

v0.1.0 是已发布的 Financial Record MVP，验证了 `InvestmentRecord`、SQLite persistence、Decimal 金额语义、repository 和基础测试。

当前 Roadmap 对它的处理是：

- 保留为可运行、可测试的工程基线；
- 不把 monolithic `InvestmentRecord` 误认为最终领域模型；
- 不因候选模型更完整而推倒重来；
- User Discovery 可以完全不改 v0.1.0；
- Controlled Prototype 优先使用最小适配或独立实验数据；
- 只有第 11 节的实际阻塞出现时，才做局部、增量、可验证的迁移。

## 13. Exit Criteria for Current Validation Stage

当前验证阶段只有在下列路径之一成立时才结束：

### 13.1 Evidence Supports Continuing

- 真实用户问题被具体历史案例支持；
- 至少部分候选用户持续参与真实 Case 实验；
- Monitoring 多次发现有意义、原本可能遗漏的 Evidence；
- 用户实际确认、纠正并触发 review；
- 价值足以抵消 Thesis setup、确认和提醒摩擦；
- 最有价值的 Evidence 类型和可接受频率开始收敛；
- 下一项最大未知可以被明确表述为一个新假设。

满足这些条件后，才决定是否把实验里程碑称为 `v0.2.0`，并只为选中的下一假设扩大最小范围。

### 13.2 Evidence Supports Changing or Stopping

- 目标用户没有真实的持有期跟踪问题；
- 用户只需要买卖结论或一次性记录；
- Evidence 很少触发 review 或改变 reasoning；
- 持续维护和提醒摩擦稳定地超过价值；
- 缩窄 Evidence、频率和交互后仍没有重复使用行为。

此时应记录学习，回到 Product Vision 或改变假设，而不是用更多自动化、数据源和功能掩盖负面证据。

## 14. How to Interpret v0.2.0

`v0.2.0` 当前只是候选的第一个 **product validation release / experiment milestone**，名称本身可以调整。它不是一组完整产品功能，也不是开始全面工程扩张的承诺。

> **v0.2.0 当前只验证：用户是否认为持有期间的 Evidence Monitoring 有持续价值。**
