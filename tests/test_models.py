import unittest
from decimal import Decimal

from src.records import (
    Action,
    AssetType,
    InvestmentRecord,
    Market,
    StrategyType,
)


def make_record(**changes) -> InvestmentRecord:
    """创建测试记录，测试只覆盖关心的字段。"""

    values = {
        "trade_date": "2026-08-09",
        "symbol": "aapl",
        "name": "Apple",
        "market": Market.US,
        "asset_type": AssetType.STOCK,
        "action": Action.BUY,
        "price": "10.50",
        "quantity": "3",
        "fee": "0.25",
        "strategy_type": StrategyType.VALUE,
        "holding_plan": "计划持有一年",
        "reason": "估值进入关注区间",
        "market_context": "市场短期回调",
        "thesis": "现金流稳定",
        "risks": "需求下降",
        "exit_conditions": "基本面恶化",
        "tags": ["价值", " 观察仓 ", "价值"],
    }
    values.update(changes)
    return InvestmentRecord(**values)


class InvestmentRecordTests(unittest.TestCase):
    def test_amount_is_calculated_automatically(self) -> None:
        record = make_record()

        self.assertEqual(record.amount, Decimal("31.50"))
        self.assertEqual(record.symbol, "AAPL")
        self.assertEqual(record.tags, ["价值", "观察仓"])

    def test_string_enum_values_are_accepted(self) -> None:
        record = make_record(
            market="HK",
            asset_type="ETF",
            action="SELL",
            strategy_type="INDEX",
        )

        self.assertEqual(record.market, Market.HK)
        self.assertEqual(record.asset_type, AssetType.ETF)
        self.assertEqual(record.action, Action.SELL)
        self.assertEqual(record.strategy_type, StrategyType.INDEX)

    def test_invalid_action_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "action 可选值"):
            make_record(action="HOLD")

    def test_price_and_quantity_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ValueError, "price 必须大于 0"):
            make_record(price="0")

        with self.assertRaisesRegex(ValueError, "quantity 必须大于 0"):
            make_record(quantity="-1")


if __name__ == "__main__":
    unittest.main()
