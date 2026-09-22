"""Unit-тесты для варианта 1 (треугольник)."""

import unittest

from triangle import (
    ERROR_COORDS,
    FIELD_SIZE,
    INVALID_COORDS,
    get_triangle_type,
    get_vertices,
    is_valid_triangle,
    process_request,
)


class TestIsValidTriangle(unittest.TestCase):
    def test_valid_triangle(self):
        self.assertTrue(is_valid_triangle(3, 4, 5))

    def test_valid_with_floats(self):
        self.assertTrue(is_valid_triangle(2.5, 3.5, 4.5))

    def test_zero_side(self):
        self.assertFalse(is_valid_triangle(0, 4, 5))

    def test_negative_side(self):
        self.assertFalse(is_valid_triangle(-1, 4, 5))

    def test_inequality_fails(self):
        self.assertFalse(is_valid_triangle(1, 2, 3))

    def test_equilateral_is_valid(self):
        self.assertTrue(is_valid_triangle(5, 5, 5))

    def test_nan_is_invalid(self):
        self.assertFalse(is_valid_triangle(float("nan"), 4, 5))

    def test_inf_is_invalid(self):
        self.assertFalse(is_valid_triangle(float("inf"), 4, 5))


class TestTriangleType(unittest.TestCase):
    def test_equilateral(self):
        self.assertEqual(get_triangle_type(5, 5, 5), "равносторонний")

    def test_isosceles(self):
        self.assertEqual(get_triangle_type(5, 5, 7), "равнобедренный")

    def test_scalene(self):
        self.assertEqual(get_triangle_type(3, 4, 5), "разносторонний")

    def test_not_a_triangle(self):
        self.assertEqual(get_triangle_type(1, 2, 3), "не треугольник")

    def test_not_a_triangle_zero_side(self):
        self.assertEqual(get_triangle_type(0, 5, 5), "не треугольник")


class TestVertices(unittest.TestCase):
    def test_valid_triangle_fits_field(self):
        vertices = get_vertices(3, 4, 5)
        self.assertEqual(len(vertices), 3)
        for x, y in vertices:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, FIELD_SIZE)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, FIELD_SIZE)

    def test_error_coords_for_not_triangle(self):
        self.assertEqual(get_vertices(1, 2, 3), [ERROR_COORDS] * 3)

    def test_error_coords_for_negative_side(self):
        self.assertEqual(get_vertices(-1, 5, 5), [ERROR_COORDS] * 3)


class TestProcessRequest(unittest.TestCase):
    def test_success(self):
        result = process_request("3", "4", "5")
        self.assertEqual(result["type"], "разносторонний")
        self.assertEqual(len(result["vertices"]), 3)

    def test_equilateral_success(self):
        result = process_request("5", "5", "5")
        self.assertEqual(result["type"], "равносторонний")

    def test_numeric_but_not_triangle(self):
        result = process_request("1", "2", "3")
        self.assertEqual(result["type"], "не треугольник")
        self.assertEqual(result["vertices"], [ERROR_COORDS] * 3)

    def test_non_numeric_data(self):
        result = process_request("abc", "def", "ghi")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["vertices"], [INVALID_COORDS] * 3)

    def test_partially_non_numeric_data(self):
        result = process_request("3", "four", "5")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["vertices"], [INVALID_COORDS] * 3)

    def test_nan_treated_as_invalid(self):
        result = process_request("nan", "4", "5")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["vertices"], [INVALID_COORDS] * 3)

    def test_inf_treated_as_invalid(self):
        result = process_request("inf", "4", "5")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["vertices"], [INVALID_COORDS] * 3)


if __name__ == "__main__":
    unittest.main()