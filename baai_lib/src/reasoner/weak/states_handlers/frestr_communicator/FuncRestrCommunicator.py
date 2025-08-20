from dataclasses import dataclass, field
from typing import Tuple, Union
from copy import deepcopy
import gc

from .config import FRESRCLARIFIER_MAIN_LOG_PATH, BAFRESTRC_RESPONSE_CONFIG 
from .llm_pipelines import FuncRestrGenerator, FuncRestrGeneratorConfig
from .utils import FRestrAddState, FRestrClarifierState, FRestrDeleteState, \
    FRestrEditState, FRestrRecommendState, FRestrClarifierCurrentState
from ...utils import AbstractWeakModule, UserResponse, BAResponse, \
    WeakReasonerState, WeakReasonerStatus, WeakStateSignal, WeakGlobalSignal
from .....specification_model import ReqSpecificationModel
from .....specification_model.utils import FunctionalRestriction
from .....db_drivers.kv_driver import KeyValueDriverConfig
from .....utils import Logger
from .....utils.data_structs import create_id


@dataclass
class FuncRestrictionsCommunicatorConfig:
    """Конфигурация FuncRestrictionsCommunicator-стадии в рамках WeakBAReasoner-стратегии общения с пользователем по формированию технического задания.
    
    :param frestr_gen_config: Конфигурация LLM-пайплайна по генерации функциональных ограничений.
    :type frestr_gen_config: FuncRestrGeneratorConfig
    :param generated_frestr_limit: Максимальное количество функциональных ограничений, которе может быть сгенерировано. Значение по умолчанию 10.
    :type generated_frestr_limit: int
    :param log: Отладочный класс для журналирования/мониторинга поведения инициализируемой компоненты. Значение по умолчанию Logger(FRESRCLARIFIER_MAIN_LOG_PATH).
    :type log: Logger
    :param verbose: Если True, то информация о поведении класса будет сохраняться в stdout и файл-журналирования (log), иначе только в файл. Значение по умолчанию False.
    :type verbose: bool
    """
    frestr_gen_config: FuncRestrGeneratorConfig = field(default_factory=lambda: FuncRestrGeneratorConfig())
    generated_frestr_limit: int = -1 #10

    log: Logger = field(default_factory=lambda: Logger(FRESRCLARIFIER_MAIN_LOG_PATH))
    verbose: bool = False

