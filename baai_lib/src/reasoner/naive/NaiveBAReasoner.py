from dataclasses import dataclass, field
from typing import Union, Dict
import gc

from .utils import NaiveReasonerState, NaiveReasonerStatus
from ..utils import BaseBAReasonerConfig, AbstractBAReasoner
from ...utils import Logger
from ...db_drivers.kv_driver import KeyValueDriverConfig
from ...specification_model import ReqSpecificationModel

from .init_communicator import InitCommunicator, InitCommunicatorConfig
from .task_clarifier import TaskClarifier, TaskClarifierConfig
from .user_stories_extractor import UserStoriesExtractor, UserStoriesExtractorConfig
from .scenarios_clarifier import ScenariosClarifier, ScenariosClarifierConfig
from .roles_extractor import RolesExtractor, RolesExtractorConfig
from .funcreqs_extractor import FuncRequirementsExtractor, FuncRequirementsExtractorConfig
from .nonfuncreqs_extractor import NonFuncRequirementsExtractor, NonFuncRequirementsExtractorConfig

from ..utils import UserResponse, BAResponse, DialogueHistory

NAIVEBAREASONER_MAIN_LOG_PATH = 'log/reasoner/naive/main'

@dataclass
class NaiveBAReasonerConfig(BaseBAReasonerConfig):
    init_communicator_config: InitCommunicatorConfig = field(default_factory=lambda: InitCommunicatorConfig())
    task_clarifier_config: TaskClarifierConfig = field(default_factory=lambda: TaskClarifierConfig())

    user_stories_extractor_config: UserStoriesExtractorConfig = field(default_factory=lambda: UserStoriesExtractorConfig())
    scenarios_clarifier_config: ScenariosClarifierConfig = field(default_factory=lambda: ScenariosClarifierConfig())
    roles_extractor_config: RolesExtractorConfig = field(default_factory=lambda: RolesExtractorConfig())
    
    #sysreqs_extractor_config: SysRequirementsExtractorConfig = field(default_factory=lambda: SysRequirementsEsxtractorConfig())
    #sysrestr_extractor_config: SysRestrictionsClarifierConfig = field(default_factory=lambda: SysRestrictionsClarifierConfig())
    
    funcreqs_extractor_config: FuncRequirementsExtractorConfig = field(default_factory=lambda: FuncRequirementsExtractorConfig())
    non_funcreqs_extractor_config: NonFuncRequirementsExtractorConfig = field(default_factory=lambda: NonFuncRequirementsExtractorConfig())

    mode: str = 'stub' # 'stub' | 'dev'
    
    log: Logger = field(default_factory=lambda: Logger(NAIVEBAREASONER_MAIN_LOG_PATH))
    verbose: bool = False

