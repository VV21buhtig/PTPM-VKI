"""Изоляционные тесты контроллера (ЛР №3).

Все соседи контроллера — подмены (Mock). Проверяется только логика
самого контроллера: когда считать, когда брать из БД, что отправить.
"""

import unittest
from unittest.mock import Mock

from src.controller import Controller


class TestControllerIsolation(unittest.TestCase):
    """Проверка веток контроллера отдельно от реальных модулей."""

    def setUp(self):
        self.ui = Mock()
        self.db = Mock()
        self.calc = Mock()
        self.ext = Mock()
        self.ext.send_result.return_value = True

    def tearDown(self):
        self.ui.reset_mock()
        self.db.reset_mock()
        self.calc.reset_mock()
        self.ext.reset_mock()

    def _controller(self):
        return Controller(self.calc, self.db, self.ui, self.ext)

    def test_cached_path_does_not_touch_calculator(self):
        self.ui.get_sides.return_value = ("3", "3", "3")
        self.db.get_record.return_value = {
            "triangle_type": "равносторонний", "error_message": None
        }
        result = self._controller().run()
        self.assertEqual(result, "равносторонний")
        self.calc.calculate.assert_not_called()
        self.db.add_record.assert_not_called()
        self.ext.send_result.assert_called_once_with("равносторонний")

    def test_cache_miss_calls_calculator_and_writes_db(self):
        self.ui.get_sides.return_value = ("2", "2", "3")
        self.db.get_record.return_value = None
        self.calc.calculate.return_value = {
            "type": "равнобедренный", "vertices": [], "error": None
        }
        result = self._controller().run()
        self.assertEqual(result, "равнобедренный")
        self.calc.calculate.assert_called_once_with("2", "2", "3")
        self.db.add_record.assert_called_once_with(
            "2", "2", "3", "равнобедренный", None
        )
        self.ext.send_result.assert_called_once_with("равнобедренный")


if __name__ == "__main__":
    unittest.main()