class FuncRestrictionsCommunicator(AbstractWeakModule):
    """Класс реализует сценарий общения с пользователем в рамках стадии по уточнению функциональных ограничений. 
    На основе коммуникации (уточняющих вопросов) в рамках предыдущих стадий и согласованного набора функциональных требований 
    пользователю будут предлагаться/генерироваться возможные функциональные ограничения для включения в формируемое ТЗ. 
    Пользователю также доступен функционал по редактированию, удалению существующих ограничений, а также их ручному добавлению.
    """
    
    def __init__(self, reqspec_model: ReqSpecificationModel, config: FuncRestrictionsCommunicatorConfig = FuncRestrictionsCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.cache_kvdriver_config = cache_kvdriver_config
        self.mode = mode

        self.frestr_generator = FuncRestrGenerator(self.config.frestr_gen_config, cache_kvdriver_config)

        self.init_state()

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.STATE = FRestrClarifierCurrentState()
        self.GENERATED_FRESTR_COUNTER = 0
        
        self.EDITING_FRESTR_ID = None
        self.SELECTED_FREQ_ID = None
        self.CHOSING_FRESTR = None

        self.IS_FREQID_VALID_FLAG = None
        self.IS_FRESTRID_VALID_FLAG = None

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None,WeakReasonerState]]:
        tmp_state_response = deepcopy(BAFRESTRC_RESPONSE_CONFIG [self.STATE.base_state])
        done_state = None

        if self.STATE.base_state == FRestrClarifierState.add:
            tmp_state_response = tmp_state_response[self.STATE.fadd_state]

            if self.STATE.fadd_state == FRestrAddState.freqid_validating:
                response_keyword = None
                if self.IS_FREQID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_FREQID_VALID_FLAG = None

            elif self.STATE.fadd_state == FRestrAddState.validating:
                ba_response = tmp_state_response['good'].ba_response
                reasoner_newstatus = tmp_state_response['good'].reasoner_newstatus
                self.STATE = tmp_state_response['good'].stage_newstate

            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate   

        elif self.STATE.base_state == FRestrClarifierState.delete:
            tmp_state_response = tmp_state_response[self.STATE.frdelete_state]

            if self.STATE.frdelete_state == FRestrDeleteState.frestrid_validating:
                response_keyword = None
                if self.IS_FRESTRID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'


                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_FRESTRID_VALID_FLAG = None
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

        elif self.STATE.base_state == FRestrClarifierState.edit:
            tmp_state_response = tmp_state_response[self.STATE.fedit_state]

            if self.STATE.fedit_state == FRestrEditState.frestrid_validating:
                response_keyword = None
                if self.IS_FRESTRID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_FRESTRID_VALID_FLAG = None

            elif self.STATE.fedit_state == FRestrEditState.editing_frestr:
                tmp_state_response.ba_response.user_base_answer = self.reqspec_model.specification_struct.reqs_info.functional_restrictions[self.EDITING_FRESTR_ID].statement

                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

            elif self.STATE.fedit_state == FRestrEditState.validating:
                ba_response = tmp_state_response['good'].ba_response
                reasoner_newstatus = tmp_state_response['good'].reasoner_newstatus
                self.STATE = tmp_state_response['good'].stage_newstate

            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

        elif self.STATE.base_state == FRestrClarifierState.recommend:
            tmp_state_response = tmp_state_response[self.STATE.frrecomm_state]

            if self.STATE.frrecomm_state == FRestrRecommendState.init:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                if self.config.generated_frestr_limit > -1 and self.GENERATED_FRESTR_COUNTER >= self.config.generated_frestr_limit:
                    self.STATE.frrecomm_state = FRestrRecommendState.limit_exceeds
                else:
                    self.STATE.frrecomm_state = FRestrRecommendState.freq_selecting

            elif self.STATE.frrecomm_state == FRestrRecommendState.freqid_validating:
                response_keyword = None
                if self.IS_FREQID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_FREQID_VALID_FLAG = None

            elif self.STATE.frrecomm_state == FRestrRecommendState.frestr_recommending:
                
                if self.mode == 'prod':
                    task_goal = self.reqspec_model.specification_struct.general.goal
                    selected_freq = self.reqspec_model.specification_struct.reqs_info.functional[self.SELECTED_FREQ_ID]
                    declined_frestrs = self.reqspec_model.states_valuable_history[WeakReasonerState.funcrestr_ccrud]['declined_frestrs'][self.SELECTED_FREQ_ID]
                    accepted_frestrs = [self.reqspec_model.specification_struct.reqs_info.functional_restrictions[frest_id] for frest_id in list(selected_freq.related_frestr_ids)]
                    
                    self.CHOSING_FRESTR = self.frestr_generator.generate(
                        task_goal, selected_freq, accepted_frestrs, declined_frestrs)
                    
                elif self.mode == 'stub':
                    stub_frestr = FunctionalRestriction(id=create_id(), statement="Функциональное ограничение 'Заглушка'")
                    self.CHOSING_FRESTR = stub_frestr
                else:
                    raise ValueError
            
                self.CHOSING_FRESTR.related_freq_ids.add(self.SELECTED_FREQ_ID)
                
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                ba_response.ba_text = ba_response.ba_text.format(rec_frestr=self.CHOSING_FRESTR.statement)
                self.GENERATED_FRESTR_COUNTER += 1

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
       
        if self.STATE.base_state == FRestrClarifierState.select_act:
            if user_response.signal == WeakGlobalSignal.next_stage:
                self.STATE.base_state = FRestrClarifierState.done

            elif user_response.signal == WeakStateSignal.add:
                self.STATE.base_state = FRestrClarifierState.add
                self.STATE.fadd_state = FRestrAddState.init

            elif user_response.signal == WeakStateSignal.delete:
                self.STATE.base_state = FRestrClarifierState.delete
                self.STATE.frdelete_state = FRestrDeleteState.init

            elif user_response.signal == WeakStateSignal.edit:
                self.STATE.base_state = FRestrClarifierState.edit
                self.STATE.fedit_state = FRestrEditState.init

            elif user_response.signal == WeakStateSignal.recommend_new:
                self.STATE.base_state = FRestrClarifierState.recommend
                self.STATE.frrecomm_state = FRestrRecommendState.init

            else:
                raise ValueError
    
        elif self.STATE.base_state == FRestrClarifierState.add:
            if self.STATE.fadd_state == FRestrAddState.freq_selecting:
                freq_id = user_response.user_text
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.fadd_state = FRestrAddState.done
                else:
                    self.IS_FREQID_VALID_FLAG = freq_id in list(self.reqspec_model.specification_struct.reqs_info.functional.keys())
                    self.STATE.fadd_state = FRestrAddState.freqid_validating
                    if self.IS_FREQID_VALID_FLAG:
                        self.SELECTED_FREQ_ID = freq_id
    
            elif self.STATE.fadd_state == FRestrAddState.adding_frestr:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.fadd_state = FRestrAddState.done
                else:
                    new_frestr = FunctionalRestriction(id=create_id(), statement=user_response.user_text, related_freq_ids={self.SELECTED_FREQ_ID})
                    self.reqspec_model.specification_struct.reqs_info.functional_restrictions[new_frestr.id] = new_frestr
                    self.reqspec_model.specification_struct.reqs_info.functional[self.SELECTED_FREQ_ID].related_frestr_ids.add(new_frestr.id)

                    self.STATE.fadd_state = FRestrAddState.validating

            else:
                raise ValueError
            
        elif self.STATE.base_state == FRestrClarifierState.delete:
            
            if self.STATE.frdelete_state == FRestrDeleteState.frestr_selecting:
                frestr_id = user_response.user_text
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.frdelete_state = FRestrDeleteState.done
                else:
                    self.IS_FRESTRID_VALID_FLAG = frestr_id in list(self.reqspec_model.specification_struct.reqs_info.functional_restrictions.keys())
                    self.STATE.frdelete_state = FRestrDeleteState.frestrid_validating
                    if self.IS_FRESTRID_VALID_FLAG:
                      related_freq_ids = self.reqspec_model.specification_struct.reqs_info.functional_restrictions[frestr_id].related_freq_ids
                      del self.reqspec_model.specification_struct.reqs_info.functional_restrictions[frestr_id]
                      
                      for freq_id in related_freq_ids:
                        self.reqspec_model.specification_struct.reqs_info.functional[freq_id].related_frestr_ids.remove(frestr_id)
            else:
                raise ValueError
            
        elif self.STATE.base_state == FRestrClarifierState.edit:

            if self.STATE.fedit_state == FRestrEditState.frestr_selecting:

                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.fedit_state = FRestrEditState.done
                else:
                    frestr_id = user_response.user_text
                    self.IS_FRESTRID_VALID_FLAG = frestr_id in list(self.reqspec_model.specification_struct.reqs_info.functional_restrictions.keys())
                    self.STATE.fedit_state = FRestrEditState.frestrid_validating
                    if self.IS_FRESTRID_VALID_FLAG:
                        self.EDITING_FRESTR_ID = frestr_id
               
            elif self.STATE.fedit_state == FRestrEditState.editing_frestr:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.fedit_state = FRestrEditState.done
                else:
                    self.reqspec_model.specification_struct.reqs_info.functional_restrictions[self.EDITING_FRESTR_ID].statement = user_response.user_text

                    self.STATE.fedit_state = FRestrEditState.validating
                    
            else:
                raise ValueError
            
        elif self.STATE.base_state == FRestrClarifierState.recommend:
            if self.STATE.frrecomm_state == FRestrRecommendState.freq_selecting:
                freq_id = user_response.user_text
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.frrecomm_state = FRestrRecommendState.done
                else:
                    self.IS_FREQID_VALID_FLAG = freq_id in list(self.reqspec_model.specification_struct.reqs_info.functional.keys())
                    self.STATE.frrecomm_state = FRestrRecommendState.freqid_validating
                    if self.IS_FREQID_VALID_FLAG:
                        self.SELECTED_FREQ_ID = freq_id

            elif self.STATE.frrecomm_state == FRestrRecommendState.frestr_recommending:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.frrecomm_state = FRestrRecommendState.done
                    
                elif user_response.signal == WeakStateSignal.approve:
                    self.reqspec_model.specification_struct.reqs_info.functional_restrictions[self.CHOSING_FRESTR.id] = self.CHOSING_FRESTR
                    self.reqspec_model.specification_struct.reqs_info.functional[self.SELECTED_FREQ_ID].related_frestr_ids.add(self.CHOSING_FRESTR.id)
                    
                    self.CHOSING_FRESTR = None
                    self.SELECTED_FREQ_ID = None
                    
                    self.STATE.frrecomm_state = FRestrRecommendState.done

                elif user_response.signal == WeakStateSignal.decline:
                    self.reqspec_model.states_valuable_history[WeakReasonerState.funcrestr_ccrud]['declined_frestrs'][self.SELECTED_FREQ_ID].append(self.CHOSING_FRESTR)

                    self.CHOSING_FRESTR = None
                    self.SELECTED_FREQ_ID = None
                    
                    self.STATE.frrecomm_state = FRestrRecommendState.done

                else:
                    raise ValueError
            else:
                raise ValueError
        else:
            raise ValueError
    
    def reset(self):
        self.init_state()
        gc.collect()