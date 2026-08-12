# Investment Tracker Decisions

> 文档性质：四轮开源研究后已接受的长期项目原则
>
> 研究依据：[`RESEARCH_SYNTHESIS.md`](research/RESEARCH_SYNTHESIS.md)
>
> 产品方向：[`PRODUCT_VISION.md`](PRODUCT_VISION.md)

本文只记录已有足够高置信度、可以约束后续设计和 Codex 行为的原则。它不是 research notes、数据库 schema、框架选型、PRD 或完整 v0.2.0 方案。

每条 Decision 的 `Not Decided Yet` 是边界的一部分：Accepted 表示原则已接受，不表示相关对象关系、实现方式或产品价值均已确定。未来如需改变已接受原则，应保留原因和替代记录，不应静默改写历史。

## D-001 — Separate Financial Facts from Investor Reasoning

- **Status:** Accepted
- **Decision:** 客观金融事实与用户投资判断必须拥有独立身份和生命周期。成交、账户、资产、价格和持仓不能与 Thesis、Assumptions、Decision 或 Revision 混成一个可被整体覆盖的历史对象。
- **Rationale:** TradeNote、Wealthfolio 与 Ghostfolio 都以不同方式说明财务事实可以独立于主观记录和组合分析存在；综合研究也显示，一项长期判断可能跨多笔交易、账户和持仓状态。将两者混写会让事实纠错同时改写历史理由，或让 reasoning revision 污染账本事实。
- **Implications:** 后续领域设计、导入、更新和删除流程必须尊重两类对象的边界；Financial Reality 的变化不得静默生成或重写 Investor Reasoning，Reasoning 也不得冒充成交或持仓事实。
- **Not Decided Yet:** 最终对象名称、数据库 schema、迁移策略、对象基数，以及 Financial Reality 与 InvestmentCase 的具体链接方式。

## D-002 — Account Is Not Asset

- **Status:** Accepted
- **Decision:** Account 与 Asset 是不同现实对象。Account 表达所有权、现金、来源和约束边界；Asset 表达可跨账户引用的金融标的身份。Broker 或 provider 也不能代替 Account identity。
- **Rationale:** Wealthfolio 与 Ghostfolio 都将账户和资产分离，并允许同一资产出现在多个账户。研究同时显示，券商只是账户的来源或平台信息，而不是账户本身。
- **Implications:** 后续设计不得只用 `broker + symbol` 同时承担账户和资产身份；同一 Asset 必须可以被多个 Account 的事实引用，账户相关限制和币种也不能被写入全局资产身份。
- **Not Decided Yet:** Account 与 InvestmentCase 的关系、首期账户字段、账户生命周期、跨账户聚合规则，以及是否需要命名 Portfolio。

## D-003 — Activity / Transaction Is Not Position

- **Status:** Accepted
- **Decision:** Activity / Transaction 表达发生过的金融事件；Position 表达某一时点、某一范围内的持仓状态。两者不得作为同一概念处理。
- **Rationale:** TradeNote 的 execution / logical trade 分层以及 Wealthfolio、Ghostfolio 的事实重放路径都说明，事件与状态具有不同语义。Position 会随事件、范围和时间变化，不能替代历史事件。
- **Implications:** 后续计算、导入和复盘必须能追溯 Position 所依据的事实或明确其 snapshot 来源；修正事件后，相关派生状态应被重新评估，而不是让两套数据各自成为真相。
- **Not Decided Yet:** 事件类型全集、成本基础方法、Position 的物化方式、Holdings snapshot 模式，以及现金用事件还是余额快照表达。

## D-004 — Position Is Not InvestmentCase

- **Status:** Accepted
- **Decision:** InvestmentCase 的 identity 和 lifecycle 不得由 Position identity 自动决定。Position 是财务状态；InvestmentCase 是用户判断过程的候选容器。
- **Rationale:** Position 可以因买卖、转仓、账户范围或重算而变化，甚至归零；一项判断却可能在建仓前形成、跨多次交易和账户延续，并在清仓后继续复盘。四轮研究均未发现可以从 Position lifecycle 推导 Case lifecycle 的依据。
- **Implications:** 后续设计不能把“有仓位”等同于“有 Case”，也不能把“仓位归零”自动等同于 Case 结束；财务计算不得负责创建、合并或关闭用户推理历史。
- **Not Decided Yet:** InvestmentCase 是否一对一或多资产、是否跨 Account、清仓再买是否新 Case、一笔 Activity 是否可关联多个 Case，以及 Case 是否可在交易前创建。

