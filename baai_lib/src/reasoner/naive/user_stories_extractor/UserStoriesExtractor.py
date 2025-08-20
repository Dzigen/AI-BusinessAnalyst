from dataclasses import dataclass, field
from typing import Tuple

from ....utils import Logger, AgentTaskSolverConfig, AgentTaskSolver, ReturnStatus
from ....agents import AgentDriver, AgentDriverConfig
from ....db_drivers.kv_driver import KeyValueDriverConfig
from ....specification_model import ReqSpecificationModel
from ....specification_model.utils import UserStory
from ..utils import AbstractNaiveModule, NaiveReasonerStatus
from ...utils import BAResponse, UserResponse, DialogueHistory
from .config import BA_USERSTORIES_SEARCH_NOTICE, DEFAULT_CUSG_TASK_CONFIG, BA_EXTRACTED_USERSTORIES_NOTICE
from .utils import UserStoriesExtractorState

USEXTRACOR_MAIN_LOG_PATH = 'log/reasoner/naive/us_extractor/main'

@dataclass
class UserStoriesExtractorConfig:
    lang: str = "ru"
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    condusgen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_CUSG_TASK_CONFIG)

    log: Logger = field(default_factory=lambda: Logger(USEXTRACOR_MAIN_LOG_PATH))
    verbose: bool = False

class UserStoriesExtractor(AbstractNaiveModule):
    def __init__(self, dialogue_history: DialogueHistory, reqspec_model: ReqSpecificationModel, 
                 config: UserStoriesExtractorConfig = UserStoriesExtractorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.dialogue_history = dialogue_history
        self.reqspec_model = reqspec_model
        self.mode = mode

        self.init_module_state()

        self.agent = AgentDriver.connect(config.adriver_config)
        self.condusgen_solver = AgentTaskSolver(
            self.agent, self.config.condusgen_task_config, cache_kvdriver_config)
        
        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_module_state(self):
        self.state = UserStoriesExtractorState.greetings

    def prepare_response(self) -> Tuple[BAResponse, NaiveReasonerStatus]:
        ba_response, new_status = None, None
        if self.state == UserStoriesExtractorState.greetings:
            ba_response = BAResponse(ba_text=BA_USERSTORIES_SEARCH_NOTICE)
            new_status = NaiveReasonerStatus.waiting_interaction
            self.state = UserStoriesExtractorState.extracting

        elif self.state == UserStoriesExtractorState.extracting:
            if self.mode == 'prod':
                user_stories, status = self.condusgen_solver.solve(lang=self.config.lang, dialogue_history=self.dialogue_history)
                if status != ReturnStatus.success:
                    # TODO: Предложить обработчик ошибки парсинга ответа LLM
                    raise ValueError
            elif self.mode == 'stub':
                user_stories = ["Пример user-истории #1", "Пример user-истории #2"]
            else:
                raise ValueError

            self.reqspec_model.specification_struct.edit_count += 1
            max_us_id = len(self.reqspec_model.specification_struct.user_stories)
            for user_story in user_stories:
                self.reqspec_model.specification_struct.user_stories[str(max_us_id)] = \
                    UserStory(id=str(max_us_id), statement=user_story)
                max_us_id += 1

            ba_response = BAResponse(ba_text=BA_EXTRACTED_USERSTORIES_NOTICE.format(extracted_us_amount=len(user_stories)))
            self.state = UserStoriesExtractorState.done
            new_status = NaiveReasonerStatus.done
        
        else:
            raise ValueError
        
        return ba_response, new_status

    def process_response(self, user_response: UserResponse) -> NaiveReasonerStatus:
        raise NotImplementedError
    
    def reset(self):
        self.init_module_state()