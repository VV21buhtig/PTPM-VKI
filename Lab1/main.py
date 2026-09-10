"""Точка входа приложения: вычисление вида треугольника и координат вершин."""

import logging
import sys

from config import setup_logging
from triangle import process_request


def main() -> int:
    """Главная точка входа приложения."""
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    if sys.stderr and hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    setup_logging()
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    if len(sys.argv) == 4:
        sides = sys.argv[1:4]
    else:
        sides = [
            input("Введите длину стороны A: ").strip(),
            input("Введите длину стороны B: ").strip(),
            input("Введите длину стороны C: ").strip(),
        ]

    result = process_request(*sides)

    triangle_type = result["type"]
    vertices = result["vertices"]
    print(f"Тип треугольника: {triangle_type!r}" if triangle_type == "" else f"Тип треугольника: {triangle_type}")
    print("Координаты вершин:", vertices)

    logging.info("Приложение завершило работу")
    return 0


if __name__ == "__main__":
    main()