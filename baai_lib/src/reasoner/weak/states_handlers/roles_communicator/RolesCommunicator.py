from dataclasses import dataclass, field
from typing import Tuple, Union
from copy import deepcopy
import gc

from .config import RCOMMUNICATOR_MAIN_LOG_PATH, BARE_RESPONSE_CONFIG 
from .utils import RExtractorCurrentState, RExtractorState
from ...utils import AbstractWeakModule, UserResponse, BAResponse, \
    WeakReasonerState, WeakReasonerStatus
from .llm_pipelines import RolesExtractor, RolesExtractorConfig
from .....specification_model import ReqSpecificationModel
from .....specification_model.utils import Role
from .....db_drivers.kv_driver import KeyValueDriverConfig
from .....utils import Logger

@dataclass
class RolesCommunicatorConfig:
    """Конфигурация RolesExtractorCommunicator-стадии в рамках WeakBAReasoner-стратегии общения с пользователем по формированию технического задания.
    
    :param roles_extractor_config: Конфигурация LLM-пайплайна по извлечению ролей из пользовательских историй.
    :type roles_extractor_config: RolesExtractorConfig
    :param log: Отладочный класс для журналирования/мониторинга поведения инициализируемой компоненты. Значение по умолчанию Logger(TCLARIFIER_MAIN_LOG_PATH).
    :type log: Logger
    :param verbose: Если True, то информация о поведении класса будет сохраняться в stdout и файл-журналирования (log), иначе только в файл. Значение по умолчанию False.
    :type verbose: bool
    """

    roles_extractor_config: RolesExtractorConfig = field(default_factory=lambda: RolesExtractorConfig())

    log: Logger = field(default_factory=lambda: Logger(RCOMMUNICATOR_MAIN_LOG_PATH))
    verbose: bool = False

class RolesCommunicator(AbstractWeakModule):
    """Класс реализует сценарий общения с пользователем в рамках стадии по извлечению ролей из согласованных пользовательских историй.
    """

    def __init__(self, reqspec_model: ReqSpecificationModel, config: RolesCommunicatorConfig = RolesCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.cache_kvdriver_config = cache_kvdriver_config
        self.mode = mode

        self.roles_extractor = RolesExtractor(self.config.roles_extractor_config, cache_kvdriver_config)

        self.init_state()

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.STATE = RExtractorCurrentState()

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None,WeakReasonerState]]:
        tmp_state_response = deepcopy(BARE_RESPONSE_CONFIG [self.STATE.base_state])
        done_state = None

        if self.STATE.base_state == RExtractorState.extracting_result:
            extracted_roles = None
            if self.mode == 'stub':
                 extracted_roles = [Role(id='1', name='Роль #1'), Role(id='2', name='Роль #2')]
            elif self.mode == 'prod':
                task_goal = self.reqspec_model.specification_struct.general.goal
                user_stories = list(self.reqspec_model.specification_struct.user_stories.values())
                extracted_roles = self.roles_extractor.extract(task_goal, user_stories)
            else:
                raise ValueError

            self.reqspec_model.specification_struct.roles = {role.id: role for role in extracted_roles}
            roles_amount = len(self.reqspec_model.specification_struct.roles)
            tmp_state_response.ba_response.ba_text = tmp_state_response.ba_response.ba_text.format(r_amount=roles_amount)

        ba_response = tmp_state_response.ba_response
        reasoner_newstatus = tmp_state_response.reasoner_newstatus
        self.STATE = tmp_state_response.stage_newstate
        
        return ba_response, reasoner_newstatus, done_state

    def process_response(self, user_response: UserResponse) -> None:
        raise NotImplementedError
    
    def reset(self):
        self.init_state()
        gc.collect()