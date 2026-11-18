"""Page Object для страницы AngularJS Simple Calculator (globalsqa).

Класс инкапсулирует все локаторы и взаимодействие с интерфейсом.
Тесты работают только через публичные методы этого класса и не обращаются
к драйверу напрямую.
"""

import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class CalculatorPage:
    """Страница калькулятора: два поля ввода, выбор операции и строка результата."""

    URL = os.getenv(
        "BASE_URL", "https://www.globalsqa.com/angularJs-protractor/SimpleCalculator/"
    )
    DEFAULT_TIMEOUT = 5

    OPERATIONS = ("+", "-", "*", "/")

    # Локаторы приватные: тесты не должны зависеть от вёрстки страницы.
    __FIRST_NUMBER = (By.CSS_SELECTOR, "input[ng-model='a']")
    __SECOND_NUMBER = (By.CSS_SELECTOR, "input[ng-model='b']")
    __OPERATION_SELECT = (By.CSS_SELECTOR, "select[ng-model='operation']")
    __RESULT = (By.CSS_SELECTOR, "b.result")

    __INCREMENT_FIRST = (
        By.XPATH,
        "//input[@ng-model='a']/ancestor::tr//button[normalize-space()='+1']",
    )
    __DECREMENT_FIRST = (
        By.XPATH,
        "//input[@ng-model='a']/ancestor::tr//button[normalize-space()='-1']",
    )
    __INCREMENT_SECOND = (
        By.XPATH,
        "//input[@ng-model='b']/ancestor::tr//button[normalize-space()='+1']",
    )
    __DECREMENT_SECOND = (
        By.XPATH,
        "//input[@ng-model='b']/ancestor::tr//button[normalize-space()='-1']",
    )

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.__driver = driver
        self.__timeout = timeout
        self.__wait = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------------
    # Навигация
    # ------------------------------------------------------------------
    def open(self):
        """Открывает страницу калькулятора и ждёт появления результата."""
        self.__driver.get(self.URL)
        self.__wait.until(EC.presence_of_element_located(self.__RESULT))
        return self

    # ------------------------------------------------------------------
    # Действия пользователя
    # ------------------------------------------------------------------
    def enter_first_number(self, value):
        """Вводит значение в поле первого числа."""
        self.__replace_value(self.__FIRST_NUMBER, value)
        return self

    def enter_second_number(self, value):
        """Вводит значение в поле второго числа."""
        self.__replace_value(self.__SECOND_NUMBER, value)
        return self

    def select_operation(self, operation):
        """Выбирает арифметическую операцию в выпадающем списке."""
        if operation not in self.OPERATIONS:
            raise ValueError(f"Неподдерживаемая операция: {operation!r}")
        Select(self.__find(self.__OPERATION_SELECT)).select_by_value(operation)
        return self

    def click_increment_first(self):
        """Нажимает кнопку '+1' рядом с первым числом."""
        self.__find(self.__INCREMENT_FIRST).click()
        return self

    def click_decrement_first(self):
        """Нажимает кнопку '-1' рядом с первым числом."""
        self.__find(self.__DECREMENT_FIRST).click()
        return self

    def click_increment_second(self):
        """Нажимает кнопку '+1' рядом со вторым числом."""
        self.__find(self.__INCREMENT_SECOND).click()
        return self

    def click_decrement_second(self):
        """Нажимает кнопку '-1' рядом со вторым числом."""
        self.__find(self.__DECREMENT_SECOND).click()
        return self

    # ------------------------------------------------------------------
    # Чтение состояния страницы
    # ------------------------------------------------------------------
    def get_first_number(self):
        """Возвращает текущее значение поля первого числа."""
        return self.__find(self.__FIRST_NUMBER).get_attribute("value")

    def get_second_number(self):
        """Возвращает текущее значение поля второго числа."""
        return self.__find(self.__SECOND_NUMBER).get_attribute("value")

    def get_selected_operation(self):
        """Возвращает выбранную сейчас операцию."""
        select = Select(self.__find(self.__OPERATION_SELECT))
        return select.first_selected_option.get_attribute("value")

    def get_available_operations(self):
        """Возвращает список операций, реально доступных в выпадающем списке."""
        select = Select(self.__find(self.__OPERATION_SELECT))
        return [option.get_attribute("value") for option in select.options]

    def get_expression(self):
        """Возвращает всю строку с примером и результатом, например '7 + 2 = 9'."""
        return self.__find(self.__RESULT).text.strip()

    def get_result(self):
        """Возвращает только результат вычисления (часть строки после '=')."""
        expression = self.get_expression()
        if "=" not in expression:
            return ""
        return expression.rsplit("=", 1)[-1].strip()

    # ------------------------------------------------------------------
    # Составные сценарии
    # ------------------------------------------------------------------
    def reset(self):
        """Возвращает калькулятор в исходное состояние без перезагрузки."""
        self.enter_first_number(0)
        self.enter_second_number(0)
        self.select_operation("+")
        self.wait_for_result("0")
        return self

    def calculate(self, first, second, operation, expected=None, timeout=None):
        """Вводит операнды, выбирает операцию и возвращает результат.

        Если передан ``expected``, метод дожидается именно этого значения
        (защита от гонки с пересчётом AngularJS), иначе возвращает текущий.
        """
        self.enter_first_number(first)
        self.enter_second_number(second)
        self.select_operation(operation)
        if expected is not None:
            self.wait_for_result(expected, timeout=timeout)
        return self.get_result()

    def wait_for_result(self, expected, timeout=None):
        """Ждёт, пока результат на странице станет равен ожидаемому."""
        wait = WebDriverWait(self.__driver, timeout or self.__timeout)
        wait.until(lambda _: self.get_result() == str(expected))
        return self

    # ------------------------------------------------------------------
    # Внутренние помощники
    # ------------------------------------------------------------------
    def __find(self, locator):
        return self.__wait.until(EC.presence_of_element_located(locator))

    def __replace_value(self, locator, value):
        element = self.__find(locator)
        element.clear()
        element.send_keys(str(value))
