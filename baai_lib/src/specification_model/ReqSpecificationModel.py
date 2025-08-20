from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, List
import gc

from .utils import SpecificationInfo
from ..reasoner.utils import DialogueHistory
from ..reasoner.weak.utils import WeakReasonerState

@dataclass
class ReqSpecificationModelConfig:
    pass

class ReqSpecificationModel:
    """Модель формируемого технического задания
    """

    def __init__(self, config: ReqSpecificationModelConfig = ReqSpecificationModelConfig()):
        self.config = config
        self.init_rsmodel()

    def init_rsmodel(self):
        self.specification_struct = SpecificationInfo()
        self.states_full_history = dict()

        self.states_valuable_history = dict()
        self.states_valuable_history[WeakReasonerState.task_clarifying] = {'general_qa': DialogueHistory()}
        self.states_valuable_history[WeakReasonerState.bp_clarifying] = {'detailed_qa': DialogueHistory()}
        self.states_valuable_history[WeakReasonerState.scenarios_ccrud] = {'declined_scenarios': defaultdict(list)}
        self.states_valuable_history[WeakReasonerState.sysrestr_ccrud] = {'declined_srestrs': defaultdict(list)}
        self.states_valuable_history[WeakReasonerState.funcrestr_ccrud] = {'declined_frestrs': defaultdict(list)}

    def clear(self) -> None:
        del self.specification_struct
        del self.states_full_history
        del self.states_valuable_history

        self.init_rsmodel()
        gc.collect()

