# TradeNote 研究后产品思考记录

> - 文档性质：TradeNote 研究后的阶段性 review notes
> - 文档目的：记录研究暴露出的新问题，以及这些问题对后续产品设计方向的影响
> - 当前状态：讨论稿；不是最终 Product Vision、PRD、领域模型或 v0.2.0 方案
> - 形成依据：[`PRODUCT_VISION_DRAFT.md`](../PRODUCT_VISION_DRAFT.md) 与 [`TRADENOTE_RESEARCH.md`](TRADENOTE_RESEARCH.md)

## 0. 阅读说明

本文使用三种性质标记，避免把研究后的候选方向误写成既定结论：

- **已发现的问题：** 已通过 TradeNote 对比或当前产品推演暴露出的逻辑缺口；它说明原设想需要进一步检验，不代表已经找到解决方案。
- **暂定设计方向：** 针对已发现问题形成的候选产品或领域模型方向；目前只用于指导后续研究，不授权直接重构代码。
- **尚未验证的假设：** 仍需通过用户访谈、原型测试、数据可得性研究或其他竞品研究回答的问题。

本文不修改研究前的 Product Vision Draft。原文仍作为研究前基线；本文件记录研究之后发生的认识变化。

## 1. 研究后暴露出的核心问题

### 1.1 “普通散户”可能不是足够准确的目标用户

**性质：已发现的问题；目标用户修订属于尚未验证的假设。**

Product Vision Draft 将初期用户概括为有一定自主判断、但缺乏系统复盘习惯的普通散户。TradeNote 研究之后，需要进一步区分“没有复盘习惯”背后的不同原因。

部分完全凭感觉操作的散户可能：

- 没有意识到投资复盘的重要性；
- 不把“提高决策质量”视为主动需求；
- 更期待工具直接给出买卖答案；
- 即使系统发现频繁交易、追涨杀跌等问题，也未必愿意改变行为；
- 最终亏损时，可能用“AI 没有帮助赚钱”评价产品，而不是评价复盘质量。

因此，以下推导并不成立：

```text
没有复盘习惯
≠
存在购买投资复盘工具的需求
```

**暂定设计方向：** 更值得验证的初期用户描述是：

> 已经开始形成自主投资逻辑、希望提高决策能力，但缺乏结构化记录、验证和复盘方法的个人投资者。

这一描述比“普通散户”更窄，也更强调用户已经存在的改进动机。但它目前只是候选用户定义，仍需通过用户研究验证其规模、痛点强度、使用意愿和付费意愿。

### 1.2 长线投资者的独立决策样本可能严重不足

**性质：已发现的问题。**

Product Vision Draft 中的长期 Decision Profile 隐含了一个前提：用户会持续积累足够多的已完成交易。但长线或低频波段投资者可能：

- 一年只有少量买入和卖出；
- 一个完整 Investment Case 持续数年；
- 很晚才产生可以被称为“最终结果”的样本；
- 在样本积累完成前无法得到有意义的 Decision Profile；
- 即使积累数年，独立 Investment Cases 数量仍可能不足以支持可靠结论。

TradeNote 通过高频 execution、trade 和多维绩效统计较快地产生分析价值；这一模式不能直接外推到长期投资者。

**结论边界：** 不能把“完成的交易数量”作为产品产生价值的唯一数据来源，也不能假设长期用户会自然积累足够多的独立样本。

### 1.3 产品不能只在买卖发生时产生价值

**性质：已发现的问题。**

如果产品流程被简化为：

```text
BUY → 长期等待 → SELL → Review
```

那么长线用户的使用频率和价值感知都会过低。实际持有期间仍会持续出现：

- 财报与公司公告；
- 行业和竞争格局变化；
- 政策与宏观环境变化；
- 估值变化；
- 用户自身观点变化；
- 对原假设有支持、冲突或暂时无法解释的新证据。

**暂定设计方向：** 产品价值可以从“交易完成以后复盘”，扩展到“在持有期间持续跟踪原投资逻辑是否得到新支持或出现冲突证据”。这引出了 `Thesis Checkpoint` 与 `Thesis Monitoring` 的候选方向。

## 2. 核心对象可能从 Transaction 转向 Investment Case / Thesis

**性质：暂定设计方向；尚未验证。**

