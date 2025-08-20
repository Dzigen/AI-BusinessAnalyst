from abc import ABC, abstractmethod
from enum import Enum
from ..utils import BaseStateSignal, BaseGlobalSignal

class AbstractNaiveModule(ABC):

    @abstractmethod
    def prepare_response(self):
        pass

    @abstractmethod
    def process_response(self):
        pass
    
    @abstractmethod
    def reset(self):
        pass


class NaiveReasonerState(Enum):
    init: int = 0
    task_clarifying: int = 1

    user_stories_extracting: int = 2
    scenarios_clarifying: int = 3
    roles_extracting: int = 4
    
    sysreqs_extracting: int = 5
    sysrestr_clarifying: int = 6

    funcreqs_extracting: int = 7
    nonfuncreqs_extracting: int = 8

    done: int = 9

class NaiveReasonerStatus(Enum):
    waiting_interaction: int = 0
    processing: int = 1
    waiting_response: int = 2
    done: int = 3

class NaiveStateSignal(BaseStateSignal):
    continue_operation: int = 'cnt_opt'

class NaiveGlobalSignal(BaseGlobalSignal):
    next_stage: int = 'brk_opt'