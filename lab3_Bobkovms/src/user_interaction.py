"""Класс взаимодействия с пользователем (п. c): ABC-интерфейс + консоль."""

from abc import ABC, abstractmethod


class UserInteraction(ABC):
    """Интерфейс получения входных данных от пользователя."""

    @abstractmethod
    def get_sides(self):
        """Возвращает тройку строк (длина1, длина2, длина3)."""
        raise NotImplementedError


class ConsoleUserInteraction(UserInteraction):
    """Консольная реализация через input()."""

    def get_sides(self):
        side_a = input("Введите длину стороны A: ").strip()
        side_b = input("Введите длину стороны B: ").strip()
        side_c = input("Введите длину стороны C: ").strip()
        return (side_a, side_b, side_c)
