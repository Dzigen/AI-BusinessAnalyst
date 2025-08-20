from dataclasses import dataclass, field
from typing import Tuple, Union
import gc
from copy import deepcopy
from time import time

from .config import SCLARIFIER_MAIN_LOG_PATH, BAUSC_RESPONSE_CONFIG
from .llm_pipelines import ScenariosGenerator, ScenariosGeneratorConfig
from .utils import SClarifierCurrentState, SClarifierState, SDeleteState, SRecommendState
from ...utils import AbstractWeakModule, UserResponse, BAResponse, \
    WeakReasonerState, WeakReasonerStatus, WeakStateSignal, WeakGlobalSignal
from ...config import WBAR_GLOBAL_SIGNALSINFO
from .....specification_model import ReqSpecificationModel
from .....specification_model.utils import Scenario
from .....utils.data_structs import create_id
from .....db_drivers.kv_driver import KeyValueDriverConfig
from .....utils import Logger

@dataclass
class ScenariosCommunicatorConfig:
    """Конфигурация ScenariosCommunicator-стадии в рамках WeakBAReasoner-стратегии общения с пользователем по формированию технического задания.
    
    :param scenario_gen_config: Конфигурация LLM-пайплайна по генерации сценариев использования.
    :type scenario_gen_config: ScenariosGeneratorConfig
    :param generated_scenarios_limit: Максимальное количество сценариев, которе может быть сгенерировано. Значение по умолчанию 10.
    :type generated_scenarios_limit: int
    :param  min_scenarios_amount: Минимальное количество сценариев, которое должно добавить пользователь для перехода на следующую стадию. Значение по умолчанию 3.
    :type  min_scenarios_amount: int
    :param log: Отладочный класс для журналирования/мониторинга поведения инициализируемой компоненты. Значение по умолчанию Logger(TCLARIFIER_MAIN_LOG_PATH).
    :type log: Logger
    :param verbose: Если True, то информация о поведении класса будет сохраняться в stdout и файл-журналирования (log), иначе только в файл. Значение по умолчанию False.
    :type verbose: bool
    """
        
    scenario_gen_config: ScenariosGeneratorConfig = field(default_factory=lambda: ScenariosGeneratorConfig())
    generated_scenarios_limit: int = -1 #10
    min_scenarios_amount: int = 1

    log: Logger = field(default_factory=lambda: Logger(SCLARIFIER_MAIN_LOG_PATH))
    verbose: bool = False

