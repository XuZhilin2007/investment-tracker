"""使用 Python 标准库 sqlite3 保存 InvestmentRecord。"""

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from src.records import InvestmentRecord
from src.records.models import utc_now


SCHEMA_VERSION = 1

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS investment_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    market TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('BUY', 'SELL')),
    price TEXT NOT NULL,
    quantity TEXT NOT NULL,
    amount TEXT NOT NULL,
    fee TEXT NOT NULL,
    strategy_type TEXT NOT NULL,
    holding_plan TEXT NOT NULL,
    reason TEXT NOT NULL,
    market_context TEXT NOT NULL,
    thesis TEXT NOT NULL,
    risks TEXT NOT NULL,
    exit_conditions TEXT NOT NULL,
    tags TEXT NOT NULL DEFAULT '[]',
    review TEXT NOT NULL DEFAULT '',
    lesson TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
"""

INSERT_SQL = """
INSERT INTO investment_records (
    trade_date, symbol, name, market, asset_type, action,
    price, quantity, amount, fee, strategy_type, holding_plan,
    reason, market_context, thesis, risks, exit_conditions,
    tags, review, lesson, created_at, updated_at
) VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
)
"""

UPDATE_SQL = """
UPDATE investment_records SET
    trade_date = ?, symbol = ?, name = ?, market = ?, asset_type = ?,
    action = ?, price = ?, quantity = ?, amount = ?, fee = ?,
    strategy_type = ?, holding_plan = ?, reason = ?, market_context = ?,
    thesis = ?, risks = ?, exit_conditions = ?, tags = ?, review = ?,
    lesson = ?, updated_at = ?
WHERE id = ?
"""


class RecordNotFoundError(LookupError):
    """修改一个不存在的记录时抛出。"""


class SQLiteInvestmentRecordRepository:
    """InvestmentRecord 的 SQLite 增、查、改操作。"""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)

    def initialize(self) -> None:
        """创建数据库目录、数据表和常用索引。"""

        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as connection:
            connection.execute(CREATE_TABLE_SQL)
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_records_trade_date "
                "ON investment_records(trade_date)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_records_symbol "
                "ON investment_records(symbol)"
            )
            connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")

    def add(self, record: InvestmentRecord) -> InvestmentRecord:
        """新增记录，并把数据库生成的 id 写回对象。"""

        if record.id is not None:
            raise ValueError("新增记录时 id 必须为空")

        record.validate()
        now = utc_now()
        record.created_at = now
        record.updated_at = now

        with self._connection() as connection:
            cursor = connection.execute(INSERT_SQL, self._insert_values(record))
            record.id = cursor.lastrowid
        return record

    def list_all(self) -> list[InvestmentRecord]:
        """查询全部记录，新交易日期排在前面。"""

        with self._connection() as connection:
            rows = connection.execute(
                "SELECT * FROM investment_records "
                "ORDER BY trade_date DESC, id DESC"
            ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def get_by_id(self, record_id: int) -> InvestmentRecord | None:
        """根据 id 查询；不存在时返回 None。"""

        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM investment_records WHERE id = ?", (record_id,)
            ).fetchone()
        return self._row_to_record(row) if row is not None else None

    def update(self, record: InvestmentRecord) -> InvestmentRecord:
        """保存修改后的记录，保留原 created_at 并刷新 updated_at。"""

        if record.id is None:
            raise ValueError("修改记录时必须提供 id")

        record.validate()
        record.updated_at = utc_now()

        values = self._update_values(record) + (record.id,)
        with self._connection() as connection:
            cursor = connection.execute(UPDATE_SQL, values)
            if cursor.rowcount == 0:
                raise RecordNotFoundError(f"找不到 id={record.id} 的投资记录")

        saved_record = self.get_by_id(record.id)
        if saved_record is None:  # 理论上不会发生，保留检查便于定位数据库问题。
            raise RecordNotFoundError(f"找不到 id={record.id} 的投资记录")
        return saved_record

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        """提供一个操作结束后一定会关闭的数据库连接。"""

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            # sqlite3.Connection 的上下文负责提交或回滚事务。
            with connection:
                yield connection
        finally:
            # with connection 本身不会关闭连接，因此必须显式关闭。
            connection.close()

    @staticmethod
    def _common_values(record: InvestmentRecord) -> tuple:
        return (
            record.trade_date.isoformat(),
            record.symbol,
            record.name,
            record.market.value,
            record.asset_type.value,
            record.action.value,
            str(record.price),
            str(record.quantity),
            str(record.amount),
            str(record.fee),
            record.strategy_type.value,
            record.holding_plan,
            record.reason,
            record.market_context,
            record.thesis,
            record.risks,
            record.exit_conditions,
            json.dumps(record.tags, ensure_ascii=False),
            record.review,
            record.lesson,
        )

    @classmethod
    def _insert_values(cls, record: InvestmentRecord) -> tuple:
        return cls._common_values(record) + (
            record.created_at.isoformat(),
            record.updated_at.isoformat(),
        )

    @classmethod
    def _update_values(cls, record: InvestmentRecord) -> tuple:
        return cls._common_values(record) + (record.updated_at.isoformat(),)

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> InvestmentRecord:
        return InvestmentRecord(
            id=row["id"],
            trade_date=row["trade_date"],
            symbol=row["symbol"],
            name=row["name"],
            market=row["market"],
            asset_type=row["asset_type"],
            action=row["action"],
            price=Decimal(row["price"]),
            quantity=Decimal(row["quantity"]),
            fee=Decimal(row["fee"]),
            strategy_type=row["strategy_type"],
            holding_plan=row["holding_plan"],
            reason=row["reason"],
            market_context=row["market_context"],
            thesis=row["thesis"],
            risks=row["risks"],
            exit_conditions=row["exit_conditions"],
            tags=json.loads(row["tags"]),
            review=row["review"],
            lesson=row["lesson"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
