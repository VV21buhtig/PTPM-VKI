"""Точка входа приложения: проверка данных пользователя при регистрации."""

import logging
import sys

from config import setup_logging
from registration import process_request


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
        login, password, confirmation = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        login = input("Введите логин: ").strip()
        password = input("Введите пароль: ").strip()
        confirmation = input("Подтвердите пароль: ").strip()

    try:
        result = process_request(login, password, confirmation)
    except Exception:
        logging.exception("Неуспешный запрос: непредвиденное исключение")
        print("Результат: False")
        print("Сообщение: непредвиденное исключение (см. лог)")
        return 1

    print(f"Результат: {result['result']}")
    print(f"Сообщение: {result['message']}")

    logging.info("Приложение завершило работу")
    return 0


if __name__ == "__main__":
    main()