# Investment Tracker Product Vision

> 文档性质：四轮开源研究后的当前正式 Product Vision
>
> 当前状态：研究支持的候选产品方向，尚未经过真实用户验证
>
> 研究依据：[`RESEARCH_SYNTHESIS.md`](research/RESEARCH_SYNTHESIS.md)
>
> 历史基线：[`PRODUCT_VISION_DRAFT.md`](PRODUCT_VISION_DRAFT.md)

本文回答 Investment Tracker 当前正在尝试解决什么问题，并约束后续产品讨论的边界。它不是营销文案、PRD、数据库设计、UI 方案或完整版本计划。

四轮开源研究已经使产品方向比研究前更聚焦，但没有证明目标用户会采用或付费。本文是当前正式 Vision，仍应随着真实用户研究和产品实验被修订。

## 1. Product Problem

很多个人投资者会做交易，却缺少结构化记录、验证和复核投资判断的方法。但“没有复盘习惯”本身不等于存在产品需求：用户可能并不重视复盘，也可能不愿承担额外记录成本。

研究后，当前真正要验证的问题被收窄为：

> 已经开始形成自主投资逻辑的个人投资者，是否需要一种低摩擦方式，把自己的 Investment Thesis 变成可持续跟踪、可验证、可修订、可回溯的判断过程？

这个问题尤其受到低频和中长期投资特点的约束：

- 一年内可能只有少量买卖，独立决策样本不足；
- 一个 Investment Case 可能持续数年，最终结果很晚才出现；
- 如果产品只在 BUY / SELL 时产生价值，使用频率和价值感知可能过低；
- 多个 Checkpoint 属于同一个决策过程，不能被当作多个独立样本；
- 因此，持有期间的 Thesis / Evidence Monitoring 是当前最值得验证的候选价值。

这仍是待验证的问题，不是已经成立的需求或 PMF。

## 2. Candidate Target User

当前候选 early adopter 是：

> 已经有一定自主投资逻辑、以中长线或低频波段为主、希望提高判断质量，但缺乏稳定的结构化跟踪和复核方法的个人投资者。

此定义标记为 `UNVALIDATED_USER_HYPOTHESIS`。开源研究只能说明这一人群与候选问题在逻辑上更匹配，不能证明其痛点强度、持续使用意愿、市场规模或付费意愿。

当前暂时不作为主要目标的两端用户是：

- 主要希望 AI 直接告诉自己买什么、卖什么，而不希望维护自身判断过程的用户；
- 已经形成成熟专业研究流程、对数据口径和 AI 可靠性要求极高的资深投资者。

这不是对任何用户群体的价值判断，只表示当前产品假设与其主要需求的匹配度不同。资深投资者仍可能是重要的研究参与者和高质量反馈来源。

## 3. Product Direction

当前内部候选定位是：

> **Investment Thesis Monitor + Decision Journal**

产品结果可以描述为：

> A system that helps self-directed investors turn investment ideas into trackable, falsifiable and reviewable investment theses.

中文表达为：帮助有自主投资逻辑的个人投资者，把投资想法转化为可持续跟踪、可验证、可修订、可回溯的 Investment Thesis。

这一定位有明确边界：

- 项目名称仍为 Investment Tracker；
- “Monitor” 不表示已经覆盖全市场数据、所有新闻或任意 Thesis；
- 系统不自动判定一项投资是否应继续持有；
- Evidence Monitoring 的用户价值尚未验证；
- 当前定位值得验证，不等于已经形成市场差异或 PMF。

## 4. Product Value Across the Investment Lifecycle

### 4.1 Before / At Decision

候选价值是帮助用户：

- 将模糊理由澄清为较明确的 Thesis；
- 识别支撑判断的 Assumptions；
- 预先定义 Review / Invalidation Conditions；
- 保存当时可知的 Context；
- 识别反例、替代解释和不确定性。

这些步骤是否会降低复盘成本，还是增加不可接受的录入摩擦，仍需验证。

### 4.2 During Holding

这是当前最值得验证的价值阶段。候选体验应帮助用户：