## D-005 — Separate Source Record, Canonical Event and Derived State

- **Status:** Accepted
- **Decision:** 任何未来导入或同步路径都必须在语义上区分 Source Record、Canonical Financial Event 和 Derived State。一条来源记录可以映射为零个、一个或多个 canonical events；派生状态不是来源记录的副本。
- **Rationale:** TradeNote、Wealthfolio 与 Ghostfolio 对导入、规范化和计算给出了正反例。特别是 Wealthfolio 的复合活动与 ImportRun 表明，原始业务记录和领域事件不必一一对应；缺少来源边界会使去重、更正、复核和重算不可解释。
- **Implications:** 后续 importer 必须保留可追溯来源、规范化结果和问题状态；AI 可以建议映射，但不应静默把低置信来源写成 canonical fact；derived state 必须说明其事实基础。
- **Not Decided Yet:** Source Record 的保存粒度、原始文件留存、去重算法、ImportRun 设计、broker adapter 接口，以及首期支持的导入来源。

## D-006 — Financial Derived State Should Be Rebuildable

- **Status:** Accepted
- **Decision:** 在拥有足够 canonical facts 的模式中，Position、Holding、Valuation、Allocation 和 Performance 等金融派生状态原则上应能从可信事实与明确参考数据重建，不应成为另一套独立真相。
- **Rationale:** Wealthfolio 与 Ghostfolio 都从事件、价格和汇率重建组合状态，且在事实变化后重算。可重建边界能避免历史纠错后出现账本与展示状态不一致。
- **Implications:** 缓存或物化结果必须可丢弃和重算，并能说明计算口径；直接导入的 Holdings Snapshot 若作为 source fact，必须明确标记其能力边界，不能声称支持不存在的交易级归因。
- **Not Decided Yet:** 首期需要哪些 derived state、计算引擎、缓存策略、重算范围、绩效公式，以及 Transactions / Holdings 两种模式是否同时支持。

## D-007 — Current Market Data Is Not Frozen Evidence

- **Status:** Accepted
- **Decision:** 当前或后来重新查询得到的 Market Data 不能替代某次判断当时实际使用的 Frozen Evidence / Context Snapshot。
- **Rationale:** OpenBB 研究表明历史数据可能因复权、restatement、revision、provider mapping、网页变化或权限变化而不同；通用缓存也不提供不可变历史 replay。仅保存查询条件无法证明用户当时看到了哪个版本。
- **Implications:** 任何参与历史决策问责的关键 Evidence 都必须保留足以追溯其当时状态的来源与时间信息；在来源提供版本信息或许可允许的情况下，应保留对应版本信息、snapshot 或 hash。无法获得的版本语义必须保持 unknown，不得推测补全。动态查询可用于当前视图，但不能静默改写旧 Context。
- **Not Decided Yet:** Snapshot 的内容与保留范围、许可策略、支持的 PIT 来源、存储格式、首期市场覆盖，以及是否使用 OpenBB。

## D-008 — Separate Evidence Source from Interpretation

- **Status:** Accepted
- **Decision:** Evidence 的原始来源、内容、版本和时间必须与 AI 或用户对它的解释分离。Interpretation 引用 Evidence，但不能覆盖或取代 Evidence。
- **Rationale:** OpenBB 显示标准化和 provider 转换可能改变可见字段；AI summary 也无法证明原文。将来源与解释混写会使后续无法判断内容变化来自现实、数据修订还是模型观点变化。
- **Implications:** supporting、contradicting、unclear 或 not relevant 等关系应被视为可复核解释；关键结论必须能够回到原始值、摘录、文档或来源标识；解释变化应保留自己的历史。
- **Not Decided Yet:** Evidence 的最终模型、原文保存策略、解释由 AI 建议还是用户先录入、确认工作流、关系粒度和 citation 展示方式。

