from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Union
from enum import Enum

class AbstractBAReasoner(ABC):

    @abstractmethod
    def prepare_response(self):
        pass

    @abstractmethod
    def process_response(self):
        pass
    
    @abstractmethod
    def reset(self):
        pass

@dataclass
class BaseBAReasonerConfig:
    pass


class BaseStateSignal(Enum):
    pass

class BaseGlobalSignal(Enum):
    pass

@dataclass
class SignalInfo:
    # привязываемый / указываемый сигнал
    signal: Union[BaseStateSignal, BaseGlobalSignal]
    # краткое пояснение назначения / обработчика по указанному сигналу (для кнопок)
    shortcut: str
    # расширенное пояснение назначения / обработчика по указанному сигналу (для пояснительных записок / справок)
    description: str = None

@dataclass
class UserResponse:
    user_text: str = None
    signal: Union[BaseStateSignal, BaseGlobalSignal, None] = None

@dataclass
class BAResponse:
    # Сообщение от бизнес-аналитика на естественном языке
    ba_text: Union[str, None] = None
    # Набор сигналов по навигации внутри стадии пайплайна / изменению модели ТЗ, который поддерживается / обрабатывается в рамках текущего сценария 
    # общения с пользователем
    available_state_signals: List[SignalInfo] = field(default_factory=lambda: list())
    # Набор сигналов по навигации между стадиями пайплайна, который поддерживатеся / обрабатывается 
    # в рамках текущего сценария общения с пользователем
    available_global_signals: List[SignalInfo] = field(default_factory=lambda: list())
    # Информация, которая вставляется в текстовое поле диалогового окна в качестве базового ответа пользователя
    user_base_answer: Union[str, None] = None
    # Если True, то поле для пользовательского ввода информации заблокировано, иначе False
    is_userinput_locked: bool = False


@dataclass
class Response:
    role: str
    text: str
    signal: Union[BaseStateSignal, BaseGlobalSignal, None] = None


@dataclass
class DialogueHistory:
    sequence: List[Response] = field(default_factory=lambda: list())
