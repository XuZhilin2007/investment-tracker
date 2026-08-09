"""InvestmentRecord 数据模型及其基础校验规则。"""

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum


class TextEnum(str, Enum):
    """可以直接保存为文本的枚举基类。"""


class Action(TextEnum):
    BUY = "BUY"
    SELL = "SELL"


class Market(TextEnum):
    CN = "CN"
    HK = "HK"
    US = "US"
    OTHER = "OTHER"


class AssetType(TextEnum):
    STOCK = "STOCK"
    ETF = "ETF"
    FUND = "FUND"
    BOND = "BOND"
    REIT = "REIT"
    OPTION = "OPTION"
    CRYPTO = "CRYPTO"
    OTHER = "OTHER"


class StrategyType(TextEnum):
    VALUE = "VALUE"
    GROWTH = "GROWTH"
    INDEX = "INDEX"
    DIVIDEND = "DIVIDEND"
    TREND = "TREND"
    EVENT_DRIVEN = "EVENT_DRIVEN"
    OTHER = "OTHER"


def utc_now() -> datetime:
    """返回带时区的 UTC 时间，便于未来跨设备同步。"""

    return datetime.now(timezone.utc)


@dataclass
class InvestmentRecord:
    """一笔交易及其决策背景和复盘信息。

    金额由价格乘以数量得到，调用方不需要也不能单独传入 amount。
    price、quantity、fee 使用 Decimal，避免普通浮点数的精度误差。
    """

    trade_date: date
    symbol: str
    name: str
    market: Market
    asset_type: AssetType
    action: Action
    price: Decimal
    quantity: Decimal
    strategy_type: StrategyType
    holding_plan: str
    reason: str
    market_context: str
    thesis: str
    risks: str
    exit_conditions: str
    fee: Decimal = Decimal("0")
    tags: list[str] = field(default_factory=list)
    review: str = ""
    lesson: str = ""
    id: int | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime | None = None
    amount: Decimal = field(init=False)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """规范字段并检查业务规则；修改记录前也可以再次调用。"""

        self.trade_date = self._to_date(self.trade_date)
        self.market = self._to_enum(self.market, Market, "market")
        self.asset_type = self._to_enum(self.asset_type, AssetType, "asset_type")
        self.action = self._to_enum(self.action, Action, "action")
        self.strategy_type = self._to_enum(
            self.strategy_type, StrategyType, "strategy_type"
        )

        self.price = self._to_decimal(self.price, "price")
        self.quantity = self._to_decimal(self.quantity, "quantity")
        self.fee = self._to_decimal(self.fee, "fee")

        if self.price <= 0:
            raise ValueError("price 必须大于 0")
        if self.quantity <= 0:
            raise ValueError("quantity 必须大于 0")
        if self.fee < 0:
            raise ValueError("fee 不能小于 0")

        required_text = {
            "symbol": self.symbol,
            "name": self.name,
            "holding_plan": self.holding_plan,
            "reason": self.reason,
            "market_context": self.market_context,
            "thesis": self.thesis,
            "risks": self.risks,
            "exit_conditions": self.exit_conditions,
        }
        for field_name, value in required_text.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} 不能为空")
            setattr(self, field_name, value.strip())

        self.symbol = self.symbol.upper()
        self.tags = self._normalize_tags(self.tags)
        self.review = self.review.strip()
        self.lesson = self.lesson.strip()

        if self.id is not None and self.id <= 0:
            raise ValueError("id 必须为正整数")

        self.created_at = self._to_datetime(self.created_at, "created_at")
        if self.updated_at is None:
            self.updated_at = self.created_at
        else:
            self.updated_at = self._to_datetime(self.updated_at, "updated_at")

        # amount 永远由当前 price 和 quantity 重新计算。
        self.amount = self.price * self.quantity

    @staticmethod
    def _to_date(value: date | str) -> date:
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("trade_date 必须是 YYYY-MM-DD 格式") from exc

    @staticmethod
    def _to_datetime(value: datetime | str, field_name: str) -> datetime:
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} 不是有效时间") from exc

    @staticmethod
    def _to_decimal(value: Decimal | int | float | str, field_name: str) -> Decimal:
        try:
            return Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} 必须是有效数字") from exc

    @staticmethod
    def _to_enum(value, enum_type, field_name: str):
        try:
            return enum_type(value)
        except (TypeError, ValueError) as exc:
            allowed = ", ".join(item.value for item in enum_type)
            raise ValueError(f"{field_name} 可选值：{allowed}") from exc

    @staticmethod
    def _normalize_tags(tags: list[str]) -> list[str]:
        if not isinstance(tags, list):
            raise ValueError("tags 必须是字符串列表")

        normalized: list[str] = []
        for tag in tags:
            if not isinstance(tag, str):
                raise ValueError("tags 必须是字符串列表")
            clean_tag = tag.strip()
            if clean_tag and clean_tag not in normalized:
                normalized.append(clean_tag)
        return normalized