Product Vision Draft 以 `Transaction` 作为决策闭环入口。这适合接收客观成交事实，也与 TradeNote 的 execution/trade 模型容易衔接。但对于长期投资，单笔 Transaction 可能不是最自然的复盘单位：同一个投资逻辑可能对应多次建仓、加仓、减仓和退出。

候选核心对象是 `InvestmentCase`。它用于表达一个持续存在的投资判断，而不是一笔孤立成交。一个 Investment Case 可能包含：

- Original Investment Thesis；
- 一个或多个 Transactions；
- Thesis assumptions；
- Invalidation / Review Conditions；
- Context snapshots；
- Thesis checkpoints；
- 用户后续 Revisions；
- Final Outcome Review。

候选关系如下：

```text
InvestmentCase
├── Original Thesis
├── Transactions
│   ├── BUY #1
│   ├── BUY #2
│   └── SELL #1
├── Thesis Assumptions
├── Invalidation / Review Conditions
├── Context Snapshots
├── Thesis Checkpoints
├── Revisions
└── Final Review
```

这一方向不否定 Transaction 的重要性。Transaction 仍是不可随意修改的客观事实；变化在于它可能成为 Investment Case 的组成部分，而不是承载全部主观判断的唯一中心。

### 2.1 与 TradeNote 数据模型研究的关系

TradeNote 已经证明 `Execution → Logical Trade → Aggregate` 的分层有通用价值，也证明客观交易事实应与 notes、tags、satisfaction 等主观补充分开。但其核心仍围绕交易日和 logical trade 组织，适合交易绩效分析，不足以直接表达一个持续数年的 thesis 生命周期。

**暂定影响：** 后续研究需要同时回答两个关系：

1. Broker transaction 如何稳定映射到真实账户、资产、持仓和组合；
2. Transaction 或 Position 如何关联到用户主动建立的 Investment Case。

当前不应据此重构 v0.1.0 的 `InvestmentRecord` 或数据库。是否需要 `InvestmentCase`、它与 asset/position 的基数关系、一个 transaction 是否可能关联多个 case，都仍未确定。

## 3. AI 的职责需要进一步收缩

**性质：已发现的问题与暂定设计原则。**

Product Vision Draft 将 AI 定义为 Investment Thinking Assistant，而不是 Investment Advisor，这一边界仍然成立。但原设想中的 “AI Counter-Thesis” 和 “AI 判断原投资逻辑是否得到验证” 仍可能让 AI 承担过强的事实判断责任。

AI 不是市场事实来源，也不能保证准确理解每一条新闻、财报、行业变化和公司基本面。如果系统直接告诉用户“投资逻辑已经反转”，可能造成：

- AI 错误判断；
- 用户被误导；
- 专业用户不信任系统；
- 产品从 thinking assistant 滑向 investment advisor；
- 用户把系统输出误解为买卖建议。

### 3.1 暂定原则

> AI should not be the source of truth.
>
> AI should be the evidence interpreter.

AI 不应决定：

- 股票是否值得买；
- 用户是否应该卖；
- 公司基本面是否已经确定反转；
- 一条投资逻辑是否已经被最终判定为正确或错误。

AI 更适合协助：

- 从用户陈述中提取可验证假设；
- 查找、整理并引用相关证据；
- 把新事实与原假设建立候选关系；
- 提醒出现支持、冲突、不确定或无关证据；
- 指出需要用户重新思考的地方；
- 记录证据来源、时间边界和解释过程。

最终是否调整 thesis、是否认为原判断失效、是否采取交易行动，应由用户完成。

### 3.2 仍需验证的边界

“Evidence Interpreter” 仍然会解释信息，而解释本身可能出错。因此，收缩 AI 职责并不能自动解决准确性问题。后续仍需研究：原始来源如何展示、AI 推理如何追溯、用户如何确认、不同来源冲突时如何处理，以及系统应在何种置信度下保持沉默。

## 4. 从“判断正确/错误”转向“证据状态”

**性质：暂定设计方向。**

系统语言应尽量避免直接使用：

- 逻辑正确；
- 逻辑错误；
- 投资逻辑反转；
- 应该买入；
- 应该卖出。

候选表达方式是记录“新信息与某条 thesis 的关系”，而不是替用户给投资判断下最终结论：

