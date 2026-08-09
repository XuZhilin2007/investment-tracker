"""本地存储实现。"""

from .sqlite_repository import (
    RecordNotFoundError,
    SQLiteInvestmentRecordRepository,
)

__all__ = ["RecordNotFoundError", "SQLiteInvestmentRecordRepository"]
