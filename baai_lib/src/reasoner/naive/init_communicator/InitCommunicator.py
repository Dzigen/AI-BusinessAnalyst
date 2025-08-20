from dataclasses import dataclass, field
from typing import Tuple

from ....utils import Logger
from ....db_drivers.kv_driver import KeyValueDriverConfig
from ..utils import AbstractNaiveModule, NaiveReasonerStatus
from ...utils import BAResponse, UserResponse
from .config import GREETINGS_BA_MESSAGE
from .utils import InitCommunicatorState

ICOMMUNICATOR_MAIN_LOG_PATH = 'log/reasoner/naive/i_communicator/main'

@dataclass
class InitCommunicatorConfig:
    log: Logger = field(default_factory=lambda: Logger(ICOMMUNICATOR_MAIN_LOG_PATH))
    verbose: bool = False

class InitCommunicator(AbstractNaiveModule):
    def __init__(self, config: InitCommunicatorConfig = InitCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.mode = mode

        self.init_module_state()

    def init_module_state(self):
        self.state = InitCommunicatorState.greetings

    def prepare_response(self) -> Tuple[BAResponse, NaiveReasonerStatus]:
        ba_response, new_state = None, None
        if self.state == InitCommunicatorState.greetings:
            ba_response = BAResponse(ba_text=GREETINGS_BA_MESSAGE)
            new_state = NaiveReasonerStatus.done
        
        else:
            raise AttributeError
        
        return ba_response, new_state
        
    def process_response(self, user_response: UserResponse) -> NaiveReasonerStatus:
        raise NotImplementedError
    
    def reset(self):
        self.init_module_state()