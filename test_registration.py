"""Unit-тесты для варианта 2 (регистрация)."""

import unittest

from registration import (
    ERROR_BAD_EMAIL,
    ERROR_BAD_LOGIN,
    ERROR_BAD_PHONE,
    ERROR_BLACKLIST,
    ERROR_EMPTY_LOGIN,
    ERROR_PASSWORD_CHARS,
    ERROR_PASSWORD_DIGIT,
    ERROR_PASSWORD_LENGTH,
    ERROR_PASSWORD_LOWER,
    ERROR_PASSWORD_MISMATCH,
    ERROR_PASSWORD_SPECIAL,
    ERROR_PASSWORD_UPPER,
    mask_password,
    process_request,
    validate_login,
    validate_password,
)


class TestMaskPassword(unittest.TestCase):
    def test_same_password_same_mask(self):
        self.assertEqual(mask_password("Пароль1!"), mask_password("Пароль1!"))

    def test_different_password_different_mask(self):
        self.assertNotEqual(mask_password("Пароль1!"), mask_password("Пароль2!"))

    def test_mask_is_not_plaintext(self):
        password = "Пароль1!"
        self.assertNotIn(password, mask_password(password))

    def test_mask_is_deterministic(self):
        self.assertEqual(mask_password("Ааа111!"), mask_password("Ааа111!"))


class TestValidateLogin(unittest.TestCase):
    def test_valid_phone(self):
        self.assertEqual(validate_login("+7-911-555-5555"), "")

    def test_valid_email(self):
        self.assertEqual(validate_login("ivan@mail.ru"), "")

    def test_valid_plain_login(self):
        self.assertEqual(validate_login("ivan_22"), "")

    def test_empty_login(self):
        self.assertEqual(validate_login(""), ERROR_EMPTY_LOGIN)

    def test_bad_phone(self):
        self.assertEqual(validate_login("+7-911-55-5555"), ERROR_BAD_PHONE)

    def test_bad_email(self):
        self.assertEqual(validate_login("ivan@mail"), ERROR_BAD_EMAIL)

    def test_bad_plain_login_too_short(self):
        self.assertEqual(validate_login("ab"), ERROR_BAD_LOGIN)

    def test_bad_plain_login_invalid_chars(self):
        self.assertEqual(validate_login("ван_я!"), ERROR_BAD_LOGIN)

    def test_blacklisted_login(self):
        self.assertEqual(validate_login("admin"), ERROR_BLACKLIST)

    def test_blacklisted_login_case_insensitive(self):
        self.assertEqual(validate_login("Admin"), ERROR_BLACKLIST)


class TestValidatePassword(unittest.TestCase):
    VALID_PASSWORD = "Пароль123!"

    def test_valid_password(self):
        self.assertEqual(validate_password(self.VALID_PASSWORD, self.VALID_PASSWORD), "")

    def test_too_short(self):
        self.assertEqual(validate_password("Пар1!", "Пар1!"), ERROR_PASSWORD_LENGTH)

    def test_latin_chars_not_allowed(self):
        self.assertEqual(
            validate_password("Password123!", "Password123!"), ERROR_PASSWORD_CHARS
        )

    def test_missing_uppercase(self):
        self.assertEqual(
            validate_password("пароль123!", "пароль123!"), ERROR_PASSWORD_UPPER
        )

    def test_missing_lowercase(self):
        self.assertEqual(
            validate_password("ПАРОЛЬ123!", "ПАРОЛЬ123!"), ERROR_PASSWORD_LOWER
        )

    def test_missing_digit(self):
        self.assertEqual(
            validate_password("Пароль!!", "Пароль!!"), ERROR_PASSWORD_DIGIT
        )

    def test_missing_special(self):
        self.assertEqual(
            validate_password("Пароль123", "Пароль123"), ERROR_PASSWORD_SPECIAL
        )

    def test_mismatch(self):
        self.assertEqual(
            validate_password(self.VALID_PASSWORD, "Пароль124!"), ERROR_PASSWORD_MISMATCH
        )

    def test_password_with_space_not_allowed(self):
        self.assertEqual(
            validate_password("Пароль 123!", "Пароль 123!"), ERROR_PASSWORD_CHARS
        )


class TestProcessRequest(unittest.TestCase):
    VALID_DATA = ("ivan_22", "Пароль123!", "Пароль123!")

    def test_success(self):
        result = process_request(*self.VALID_DATA)
        self.assertTrue(result["result"])
        self.assertEqual(result["message"], "")

    def test_success_phone_login(self):
        result = process_request("+7-911-555-5555", "Пароль123!", "Пароль123!")
        self.assertTrue(result["result"])

    def test_success_email_login(self):
        result = process_request("ivan@mail.ru", "Пароль123!", "Пароль123!")
        self.assertTrue(result["result"])

    def test_failed_login(self):
        result = process_request("admin", self.VALID_DATA[1], self.VALID_DATA[2])
        self.assertFalse(result["result"])
        self.assertEqual(result["message"], ERROR_BLACKLIST)

    def test_failed_password(self):
        result = process_request(self.VALID_DATA[0], "short", "short")
        self.assertFalse(result["result"])
        self.assertEqual(result["message"], ERROR_PASSWORD_LENGTH)

    def test_failed_mismatch(self):
        result = process_request(self.VALID_DATA[0], "Пароль123!", "Пароль124!")
        self.assertFalse(result["result"])
        self.assertEqual(result["message"], ERROR_PASSWORD_MISMATCH)

    def test_failed_empty_inputs(self):
        result = process_request("", "", "")
        self.assertFalse(result["result"])
        self.assertEqual(result["message"], ERROR_EMPTY_LOGIN)


if __name__ == "__main__":
    unittest.main()