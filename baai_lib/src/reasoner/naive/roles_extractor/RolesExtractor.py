from dataclasses import dataclass, field
from typing import Tuple

from ....utils import Logger, AgentTaskSolverConfig, AgentTaskSolver, ReturnStatus
from ....db_drivers.kv_driver import KeyValueDriverConfig
from ....specification_model import ReqSpecificationModel
from ....specification_model.utils import Role
from ....agents import AgentDriver, AgentDriverConfig
from ..utils import AbstractNaiveModule, NaiveReasonerStatus
from ...utils import BAResponse, UserResponse
from .config import BA_ROLES_EXTRACTING_NOTICE, DEFAULT_CRG_TASK_CONFIG, BA_EXTRACTED_ROLES_NOTICE
from .utils import RolesExtractorState

REXTRACTOR_MAIN_LOG_PATH = 'log/reasoner/naive/r_extractor/main'

@dataclass
class RolesExtractorConfig:
    lang: str = "ru"
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    condrgen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_CRG_TASK_CONFIG)

    log: Logger = field(default_factory=lambda: Logger(REXTRACTOR_MAIN_LOG_PATH))
    verbose: bool = False

class RolesExtractor(AbstractNaiveModule):
    def __init__(self, reqspec_model: ReqSpecificationModel, config: RolesExtractorConfig = RolesExtractorConfig(),
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.mode = mode

        self.init_module_state()

        self.agent = AgentDriver.connect(config.adriver_config)
        self.condrgen_solver = AgentTaskSolver(
            self.agent, self.config.condrgen_task_config, cache_kvdriver_config)
        
        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_module_state(self):
        self.state = RolesExtractorState.greetings

    def prepare_response(self) -> Tuple[BAResponse, NaiveReasonerStatus]:
        ba_response, new_status = None, None
        if self.state == RolesExtractorState.greetings:
            ba_response = BAResponse(ba_text=BA_ROLES_EXTRACTING_NOTICE)
            new_status = NaiveReasonerStatus.waiting_interaction
            self.state = RolesExtractorState.extracting

        elif self.state == RolesExtractorState.extracting:
            unique_roles = set()
            for user_story in self.reqspec_model.specification_struct.user_stories.values():
                if self.mode == 'prod':
                    roles, status = self.condrgen_solver.solve(
                        lang=self.config.lang, user_story=user_story.statement)
                    if status != ReturnStatus.success:
                        # TODO: Предложить обработчик ошибки парсинга ответа LLM
                        raise ValueError
                elif self.mode == 'stub':
                    roles = ['Роль #1', 'Роль #2']
                else:
                    raise ValueError

                unique_roles.update(roles)

            self.reqspec_model.specification_struct.edit_count += 1
            for i, role in enumerate(list(unique_roles)):
                self.reqspec_model.specification_struct.roles[str(i)] = Role(id=str(i), name=role)
            
            ba_response = BAResponse(ba_text=BA_EXTRACTED_ROLES_NOTICE.format(extracted_r_amount=len(unique_roles)))
            new_status = NaiveReasonerStatus.done
            self.state = RolesExtractorState.done
        else:
            raise ValueError
        
        return ba_response, new_status

    def process_response(self, user_response: UserResponse) -> NaiveReasonerStatus:
        raise NotImplementedError
    
    def reset(self):
        self.init_module_state()