- 发现与原 Thesis 相关的新 Evidence；
- 将 Evidence 与 Thesis 的关系区分为 `SUPPORTING`、`CONTRADICTING`、`UNCLEAR` 或 `NOT_RELEVANT`；
- 检查用户预先设定的 Review Conditions 是否触发；
- 保存阶段性 Checkpoint；
- 允许用户通过 Revision 更新认知；
- 不静默改写 Original Thesis 或过去的判断。

这些关系状态仍可能包含解释，不是纯客观真相。AI 可以提出建议，最终相关性、判断和行动由用户确认。

### 4.3 After Outcome

候选价值是帮助用户：

- 对比 Original Thesis 与后续实际发展；
- 区分 Investment Outcome 与 Decision Quality；
- 形成 Final Review；
- 只在独立样本足够、覆盖周期合理且不确定性可表达时，逐步形成 Decision Profile。

Decision Profile 是远期方向，不是当前核心价值，也不能用同一 Investment Case 的多个 Checkpoint 人为扩大样本量。

## 5. AI's Product Role

> **AI is a Socratic and Evidence Assistant, not an Investment Advisor and not the source of truth.**

AI 可以：

- 澄清模糊 Thesis，并提出可验证的问题；
- 识别隐含 Assumptions、反例和替代解释；
- 检索候选 Evidence；
- 从可追溯来源中提取和整理事实；
- 比较多期数据及其口径；
- 建议 Evidence 与 Thesis 的关系；
- 指出缺失、冲突和 uncertainty；
- 生成 Checkpoint 草稿。

AI 不应：

- 自动决定某项资产值得买入或用户应该卖出；
- 宣布一项 Thesis 已经“正确”或“错误”；
- 把缺失、未知或冲突的数据补写成事实；
- 静默修改用户的 Original Investment Reasoning；
- 把 AI summary 当作原始 Evidence；
- 提供或执行自动交易。

原始来源是事实核验的基础；AI interpretation 与用户判断均可被复核和修订。最终 Judgment 与 Investment Action 属于用户。

## 6. Core Product Principles

### 6.1 Financial Reality 与 Investor Reasoning 分离

实际成交、账户、资产、持仓和价格回答“实际发生了什么”；用户的 Thesis、Assumptions、Decision 和 Revision 回答“用户当时为什么这样判断”。两者可以关联，但不应混成同一个可被一起覆盖的历史对象。

### 6.2 Evidence 与 Interpretation 分离

Evidence 的原始来源、版本、时间和内容不应因 AI 或用户后续解释变化而变化。AI 建议和用户确认应引用 Evidence，而不是取代 Evidence。

### 6.3 Freeze + Revision

Original Thesis 和当时实际被系统捕获并纳入判断的 ContextSnapshot 应被冻结。事实错误可以按可追溯方式更正；用户认知变化应通过 Revision 追加，不能覆盖过去的判断。

### 6.4 Outcome ≠ Decision Quality

赚钱不能自动证明判断正确，亏钱也不能自动证明判断错误。结果是复盘输入之一，不是对决策过程的自动判决。

### 6.5 Unknown Must Remain Unknown

当来源、时间、单位、版本、数据口径或 Evidence relationship 无法可靠确认时，系统应允许 `UNKNOWN` / `UNCLEAR`，而不是用猜测制造确定答案。

## 7. Candidate Three-Layer Understanding

当前用三层职责理解产品问题：

```text
Financial Reality
Investor Reasoning
Evidence & Review
```

- **Financial Reality** 回答：“实际发生了什么？”
- **Investor Reasoning** 回答：“用户当时为什么这样判断？”
- **Evidence & Review** 回答：“当时和后来分别出现了什么证据，这些证据如何影响复核？”

三层表示职责边界，不表示最终数据库表、服务拆分或对象关系已经确定。详细领域关系留给未来的架构讨论。

## 8. Differentiation Boundary

下列能力已经是成熟的行业能力或基础设施，不能再作为核心创新：

- trade import、broker parser、broker sync；
- notes、tags、screenshots 和通用 Trading Journal；
- performance dashboards；
- Account、Asset、Position、portfolio valuation 和 multi-currency；
- provider abstraction 和 AI 调用金融数据；
- 通用 AI 投资总结。

它们未来可能是必要的基础设施或体验能力，但建设规模不能证明产品价值。

