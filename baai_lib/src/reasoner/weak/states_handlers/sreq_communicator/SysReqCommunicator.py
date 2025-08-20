from dataclasses import dataclass, field
from typing import Tuple, Union
from copy import deepcopy
import gc

from .config import SREQEXTRACTOR_MAIN_LOG_PATH, BASREQC_MESSAGE_TAMPLATES
from .llm_pipelines import SysReqExtractor, SysReqExtractorConfig
from .utils import SReqClarifierCurrentState, SReqAddState, SReqDeleteState, \
    SReqEditState, SReqClarifierState, SReqExtractingState
from ...utils import AbstractWeakModule, UserResponse, BAResponse, \
    WeakReasonerState, WeakReasonerStatus, WeakStateSignal, WeakGlobalSignal
from .....specification_model import ReqSpecificationModel
from .....specification_model.utils import SystemRequirement
from .....db_drivers.kv_driver import KeyValueDriverConfig
from .....utils import Logger
from .....utils.data_structs import create_id

@dataclass
class SysRequirementsCommunicatorConfig:
    """Конфигурация SysRequirementsCommunicator-стадии в рамках WeakBAReasoner-стратегии общения с пользователем по формированию технического задания.
    
    :param sysreq_extr_config: Конфигурация LLM-пайплайна по генерации системных требований.
    :type sysreq_extr_config: SysReqExtractorConfig
    :param extracted_sysreq_limit: Максимальное количество системных требований, которое может быть автоматически сформировано/сгенерировано. Значение по умолчанию 10.
    :type extracted_sysreq_limit: int
    :param log: Отладочный класс для журналирования/мониторинга поведения инициализируемой компоненты. Значение по умолчанию Logger(SREQEXTRACTOR_MAIN_LOG_PATH).
    :type log: Logger
    :param verbose: Если True, то информация о поведении класса будет сохраняться в stdout и файл-журналирования (log), иначе только в файл. Значение по умолчанию False.
    :type verbose: bool
    """
    sysreq_extr_config: SysReqExtractorConfig = field(default_factory=lambda: SysReqExtractorConfig())

    extracted_sysreq_limit: int = -1 #10

    log: Logger = field(default_factory=lambda: Logger(SREQEXTRACTOR_MAIN_LOG_PATH))
    verbose: bool = False

