import sqlite3
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from main import DEFAULT_DATABASE_PATH
from src.records import InvestmentRecord
from src.storage import RecordNotFoundError, SQLiteInvestmentRecordRepository
from tests.test_models import make_record


class SQLiteInvestmentRecordRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        database_path = Path(self.temporary_directory.name) / "records.db"
        self.repository = SQLiteInvestmentRecordRepository(database_path)
        self.repository.initialize()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_default_database_path_is_anchored_to_project_directory(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        expected_path = project_root / "data" / "investment_tracker.db"

        self.assertTrue(DEFAULT_DATABASE_PATH.is_absolute())
        self.assertEqual(DEFAULT_DATABASE_PATH, expected_path)

    def test_initialize_creates_database_and_schema(self) -> None:
        self.assertTrue(self.repository.database_path.exists())

        connection = sqlite3.connect(self.repository.database_path)
        try:
            columns = connection.execute(
                "PRAGMA table_info(investment_records)"
            ).fetchall()
            version = connection.execute("PRAGMA user_version").fetchone()[0]
        finally:
            connection.close()

        column_names = [column[1] for column in columns]
        self.assertIn("amount", column_names)
        self.assertNotIn("profit", column_names)
        self.assertEqual(version, 1)

    def test_add_and_get_by_id(self) -> None:
        saved = self.repository.add(make_record())

        self.assertIsNotNone(saved.id)
        loaded = self.repository.get_by_id(saved.id)
        self.assertIsInstance(loaded, InvestmentRecord)
        self.assertEqual(loaded.symbol, "AAPL")
        self.assertEqual(loaded.amount, Decimal("31.50"))
        self.assertEqual(loaded.tags, ["价值", "观察仓"])

    def test_list_all_returns_every_record(self) -> None:
        self.repository.add(make_record(symbol="AAPL", trade_date="2026-08-08"))
        self.repository.add(make_record(symbol="MSFT", trade_date="2026-08-09"))

        records = self.repository.list_all()

        self.assertEqual(len(records), 2)
        self.assertEqual([record.symbol for record in records], ["MSFT", "AAPL"])

    def test_update_preserves_amount_and_saves_review(self) -> None:
        record = self.repository.add(make_record(amount="31.49"))
        record.price = Decimal("12")
        record.quantity = Decimal("4")
        record.review = "执行符合计划"
        record.lesson = "下次提前写清检查清单"

        updated = self.repository.update(record)

        self.assertEqual(updated.amount, Decimal("31.49"))
        self.assertEqual(updated.calculated_amount, Decimal("48"))
        self.assertEqual(updated.review, "执行符合计划")
        self.assertEqual(updated.lesson, "下次提前写清检查清单")
        self.assertGreaterEqual(updated.updated_at, updated.created_at)

    def test_get_missing_record_returns_none(self) -> None:
        self.assertIsNone(self.repository.get_by_id(999))

    def test_updating_missing_record_raises_clear_error(self) -> None:
        record = make_record()
        record.id = 999

        with self.assertRaises(RecordNotFoundError):
            self.repository.update(record)


if __name__ == "__main__":
    unittest.main()
