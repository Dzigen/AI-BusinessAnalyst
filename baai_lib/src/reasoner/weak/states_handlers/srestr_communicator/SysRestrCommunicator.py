from dataclasses import dataclass, field
from typing import Tuple, Union
import gc 
from copy import deepcopy

from .config import SRESRCLARIFIER_MAIN_LOG_PATH, BASRESTRC_RESPONSE_CONFIG
from .llm_pipelines import SysRestrGenerator, SysRestrGeneratorConfig
from .utils import SRestrAddState, SRestrClarifierCurrentState, SRestrClarifierState, \
    SRestrDeleteState, SRestrEditState, SRestrRecommendState
from ...utils import AbstractWeakModule, UserResponse, BAResponse, \
    WeakReasonerState, WeakReasonerStatus, WeakStateSignal, WeakGlobalSignal
from .....specification_model import ReqSpecificationModel
from .....specification_model.utils import SystemRestriction
from .....db_drivers.kv_driver import KeyValueDriverConfig
from .....utils import Logger
from .....utils.data_structs import create_id

@dataclass
class SysRestrictionsCommunicatorConfig:
    """Конфигурация SysRestrictionsCommunicator-стадии в рамках WeakBAReasoner-стратегии общения с пользователем по формированию технического задания.
    
    :param srestr_gen_config: Конфигурация LLM-пайплайна по генерации системных ограничений.
    :type srestr_gen_config: SysRestrGeneratorConfig
    :param generated_srestr_limit: Максимальное количество системных ограничений, которе может быть сгенерировано. Значение по умолчанию 10.
    :type generated_srestr_limit: int
    :param log: Отладочный класс для журналирования/мониторинга поведения инициализируемой компоненты. Значение по умолчанию Logger(SRESRCLARIFIER_MAIN_LOG_PATH).
    :type log: Logger
    :param verbose: Если True, то информация о поведении класса будет сохраняться в stdout и файл-журналирования (log), иначе только в файл. Значение по умолчанию False.
    :type verbose: bool
    """

    srestr_gen_config: SysRestrGeneratorConfig = field(default_factory=lambda: SysRestrGeneratorConfig())
    generated_srestr_limit: int = -1 #10

    log: Logger = field(default_factory=lambda: Logger(SRESRCLARIFIER_MAIN_LOG_PATH))
    verbose: bool = False

