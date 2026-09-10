"""Вариант 2: проверка данных пользователя при регистрации."""

import hashlib
import logging
import re

PHONE_RE = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
LOGIN_RE = re.compile(r"^[A-Za-z0-9_]{5,}$")
ONLY_CYRILLIC_DIGITS_SPECIAL_RE = re.compile(r"^[а-яёА-ЯЁ0-9!@#$%^&*()\-_+=.,;:?~№]+$")
UPPER_CYRILLIC_RE = re.compile(r"[А-ЯЁ]")
LOWER_CYRILLIC_RE = re.compile(r"[а-яё]")
DIGIT_RE = re.compile(r"\d")

SPECIAL_CHARS = set("!@#$%^&*()-_+=.,;:?~№")

MIN_LOGIN_LENGTH = 5
MIN_PASSWORD_LENGTH = 7

BLACKLIST = {
    "admin",
    "root",
    "user",
    "guest",
    "test",
    "administrator",
    "moderator",
}

ERROR_EMPTY_LOGIN = "Логин не может быть пустым"
ERROR_BAD_PHONE = "Логин: телефон должен соответствовать маске +x-xxx-xxx-xxxx"
ERROR_BAD_EMAIL = "Логин: некорректный формат email"
ERROR_BAD_LOGIN = "Логин: минимум 5 символов, только латиница, цифры и подчёркивание"
ERROR_BLACKLIST = "Логин запрещён (черный список)"
ERROR_PASSWORD_LENGTH = f"Пароль: минимум {MIN_PASSWORD_LENGTH} символов"
ERROR_PASSWORD_CHARS = "Пароль: допустимы только кириллица, цифры и спецсимволы"
ERROR_PASSWORD_UPPER = "Пароль: нужна минимум одна заглавная кириллическая буква"
ERROR_PASSWORD_LOWER = "Пароль: нужна минимум одна строчная кириллическая буква"
ERROR_PASSWORD_DIGIT = "Пароль: нужна минимум одна цифра"
ERROR_PASSWORD_SPECIAL = "Пароль: нужен минимум один спецсимвол"
ERROR_PASSWORD_MISMATCH = "Пароль и подтверждение не совпадают"


def mask_password(password: str) -> str:
    """
    Детерминированное маскирование пароля.

    Возвращает одинаковое значение для одинаковых паролей и разное для
    отличающихся. Реальный пароль в открытом виде нигде не фигурирует.
    """
    if password is None:
        password = ""
    digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return f"sha256:{digest[:12]}"


def _normalize(value) -> str:
    return "" if value is None else str(value)


def validate_login(login: str) -> str:
    """Возвращает пустую строку при валидном логине или текст ошибки."""
    if not login:
        return ERROR_EMPTY_LOGIN
    if login.startswith("+"):
        if not PHONE_RE.match(login):
            return ERROR_BAD_PHONE
    elif "@" in login:
        if not EMAIL_RE.match(login):
            return ERROR_BAD_EMAIL
    else:
        if not LOGIN_RE.match(login):
            return ERROR_BAD_LOGIN
    if login.lower() in BLACKLIST:
        return ERROR_BLACKLIST
    return ""


def validate_password(password: str, confirmation: str) -> str:
    """Возвращает пустую строку при валидном пароле или текст ошибки."""
    if len(password) < MIN_PASSWORD_LENGTH:
        return ERROR_PASSWORD_LENGTH
    if not ONLY_CYRILLIC_DIGITS_SPECIAL_RE.match(password):
        return ERROR_PASSWORD_CHARS
    if not UPPER_CYRILLIC_RE.search(password):
        return ERROR_PASSWORD_UPPER
    if not LOWER_CYRILLIC_RE.search(password):
        return ERROR_PASSWORD_LOWER
    if not DIGIT_RE.search(password):
        return ERROR_PASSWORD_DIGIT
    if not any(ch in SPECIAL_CHARS for ch in password):
        return ERROR_PASSWORD_SPECIAL
    if password != confirmation:
        return ERROR_PASSWORD_MISMATCH
    return ""


def process_request(login, password, confirmation) -> dict:
    """Валидирует данные регистрации, возвращая результат и сообщение."""
    login = _normalize(login)
    password = _normalize(password)
    confirmation = _normalize(confirmation)

    login_error = validate_login(login)
    if login_error:
        logging.error(
            "Неуспешный запрос: login='%s', password=%s, confirm=%s -> %s",
            login, mask_password(password), mask_password(confirmation), login_error,
        )
        return {"result": False, "message": login_error}

    password_error = validate_password(password, confirmation)
    if password_error:
        logging.error(
            "Неуспешный запрос: login='%s', password=%s, confirm=%s -> %s",
            login, mask_password(password), mask_password(confirmation), password_error,
        )
        return {"result": False, "message": password_error}

    logging.info(
        "Успешный запрос: login='%s', password=%s, confirm=%s -> регистрация успешна",
        login, mask_password(password), mask_password(confirmation),
    )
    return {"result": True, "message": ""}