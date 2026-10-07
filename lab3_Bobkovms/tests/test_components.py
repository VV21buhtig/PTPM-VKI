"""Компонентные тесты: БД, ввод, внешний сервис (ЛР №3)."""

import unittest
from unittest.mock import patch

from src.database import TriangleDatabase
from src.external_service import EmailServiceSimulator
from src.user_interaction import ConsoleUserInteraction


class TestDatabase(unittest.TestCase):
    """Жизненный цикл записи: add/get/delete."""

    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_get_delete_lifecycle(self):
        self.assertIsNone(self.db.get_record("7", "7", "7"))
        self.db.add_record("7", "7", "7", "равносторонний", None)
        rec = self.db.get_record("7", "7", "7")
        self.assertEqual(rec["triangle_type"], "равносторонний")
        # повторная вставка перезаписывает запись (INSERT OR REPLACE)
        self.db.add_record(
            "7", "7", "7", "не треугольник", "Стороны не образуют треугольник"
        )
        rec = self.db.get_record("7", "7", "7")
        self.assertEqual(rec["triangle_type"], "не треугольник")
        self.assertTrue(self.db.delete_record("7", "7", "7"))
        self.assertIsNone(self.db.get_record("7", "7", "7"))
        self.assertFalse(self.db.delete_record("7", "7", "7"))


class TestUserInteraction(unittest.TestCase):
    """Чтение трех вводов пользователя."""

    def test_reads_three_inputs(self):
        ui = ConsoleUserInteraction()
        with patch("builtins.input", side_effect=["3", "4", "5"]):
            self.assertEqual(ui.get_sides(), ("3", "4", "5"))


class TestExternalService(unittest.TestCase):
    """Имитация отправки результата."""

    def test_records_sent(self):
        svc = EmailServiceSimulator()
        self.assertTrue(svc.send_result("разносторонний"))
        self.assertEqual(svc.sent, ["разносторонний"])


if __name__ == "__main__":
    unittest.main()
