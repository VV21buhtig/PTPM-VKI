"""Unit-тесты для delivery_service (бизнес-логика доставки)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from delivery_service import calculate_delivery_cost  # noqa: E402


class TestDeliveryValidation(unittest.TestCase):
    def test_validation_rejects_weight_below_minimum(self):
        self.assertEqual(
            calculate_delivery_cost(0.09, 100, "обычный"), (-1, "0000-00-00")
        )

    def test_validation_accepts_weight_at_lower_bound(self):
        cost, date = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertEqual(cost, 700)
        self.assertEqual(date, "2026-09-04")

    def test_validation_accepts_weight_at_upper_bound(self):
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertEqual(cost, 1050)  # 700 * 1.5

    def test_validation_rejects_weight_above_maximum(self):
        self.assertEqual(
            calculate_delivery_cost(50.1, 100, "обычный"), (-1, "0000-00-00")
        )

    def test_validation_rejects_zero_distance(self):
        self.assertEqual(
            calculate_delivery_cost(1, 0, "обычный"), (-1, "0000-00-00")
        )

    def test_validation_accepts_max_distance(self):
        cost, date = calculate_delivery_cost(1, 5000, "обычный")
        self.assertEqual(cost, 25200)  # 200 + 5000*5
        self.assertEqual(date, "2026-09-13")  # 5000//500 = 10 дней

    def test_validation_rejects_distance_above_maximum(self):
        self.assertEqual(
            calculate_delivery_cost(1, 5001, "обычный"), (-1, "0000-00-00")
        )

    def test_validation_rejects_unknown_package_type(self):
        self.assertEqual(
            calculate_delivery_cost(1, 100, "подарок"), (-1, "0000-00-00")
        )


class TestDeliveryTariffs(unittest.TestCase):
    def test_tariff_applies_no_coefficient_at_weight_5(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_tariff_applies_coefficient_12_above_5kg(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)  # 700 * 1.2

    def test_tariff_applies_coefficient_15_at_weight_20(self):
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)  # 700 * 1.5

    def test_tariff_adds_fragile_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий")
        self.assertEqual(cost, 1000)  # 700 + 300

    def test_tariff_adds_dangerous_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "опасный")
        self.assertEqual(cost, 1700)  # 700 + 1000

    def test_tariff_calculates_long_distance_date(self):
        _, date = calculate_delivery_cost(1, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")  # 1000//500 = 2 дня


class TestDeliveryExpress(unittest.TestCase):
    def test_express_costs_more_than_ordinary(self):
        ordinary, _ = calculate_delivery_cost(1, 100, "обычный", False)
        express, _ = calculate_delivery_cost(1, 100, "обычный", True)
        self.assertGreater(express, ordinary)

    def test_express_applies_50_percent_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный", True)
        self.assertEqual(cost, 1050)  # 700 * 1.5

    def test_express_never_delivers_on_send_day(self):
        _, date = calculate_delivery_cost(1, 100, "обычный", True)
        self.assertEqual(date, "2026-09-04")  # минимум 1 день, а не 0

    def test_express_halves_long_delivery_time(self):
        _, date = calculate_delivery_cost(1, 1000, "обычный", True)
        self.assertEqual(date, "2026-09-04")  # 2 дня // 2 = 1 день

    def test_express_combined_with_fragile(self):
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий", True)
        self.assertEqual(cost, 1500)  # (700 + 300) * 1.5

    def test_express_combined_with_heavy_weight(self):
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный", True)
        self.assertEqual(cost, 1575)  # 700 * 1.5 * 1.5


if __name__ == "__main__":
    unittest.main()