class NaiveBAReasoner(AbstractBAReasoner):
    
    def __init__(self, reqspec_model: ReqSpecificationModel, config: NaiveBAReasonerConfig = NaiveBAReasonerConfig(), 
                 cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.cache_kvdriver_config = cache_kvdriver_config
        self.fluent_dialogue_history = DialogueHistory()
        self.init_interaction_pipeline(reqspec_model)

    def change_mode_to(self, new_mode: str = 'stub') -> None:
        self.config.mode = new_mode
        for module_name in self.MODULES_EXECUTION_SEQUENCE[1:-1]:
            self.MODULES_MAP[module_name].mode = self.config.mode

    def get_state_description(state: NaiveReasonerState):
        # TODO
        pass

    def init_interaction_pipeline(self, reqspec_model: ReqSpecificationModel):
        del self.fluent_dialogue_history
        self.fluent_dialogue_history = DialogueHistory()
        self.reqspec_model = reqspec_model
        self.REASONER_STATUS = NaiveReasonerStatus.waiting_interaction 
        self.REASONER_STATE = NaiveReasonerState.init
        self.__REASONER_STATE_INDEX__ = 0

        self.MODULES_MAP = {
            NaiveReasonerState.init: InitCommunicator(self.config.init_communicator_config, self.config.mode, self.cache_kvdriver_config),
            NaiveReasonerState.task_clarifying: TaskClarifier(self.fluent_dialogue_history, self.config.task_clarifier_config, self.config.mode, self.cache_kvdriver_config),
            NaiveReasonerState.user_stories_extracting: UserStoriesExtractor(
                self.fluent_dialogue_history, self.reqspec_model, self.config.user_stories_extractor_config, self.config.mode, self.cache_kvdriver_config),
            NaiveReasonerState.scenarios_clarifying: ScenariosClarifier(
                self.reqspec_model, self.config.scenarios_clarifier_config, self.config.mode, self.cache_kvdriver_config),
            NaiveReasonerState.roles_extracting: RolesExtractor(
                self.reqspec_model, self.config.roles_extractor_config, self.config.mode, self.cache_kvdriver_config),
            NaiveReasonerState.funcreqs_extracting: FuncRequirementsExtractor(
                self.fluent_dialogue_history, self.reqspec_model, self.config.funcreqs_extractor_config, self.config.mode, self.cache_kvdriver_config),
            NaiveReasonerState.nonfuncreqs_extracting: NonFuncRequirementsExtractor(
                self.fluent_dialogue_history, self.reqspec_model, self.config.non_funcreqs_extractor_config, self.config.mode, self.cache_kvdriver_config),
            NaiveReasonerState.done: None
        }

        self.MODULES_EXECUTION_SEQUENCE = [
            NaiveReasonerState.init, NaiveReasonerState.task_clarifying, NaiveReasonerState.user_stories_extracting, 
            NaiveReasonerState.scenarios_clarifying, NaiveReasonerState.roles_extracting, NaiveReasonerState.funcreqs_extracting,
            NaiveReasonerState.nonfuncreqs_extracting, NaiveReasonerState.done]
    
        for module_name in self.MODULES_EXECUTION_SEQUENCE[:-1]:
            self.MODULES_MAP[module_name].init_module_state()

        gc.collect()

    def change_state(self, direction: str = 'forward') -> None:
        if direction == 'forward':
            self.__REASONER_STATE_INDEX__ += 1
        else:
            raise ValueError
        
        self.REASONER_STATE = self.MODULES_EXECUTION_SEQUENCE[self.__REASONER_STATE_INDEX__]

    def prepare_response(self) -> BAResponse:
        if self.REASONER_STATUS == NaiveReasonerStatus.waiting_interaction:
            self.REASONER_STATUS = NaiveReasonerStatus.processing
            response, new_rstatus = self.MODULES_MAP[self.REASONER_STATE].prepare_response()

            if new_rstatus == NaiveReasonerStatus.done:
                self.change_state(direction='forward')
                if self.REASONER_STATE == NaiveReasonerState.done:
                    self.REASONER_STATUS = NaiveReasonerStatus.done
                else:
                    self.REASONER_STATUS = NaiveReasonerStatus.waiting_interaction
            else:
                self.REASONER_STATUS = new_rstatus
        else:
            raise AttributeError

        return response

    def process_response(self, user_response: UserResponse) -> None:
        if self.REASONER_STATUS == NaiveReasonerStatus.waiting_response:
            self.REASONER_STATUS = NaiveReasonerStatus.processing
            new_rstatus = self.MODULES_MAP[self.REASONER_STATE].process_response(user_response)

            if new_rstatus == NaiveReasonerStatus.done:
                self.change_state(direction='forward')
                if self.REASONER_STATE == NaiveReasonerState.done:
                    self.REASONER_STATUS = NaiveReasonerStatus.done
                else:
                    self.REASONER_STATUS = NaiveReasonerStatus.waiting_interaction
            else:
                self.REASONER_STATUS = new_rstatus
        else:
            raise AttributeError

    def get_task_description(self, format: str = 'markdown') -> Union[Dict[str,Union[Dict[str,str], str]],str]:
        formated_description = None
        if format == 'markdown':
            scenarios_subsection = "\n## Функциональная модель\n\n{scenarios}"
            formated_scenarios = '\n\n'.join(list(map(lambda item: f"Сценарий {item.id}\n{item.statement}", self.reqspec_model.specification_struct.scenarios.values())))
            merged_scenarios = scenarios_subsection.format(scenarios=formated_scenarios)

            roles_subsection = "\n## Модели пользователей системы\n{roles}"
            formated_roles = "\nВиды пользователей:\n\n" + '\n'.join(list(map(lambda item: f"* {item.name}", self.reqspec_model.specification_struct.roles.values())))
            merged_roles = roles_subsection.format(roles=formated_roles)

            funcreq_subsection = "\n## Функциональные требования\n\n{funcreq}"
            formated_funcreq = '\n'.join(list(map(lambda item: f"* {item.statement} (ФТ{item.id})", self.reqspec_model.specification_struct.reqs_info.functional.values())))
            merged_funcreq = funcreq_subsection.format(funcreq=formated_funcreq)

            nonfuncreq_subsection = "\n## Ограничения\n\n{nonfuncreq}"
            formated_nonfuncreq = '\n'.join(list(map(lambda item: f"* {item.statement} (НФТ{item.id})", self.reqspec_model.specification_struct.reqs_info.non_functional.values())))
            merged_nonfuncreq = nonfuncreq_subsection.format(nonfuncreq=formated_nonfuncreq)

            formated_description = f"# Первичный список требований\n{merged_funcreq}\n{merged_nonfuncreq}\n\n# Модели требований\n{merged_roles}\n{merged_scenarios}"

        elif format == 'dict':
            # TODO
            raise NotImplementedError
        
        else:
            raise ValueError
        
        return formated_description

    def reset(self, reqspec_model: ReqSpecificationModel):
        self.init_interaction_pipeline(reqspec_model)

    