| Evidence Status | 暂定含义 |
| --- | --- |
| `SUPPORTING` | 新证据与原假设方向一致，可能增加其可信度 |
| `CONTRADICTING` | 新证据与原假设存在实质冲突，需要重新检查 |
| `UNCLEAR` | 当前信息不足、含义不确定或存在相互矛盾的解释 |
| `NOT_RELEVANT` | 与该条 thesis 没有足够直接的关系 |

例如：

```text
原假设：公司未来毛利率会持续改善。
新事实：毛利率连续三个季度下降。

候选系统表达：
检测到与原假设冲突的新证据。
```

系统不应直接推导为：

```text
你的投资逻辑错误，因此应该卖出。
```

**边界：** `SUPPORTING` 或 `CONTRADICTING` 仍是对证据关系的解释，不是完全客观的标签。状态由 AI 建议、规则触发还是用户确认，目前尚未确定。

## 5. 让用户提前定义 Invalidation / Review Conditions

**性质：暂定设计方向；用户接受度尚未验证。**

用户形成 Investment Thesis 时，除记录“为什么买”，还可以提前记录：

> 出现什么事实时，我需要重新评估这个判断？

例如：

```text
Thesis:
未来两年公司收入维持较高增长。

Invalidation / Review Condition:
如果连续两个季度收入增速低于 10%，重新评估该 thesis。
```

如果未来满足条件，系统可以客观提示：

```text
你当初设定的重新评估条件已经触发。
```

而不是让 AI 自行宣布：

```text
该投资逻辑已经失效。
```

这种设计可能带来三项价值：

1. 把模糊预期转化为可观察条件；
2. 减少事后移动标准或重新包装理由；
3. 降低 AI 越权给出投资结论的风险。

但它也可能显著增加录入摩擦，并诱导用户设置过于简单、机械或错误的阈值。是否要求定量条件、如何表达非量化条件、条件触发后是否仍需人工确认，都属于开放问题。

## 6. 重新理解 AI Counter-Thesis

**性质：原概念的暂定修订方向。**

AI Counter-Thesis 如果只是生成几个反对投资的理由，容易退化成泛泛风险提示，既缺乏可操作性，也可能让用户快速忽略。

更值得验证的方向是把 AI 设计为类似 Socratic Assistant 的澄清者：它不急于反驳，而是帮助用户把模糊判断转换成可追踪、可验证、可证伪的 thesis。

例如用户说：

> 我觉得新能源未来很好。

AI 可以继续帮助澄清：

- “未来很好”具体对应什么可观察变化？
- 收入增长达到多少才符合预期？
- 市场份额预计如何变化？
- 毛利率底线是什么？
- 哪些事实出现时需要重新考虑？
- 预期验证时间大约多久？

候选价值转化是：

```text
感觉和故事
→
可追踪、可验证、可证伪的假设
```

Counter-Thesis 仍可以保留，但它可能更适合作为 thesis clarification 的一部分：检查反例、隐含前提、失败条件和替代解释，而不是单独生成一段反对意见。

**尚未验证：** 用户是否愿意回答这些追问；AI 能否提出足够具体且不诱导的澄清问题；这一过程是否比直接写一段自由文本更有价值。

## 7. 持仓期间的产品价值：Thesis Monitoring

**性质：暂定设计方向；不是已确定功能。**

候选方向是在一个长期 Investment Case 中持续建立 `Thesis Checkpoint`。每个 checkpoint 记录某个时点出现的新事实、它与原 thesis 的候选关系，以及用户当时如何处理该信息。

例如，原始理由包含：

1. 海外收入高速增长；
2. 毛利率改善；
3. 当前估值合理。

持有期间出现新财报或数据后，系统可以展示：

```text
Thesis 1
新证据：SUPPORTING

Thesis 2
新证据：CONTRADICTING

Thesis 3
当前状态：发生明显变化，关系仍待确认
```

系统不直接给出买卖建议。用户可以：

- 保持原观点；
- 修改观点；
- 增加新的 thesis；
- 标记需要重新评估；
- 将某条证据标记为无关或不确定。

每次变化应保留时间、证据来源、用户确认状态和历史版本，不能静默覆盖原始判断。

### 7.1 它试图解决的问题

Thesis Monitoring 试图让产品在买入和卖出之间持续产生价值，并使 Final Review 不必依赖用户几年后回忆当时发生过什么。

### 7.2 它没有自动解决的问题

