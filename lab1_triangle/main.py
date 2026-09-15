"""Точка входа приложения: вычисление вида треугольника и координат вершин."""

import logging
import sys

from config import setup_logging
from triangle import process_request


def main() -> int:
    """Главная точка входа приложения."""
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.stderr and hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    setup_logging()
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")
    logging.debug("Аргументы командной строки: %s", sys.argv)

    if len(sys.argv) == 4:
        sides = sys.argv[1:4]
    else:
        sides = [
            input("Введите длину стороны A: ").strip(),
            input("Введите длину стороны B: ").strip(),
            input("Введите длину стороны C: ").strip(),
        ]

    try:
        result = process_request(*sides)
    except Exception:
        logging.exception(
            "Непредвиденная ошибка при обработке запроса, стороны=%s", sides
        )
        print("Внутренняя ошибка, подробности в логе.")
        return 1

    triangle_type = result["type"]
    vertices = result["vertices"]

    if triangle_type == "":
        print("Тип треугольника: '' (нечисловые данные)")
    else:
        print(f"Тип треугольника: {triangle_type}")
    print("Координаты вершин:", vertices)

    logging.info("Приложение завершило работу")
    return 0


if __name__ == "__main__":
    sys.exit(main())