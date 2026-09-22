"""Unit-тесты для my_project (треугольник, ЛР1)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from my_project import (  # noqa: E402
    ERROR_COORDS,
    FIELD_SIZE,
    INVALID_COORDS,
    _fit_into_field,
    get_triangle_type,
    get_vertices,
    is_valid_triangle,
    process_request,
)


class TestIsValidTriangle(unittest.TestCase):
    def test_is_valid_returns_true_for_scalene_3_4_5(self):
        self.assertTrue(is_valid_triangle(3, 4, 5))

    def test_is_valid_returns_true_for_equilateral(self):
        self.assertTrue(is_valid_triangle(5, 5, 5))

    def test_is_valid_returns_true_for_float_sides(self):
        self.assertTrue(is_valid_triangle(2.5, 3.5, 4.5))

    def test_is_valid_rejects_zero_side(self):
        self.assertFalse(is_valid_triangle(0, 4, 5))

    def test_is_valid_rejects_negative_side(self):
        self.assertFalse(is_valid_triangle(-1, 4, 5))

    def test_is_valid_rejects_degenerate_equality(self):
        self.assertFalse(is_valid_triangle(1, 2, 3))

    def test_is_valid_rejects_nan_side(self):
        self.assertFalse(is_valid_triangle(float("nan"), 4, 5))

    def test_is_valid_rejects_inf_side(self):
        self.assertFalse(is_valid_triangle(float("inf"), 4, 5))


class TestTriangleType(unittest.TestCase):
    def test_type_detects_equilateral(self):
        self.assertEqual(get_triangle_type(5, 5, 5), "равносторонний")

    def test_type_detects_isosceles_with_ab_equal(self):
        self.assertEqual(get_triangle_type(5, 5, 7), "равнобедренный")

    def test_type_detects_isosceles_with_bc_equal(self):
        self.assertEqual(get_triangle_type(7, 5, 5), "равнобедренный")

    def test_type_detects_isosceles_with_ac_equal(self):
        self.assertEqual(get_triangle_type(5, 7, 5), "равнобедренный")

    def test_type_detects_scalene(self):
        self.assertEqual(get_triangle_type(3, 4, 5), "разносторонний")

    def test_type_returns_not_triangle_for_degenerate(self):
        self.assertEqual(get_triangle_type(1, 2, 3), "не треугольник")

    def test_type_treats_close_floats_within_epsilon_as_equilateral(self):
        self.assertEqual(get_triangle_type(5.0, 5.0 + 5e-10, 5.0), "равносторонний")

    def test_type_treats_float_02_sum_as_isosceles(self):
        # 0.1 + 0.2 != 0.3 в IEEE 754, допуск EPSILON должен спасти сравнение
        self.assertEqual(get_triangle_type(0.1 + 0.2, 0.3, 0.5), "равнобедренный")


class TestVertices(unittest.TestCase):
    def test_vertices_fit_into_100x100_field(self):
        vertices = get_vertices(3, 4, 5)
        self.assertEqual(len(vertices), 3)
        for x, y in vertices:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, FIELD_SIZE)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, FIELD_SIZE)

    def test_vertices_return_error_coords_for_not_triangle(self):
        self.assertEqual(get_vertices(1, 2, 3), [ERROR_COORDS] * 3)

    def test_vertices_return_error_coords_for_negative_side(self):
        self.assertEqual(get_vertices(-1, 5, 5), [ERROR_COORDS] * 3)

    def test_vertices_handle_nearly_degenerate_without_crash(self):
        vertices = get_vertices(2, 3, 4.999)
        self.assertEqual(len(vertices), 3)
        for x, y in vertices:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, FIELD_SIZE)

    def test_fit_into_field_rejects_zero_area(self):
        self.assertEqual(
            _fit_into_field([(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]),
            [ERROR_COORDS] * 3,
        )


class TestProcessRequest(unittest.TestCase):
    def test_process_request_succeeds_for_scalene_strings(self):
        result = process_request("3", "4", "5")
        self.assertEqual(result["type"], "разносторонний")
        self.assertEqual(len(result["vertices"]), 3)

    def test_process_request_succeeds_for_equilateral(self):
        result = process_request("5", "5", "5")
        self.assertEqual(result["type"], "равносторонний")

    def test_process_request_flags_numeric_not_triangle(self):
        result = process_request("1", "2", "3")
        self.assertEqual(result["type"], "не треугольник")
        self.assertEqual(result["vertices"], [ERROR_COORDS] * 3)

    def test_process_request_rejects_non_numeric_strings(self):
        result = process_request("abc", "def", "ghi")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["vertices"], [INVALID_COORDS] * 3)

    def test_process_request_rejects_partially_non_numeric(self):
        result = process_request("3", "four", "5")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["vertices"], [INVALID_COORDS] * 3)

    def test_process_request_rejects_none_input(self):
        result = process_request(None, "4", "5")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["vertices"], [INVALID_COORDS] * 3)

    def test_process_request_treats_nan_as_invalid(self):
        result = process_request("nan", "4", "5")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["vertices"], [INVALID_COORDS] * 3)

    def test_process_request_treats_inf_as_invalid(self):
        result = process_request("inf", "4", "5")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["vertices"], [INVALID_COORDS] * 3)


if __name__ == "__main__":
    unittest.main()