## D-009 — AI Is Not the Source of Truth

- **Status:** Accepted
- **Decision:** AI 的正式角色是 Socratic and Evidence Assistant。它可以澄清、检索、提取、比较和提出解释建议，但不得创造金融事实、填补未知、宣布 Thesis 真伪或代替用户作最终投资判断。
- **Rationale:** 四轮研究都没有提供让 AI 成为可靠金融事实来源的依据；OpenBB 的工具调用和 citation 也不能保证模型解释正确。让 AI 越界会放大错误、诱导和投资建议风险。
- **Implications:** AI 输出必须与来源事实分离并可被复核；关键分类默认是 proposal；最终 Judgment 与 Investment Action 属于用户；系统不得把生成式摘要当作原始 Evidence。
- **Not Decided Yet:** 使用何种模型或 provider、具体 prompt、人工确认粒度、置信度表达、自动化程度，以及哪些任务完全不使用 AI。

## D-010 — Fact Correction Is Not Reasoning Revision

- **Status:** Accepted
- **Decision:** 金融事实纠错与用户认知变化是两种不同修改。事实可以按可追溯方式更正；Original Reasoning 应被冻结，后续变化通过 Revision 追加。
- **Rationale:** 财务来源可能存在导入、映射或录入错误，而用户也会因新 Evidence 改变观点。两者若共用原地覆盖语义，就无法区分“过去记录错了”与“用户后来改变了判断”，也无法防止 hindsight bias。
- **Implications:** 后续更新流程必须先识别修改性质；事实更正应触发相关 derived state 重评，reasoning revision 应保留旧版本、时间和原因；任何自动化都不得静默改写 Original Thesis。
- **Not Decided Yet:** 审计日志实现、更正审批、Revision 粒度、版本比较方式、撤销流程，以及现有 v0.1 数据的迁移策略。

## D-011 — Investment Outcome Is Not Decision Quality

- **Status:** Accepted
- **Decision:** Investment Outcome 与 Decision Quality 不得自动等价。盈利不自动证明判断过程正确，亏损也不自动证明判断过程错误。
- **Rationale:** TradeNote 已经用 Satisfaction 触及过程与 P&L 分离，综合研究进一步表明，只有结合 Original Thesis、当时 Context、Assumptions 和后续 Evidence，才可能讨论判断质量。市场结果还可能受 timing、position sizing、执行和运气影响。
- **Implications:** 后续复盘不得仅用收益给决策打对错标签；Outcome 可以约束复盘，但 Decision Quality 的任何评价都必须呈现依据、不确定性和样本边界。
- **Not Decided Yet:** Decision Quality 的维度、评分与否、用户是否重视该概念、结果归因方法，以及长期 Decision Profile 的具体形式。

## D-012 — Keep Time Semantics Distinct

- **Status:** Accepted
- **Decision:** 在 Evidence、PIT 和历史复核场景中，observation time、publication time、filing / accepted time、revision time 与 captured time 必须在语义上保持可区分；不得压成一个含义不明的 `date`。
- **Rationale:** OpenBB 研究显示 observation period 不代表信息当时已公开，后来重述或修订的历史值还可能引入 look-ahead bias。缺少时间语义会使 Context Reconstruction 看似精确但不可审计。
- **Implications:** 后续数据接入和 Evidence 设计必须声明时间字段的业务含义；未知的时间必须保持未知；任何 as-of 判断都需说明使用了哪种 cutoff 和版本。
- **Not Decided Yet:** 各 Evidence 类型必需的时间字段、时区策略、时间精度、provider 映射规则、PIT 覆盖范围，以及缺失时间的产品处理方式。

## D-013 — Internal Asset Identity Is Not a Provider Symbol

