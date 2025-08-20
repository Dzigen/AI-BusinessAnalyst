from dataclasses import dataclass, field
from typing import Dict, Tuple, Union
from copy import deepcopy
import gc

from .config import BPCLARIFIER_MAIN_LOG_PATH, BABPC_RESPONSE_CONFIG
from .utils import BPClarifierCurrentState, BPClarifierState, BPCAskingState
from .llm_pipelines import BPClarifierConfig, BPClarifier
from ...utils import WeakReasonerState, AbstractWeakModule, WeakReasonerStatus
from ...utils import WeakGlobalSignal
from ....utils import UserResponse, BAResponse, Response
from .....utils import Logger
from .....specification_model import ReqSpecificationModel
from .....db_drivers.kv_driver import KeyValueDriverConfig

@dataclass
class BusinessProcessesCommunicatorConfig:
    """Конфигурация BusinessProcessesCommunicator-стадии в рамках WeakBAReasoner-стратегии общения с пользователем по формированию технического задания.
    
    :param bpq_generator_config: Конфигурация LLM-пайплайна по генерации вопросов для уточнения деталей специфицируемого проекта.
    :type bpq_generator_config: BPClarifierConfig
    :param clrf_questions_limit: Максимальное количество вопросов, которое может быть задано пользователю. Значение по умолчанию 10.
    :type clrf_questions_limit: int
    :param log: Отладочный класс для журналирования/мониторинга поведения инициализируемой компоненты. Значение по умолчанию Logger(TCLARIFIER_MAIN_LOG_PATH).
    :type log: Logger
    :param verbose: Если True, то информация о поведении класса будет сохраняться в stdout и файл-журналирования (log), иначе только в файл. Значение по умолчанию False.
    :type verbose: bool
    """
    
    bpq_generator_config: BPClarifierConfig = field(default_factory=lambda: BPClarifierConfig())

    clrf_questions_limit: int = -1 #10

    log: Logger = field(default_factory=lambda: Logger(BPCLARIFIER_MAIN_LOG_PATH))
    verbose: bool = False

class BusinessProcessesCommunicator(AbstractWeakModule):
    """Класс реализует сценарий общения с пользователем в рамках стадии по уточнению деталей проекта за счёт вопросов. 
    На основе коммуникации (уточняющих вопросов) в рамках текущей и предыдущих стадий будут формироваться дополнительные вопросы для пользователя.
    """

    def __init__(self, reqspec_model: ReqSpecificationModel, config: BusinessProcessesCommunicatorConfig = BusinessProcessesCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.cache_kvdriver_config = cache_kvdriver_config
        self.reqspec_model = reqspec_model
        self.mode = mode

        self.init_state()
        
        self.bp_clarifier = BPClarifier(self.config.bpq_generator_config, cache_kvdriver_config)

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.STATE = BPClarifierCurrentState()
        self.ASKED_QUESTIONS_COUNTER = 0
        self.CURRENT_QUESTION = None

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None, WeakReasonerState]]:
        tmp_state_response = deepcopy(BABPC_RESPONSE_CONFIG[self.STATE.base_state])
        done_state = None

        if self.STATE.base_state == BPClarifierState.clarify:            
            if self.config.clrf_questions_limit < 0 or self.ASKED_QUESTIONS_COUNTER < self.config.clrf_questions_limit:

                new_cquestion = None
                if self.mode == 'stub':
                    new_cquestion = "Уточняющий вопрос 'Заглушка'"
                elif self.mode == 'prod':
                    base_dhistory = self.reqspec_model.states_valuable_history[WeakReasonerState.task_clarifying]['general_qa']
                    detailed_dhistory = self.reqspec_model.states_valuable_history[WeakReasonerState.bp_clarifying]['detailed_qa']
                    new_cquestion = self.bp_clarifier.generate_question(base_dhistory, detailed_dhistory)
                else:
                    raise ValueError
                
                ba_response = tmp_state_response[BPCAskingState.question_preparing].ba_response
                reasoner_newstatus = tmp_state_response[BPCAskingState.question_preparing].reasoner_newstatus
                self.STATE = tmp_state_response[BPCAskingState.question_preparing].stage_newstate

                ba_response.ba_text = new_cquestion
                self.CURRENT_QUESTION = new_cquestion

            else:
                ba_response = tmp_state_response[BPCAskingState.limit_exceeded].ba_response
                reasoner_newstatus = tmp_state_response[BPCAskingState.limit_exceeded].reasoner_newstatus
                self.STATE = tmp_state_response[BPCAskingState.limit_exceeded].stage_newstate
        else:
            ba_response = tmp_state_response.ba_response
            reasoner_newstatus = tmp_state_response.reasoner_newstatus
            self.STATE = tmp_state_response.stage_newstate

        return ba_response, reasoner_newstatus, done_state

    def process_response(self, user_response: UserResponse) -> None:
        if user_response.signal is not None and user_response.signal == WeakGlobalSignal.next_stage:
            self.STATE.base_state = BPClarifierState.done

        elif self.STATE.base_state == BPClarifierState.clarify and self.STATE.askq_state == BPCAskingState.question_preparing:
            qa_pair = [Response(role='ba', text=self.CURRENT_QUESTION),Response(role='user', text=user_response.user_text)]    
            self.reqspec_model.states_valuable_history[WeakReasonerState.bp_clarifying]['detailed_qa'].sequence += qa_pair

            self.ASKED_QUESTIONS_COUNTER += 1
            self.CURRENT_QUESTION = None
        else:
            raise ValueError
    
    def reset(self):
        self.init_state()
        gc.collect()
        