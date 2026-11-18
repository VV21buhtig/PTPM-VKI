"""Тесты для страницы Simple Calculator (Page Object Model)."""

from pages.calculator_page import CalculatorPage
from tests.base_test import BaseUITest


class SimpleCalculatorTest(BaseUITest):
    """Проверка арифметики, граничных значений и поведения интерфейса."""

    page_class = CalculatorPage

    # ------------------------------------------------------------------
    # Исходное состояние страницы
    # ------------------------------------------------------------------
    def test_default_state(self):
        """При открытии страницы выбран '+' и отображается '0 + 0 = 0'."""
        self.assertEqual(self.page.get_expression(), "0 + 0 = 0")
        self.assertEqual(self.page.get_selected_operation(), "+")
        self.assertEqual(self.page.get_available_operations(), ["+", "-", "*", "/"])

    # ------------------------------------------------------------------
    # Арифметические операции
    # ------------------------------------------------------------------
    def test_addition(self):
        self.assertEqual(self.page.calculate(7, 2, "+", expected="9"), "9")
        self.assertEqual(self.page.get_expression(), "7 + 2 = 9")

    def test_subtraction(self):
        self.assertEqual(self.page.calculate(7, 2, "-", expected="5"), "5")
        self.assertEqual(self.page.calculate(2, 10, "-", expected="-8"), "-8")

    def test_multiplication(self):
        self.assertEqual(self.page.calculate(7, 2, "*", expected="14"), "14")

    def test_division(self):
        self.assertEqual(self.page.calculate(7, 2, "/", expected="3.5"), "3.5")
        self.assertEqual(self.page.calculate(10, 4, "/", expected="2.5"), "2.5")

    def test_decimal_and_negative_operands(self):
        self.assertEqual(self.page.calculate(2.5, 1.5, "+", expected="4"), "4")
        self.assertEqual(self.page.calculate(-4, -2.5, "*", expected="10"), "10")

    def test_zero_operand(self):
        self.assertEqual(self.page.calculate(0, 7, "*", expected="0"), "0")

    # ------------------------------------------------------------------
    # Граничные значения
    # ------------------------------------------------------------------
    def test_large_numbers(self):
        self.assertEqual(
            self.page.calculate(1000000, 1000000, "*", expected="1000000000000"),
            "1000000000000",
        )

    def test_precision_limit_of_javascript_number(self):
        """Большие целые теряют точность: JS Number хранит ~15-17 значащих цифр."""
        self.assertEqual(
            self.page.calculate(
                999999999, 999999999, "*", expected="999999998000000000"
            ),
            "999999998000000000",
        )

    # ------------------------------------------------------------------
    # Деление на ноль
    # ------------------------------------------------------------------
    def test_division_by_zero(self):
        """Деление на ноль и 0/0 отображаются как 'null'."""
        for first, second in ((1, 0), (0, 0), (-5, 0)):
            with self.subTest(first=first, second=second):
                self.assertEqual(
                    self.page.calculate(first, second, "/", expected="null"),
                    "null",
                )

    # ------------------------------------------------------------------
    # Поведение интерфейса
    # ------------------------------------------------------------------
    def test_operation_switch_recalculates(self):
        """Смена операции пересчитывает результат без повторного ввода чисел."""
        self.page.calculate(6, 3, "+", expected="9")
        self.page.select_operation("*")
        self.assertEqual(self.page.get_result(), "18")
        self.page.select_operation("/")
        self.assertEqual(self.page.get_result(), "2")

    def test_increment_and_decrement_buttons(self):
        """Кнопки '+1' и '-1' меняют числа и результат для обоих полей."""
        self.page.calculate(5, 5, "+", expected="10")

        self.page.click_increment_first()
        self.page.wait_for_result("11")
        self.assertEqual(self.page.get_first_number(), "6")

        self.page.click_decrement_first()
        self.page.wait_for_result("10")
        self.assertEqual(self.page.get_first_number(), "5")

        self.page.click_increment_second()
        self.page.wait_for_result("11")
        self.assertEqual(self.page.get_second_number(), "6")

        self.page.click_decrement_second()
        self.page.wait_for_result("10")
        self.assertEqual(self.page.get_second_number(), "5")
