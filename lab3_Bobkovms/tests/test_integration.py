"""Интеграционные тесты сквозного сценария (ЛР №3).

Каждый тест запускает настоящий Controller с настоящим калькулятором
и настоящей БД в памяти. Подменены только ввод и внешний сервис.
"""

import unittest
from unittest.mock import Mock

from src.calculator import TriangleCalculator
from src.controller import Controller
from src.database import TriangleDatabase


class TestControllerIntegration(unittest.TestCase):
    """Проверка связки ввод -> БД/расчет -> отправка."""

    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.calc = TriangleCalculator()
        self.ext = Mock()

    def tearDown(self):
        self.db.close()

    def _run(self, sides, calc=None, db=None):
        ui = Mock()
        ui.get_sides.return_value = sides
        ctrl = Controller(
            calc if calc is not None else self.calc,
            db if db is not None else self.db,
            ui,
            self.ext,
        )
        return ctrl.run()

    def test_new_valid_scalene_saved_and_sent(self):
        result = self._run(("3", "4", "5"))
        self.assertEqual(result, "разносторонний")
        record = self.db.get_record("3", "4", "5")
        self.assertIsNotNone(record)
        self.assertEqual(record["triangle_type"], "разносторонний")
        self.assertIsNone(record["error_message"])
        self.ext.send_result.assert_called_once_with("разносторонний")

    def test_cached_record_skips_calculation(self):
        self.db.add_record("5", "5", "5", "равносторонний", None)
        spy = Mock()
        spy.calculate = Mock(wraps=self.calc.calculate)
        result = self._run(("5", "5", "5"), calc=spy)
        self.assertEqual(result, "равносторонний")
        spy.calculate.assert_not_called()
        self.ext.send_result.assert_called_once_with("равносторонний")

    def test_invalid_triangle_saves_error_and_sends(self):
        result = self._run(("1", "2", "10"))
        self.assertIn("не треугольник", result)
        record = self.db.get_record("1", "2", "10")
        self.assertIsNotNone(record)
        self.assertEqual(record["triangle_type"], "не треугольник")
        self.assertIsNotNone(record["error_message"])
        self.ext.send_result.assert_called_once_with(result)

    def test_non_numeric_input_reports_error(self):
        result = self._run(("abc", "4", "5"))
        self.assertTrue(result.startswith("Ошибка:"))
        record = self.db.get_record("abc", "4", "5")
        self.assertIsNotNone(record)
        self.assertEqual(record["triangle_type"], "")
        self.assertIsNotNone(record["error_message"])
        self.ext.send_result.assert_called_once_with(result)

    def test_equilateral_fresh_calculation(self):
        result = self._run(("5", "5", "5"))
        self.assertEqual(result, "равносторонний")
        self.ext.send_result.assert_called_once_with("равносторонний")

    def test_isosceles_fresh_calculation(self):
        result = self._run(("2", "2", "3"))
        self.assertEqual(result, "равнобедренный")
        self.ext.send_result.assert_called_once_with("равнобедренный")

    def test_non_finite_input_reports_error(self):
        result = self._run(("inf", "3", "4"))
        self.assertTrue(result.startswith("Ошибка:"))
        record = self.db.get_record("inf", "3", "4")
        self.assertEqual(record["triangle_type"], "")
        self.ext.send_result.assert_called_once_with(result)

    def test_zero_side_reports_not_triangle(self):
        result = self._run(("0", "4", "5"))
        self.assertIn("не треугольник", result)
        self.ext.send_result.assert_called_once_with(result)


if __name__ == "__main__":
    unittest.main()
