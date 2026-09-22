"""Вариант 1: вычисление вида треугольника и координат его вершин."""

import logging
import math

FIELD_SIZE = 100
ERROR_COORDS = (-1, -1)
INVALID_COORDS = (-2, -2)
MAX_DIMENSION = 90
EPSILON = 1e-9


def is_valid_triangle(side_a: float, side_b: float, side_c: float) -> bool:
    """Проверяет, можно ли из трёх положительных сторон построить треугольник."""
    if not (math.isfinite(side_a) and math.isfinite(side_b) and math.isfinite(side_c)):
        return False
    if side_a <= 0 or side_b <= 0 or side_c <= 0:
        return False
    return (
        side_a + side_b > side_c
        and side_a + side_c > side_b
        and side_b + side_c > side_a
    )


def get_triangle_type(side_a: float, side_b: float, side_c: float) -> str:
    """Определяет тип треугольника по трём сторонам."""
    if not is_valid_triangle(side_a, side_b, side_c):
        return "не треугольник"
    if (
        math.isclose(side_a, side_b, abs_tol=EPSILON)
        and math.isclose(side_b, side_c, abs_tol=EPSILON)
    ):
        return "равносторонний"
    if (
        math.isclose(side_a, side_b, abs_tol=EPSILON)
        or math.isclose(side_b, side_c, abs_tol=EPSILON)
        or math.isclose(side_a, side_c, abs_tol=EPSILON)
    ):
        return "равнобедренный"
    return "разносторонний"


def _fit_into_field(vertices: list[tuple[float, float]]) -> list[tuple[int, int]]:
    """Масштабирует треугольник до поля и размещает его по центру."""
    xs = [point[0] for point in vertices]
    ys = [point[1] for point in vertices]

    width = max(xs) - min(xs)
    height = max(ys) - min(ys)

    if width <= 0 or height <= 0:
        return [ERROR_COORDS, ERROR_COORDS, ERROR_COORDS]

    scale = min(MAX_DIMENSION / width, MAX_DIMENSION / height)

    shift_x = (FIELD_SIZE - width * scale) / 2 - min(xs) * scale
    shift_y = (FIELD_SIZE - height * scale) / 2 - min(ys) * scale

    return [
        (round(x * scale + shift_x), round(y * scale + shift_y))
        for x, y in vertices
    ]


def get_vertices(side_a: float, side_b: float, side_c: float) -> list[tuple[int, int]]:
    """Возвращает координаты вершин треугольника в поле 100x100."""
    if not is_valid_triangle(side_a, side_b, side_c):
        return [ERROR_COORDS, ERROR_COORDS, ERROR_COORDS]

    point_a = (0.0, 0.0)
    point_b = (side_c, 0.0)
    x3 = (side_a ** 2 + side_c ** 2 - side_b ** 2) / (2 * side_c)
    y3 = math.sqrt(side_a ** 2 - x3 ** 2)
    point_c = (x3, y3)

    return _fit_into_field([point_a, point_b, point_c])


def process_request(side_a_str, side_b_str, side_c_str) -> dict:
    """
    Обрабатывает запрос, возвращая тип треугольника и координаты вершин.

    * нечисловые (включая nan/inf) данные -> тип "" и координаты (-2, -2)
    * числовые, но не треугольник          -> тип "не треугольник" и (-1, -1)
    """
    try:
        side_a = float(side_a_str)
        side_b = float(side_b_str)
        side_c = float(side_c_str)
    except (TypeError, ValueError):
        logging.error(
            "Неуспешный запрос: стороны '%s', '%s', '%s' не являются вещественными числами",
            side_a_str, side_b_str, side_c_str,
        )
        return {"type": "", "vertices": [INVALID_COORDS] * 3}

    sides = (side_a, side_b, side_c)

    if not all(math.isfinite(s) for s in sides):
        logging.error(
            "Неуспешный запрос: стороны %s не являются конечными числами", sides
        )
        return {"type": "", "vertices": [INVALID_COORDS] * 3}

    if not is_valid_triangle(*sides):
        logging.error(
            "Неуспешный запрос: стороны %s не образуют треугольник", sides
        )
        return {"type": "не треугольник", "vertices": [ERROR_COORDS] * 3}

    triangle_type = get_triangle_type(*sides)
    vertices = get_vertices(*sides)
    logging.info(
        "Успешный запрос: стороны %s -> тип='%s', вершины=%s",
        sides, triangle_type, vertices,
    )
    return {"type": triangle_type, "vertices": vertices}