"""Точка входа демо: ввод -> расчёт/БД -> отправка."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.calculator import TriangleCalculator
from src.controller import Controller
from src.database import TriangleDatabase
from src.external_service import EmailServiceSimulator
from src.user_interaction import ConsoleUserInteraction


def main() -> int:
    db = TriangleDatabase("triangles.db")
    ctrl = Controller(
        TriangleCalculator(), db, ConsoleUserInteraction(), EmailServiceSimulator()
    )
    try:
        result = ctrl.run()
    finally:
        db.close()
    print(f"Результат: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