class ScenariosCommunicator(AbstractWeakModule):
    """Класс реализует сценарий общения с пользователем в рамках стадии по предложению/генерации сценариев использования. 
    На основе коммуникации (уточняющих вопросов) в рамках предыдущих стадий и согласованного набора user-историй 
    пользователю будут предлагаться/генерироваться сценарии использования для включения в формируемое ТЗ. 
    Пользователю также доступен функционал по удалению существующих сценариев.
    """

    def __init__(self, reqspec_model: ReqSpecificationModel, config: ScenariosCommunicatorConfig = ScenariosCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.cache_kvdriver_config = cache_kvdriver_config
        self.mode = mode

        self.scenario_generator = ScenariosGenerator(self.config.scenario_gen_config, cache_kvdriver_config)

        self.init_state()

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.STATE = SClarifierCurrentState()
        self.GENERATED_SCENARIOS_COUNTER = 0
        
        self.SELECTED_US_ID = None
        self.CHOSING_SCENARIO = None

        self.IS_SID_VALID_FLAG = None
        self.IS_USID_VALID_FLAG = None

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None,WeakReasonerState]]:
        tmp_state_response = deepcopy(BAUSC_RESPONSE_CONFIG[self.STATE.base_state])
        done_state = None
            
        if self.STATE.base_state == SClarifierState.select_act:
            ba_response = tmp_state_response.ba_response
            reasoner_newstatus = tmp_state_response.reasoner_newstatus
            self.STATE = tmp_state_response.stage_newstate

            if len(list(self.reqspec_model.specification_struct.scenarios.keys())) >= self.config.min_scenarios_amount:
                ba_response.available_global_signals = list(WBAR_GLOBAL_SIGNALSINFO.values())
            else:
                ba_response.available_global_signals = []
        
        elif self.STATE.base_state == SClarifierState.delete:
            tmp_state_response = tmp_state_response[self.STATE.sdelete_state]

            if self.STATE.sdelete_state == SDeleteState.sid_validating:
                response_keyword = None
                if self.IS_SID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'


                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_SID_VALID_FLAG = None
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate
            
        elif self.STATE.base_state == SClarifierState.recommend:
            tmp_state_response = tmp_state_response[self.STATE.srecomm_state]

            if self.STATE.srecomm_state == SRecommendState.init:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                if self.config.generated_scenarios_limit > -1 and self.GENERATED_SCENARIOS_COUNTER >= self.config.generated_scenarios_limit:
                    self.STATE.srecomm_state = SRecommendState.limit_exceeds
                else:
                    self.STATE.srecomm_state = SRecommendState.us_selecting

            elif self.STATE.srecomm_state == SRecommendState.usid_validating:
                response_keyword = None
                if self.IS_USID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_USID_VALID_FLAG = None

            elif self.STATE.srecomm_state == SRecommendState.s_recommending:
                
                if self.mode == 'prod':
                    task_goal = self.reqspec_model.specification_struct.general.goal
                    selected_userstory = self.reqspec_model.specification_struct.user_stories[self.SELECTED_US_ID]
                    declined_scenarios = self.reqspec_model.states_valuable_history[WeakReasonerState.scenarios_ccrud]['declined_scenarios'][self.SELECTED_US_ID]
                    accepted_scenarios = [self.reqspec_model.specification_struct.scenarios[s_id] for s_id in selected_userstory.related_scenario_ids]
                    
                    self.CHOSING_SCENARIO = self.scenario_generator.generate(
                        task_goal, selected_userstory, accepted_scenarios, declined_scenarios)
                    
                elif self.mode == 'stub':
                    stub_scenario = Scenario(id=create_id(str(time())), title="Заголовок заглушка", steps=["действие №1", "действие №2"])
                    self.CHOSING_SCENARIO = stub_scenario
                else:
                    raise ValueError
                
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                ba_response.ba_text = ba_response.ba_text.format(rec_s=self.CHOSING_SCENARIO.formate_to_str())
                self.GENERATED_SCENARIOS_COUNTER += 1

            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate
            
        else:
            ba_response = tmp_state_response.ba_response
            reasoner_newstatus = tmp_state_response.reasoner_newstatus
            self.STATE = tmp_state_response.stage_newstate
        
        return ba_response, reasoner_newstatus, done_state

    def process_response(self, user_response: UserResponse) -> None:
       
        if self.STATE.base_state == SClarifierState.select_act:
            if user_response.signal == WeakGlobalSignal.next_stage:
                self.STATE.base_state = SClarifierState.done

            elif user_response.signal == WeakStateSignal.delete:
                self.STATE.base_state = SClarifierState.delete
                self.STATE.sdelete_state = SDeleteState.init

            elif user_response.signal == WeakStateSignal.recommend_new:
                self.STATE.base_state = SClarifierState.recommend
                self.STATE.srecomm_state = SRecommendState.init

            else:
                raise ValueError
            
        elif self.STATE.base_state == SClarifierState.delete:
            
            if self.STATE.sdelete_state == SDeleteState.s_selecting:
                s_id = user_response.user_text
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.sdelete_state = SDeleteState.done
                else:
                    self.IS_SID_VALID_FLAG = s_id in list(self.reqspec_model.specification_struct.scenarios.keys())
                    self.STATE.sdelete_state = SDeleteState.sid_validating
                    if self.IS_SID_VALID_FLAG:
                      del self.reqspec_model.specification_struct.scenarios[s_id]
            else:
                raise ValueError
            
        elif self.STATE.base_state == SClarifierState.recommend:
            if self.STATE.srecomm_state == SRecommendState.us_selecting:
                us_id = user_response.user_text
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.srecomm_state = SRecommendState.done
                else:
                    self.IS_USID_VALID_FLAG = us_id in list(self.reqspec_model.specification_struct.user_stories.keys())
                    self.STATE.srecomm_state = SRecommendState.usid_validating
                    if self.IS_USID_VALID_FLAG:
                        self.SELECTED_US_ID = us_id

            elif self.STATE.srecomm_state == SRecommendState.s_recommending:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.srecomm_state = SRecommendState.done
                    
                elif user_response.signal == WeakStateSignal.approve:
                    self.reqspec_model.specification_struct.user_stories[self.SELECTED_US_ID].related_scenario_ids.append(self.CHOSING_SCENARIO.id)
                    self.reqspec_model.specification_struct.scenarios[self.CHOSING_SCENARIO.id] = self.CHOSING_SCENARIO
                    
                    self.CHOSING_SCENARIO = None
                    self.SELECTED_US_ID = None
                    
                    self.STATE.srecomm_state = SRecommendState.done

                elif user_response.signal == WeakStateSignal.decline:
                    self.reqspec_model.states_valuable_history[WeakReasonerState.scenarios_ccrud]['declined_scenarios'][self.SELECTED_US_ID].append(self.CHOSING_SCENARIO)
                    
                    self.CHOSING_SCENARIO = None
                    self.SELECTED_US_ID = None
                    
                    self.STATE.srecomm_state = SRecommendState.done

                else:
                    raise ValueError
            else:
                raise ValueError
        else:
            raise ValueError
    
    def reset(self):
        self.init_state()
        gc.collect()