- **Status:** Accepted
- **Decision:** 内部 Asset identity 不得永久依赖任一数据 provider 的 symbol。内部身份、listing / market identity 和 provider identifier 必须能够分别演进。
- **Rationale:** Wealthfolio、Ghostfolio 与 OpenBB 都显示 symbol 格式依 provider 和市场而异，且会遇到跨市场同码、share class、dual listing、代码变化和 provider 切换。Provider symbol 适合作为映射，不适合作为长期唯一身份。
- **Implications:** 后续事实和 reasoning 链接应引用稳定的内部身份或明确的映射结果；切换数据源不得自动创建另一项现实资产；无法可靠映射时应进入待复核或 unknown，而不是猜测。
- **Not Decided Yet:** Asset / Listing 的最终模型、身份合并与拆分流程、外部标识集合、A/H/美股覆盖、代码沿革和首期 symbol mapping 策略。

## D-014 — Unknown Must Remain Unknown

- **Status:** Accepted
- **Decision:** 当 source、版本、单位、币种、时间、身份映射或 Evidence relationship 无法可靠确定时，系统必须允许 `UNKNOWN` / `UNCLEAR`，不得为追求完整叙事而猜测。
- **Rationale:** 四轮研究反复暴露来源残缺、provider 能力差异、历史修订、导入歧义和 AI 误解释风险。虚假的确定性会污染财务事实、PIT Context 和用户判断链，且往往难以事后发现。
- **Implications:** 数据模型、API、AI 输出和用户体验都必须容纳未知与冲突；缺失、不适用、无权限、解析失败和来源冲突不应被压成同一种“空”；自动化应在证据不足时停止或请求复核。
- **Not Decided Yet:** 具体状态枚举、质量分级、人工复核流程、哪些不确定项阻止后续计算，以及不同场景的容错阈值。

## D-015 — Checkpoints Are Not Independent Decision Samples

- **Status:** Accepted
- **Decision:** 同一个 InvestmentCase 内的多个 Checkpoint 是同一决策过程的多次观察，不能被计作多个独立决策样本。
- **Rationale:** 中长期投资的独立 Case 数量本来就少。若用 Checkpoint 数量扩大样本，Decision Profile 会产生伪精确和虚假置信度；TradeNote 的高频交易统计不能直接外推到长期 Thesis。
- **Implications:** 未来任何行为模式、成功率或 Decision Profile 都必须以独立 Case、样本量、覆盖周期和 evidence strength 为边界；数据不足时应明确表示 insufficient data。
- **Not Decided Yet:** 什么构成独立 InvestmentCase、最低样本量、pattern maturity、统计方法、市场周期要求，以及 Decision Profile 是否最终值得建设。

## D-016 — No Automated Trading

- **Status:** Accepted
- **Decision:** Investment Tracker 的当前和长期产品定位均不执行自动交易。AI 不连接执行链代替用户提交买卖操作，也不把建议包装成自动行动。
- **Rationale:** 产品目标是改善用户的判断过程和证据复核，而不是承担投资执行权。自动交易会改变产品类别、风险、信任边界与合规要求，并与用户拥有最终 Judgment / Action 的原则冲突。
- **Implications:** 后续 broker 或账户能力如存在，只能服务于事实导入、只读同步或用户主动完成的工作流；任何 AI 建议与投资执行之间必须保持明确的人类决策边界。
- **Not Decided Yet:** 是否支持只读 broker sync、用户主动导出指令、提醒或手工记录；这些能力不得被解释为自动交易授权。

## Open Questions Not Accepted as Decisions

以下事项仍未决定，不得由本文中的 Accepted 原则外推出答案：

- InvestmentCase 是单资产、多资产、主题还是其他心智模型；
- InvestmentCase 是否跨 Account，以及一笔 Activity 是否可关联多个 Case；
- 清仓再买默认创建新 Case、恢复旧 Case，还是由用户选择；
- Portfolio 是否需要持久化实体；
- Cash 使用 event ledger、balance snapshot 或两种受限模式；
- local-first、cloud、self-hosted 或混合部署；
- SQLite 是否长期保留；
- 是否使用 OpenBB 或任何特定金融数据 provider；
- 最终数据库 schema、服务边界和迁移方案；
- Web、desktop 或 hybrid 产品形态；
- v0.2.0 的最终 UI 和完整范围；
- 是否以 A 股作为首发市场；
- Evidence Monitoring 是否已经有用户需求、合适频率为何、用户是否愿意付费。

这些问题应由未来用户研究、受控产品实验或架构文档明确处理；在此之前必须保持可撤销。
