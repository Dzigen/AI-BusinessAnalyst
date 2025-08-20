from dataclasses import dataclass, field
from typing import Tuple, Union
from copy import deepcopy
import gc

from .config import ICOMMUNICATOR_MAIN_LOG_PATH, BAIC_RESPONSE_CONFIG
from .utils import ICommCurrentState
from ...utils import AbstractWeakModule, WeakReasonerStatus, WeakReasonerState
from ....utils import BAResponse, UserResponse
from .....utils import Logger

@dataclass
class InitCommunicatorConfig:
    log: Logger = field(default_factory=lambda: Logger(ICOMMUNICATOR_MAIN_LOG_PATH))
    verbose: bool = False

class InitCommunicator(AbstractWeakModule):
    def __init__(self, config: InitCommunicatorConfig = InitCommunicatorConfig()):
        self.config = config

        self.init_state()

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.STATE = ICommCurrentState()

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None, WeakReasonerState]]:
        ba_response = deepcopy(BAIC_RESPONSE_CONFIG[self.STATE.base_state].ba_response)
        reasoner_newstatus = BAIC_RESPONSE_CONFIG[self.STATE.base_state].reasoner_newstatus
        self.STATE = deepcopy(BAIC_RESPONSE_CONFIG[self.STATE.base_state].stage_newstate)
        done_state = None
        
        return ba_response, reasoner_newstatus, done_state
        
    def process_response(self, user_response: UserResponse) -> None:
        raise NotImplementedError
    
    def reset(self):
        self.init_state()
        gc.collect()