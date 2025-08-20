from dataclasses import dataclass
from ...utils import BaseWeakStagesState

class TaskGeneralCommunicatorState(BaseWeakStagesState):
    init: int = 0
    clarifying: int = 1
    task_classifying: int = 2
    info_extracting: int = 3
    done: int = 4

class TGCAskingState(BaseWeakStagesState):
    init: int = 0
    question_preparing: int = 1
    limit_exceeded: int = 2

class TGCTaskClassifyingState(BaseWeakStagesState):
    init: int = 0
    classifying: int = 1
    done: int = 2

class TGCInfoExtractingState(BaseWeakStagesState):
    init: int = 0
    goal_extr_notice: int = 1
    goal_extr_process: int = 2
    subt_extr_notice: int = 3
    subt_extr_process: int = 4
    integr_extr_notice: int = 5
    integr_extr_process: int = 6
    done: int = 7

@dataclass
class TGClarifierCurrentState:
    base_state: TaskGeneralCommunicatorState = TaskGeneralCommunicatorState.init
    askq_state: TGCAskingState = TGCAskingState.init
    tcls_state: TGCTaskClassifyingState = TGCTaskClassifyingState.init
    iextr_state: TGCInfoExtractingState = TGCInfoExtractingState.init