class SysRequirementsCommunicator(AbstractWeakModule):
    """Класс реализует сценарий общения с пользователем в рамках стадии по уточнению системных требований. 
    На основе коммуникации (уточняющих вопросов) в рамках предыдущих стадий будет автоматически сформировано базовый набор системныъ требований. 
    Пользователю будет доступен функционал по ручному добавлению новых требований, а также их удалению и редактированию.
    """

    def __init__(self, reqspec_model: ReqSpecificationModel, config: SysRequirementsCommunicatorConfig = SysRequirementsCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.cache_kvdriver_config = cache_kvdriver_config
        self.mode = mode

        self.sysreq_extractor = SysReqExtractor(self.config.sysreq_extr_config, cache_kvdriver_config)

        self.init_state()

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.STATE = SReqClarifierCurrentState()
        self.EDITING_SREQ_ID = None

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None,WeakReasonerState]]:
        tmp_state_response = deepcopy(BASREQC_MESSAGE_TAMPLATES[self.STATE.base_state])
        done_state = None

        if self.STATE.base_state == SReqClarifierState.sreq_extracting:
            tmp_state_response = tmp_state_response[self.STATE.srextr_state]
            
            if self.STATE.srextr_state == SReqExtractingState.done:

                sys_requirements = None
                if self.mode == 'prod':
                    task_goal = self.reqspec_model.specification_struct.general.goal
                    base_dhistory = self.reqspec_model.states_valuable_history[WeakReasonerState.task_clarifying]['general_qa']
                    detailed_dhistory = self.reqspec_model.states_valuable_history[WeakReasonerState.bp_clarifying]['detailed_qa']
                    
                    sys_requirements = self.sysreq_extractor.extract(
                        task_goal, base_dhistory, detailed_dhistory, sr_limit=self.config.extracted_sysreq_limit)
                    
                elif self.mode == 'stub':
                    sys_requirements = [
                        SystemRequirement(id='1', statement="Системное требование 'Заглушка' #1"),
                        SystemRequirement(id='2', statement="Системное требование 'Заглушка' #2"),
                        SystemRequirement(id='3', statement="Системное требование 'Заглушка' #3")]
                else: 
                    raise ValueError

                self.reqspec_model.specification_struct.system_info.requirements = {sreq.id: sreq for sreq in sys_requirements}

                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                ba_response.ba_text = ba_response.ba_text.format(sr_amount=len(sys_requirements))
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

        elif self.STATE.base_state == SReqClarifierState.add:
            tmp_state_response = tmp_state_response[self.STATE.sradd_state]

            if self.STATE.sradd_state == SReqAddState.validating:
                ba_response = tmp_state_response['good'].ba_response
                reasoner_newstatus = tmp_state_response['good'].reasoner_newstatus
                self.STATE = tmp_state_response['good'].stage_newstate
                
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate
  
        elif self.STATE.base_state == SReqClarifierState.delete:
            tmp_state_response = tmp_state_response[self.STATE.srdelete_state]

            if self.STATE.srdelete_state == SReqDeleteState.sreqid_validating:
                response_keyword = None
                if self.IS_SREQID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_SREQID_VALID_FLAG = None
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate
            
        elif self.STATE.base_state == SReqClarifierState.edit:
            tmp_state_response = tmp_state_response[self.STATE.sredit_state]

            if self.STATE.sredit_state == SReqEditState.sreqid_validating:
                response_keyword = None
                if self.IS_SREQID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_SREQID_VALID_FLAG = None

            elif self.STATE.sredit_state == SReqEditState.editing_sreq:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                ba_response.user_base_answer = self.reqspec_model.specification_struct.system_info.requirements[self.EDITING_SREQ_ID].statement
                
            elif self.STATE.sredit_state == SReqEditState.validating:
                ba_response = tmp_state_response['good'].ba_response
                reasoner_newstatus = tmp_state_response['good'].reasoner_newstatus
                self.STATE = tmp_state_response['good'].stage_newstate
                
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
        if self.STATE.base_state == SReqClarifierState.select_act:
            if user_response.signal is None:
                raise ValueError
            
            if user_response.signal == WeakGlobalSignal.next_stage:
                self.STATE.base_state = SReqClarifierState.done

            elif user_response.signal == WeakStateSignal.add:
                self.STATE.base_state = SReqClarifierState.add
                self.STATE.sradd_state = SReqAddState.init
            
            elif user_response.signal == WeakStateSignal.delete:
                self.STATE.base_state = SReqClarifierState.delete
                self.STATE.srdelete_state = SReqDeleteState.init
            
            elif user_response.signal == WeakStateSignal.edit:
                self.STATE.base_state = SReqClarifierState.edit
                self.STATE.sredit_state = SReqEditState.init
            
            else:
                raise ValueError

        elif self.STATE.base_state == SReqClarifierState.add:
    
            if self.STATE.sradd_state == SReqAddState.adding_sreq:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.sradd_state = SReqAddState.done
                else:
                    new_sysreq = SystemRequirement(id=create_id(), statement=user_response.user_text)
                    self.reqspec_model.specification_struct.system_info.requirements[new_sysreq.id] = new_sysreq
                    self.STATE.sradd_state = SReqAddState.validating

            else:
                raise ValueError
            
        elif self.STATE.base_state == SReqClarifierState.delete:
            
            if self.STATE.srdelete_state == SReqDeleteState.sreq_selecting:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.srdelete_state = SReqDeleteState.done
                else:
                    sysreq_id = user_response.user_text
                    self.IS_SREQID_VALID_FLAG = sysreq_id in list(self.reqspec_model.specification_struct.system_info.requirements.keys())
                    self.STATE.srdelete_state = SReqDeleteState.sreqid_validating
                    if self.IS_SREQID_VALID_FLAG:
                      del self.reqspec_model.specification_struct.system_info.requirements[sysreq_id]
            else:
                raise ValueError
            
        elif self.STATE.base_state == SReqClarifierState.edit:

            if self.STATE.sredit_state == SReqEditState.sreq_selecting:

                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.sredit_state = SReqEditState.done
                else:
                    sysreq_id = user_response.user_text
                    self.IS_SREQID_VALID_FLAG = sysreq_id in list(self.reqspec_model.specification_struct.system_info.requirements.keys())
                    self.STATE.sredit_state = SReqEditState.sreqid_validating
                    if self.IS_SREQID_VALID_FLAG:
                        self.EDITING_SREQ_ID = user_response.user_text
               
            elif self.STATE.sredit_state == SReqEditState.editing_sreq:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.sredit_state = SReqEditState.done
                else:
                    edited_sysreq = SystemRequirement(id=self.EDITING_SREQ_ID, statement=user_response.user_text)
                    self.reqspec_model.specification_struct.system_info.requirements[self.EDITING_SREQ_ID] = edited_sysreq
                    self.STATE.sredit_state = SReqEditState.validating
                    
            else:
                raise ValueError
        else:
            raise ValueError
    
    def reset(self):
        self.init_state()
        gc.collect()