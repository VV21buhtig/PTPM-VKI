import sqlite3
import unittest
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseRepository(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_success(self):
        result = self.db.add(1, "ponchik", "<p>Привет, форум!</p>")
        self.assertTrue(result)
        record = self.db.get_by_id(1)
        self.assertEqual(record["name"], "ponchik")

    def test_add_duplicate_id_raises_error(self):
        self.db.add(1, "ponchik", "Первое сообщение")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.add(1, "other_user", "Дубликат ID")

    def test_add_validation_length_error(self):
        too_long_name = "a" * 257
        with self.assertRaises(ValueError):
            self.db.add(2, too_long_name, "Нормальное сообщение")

    def test_get_by_id_existing(self):
        self.db.add(10, "arch_user", "<b>I use Arch btw</b>")
        record = self.db.get_by_id(10)
        self.assertIsNotNone(record)
        self.assertEqual(record["id"], 10)
        self.assertEqual(record["message"], "<b>I use Arch btw</b>")

    def test_get_by_id_non_existing_returns_none(self):
        record = self.db.get_by_id(999)
        self.assertIsNone(record)

    def test_get_by_name_multiple_records(self):
        self.db.add(1, "tester", "Пост 1")
        self.db.add(2, "tester", "Пост 2")
        self.db.add(3, "other", "Пост 3")
        records = self.db.get_by_name("tester")
        self.assertEqual(len(records), 2)

    def test_get_by_name_no_records_returns_empty_list(self):
        records = self.db.get_by_name("unknown_user")
        self.assertEqual(records, [])

    def test_update_existing_record(self):
        self.db.add(5, "ponchik", "Старый текст")
        result = self.db.update(5, "Новый обновленный текст")
        self.assertTrue(result)
        self.assertEqual(self.db.get_by_id(5)["message"], "Новый обновленный текст")

    def test_update_non_existing_id_raises_error(self):
        with self.assertRaises(KeyError):
            self.db.update(404, "Попытка обновить несуществующий пост")

    def test_delete_existing_record(self):
        self.db.add(7, "ponchik", "Удаляемое сообщение")
        result = self.db.delete(7)
        self.assertTrue(result)
        self.assertIsNone(self.db.get_by_id(7))

    def test_delete_non_existing_id_raises_error(self):
        with self.assertRaises(KeyError):
            self.db.delete(404)


if __name__ == "__main__":
    unittest.main()
