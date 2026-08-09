"""第一阶段 MVP 入口：初始化本地 SQLite 数据库。"""

from pathlib import Path

from src.storage import SQLiteInvestmentRecordRepository


# 数据库路径以 main.py 所在的项目目录为基准，不受启动目录影响。
PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "data" / "investment_tracker.db"


def main() -> None:
    repository = SQLiteInvestmentRecordRepository(DEFAULT_DATABASE_PATH)
    repository.initialize()
    print(f"数据库已准备好：{DEFAULT_DATABASE_PATH.resolve()}")


if __name__ == "__main__":
    main()
