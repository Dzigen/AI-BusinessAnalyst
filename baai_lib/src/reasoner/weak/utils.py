from typing import Tuple, Union, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from ..utils import BaseStateSignal, BaseGlobalSignal, BAResponse, UserResponse

class WeakReasonerState(Enum):
    # Приветствие
    init: int = 0
    # Общение по фиксированному количеству общих вопросов
    task_clarifying: int = 1
    # Уточнение деталей / предложение новых бизнес процессов
    bp_clarifying: int = 2
    # Изменение user-историй
    userstories_crud: int = 3
    # Извлечение ролей
    roles_extracting: int = 4
    # Уточнение / изменение сценариев
    scenarios_ccrud: int = 5
    # Извлечение функциональных требований
    funcreq_extracting: int = 6
    # Уточнение / Изменение системных ограничений
    funcrestr_ccrud: int = 9
    # Уточнение / изменение системных требований
    sysreq_crud: int = 7
    # Уточнение / изменение системных ограничений
    sysrestr_ccrud: int = 8
    # Пайплайн завершился из-за неподдерживаемого типа ТЗ
    done_unsupported_task: int = 10
    # Успешное завершение работы пайплайна
    done: int = 11

class GeneralAddState(Enum):
    init: int = 0
    input_request: int = 1
    bad_input: int = 2
    cancel: int = 3
    success: int = 4
    done: int = 5

class GeneralDeleteState(Enum):
    init: int = 0
    select_request: int = 1
    bad_select: int = 2
    success: int = 3
    done: int = 4

class GeneralEditState(Enum):
    init: int = 0
    select_request: int = 1
    bad_select: int = 2
    editing: int = 3
    bad_input: int = 4
    success: int = 5
    done: int = 6

class GeneralRecommendState(Enum):
    init: int = 0
    recommend: int = 1
    chose: int = 2
    done: int = 3

class WeakReasonerStatus(Enum):
    waiting_interaction: int = 0
    processing: int = 1
    waiting_response: int = 2
    done: int = 3

class WeakStateSignal(BaseStateSignal):
    cancel_operation: int = 0
    return_item_operation: int = 1
    next_item_operation: int = 2
    prev_item_operation: int = 3

    approve: int = 4
    decline: int = 5
    
    add: int = 6
    delete: int = 7
    edit: int = 8

    recommend_new: int = 9

class WeakGlobalSignal(BaseGlobalSignal):
    # Перейти к следующей стадии по формированию ТЗ
    next_stage: int = 0


class AbstractWeakModule(ABC):

    @abstractmethod
    def init_state(self):
        pass

    @abstractmethod
    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None,WeakReasonerState]]:
        pass

    @abstractmethod
    def process_response(self, user_response: UserResponse) -> None:
        pass
    
    @abstractmethod
    def reset(self):
        pass

class BaseWeakStagesState(Enum):
    pass

@dataclass
class StateAction:
    ba_response: BAResponse
    reasoner_newstatus: WeakReasonerStatus
    stage_newstate: Dict[str, BaseWeakStagesState]
    reasoner_donestate: Union[None, WeakReasonerState] = None 