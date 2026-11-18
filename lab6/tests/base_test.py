"""Базовый класс UI-тестов: создание и закрытие браузера на каждый тест."""

import os
import shutil
import unittest

from selenium import webdriver

# Имена бинарников Chrome/Chromium, которые ищем в PATH.
_CHROME_CANDIDATES = (
    "google-chrome-stable",
    "google-chrome",
    "chromium",
    "chromium-browser",
    "chrome",
)

# Типовые пути установки, если браузера нет в PATH.
_CHROME_FALLBACK_PATHS = (
    "/opt/google/chrome/chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/lib/chromium/chromium",
)


def detect_chrome_binary():
    """Возвращает путь к браузеру: CHROME_BINARY, PATH или типовой путь."""
    explicit_path = os.getenv("CHROME_BINARY")
    if explicit_path:
        return explicit_path

    for name in _CHROME_CANDIDATES:
        found = shutil.which(name)
        if found:
            return found

    for path in _CHROME_FALLBACK_PATHS:
        if os.path.exists(path):
            return path

    return None


def create_driver():
    """Создаёт новый экземпляр Chrome WebDriver.

    Переменные окружения:
        CHROME_BINARY — путь к бинарнику браузера;
        HEADLESS=0    — запустить браузер с окном (по умолчанию headless).
    """
    options = webdriver.ChromeOptions()

    if os.getenv("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1440,1000")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Ускорение запуска: не тратим время на фоновые сервисы Chrome.
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-sync")
    options.add_argument("--no-first-run")
    options.add_argument("--mute-audio")

    # Не ждём полной загрузки всех ресурсов: готовность страницы
    # дополнительно проверяется через WebDriverWait в Page Object.
    options.page_load_strategy = "eager"

    binary_path = detect_chrome_binary()
    if binary_path:
        options.binary_location = binary_path

    # Selenium Manager сам подберёт и скачает подходящий chromedriver.
    return webdriver.Chrome(options=options)


class BaseUITest(unittest.TestCase):
    """Общая инициализация: один браузер на класс, чистая страница на тест.

    Браузер поднимается в setUpClass() и закрывается в tearDownClass(),
    а перед каждым тестом страница открывается заново — тесты не влияют
    друг на друга и могут запускаться по отдельности.
    """

    page_class = None

    @classmethod
    def setUpClass(cls):
        cls.driver = create_driver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        if self.page_class is None:
            self.fail("В тестовом классе не задан page_class")
        self.driver.delete_all_cookies()
        self.page = self.page_class(self.driver).open()
