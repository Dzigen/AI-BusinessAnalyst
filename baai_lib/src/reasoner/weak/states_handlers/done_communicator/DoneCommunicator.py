from dataclasses import dataclass, field
from typing import Tuple, Union
from copy import deepcopy
import gc

from .config import DCOMMUNICATOR_MAIN_LOG_PATH, BADC_RESPONSE_CONFIG
from .utils import DCommCurrentState
from ...utils import AbstractWeakModule, WeakReasonerStatus, WeakReasonerState
from ....utils import BAResponse, UserResponse
from .....utils import Logger
from .....specification_model import ReqSpecificationModel

@dataclass
class DoneCommunicatorConfig:
    log: Logger = field(default_factory=lambda: Logger(DCOMMUNICATOR_MAIN_LOG_PATH))
    verbose: bool = False

class DoneCommunicator(AbstractWeakModule):
    def __init__(self, reqspec_model: ReqSpecificationModel, config: DoneCommunicatorConfig = DoneCommunicatorConfig(), 
                 mode: str = 'prod'):
        self.config = config
        self.mode = mode
        self.reqspec_mode = reqspec_model

        self.init_state()

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.STATE = DCommCurrentState()

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None, WeakReasonerState]]:
        ba_response = deepcopy(BADC_RESPONSE_CONFIG[self.STATE.base_state].ba_response)
        reasoner_newstatus = BADC_RESPONSE_CONFIG[self.STATE.base_state].reasoner_newstatus
        done_state = BADC_RESPONSE_CONFIG[self.STATE.base_state].reasoner_donestate
        self.STATE = deepcopy(BADC_RESPONSE_CONFIG[self.STATE.base_state].stage_newstate)
            
        return ba_response, reasoner_newstatus, done_state
        
    def process_response(self, user_response: UserResponse) -> None:
        raise NotImplementedError
    
    def reset(self):
        self.init_state()
        gc.collect()