"""Класс-контроллер (п. e): сквозной сценарий бизнес-логики."""


class Controller:
    """Объединяет ввод -> БД/расчёт -> внешний сервис.

    Сценарий run():
    1. Запрашивает входные данные через user_interaction.
    2. Если записи в БД нет -> считает через calculator и добавляет в БД;
       если есть -> берёт результат из БД.
    3. Отправляет строку-результат через external_service.
    4. Возвращает результат.
    """

    def __init__(self, calculator, database, user_interaction, external_service):
        self.calculator = calculator
        self.database = database
        self.user_interaction = user_interaction
        self.external_service = external_service

    @staticmethod
    def _result_string(triangle_type: str, error_message) -> str:
        if error_message:
            if triangle_type:
                return f"{triangle_type}: {error_message}"
            return f"Ошибка: {error_message}"
        return triangle_type

    def run(self) -> str:
        side_a, side_b, side_c = self.user_interaction.get_sides()

        record = self.database.get_record(side_a, side_b, side_c)
        if record is not None:
            result = self._result_string(record["triangle_type"], record["error_message"])
        else:
            calc = self.calculator.calculate(side_a, side_b, side_c)
            self.database.add_record(
                side_a, side_b, side_c, calc["type"], calc["error"]
            )
            result = self._result_string(calc["type"], calc["error"])

        self.external_service.send_result(result)
        return result
