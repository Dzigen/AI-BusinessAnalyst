from enum import Enum
from dataclasses import dataclass, field
from typing import List

class ReturnStatus(Enum):
    success = 0
    empty_input_text = 1
    bad_formater = 2
    bad_parser = 3
    bad_postprocessor = 4
    not_supported_lang = 5
    unknown_lang = 6
    empty_answer = 7
    bad_user_prompt_maping = 8

STATUS_MESSAGE = {
    ReturnStatus.success: "Операция выполнена успешно.",
    ReturnStatus.empty_input_text: "Пустая входная строка",
    # agent solver
    ReturnStatus.bad_formater: "Не удалось вставить кастомную информацию в user-prompt.",
    ReturnStatus.bad_parser: "Не удалось разобрать ответ LLM-агента.",
    ReturnStatus.bad_postprocessor: "Не удалось привести разобранный ответ LLM-агента к заданному формату.",
    ReturnStatus.bad_user_prompt_maping: "Не удалось вставить кастомную информацию в user-prompt.",
    # detect language
    ReturnStatus.not_supported_lang: "Данный язык не поддерживается.",
    ReturnStatus.unknown_lang: "Не удалось распознать язык входного текста.",
    # qa-pipeline (answer generation)
    ReturnStatus.empty_answer: 'Не удалось получить ответ на вопрос.'
}

@dataclass
class ReturnInfo:
    """Класс предназначен для хранения пояснительной информации к полученному результату в рамках
    некоторой операции.

    :param occurred_warning: Предупреждения, которые возникли в процессе выполнения операции.
    :type occurred_warning: List[ReturnStatus]
    :param status: Статус завершения операции.
    :type status: ReturnStatus
    :param  message: Пояснительное сообщение к статусу возврата.
    :type  message: str
    """
    occurred_warning: List[ReturnStatus] = field(default_factory=lambda: list())
    status: ReturnStatus = ReturnStatus.success
    message: str = ""