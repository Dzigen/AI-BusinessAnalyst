from dataclasses import dataclass, field
from typing import Tuple, Union
from copy import deepcopy
import gc

from .config import FREQEXTRACTOR_MAIN_LOG_PATH, BAFREQC_MESSAGE_TAMPLATES
from .utils import FRExtractorState, FRExtractorCurrentState
from .llm_pipelines import FuncReqExtractor, FuncReqExtractorConfig
from ...utils import AbstractWeakModule, UserResponse, BAResponse, WeakReasonerState, WeakReasonerStatus
from .....specification_model import ReqSpecificationModel
from .....specification_model.utils import FunctionalRequirement, FunctionalRequirementGroup
from .....db_drivers.kv_driver import KeyValueDriverConfig
from .....utils import Logger

@dataclass
class FuncRequirementsCommunicatorConfig:
    """Конфигурация FuncRequirementsCommunicator-стадии в рамках WeakBAReasoner-стратегии общения с пользователем по формированию технического задания.
    
    :param funcreq_extr_config: Конфигурация LLM-пайплайна по генерации функциональных требований к специфицируемому проекту.
    :type funcreq_extr_config: FuncReqExtractorConfig
    :param log: Отладочный класс для журналирования/мониторинга поведения инициализируемой компоненты. Значение по умолчанию Logger(TCLARIFIER_MAIN_LOG_PATH).
    :type log: Logger
    :param verbose: Если True, то информация о поведении класса будет сохраняться в stdout и файл-журналирования (log), иначе только в файл. Значение по умолчанию False.
    :type verbose: bool
    """
        
    funcreq_extr_config: FuncReqExtractorConfig = field(default_factory=lambda: FuncReqExtractorConfig())

    log: Logger = field(default_factory=lambda: Logger(FREQEXTRACTOR_MAIN_LOG_PATH))
    verbose: bool = False

class FuncRequirementsCommunicator(AbstractWeakModule):
    """Класс реализует сценарий общения с пользователем в рамках стадии по генерации функциональных требований.
    """

    def __init__(self, reqspec_model: ReqSpecificationModel, config: FuncRequirementsCommunicatorConfig = FuncRequirementsCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.cache_kvdriver_config = cache_kvdriver_config
        self.mode = mode

        self.freq_extractor = FuncReqExtractor(self.config.funcreq_extr_config, self.cache_kvdriver_config)

        self.init_state()

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.STATE = FRExtractorCurrentState()

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None,WeakReasonerState]]:
        tmp_state_response = deepcopy(BAFREQC_MESSAGE_TAMPLATES[self.STATE.base_state])
        done_state = None

        if self.STATE.base_state == FRExtractorState.extract_results:
            freq_groups, freqs = None, None
            if self.mode == 'stub':
                freqs = {
                    '1': FunctionalRequirement(id='1', statement="Функциональное требование 'Заглушка' #1"),
                    '2': FunctionalRequirement(id='2', statement="Функциональное требование 'Заглушка' #2"),
                    '3': FunctionalRequirement(id='3', statement="Функциональное требование 'Заглушка' #3"),
                    '4': FunctionalRequirement(id='4', statement="Функциональное требование 'Заглушка' #4"),
                    '5': FunctionalRequirement(id='5', statement="Функциональное требование 'Заглушка' #5"),
                    '6': FunctionalRequirement(id='6', statement="Функциональное требование 'Заглушка' #6"),
                    '7': FunctionalRequirement(id='7', statement="Функциональное требование 'Заглушка' #7")
                }
                freq_groups = {
                    '1': FunctionalRequirementGroup(id='1', title="Название группы #1", grouped_funcreq_ids=['1','3','5']),
                    '2': FunctionalRequirementGroup(id='2', title="Название группы #2", grouped_funcreq_ids=['2','4']),
                    '3': FunctionalRequirementGroup(id='3', title="Название группы #3", grouped_funcreq_ids=['6','7']),
                }

            elif self.mode == 'prod':
                task_goal = self.reqspec_model.specification_struct.general.goal
                user_stories = list(self.reqspec_model.specification_struct.user_stories.values())
                accepted_scenarios = dict()
                for us in user_stories:
                    accepted_scenarios[us.id] = [self.reqspec_model.specification_struct.scenarios[s_id] for s_id in us.related_scenario_ids]
                
                freq_groups, freqs = self.freq_extractor.extract(task_goal, user_stories, accepted_scenarios)

            else:
                raise ValueError
            
            self.reqspec_model.specification_struct.reqs_info.functional = freqs
            self.reqspec_model.specification_struct.reqs_info.fgroups = freq_groups

            ba_response = tmp_state_response.ba_response
            reasoner_newstatus = tmp_state_response.reasoner_newstatus
            self.STATE = tmp_state_response.stage_newstate

            freq_count = len(freqs)
            ba_response.ba_text = ba_response.ba_text.format(freq_count=freq_count)
            
        else:
            ba_response = tmp_state_response.ba_response
            reasoner_newstatus = tmp_state_response.reasoner_newstatus
            self.STATE = tmp_state_response.stage_newstate
        
        return ba_response, reasoner_newstatus, done_state

    def process_response(self, user_response: UserResponse) -> None:
        raise NotImplementedError
    
    def reset(self):
        self.init_state(self)
        gc.collect()