- 信息抓取可能产生噪声；
- 一条信息可能同时支持一项假设、冲突另一项假设；
- 财报指标变化不一定具有因果含义；
- checkpoint 过密会造成信息轰炸；
- 用户可能只确认支持自己观点的证据；
- AI 的证据关联和解释可能出错。

因此 Thesis Monitoring 目前只能作为候选产品方向，而不能被写成已经验证的优势。

## 8. Decision Profile 的样本量与独立性问题

**性质：已发现的问题；统计表达方式属于暂定方向。**

长期行为画像不能在样本不足时生成强结论。例如，5 个独立 Investment Cases 通常不足以可靠得出“用户容易追涨”这样的结论。

候选 Decision Profile 应显式考虑：

- sample size；
- evidence strength；
- confidence；
- pattern maturity；
- 独立 Investment Cases 数量；
- 覆盖的市场周期与持有周期。

候选状态可以包括：

| Pattern State | 暂定含义 |
| --- | --- |
| `INSUFFICIENT_DATA` | 独立样本不足，不生成方向性结论 |
| `PRELIMINARY_PATTERN` | 出现初步迹象，但证据较弱或覆盖范围有限 |
| `REPEATED_PATTERN` | 在多个相对独立的 Investment Cases 中重复出现 |

### 8.1 Checkpoint 不能扩大独立样本量

同一个 Investment Case 的十次 checkpoints 是一个决策过程中的十次观察，不是十次独立投资决策。Checkpoints 可以帮助研究 thesis 如何演化、用户如何处理新证据，但不能被简单计为十个成功或失败样本。

**尚未验证：** 什么算一个独立 Investment Case；同一资产的多轮投资如何处理；最低样本量是否能统一设定；如何向用户解释不确定性而不过度复杂化产品。

## 9. 产品价值可能分布在三个时间尺度

**性质：暂定价值框架。**

原来的价值路径较偏：

```text
积累很多交易 → AI 复盘 → Decision Profile
```

研究后形成的候选框架把价值分布到投资决策的三个阶段。

### 9.1 交易发生时

帮助用户把模糊投资理由转换成：

- 清晰 thesis；
- 可验证 assumptions；
- invalidation / review conditions；
- risk 与 counter evidence；
- 预期验证时间。

### 9.2 持有期间

帮助用户：

- 跟踪与 thesis 相关的新事实；
- 提醒可能的 supporting / contradicting / unclear evidence；
- 触发用户预先定义的 review conditions；
- 保存用户确认、忽略或重新解释证据的过程；
- 保存 thesis revision，而不覆盖历史版本。

### 9.3 投资结束以后

帮助用户：

- 对比 Original Thesis 与实际发展；
- 分离 Investment Outcome 与 Decision Quality；
- 形成 Final Case Review；
- 在独立样本足够时逐渐建立 Decision Profile。

**候选价值：** 即使用户一年只完成少量交易，产品仍可能通过 thesis clarification 和持有期间 checkpoints 产生持续价值。

**尚未验证：** 三个阶段中哪个痛点最强、哪个最适合作为最小验证入口，以及用户是否会认为持续 monitoring 的价值高于其操作和信息成本。

## 10. 当前新的候选产品方向

**性质：尚未验证的定位假设。**

Product Vision Draft 中的候选方向是：

> AI Investment Decision Journal

TradeNote 研究后的产品思考可能进一步演化为：

> Investment Thesis Monitor + Decision Journal

更抽象的英文描述可以暂时写为：

> A system that turns investment decisions into trackable, falsifiable and reviewable investment theses.

暂定中文表达：

> 将投资行为转化为可持续跟踪、可证伪、可回溯的投资逻辑。

这一变化意味着产品重心可能从“保存和分析交易”转向“管理 investment thesis 的生命周期”，但它目前只是研究后的候选假设：

- 不是最终产品定位；
- 不是已被证实的创新；
- 不是项目改名决定；
- 不是 v0.2.0 范围；
- 不应立即驱动代码或数据库重构。

## 11. 目前仍未解决的开放问题

**性质：尚未验证的假设与研究问题。**

### 11.1 用户行为与产品摩擦

1. 用户是否真的愿意在投资时定义 thesis 和 invalidation conditions？
2. 这套流程是否增加了过多操作摩擦？
3. 长期投资者是否愿意在持有期间持续回来使用？
4. 多久一次 checkpoint 才不会造成信息轰炸？