class SysRestrictionsCommunicator(AbstractWeakModule):
    """Класс реализует сценарий общения с пользователем в рамках стадии по уточнению системных ограничений. 
    На основе коммуникации (уточняющих вопросов) в рамках предыдущих стадий и согласованного набора системных требований 
    пользователю будут предлагаться/генерироваться возможные системные ограничения для включения в формируемое ТЗ. 
    Пользователю также доступен функционал по редактированию, удалению существующих ограничений, а также их ручному добавлению.
    """
    def __init__(self, reqspec_model: ReqSpecificationModel, config: SysRestrictionsCommunicatorConfig = SysRestrictionsCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.cache_kvdriver_config = cache_kvdriver_config
        self.mode = mode

        self.srestr_generator = SysRestrGenerator(self.config.srestr_gen_config, cache_kvdriver_config)

        self.init_state()

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.STATE = SRestrClarifierCurrentState()
        self.GENERATED_SRESTR_COUNTER = 0
        
        self.EDITING_SRESTR_ID = None
        self.SELECTED_SREQ_ID = None
        self.CHOSING_SRESTR = None

        self.IS_SREQID_VALID_FLAG = None
        self.IS_SRESTRID_VALID_FLAG = None

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None,WeakReasonerState]]:
        tmp_state_response = deepcopy(BASRESTRC_RESPONSE_CONFIG [self.STATE.base_state])
        done_state = None

        if self.STATE.base_state == SRestrClarifierState.add:
            tmp_state_response = tmp_state_response[self.STATE.sadd_state]

            if self.STATE.sadd_state == SRestrAddState.sreqid_validating:
                response_keyword = None
                if self.IS_SREQID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_SREQID_VALID_FLAG = None

            elif self.STATE.sadd_state == SRestrAddState.validating:
                ba_response = tmp_state_response['good'].ba_response
                reasoner_newstatus = tmp_state_response['good'].reasoner_newstatus
                self.STATE = tmp_state_response['good'].stage_newstate
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate   

        elif self.STATE.base_state == SRestrClarifierState.delete:
            tmp_state_response = tmp_state_response[self.STATE.srdelete_state]

            if self.STATE.srdelete_state == SRestrDeleteState.srestrid_validating:
                response_keyword = None
                if self.IS_SRESTRID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'


                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_SRESTRID_VALID_FLAG = None
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

        elif self.STATE.base_state == SRestrClarifierState.edit:
            tmp_state_response = tmp_state_response[self.STATE.sedit_state]

            if self.STATE.sedit_state == SRestrEditState.srestrid_validating:
                response_keyword = None
                if self.IS_SRESTRID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_SRESTRID_VALID_FLAG = None

            elif self.STATE.sedit_state == SRestrEditState.editing_srestr:
                tmp_state_response.ba_response.user_base_answer = self.reqspec_model.specification_struct.system_info.restrictions[self.EDITING_SRESTR_ID].statement

                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

            elif self.STATE.sedit_state == SRestrEditState.validating:
                ba_response = tmp_state_response['good'].ba_response
                reasoner_newstatus = tmp_state_response['good'].reasoner_newstatus
                self.STATE = tmp_state_response['good'].stage_newstate

            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

        elif self.STATE.base_state == SRestrClarifierState.recommend:
            tmp_state_response = tmp_state_response[self.STATE.srrecomm_state]

            if self.STATE.srrecomm_state == SRestrRecommendState.init:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                if self.config.generated_srestr_limit > -1 and self.GENERATED_SRESTR_COUNTER >= self.config.generated_srestr_limit:
                    self.STATE.srrecomm_state = SRestrRecommendState.limit_exceeds
                else:
                    self.STATE.srrecomm_state = SRestrRecommendState.sreq_selecting

            if self.STATE.srrecomm_state == SRestrRecommendState.sreqid_validating:
                response_keyword = None
                if self.IS_SREQID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_SREQID_VALID_FLAG = None

            elif self.STATE.srrecomm_state == SRestrRecommendState.srestr_recommending:
                
                if self.mode == 'prod':
                    task_goal = self.reqspec_model.specification_struct.general.goal
                    selected_sreq = self.reqspec_model.specification_struct.system_info.requirements[self.SELECTED_SREQ_ID]
                    declined_srestrs = self.reqspec_model.states_valuable_history[WeakReasonerState.sysrestr_ccrud]['declined_srestrs'][self.SELECTED_SREQ_ID]
                    accepted_srestrs = [self.reqspec_model.specification_struct.system_info.restrictions[srest_id] for srest_id in list(selected_sreq.related_srestr_ids)]
                    
                    self.CHOSING_SRESTR = self.srestr_generator.generate(
                        task_goal, selected_sreq, accepted_srestrs, declined_srestrs)
                    
                elif self.mode == 'stub':
                    stub_srestr = SystemRestriction(id=create_id(), statement="Системное ограничение 'Заглушка'")
                    self.CHOSING_SRESTR = stub_srestr
                else:
                    raise ValueError
            
                self.CHOSING_SRESTR.related_sreq_ids.add(self.SELECTED_SREQ_ID)
                
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                ba_response.ba_text = ba_response.ba_text.format(rec_srestr=self.CHOSING_SRESTR.statement)
                self.GENERATED_SRESTR_COUNTER += 1

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
       
        if self.STATE.base_state == SRestrClarifierState.select_act:
            if user_response.signal == WeakGlobalSignal.next_stage:
                self.STATE.base_state = SRestrClarifierState.done

            elif user_response.signal == WeakStateSignal.add:
                self.STATE.base_state = SRestrClarifierState.add
                self.STATE.sadd_state = SRestrAddState.init

            elif user_response.signal == WeakStateSignal.delete:
                self.STATE.base_state = SRestrClarifierState.delete
                self.STATE.srdelete_state = SRestrDeleteState.init

            elif user_response.signal == WeakStateSignal.edit:
                self.STATE.base_state = SRestrClarifierState.edit
                self.STATE.sedit_state = SRestrEditState.init

            elif user_response.signal == WeakStateSignal.recommend_new:
                self.STATE.base_state = SRestrClarifierState.recommend
                self.STATE.srrecomm_state = SRestrRecommendState.init

            else:
                raise ValueError
    
        elif self.STATE.base_state == SRestrClarifierState.add:
            if self.STATE.sadd_state == SRestrAddState.sreq_selecting:
                sreq_id = user_response.user_text
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.sadd_state = SRestrAddState.done
                else:
                    self.IS_SREQID_VALID_FLAG = sreq_id in list(self.reqspec_model.specification_struct.system_info.requirements.keys())
                    self.STATE.sadd_state = SRestrAddState.sreqid_validating
                    if self.IS_SREQID_VALID_FLAG:
                        self.SELECTED_SREQ_ID = sreq_id

            elif self.STATE.sadd_state == SRestrAddState.adding_srestr:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.sadd_state = SRestrAddState.done
                else:
                    new_srestr = SystemRestriction(id=create_id(), statement=user_response.user_text, related_sreq_ids={self.SELECTED_SREQ_ID})
                    self.reqspec_model.specification_struct.system_info.restrictions[new_srestr.id] = new_srestr
                    self.reqspec_model.specification_struct.system_info.requirements[self.SELECTED_SREQ_ID].related_srestr_ids.add(new_srestr.id)

                    self.STATE.sadd_state = SRestrAddState.validating

            else:
                raise ValueError
            
        elif self.STATE.base_state == SRestrClarifierState.delete:
            
            if self.STATE.srdelete_state == SRestrDeleteState.srestr_selecting:
                srestr_id = user_response.user_text
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.srdelete_state = SRestrDeleteState.done
                else:
                    self.IS_SRESTRID_VALID_FLAG = srestr_id in list(self.reqspec_model.specification_struct.system_info.restrictions.keys())
                    self.STATE.srdelete_state = SRestrDeleteState.srestrid_validating
                    if self.IS_SRESTRID_VALID_FLAG:
                      related_sreq_ids = self.reqspec_model.specification_struct.system_info.restrictions[srestr_id].related_sreq_ids
                      del self.reqspec_model.specification_struct.system_info.restrictions[srestr_id]
                      
                      for sreq_id in related_sreq_ids:
                        self.reqspec_model.specification_struct.system_info.requirements[sreq_id].related_srestr_ids.remove(srestr_id)
            else:
                raise ValueError
            
        elif self.STATE.base_state == SRestrClarifierState.edit:

            if self.STATE.sedit_state == SRestrEditState.srestr_selecting:

                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.sedit_state = SRestrEditState.done
                else:
                    srestr_id = user_response.user_text
                    self.IS_SRESTRID_VALID_FLAG = srestr_id in list(self.reqspec_model.specification_struct.system_info.restrictions.keys())
                    self.STATE.sedit_state = SRestrEditState.srestrid_validating
                    if self.IS_SRESTRID_VALID_FLAG:
                        self.EDITING_SRESTR_ID = srestr_id
               
            elif self.STATE.sedit_state == SRestrEditState.editing_srestr:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.sedit_state = SRestrEditState.done
                else:
                    self.reqspec_model.specification_struct.system_info.restrictions[self.EDITING_SRESTR_ID].statement = user_response.user_text

                    self.STATE.sedit_state = SRestrEditState.validating
                    
            else:
                raise ValueError
            
        elif self.STATE.base_state == SRestrClarifierState.recommend:
            if self.STATE.srrecomm_state == SRestrRecommendState.sreq_selecting:
                sreq_id = user_response.user_text
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.srrecomm_state = SRestrRecommendState.done
                else:
                    self.IS_SREQID_VALID_FLAG = sreq_id in list(self.reqspec_model.specification_struct.system_info.requirements.keys())
                    self.STATE.srrecomm_state = SRestrRecommendState.sreqid_validating
                    if self.IS_SREQID_VALID_FLAG:
                        self.SELECTED_SREQ_ID = sreq_id

            elif self.STATE.srrecomm_state == SRestrRecommendState.srestr_recommending:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.srrecomm_state = SRestrRecommendState.done
                    
                elif user_response.signal == WeakStateSignal.approve:
                    self.reqspec_model.specification_struct.system_info.restrictions[self.CHOSING_SRESTR.id] = self.CHOSING_SRESTR
                    self.reqspec_model.specification_struct.system_info.requirements[self.SELECTED_SREQ_ID].related_srestr_ids.add(self.CHOSING_SRESTR.id)
                    
                    self.CHOSING_SRESTR = None
                    self.SELECTED_SREQ_ID = None
                    
                    self.STATE.srrecomm_state = SRestrRecommendState.done

                elif user_response.signal == WeakStateSignal.decline:
                    self.reqspec_model.states_valuable_history[WeakReasonerState.sysrestr_ccrud]['declined_srestrs'][self.SELECTED_SREQ_ID].append(self.CHOSING_SRESTR)

                    self.CHOSING_SRESTR = None
                    self.SELECTED_SREQ_ID = None
                    
                    self.STATE.srrecomm_state = SRestrRecommendState.done

                else:
                    raise ValueError
            else:
                raise ValueError
        else:
            raise ValueError
    
    def reset(self):
        self.init_state()
        gc.collect()