当前真正值得继续验证的候选差异是：

1. Investment Thesis Lifecycle；
2. Thesis / Evidence Monitoring；
3. Point-in-Time Decision Accountability；
4. AI as Socratic / Evidence Assistant；
5. Outcome 与 Decision Quality 分离。

“值得验证”不等于“已有用户需求”，也不等于“已经形成市场差异”。

## 9. One Core Hypothesis for v0.2.0

如果下一版本只验证一个产品假设，应验证：

> **用户是否认为持有期间的 Evidence Monitoring 有持续价值？**

这是当前优先验证假设，因为它直接决定产品能否在交易之间持续产生价值。

如果假设不成立，围绕持续 Monitoring 构建的完整 Thesis Lifecycle、自动数据监控、大规模 PIT / Snapshot 基础设施和 AI classification 等建设都应重新评估。如果假设成立，才有理由继续验证：

- 用户是否愿意结构化 Thesis；
- AI 是否降低 Thesis 输入摩擦；
- Freeze + Revision 是否有可感知价值；
- Decision Quality 模型是否值得长期建设。

这里定义的是验证焦点，不是完整 v0.2.0 PRD、功能列表或交付承诺。

## 10. Current Validation Status

### 10.1 Research-Supported

四轮开源研究为以下方向提供了较强交叉证据：

- Financial Reality、Investor Reasoning、Evidence & Review 应保持职责分层；
- Account 与 Asset 是不同现实对象；
- Activity / Transaction 与 Position 是事件和状态的不同概念；
- Position 不等于 InvestmentCase；
- Source Record、Canonical Event 与 Derived State 应分离；
- MarketData / Current Query 不等于 Frozen Evidence；
- Evidence Source 不等于 AI Interpretation；
- AI 不应成为 Source of Truth；
- provenance、point-in-time time semantics、snapshot 和 revision 对可信复核很重要；
- Investment Outcome 不等于 Decision Quality。

“Research-Supported”只表示可以约束后续设计方向，不表示相应产品价值已经被用户验证。

### 10.2 User-Unvalidated

以下仍是用户或市场假设：

- early adopter 的当前定义；
- Evidence Monitoring 的持续用户价值；
- 用户结构化输入 Thesis 的意愿；
- 用户定义 Review / Invalidation Conditions 的意愿；
- 合适的 Monitoring 内容、频率和提醒阈值；
- 用户对 AI evidence classification 的接受与纠正意愿；
- 用户是否理解并重视 Freeze + Revision；
- 用户是否理解并重视 Decision Quality 与 Outcome 的区别；
- 中文 / A 股场景是否形成产品优势；
- local-first、cloud 或其他部署方式的偏好；
- 付费意愿。

这些事项在获得真实证据前，不得被后续文档或实现叙述为已验证结论。

## 11. Current Non-Goals

### 11.1 Long-Term Product Boundaries

- Investment Tracker 不执行自动交易；
- 不建设高频交易执行系统；
- 不以 AI 代替用户做最终买卖决策；
- 不提供收益保证或把预测包装成确定结论。

这些属于长期产品定位边界，不只是当前版本暂缓。

### 11.2 Current Validation-Stage Non-Goals

当前产品验证阶段暂不建设：

- 完整 broker sync；
- 完整 Portfolio Engine；
- 完整 Web multi-user SaaS；
- 完整 A 股数据平台；
- 全市场新闻聚合；
- 任意 Thesis 的全自动理解；
- 全自动 Evidence classification；
- Decision Profile；
- 完整 Portfolio / Tax / Lot / Corporate Action Engine。

这些属于当前验证阶段暂不建设的能力，不是永久拒绝；未来是否进入范围取决于真实用户证据和产品方向。

## 12. Vision Revision Boundary

本文相对于研究前的 `PRODUCT_VISION_DRAFT.md`，将重心从“更完整的交易记录与交易后复盘”收窄为“围绕 Investment Thesis 的持有期跟踪和可回溯复核”，并把目标用户、AI 角色与基础设施边界写得更明确。

下一次重大修订应优先来自真实用户行为和产品实验，而不是继续以更多竞品功能缺口替代用户证据。