### 11.2 AI 与证据可靠性

5. AI 是否真的能把模糊理由转换成高质量、可验证的假设？
6. Point-in-time context 是否能可靠获取？
7. 如何判断一条新信息真正与某个 thesis 相关？
8. 如何防止 AI 错误解释财报和新闻？
9. Supporting / contradicting evidence 应由谁最终确认？

### 11.3 长期画像与商业可行性

10. Decision Profile 最低需要多少独立 Investment Cases？
11. 免费功能和付费功能应该如何区分？
12. 中文 / A 股场景是否真的能形成产品优势？

这些问题在得到证据之前，不应被产品文案或内部规划写成确定答案。

## 12. 对后续竞品研究的影响

**性质：已调整的研究方向。**

下一步仍计划研究：

- Wealthfolio；
- Ghostfolio；
- OpenBB。

研究范围不应再局限于 Trading Journal 功能，而应同时检查 portfolio domain 如何承载长期 Investment Case。

### 12.1 Wealthfolio 的重点问题

应重点研究以下对象及其关系：

- Account；
- Asset；
- Activity；
- Position；
- Portfolio；
- 多币种；
- long-lived holding。

需要回答：

1. Activity/Transaction 如何改变 Position；
2. Position 如何归属于 Account 和 Portfolio；
3. Asset identity、币种、价格和 corporate actions 如何处理；
4. 长期持仓如何跨多次买卖持续存在；
5. 未来候选 `InvestmentCase / Thesis` 应关联 Asset、Position、Transaction 还是它们的组合；
6. 一个 Investment Case 是否可以跨账户、跨多次持仓或跨多个相关资产。

目的不是复制 Wealthfolio，也不是现在确定 InvestmentCase 模型，而是为“thesis 如何与真实资产、交易和持仓建立稳定关系”补充领域证据。

### 12.2 Ghostfolio 与 OpenBB 的研究视角

- 研究 Ghostfolio 时，需要关注 portfolio、holdings、performance、asset allocation 与 long-term tracking 的边界，判断哪些属于成熟的 Portfolio Tracking 基础设施。
- 研究 OpenBB 时，需要关注市场数据、基本面、新闻、provider abstraction、point-in-time 数据能力与来源可追溯性，判断 Context Reconstruction 和 Thesis Monitoring 的数据前提是否现实。

这两项也只是研究问题的调整，不代表已经为本项目选择技术栈或功能范围。

## 13. 本轮认识变化摘要

| 研究前倾向 | 研究后暴露的问题 | 当前候选方向 | 状态 |
| --- | --- | --- | --- |
| 面向“普通散户” | 无复盘习惯不等于主动需求 | 验证已有自主逻辑且有改进动机的个人投资者 | 尚未验证 |
| 以 Transaction 为主要入口 | 长期 thesis 跨越多次交易和多年持有 | 探索 InvestmentCase 作为主观决策容器 | 暂定方向 |
| 交易后复盘 | 低频用户在持有期间缺乏持续价值 | 探索 Thesis Checkpoints / Monitoring | 暂定方向 |
| AI 判断逻辑是否成立 | AI 不是事实来源，可能越权或误导 | AI 作为 evidence interpreter，最终判断归用户 | 暂定原则 |
| 正确/错误评价 | 容易混淆证据、判断和买卖建议 | 使用 supporting / contradicting / unclear / not relevant | 暂定方向 |
| 事后判断失效条件 | 容易移动标准和产生后见偏差 | 用户提前定义 Invalidation / Review Conditions | 尚未验证 |
| Counter-Thesis 生成反对理由 | 容易退化为泛泛风险提示 | 以 Socratic clarification 形成可证伪 thesis | 尚未验证 |
| 多笔交易后建立 Decision Profile | 长期用户样本少，checkpoint 也不独立 | 显示样本量、证据强度与 pattern maturity | 暂定方向 |
| 降低复盘成本即构成差异 | TradeNote 已实现大量通用降本能力 | 验证 thesis lifecycle 是否提供额外价值 | 尚未验证 |

当前最重要的变化不是增加了一组新功能，而是研究问题发生了转移：

```text
从“怎样做一个更完整的交易日志”
转向
“用户是否需要、并愿意使用一个可持续跟踪和验证投资逻辑的系统”
```

在这一问题得到验证前，候选定位、领域模型和 AI 工作流都应保持可撤销。
