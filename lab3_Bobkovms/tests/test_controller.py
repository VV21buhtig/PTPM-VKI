"""Интеграционные + изоляционные тесты контроллера (ЛР №3).

Требования: >= 5 тестов, минимум 3 интеграционных, изоляция через
заглушки (Mock/patch) для ввода пользователя и внешнего сервера.
"""

import unittest
from unittest.mock import Mock, patch

from src.calculator import TriangleCalculator
from src.controller import Controller
from src.database import TriangleDatabase
from src.external_service import EmailServiceSimulator
from src.user_interaction import ConsoleUserInteraction


def make_controller(ui_sides, db=None, calc=None, external=None):
    """Собирает контроллер с заглушкой ввода и реальными/мок-компонентами."""
    ui = Mock()
    ui.get_sides.return_value = ui_sides
    db = db if db is not None else TriangleDatabase(":memory:")
    calc = calc if calc is not None else TriangleCalculator()
    external = external if external is not None else Mock()
    return Controller(calc, db, ui, external), db, calc, external


class TestControllerIntegration(unittest.TestCase):
    """Интеграционные тесты сквозного сценария."""

    def test_integration_new_valid_scalene_saved_and_sent(self):
        ctrl, db, _, ext = make_controller(("3", "4", "5"))
        result = ctrl.run()
        self.assertEqual(result, "разносторонний")
        record = db.get_record("3", "4", "5")
        self.assertIsNotNone(record)
        self.assertEqual(record["triangle_type"], "разносторонний")
        self.assertIsNone(record["error_message"])
        ext.send_result.assert_called_once_with("разносторонний")
        db.close()

    def test_integration_cached_record_skips_calculation(self):
        db = TriangleDatabase(":memory:")
        db.add_record("5", "5", "5", "равносторонний", None)
        real_calc = TriangleCalculator()
        spy_calc = Mock()
        spy_calc.calculate = Mock(wraps=real_calc.calculate)
        ctrl, _, _, ext = make_controller(("5", "5", "5"), db=db, calc=spy_calc)
        result = ctrl.run()
        self.assertEqual(result, "равносторонний")
        spy_calc.calculate.assert_not_called()
        ext.send_result.assert_called_once_with("равносторонний")
        db.close()

    def test_integration_invalid_triangle_saves_error_and_sends(self):
        ctrl, db, _, ext = make_controller(("1", "2", "10"))
        result = ctrl.run()
        self.assertIn("не треугольник", result)
        record = db.get_record("1", "2", "10")
        self.assertIsNotNone(record)
        self.assertEqual(record["triangle_type"], "не треугольник")
        self.assertIsNotNone(record["error_message"])
        ext.send_result.assert_called_once_with(result)
        db.close()

    def test_integration_non_numeric_input_reports_error(self):
        ctrl, db, _, ext = make_controller(("abc", "4", "5"))
        result = ctrl.run()
        self.assertTrue(result.startswith("Ошибка:"))
        record = db.get_record("abc", "4", "5")
        self.assertIsNotNone(record)
        self.assertEqual(record["triangle_type"], "")
        self.assertIsNotNone(record["error_message"])
        ext.send_result.assert_called_once_with(result)
        db.close()

    def test_integration_equilateral_fresh_calculation(self):
        ctrl, db, _, ext = make_controller(("5", "5", "5"))
        result = ctrl.run()
        self.assertEqual(result, "равносторонний")
        ext.send_result.assert_called_once_with("равносторонний")
        db.close()

    def test_integration_isosceles_fresh_calculation(self):
        ctrl, db, _, ext = make_controller(("2", "2", "3"))
        result = ctrl.run()
        self.assertEqual(result, "равнобедренный")
        ext.send_result.assert_called_once_with("равнобедренный")
        db.close()

    def test_integration_non_finite_input_reports_error(self):
        ctrl, db, _, ext = make_controller(("inf", "3", "4"))
        result = ctrl.run()
        self.assertTrue(result.startswith("Ошибка:"))
        record = db.get_record("inf", "3", "4")
        self.assertEqual(record["triangle_type"], "")
        ext.send_result.assert_called_once_with(result)
        db.close()

    def test_integration_zero_side_reports_not_triangle(self):
        ctrl, db, _, ext = make_controller(("0", "4", "5"))
        result = ctrl.run()
        self.assertIn("не треугольник", result)
        ext.send_result.assert_called_once_with(result)
        db.close()


class TestControllerIsolation(unittest.TestCase):
    """Проверка изоляции модулей через заглушки."""

    def test_isolation_cached_path_does_not_touch_calculator(self):
        ui = Mock()
        ui.get_sides.return_value = ("3", "3", "3")
        db = Mock()
        db.get_record.return_value = {
            "triangle_type": "равносторонний", "error_message": None
        }
        calc = Mock()
        ext = Mock()
        ctrl = Controller(calc, db, ui, ext)
        result = ctrl.run()
        self.assertEqual(result, "равносторонний")
        calc.calculate.assert_not_called()
        db.add_record.assert_not_called()
        ext.send_result.assert_called_once_with("равносторонний")

    def test_isolation_cache_miss_calls_calculator_and_writes_db(self):
        ui = Mock()
        ui.get_sides.return_value = ("2", "2", "3")
        db = Mock()
        db.get_record.return_value = None
        calc = Mock()
        calc.calculate.return_value = {
            "type": "равнобедренный", "vertices": [], "error": None
        }
        ext = Mock()
        ext.send_result.return_value = True
        ctrl = Controller(calc, db, ui, ext)
        result = ctrl.run()
        self.assertEqual(result, "равнобедренный")
        calc.calculate.assert_called_once_with("2", "2", "3")
        db.add_record.assert_called_once_with(
            "2", "2", "3", "равнобедренный", None
        )
        ext.send_result.assert_called_once_with("равнобедренный")


class TestHelpers(unittest.TestCase):
    """Покрытие вспомогательных классов (БД, ввод, внешний сервис)."""

    def test_database_add_get_delete_lifecycle(self):
        db = TriangleDatabase(":memory:")
        self.assertIsNone(db.get_record("7", "7", "7"))
        db.add_record("7", "7", "7", "равносторонний", None)
        rec = db.get_record("7", "7", "7")
        self.assertEqual(rec["triangle_type"], "равносторонний")
        # повторная вставка перезаписывает запись (INSERT OR REPLACE)
        db.add_record("7", "7", "7", "не треугольник", "Стороны не образуют треугольник")
        rec = db.get_record("7", "7", "7")
        self.assertEqual(rec["triangle_type"], "не треугольник")
        self.assertTrue(db.delete_record("7", "7", "7"))
        self.assertIsNone(db.get_record("7", "7", "7"))
        self.assertFalse(db.delete_record("7", "7", "7"))
        db.close()

    def test_user_interaction_reads_three_inputs(self):
        ui = ConsoleUserInteraction()
        with patch("builtins.input", side_effect=["3", "4", "5"]):
            self.assertEqual(ui.get_sides(), ("3", "4", "5"))

    def test_external_service_records_sent(self):
        svc = EmailServiceSimulator()
        self.assertTrue(svc.send_result("разносторонний"))
        self.assertEqual(svc.sent, ["разносторонний"])


if __name__ == "__main__":
    unittest.main()
