"""Класс сторонней зависимости (п. d): ABC-интерфейс + имитация отправки."""

from abc import ABC, abstractmethod


class ExternalService(ABC):
    """Интерфейс передачи данных стороннему процессу."""

    @abstractmethod
    def send_result(self, result: str) -> bool:
        """Имитирует отправку строки-результата. Возвращает True при успехе."""
        raise NotImplementedError


class EmailServiceSimulator(ExternalService):
    """Имитация отправки результата на внешний email-сервер."""

    def __init__(self):
        self.sent = []

    def send_result(self, result: str) -> bool:
        # Только имитация передачи данных, без реальной сети.
        self.sent.append(result)
        print(f"[EmailService] Отправлен результат: {result}")
        return True
