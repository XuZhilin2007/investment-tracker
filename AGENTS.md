# Repository Working Guide

本文件是 Codex 在 Investment Tracker 中工作的简短执行手册。项目背景见 [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md)，不要在此复制 Product Vision 或研究结论。

## Required Reading

进行非微小修改前依次阅读：

1. `docs/PROJECT_CONTEXT.md`
2. `docs/PRODUCT_VISION.md`
3. `docs/DECISIONS.md`

按任务补充阅读：

- Architecture / domain：`docs/ARCHITECTURE.md`
- Roadmap / scope / v0.2：`docs/ROADMAP.md`
- Research rationale：必要时读 `docs/research/RESEARCH_SYNTHESIS.md`

不要默认读取或重新研究所有单项目开源报告。

## Current Stage

当前阶段是 **Product Validation Before v0.2.0 Expansion**。

唯一核心未验证假设：用户是否认为持有期间的 Evidence Monitoring 有持续价值？

本节是当前阶段快照；如果 `docs/PROJECT_CONTEXT.md` 或 `docs/ROADMAP.md` 经明确决策更新了项目阶段，应在同一任务中同步更新本节，不得让 `AGENTS.md` 长期保留过期阶段。

- 不擅自扩大 v0.2.0；
- 不因存在候选 Architecture 就重构整个代码库；
- 不用更多竞品研究替代用户研究。

## Engineering Rules

- 修改前执行 `git status`，识别并保留无关用户修改。
- 做满足任务所需的最小范围变更；不要顺手改无关文件。
- 以 code 和 tests 判断当前实现，以正式 docs 判断当前产品方向；发现矛盾时记录并报告，不擅自统一。
- 运行与变更相关的 tests；当前完整测试命令为 `python -m unittest discover -s tests -v`。
- 如果测试结构或工具链以后经明确修改，应先根据 repository 实际状态验证新的测试命令，再同步更新本文件；不要把当前命令视为永久不变。
- 若 `python` 不在 `PATH`，使用当前已配置环境的 Python executable，不要把机器专属绝对路径写入项目。
- 完成前执行 `git diff --check`，并报告 tests、diff 和 Git status。
- 未经用户明确要求，不执行 commit、push、tag 或 release；不修改历史 release。
- database、本地用户数据、secrets、API keys、真实 brokerage statement 和 account information 不得提交或上传到公共 repository。
- 涉及真实用户或外部数据时，实施与任务范围相称的最小安全、隐私、访问、许可和数据保留约束。

## Domain Rules

以下边界不得违反；详细 rationale 见 `docs/DECISIONS.md`：

```text
Financial Fact ≠ Investor Reasoning
Account ≠ Asset
Activity / Transaction ≠ Position
Position ≠ InvestmentCase
Source Record ≠ Canonical Event ≠ Derived State
Current Market Data ≠ Frozen Evidence
Evidence Source ≠ AI Interpretation
AI ≠ Source of Truth
Fact Correction ≠ Reasoning Revision
Investment Outcome ≠ Decision Quality
Internal Asset Identity ≠ Provider Symbol
Unknown must remain unknown
Checkpoints ≠ Independent Decision Samples
No automated trading
```

## Do Not Assume

不得自行决定：

- InvestmentCase cardinality、是否跨 Account、Activity 与 Case 的关系；
- 清仓再买或 Case lifecycle；
- Portfolio 是否持久化、Cash 的最终表达；
- Evidence / Snapshot 或最终 schema；
- OpenBB 或其他 provider 已被选为 dependency；
- local-first / cloud / self-hosted；web / desktop / hybrid；
- SQLite 是长期数据库；
- A 股是首发市场；
- Evidence Monitoring、持续使用或付费意愿已被验证。

先查正式文档并标记 Open Question。若当前任务确实需要选择，向用户说明证据、tradeoff 和可撤销边界，不要默认为定案。

## AI and Financial Safety

- AI 是 Socratic / Evidence Assistant，不是 Investment Advisor。
- AI 输出不是 canonical financial fact；不得填补 unknown。
- Evidence 必须能回到 source；summary 或 interpretation 不能取代来源。
- AI 不自动宣布 Thesis 对错，不替用户作最终买卖决定，不执行自动交易。
- 用户保留最终 Judgment 与 Action。

## Refactoring Rule

> **Refactor in response to validated product needs, not architectural curiosity.**

仅因 `docs/ARCHITECTURE.md` 描述了更好的候选模型，不得主动重构 v0.1。先说明真实用户需求或可信实验被当前模型具体阻塞在哪里，再做解除阻塞所需的最小增量修改。

## Communication

- 默认用中文解释；code identifiers、file names、CLI commands 和 public README 可保留英文。
- 对初学者说明修改目的和关键风险，不只给命令。
- 完成后简洁报告：改了什么、为什么、测试结果、Git status，以及仍未决定的问题。
- 区分 repository facts、research-supported direction 和 unvalidated user hypothesis；不要用营销式确定语气描述候选方向。
