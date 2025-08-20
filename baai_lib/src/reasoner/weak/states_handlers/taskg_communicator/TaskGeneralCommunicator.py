from dataclasses import dataclass, field
from typing import Tuple, Dict, Union
from copy import deepcopy
import random
import gc

from .config import BATC_RESPONSE_CONFIG, TASK_GENERAL_QUESTIONS, TCLARIFIER_MAIN_LOG_PATH
from .utils import TaskGeneralCommunicatorState, TGCTaskClassifyingState, TGCAskingState, \
    TGCInfoExtractingState, TGClarifierCurrentState
from .llm_pipelines import TaskClassifier, TaskClassifierConfig, GeneralInfoExtractor, GeneralInfoExtractorConfig
from ...utils import AbstractWeakModule, WeakReasonerStatus, WeakGlobalSignal, WeakReasonerState
from ....utils import BAResponse, UserResponse, Response
from .....specification_model import ReqSpecificationModel
from .....db_drivers.kv_driver import KeyValueDriverConfig
from .....utils import Logger

@dataclass
class TaskGeneralCommunicatorConfig:
    """Конфигурация TaskGeneralCommunicator-стадии в рамках WeakBAReasoner-стратегии общения с пользователем по формированию технического задания.
    
    :param task_classificator_config: Конфигурация LLM-пайплайна по определению типа ТЗ на основении описанного пользователем проекта/задачи. 
    :type task_classificator_config: TaskClassifierConfig
    :param generalinfo_extractor_config: Конфигурация LLM-пайплайна по извлечению общей информации по теме проекта из стартового диалога с пользователем. 
    :type generalinfo_extractor_config:  GeneralInfoExtractorConfig
    :param min_questions_amount: Минимальное количество вопросов от бизнес-аналитика, на которые должен ответить пользователем, чтобы получить возможность пропуска оставшихя вопросов и перехода на следующую стадию общения.Значение по умолчанию 2.
    :type min_questions_amount: int
    :param log: Отладочный класс для журналирования/мониторинга поведения инициализируемой компоненты. Значение по умолчанию Logger(TCLARIFIER_MAIN_LOG_PATH).
    :type log: Logger
    :param verbose: Если True, то информация о поведении класса будет сохраняться в stdout и файл-журналирования (log), иначе только в файл. Значение по умолчанию False.
    :type verbose: bool
    """

    task_classificator_config: TaskClassifierConfig = field(default_factory=lambda: TaskClassifierConfig())
    generalinfo_extractor_config: GeneralInfoExtractorConfig = field(default_factory=lambda: GeneralInfoExtractorConfig())

    min_questions_amount: int = 2

    log: Logger = field(default_factory=lambda: Logger(TCLARIFIER_MAIN_LOG_PATH))
    verbose: bool = False

class TaskGeneralCommunicator(AbstractWeakModule):
    """Класс реализует сценарий общения с пользователем в рамках стадии по уточнению общих моментов по формируемому техническому заданию. 
    Пользователю будет задано фиксированное количество шаблонных вопросов. После будет выполнена проверка: на основании описанного проекта, 
    поддерживается ли в рамках данной библиотеки определённая стратегия общения по формированию ТЗ релевантного типа.
    Если необходимый тип ТЗ поддерживается, то выполняется переход на следующую стадию общения; предварительно на основе полученной информации 
    от пользователя формулируется назначение проекта, основные задачи в рамках проекта и предложение о необходимости интеграции будущего продукта 
    в сторонние системы.
    """

    def __init__(self, reqspec_model: ReqSpecificationModel, config: TaskGeneralCommunicatorConfig = TaskGeneralCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.mode = mode

        self.init_state()
        
        self.task_classifier = TaskClassifier(self.config.task_classificator_config, cache_kvdriver_config)
        self.ginfo_extractor = GeneralInfoExtractor(self.config.generalinfo_extractor_config, cache_kvdriver_config)

        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_state(self):
        self.CURRENT_QUESTION_IDX = -1
        self.STATE = TGClarifierCurrentState()
        self.IS_TASK_SUPPORTED = None

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[WeakReasonerState]]:
        tmp_state_response = deepcopy(BATC_RESPONSE_CONFIG[self.STATE.base_state])
        done_state = None

        # Формирование уточняющих вопросов
        if self.STATE.base_state == TaskGeneralCommunicatorState.clarifying:
            self.CURRENT_QUESTION_IDX += 1

            if self.CURRENT_QUESTION_IDX >= len(TASK_GENERAL_QUESTIONS):
                ba_response = tmp_state_response[TGCAskingState.limit_exceeded].ba_response
                reasoner_newstatus = tmp_state_response[TGCAskingState.limit_exceeded].reasoner_newstatus
                self.STATE = tmp_state_response[TGCAskingState.limit_exceeded].stage_newstate
                
            else:
                ba_response = tmp_state_response[TGCAskingState.question_preparing].ba_response
                reasoner_newstatus = tmp_state_response[TGCAskingState.question_preparing].reasoner_newstatus
                self.STATE = tmp_state_response[TGCAskingState.question_preparing].stage_newstate
                
                if self.CURRENT_QUESTION_IDX < self.config.min_questions_amount:
                    ba_response.available_global_signals = list()

                ba_response.ba_text = TASK_GENERAL_QUESTIONS[self.CURRENT_QUESTION_IDX]

        # Выполнение классификации типа ТЗ 
        elif self.STATE.base_state == TaskGeneralCommunicatorState.task_classifying:
            tmp_state_response = tmp_state_response[self.STATE.tcls_state]

            # Классификации релевантного типа ТЗ под описанный пользователем проект
            if self.STATE.tcls_state == TGCTaskClassifyingState.classifying:
                if self.mode == 'stub':
                    #self.IS_TASK_SUPPORTED= random.sample([True,False],1)[0]
                    self.IS_TASK_SUPPORTED= True

                elif self.mode == 'prod':
                    base_dhistory = self.reqspec_model.states_valuable_history[WeakReasonerState.task_clarifying]['general_qa']
                    self.IS_TASK_SUPPORTED = self.task_classifier.is_task_supported(base_dhistory)
                else:
                    raise ValueError

                if self.IS_TASK_SUPPORTED:
                    text_clsinfo = "поддерживается"
                else:
                    text_clsinfo = "не поддерживается"

                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                ba_response.ba_text = ba_response.ba_text.format(t_cls=text_clsinfo)

            # Уведомление о завершении операции
            elif self.STATE.tcls_state == TGCTaskClassifyingState.done:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                # Принимается решение: продолжить формирование тз или завершить процесс
                if self.IS_TASK_SUPPORTED:
                    self.STATE.base_state = TaskGeneralCommunicatorState.info_extracting
                else:
                    self.STATE.base_state = TaskGeneralCommunicatorState.done
                    done_state = WeakReasonerState.done_unsupported_task
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate
        
        # Извлекаем информацию из деилога с пользователем для формирования
        # некоторыъ разделов ТЗ
        elif self.STATE.base_state == TaskGeneralCommunicatorState.info_extracting:
            ba_response = tmp_state_response[self.STATE.iextr_state].ba_response
            reasoner_newstatus = tmp_state_response[self.STATE.iextr_state].reasoner_newstatus
            self.STATE = tmp_state_response[self.STATE.iextr_state].stage_newstate

            # Генерация секции ТЗ с описанием назначения проекта 
            if self.STATE.iextr_state == TGCInfoExtractingState.goal_extr_process:
                tgoal_summary = None
                if self.mode == 'stub':
                    tgoal_summary = "Заглушка с описанием назначения проекта."
                elif self.mode == 'prod':
                    tgoal_summary = self.ginfo_extractor.summarize_task_goal(
                        self.reqspec_model.states_valuable_history[WeakReasonerState.task_clarifying]['general_qa'])
                else:
                    raise ValueError
                
                self.reqspec_model.specification_struct.general.goal = tgoal_summary

            # Генерация секции ТЗ с описанием основных задач в рамках проекта
            elif self.STATE.iextr_state == TGCInfoExtractingState.subt_extr_process:
                subt_summary = None
                if self.mode == 'stub':
                    subt_summary = "Заглушка с описанием основных задач в рамках проекта."
                elif self.mode == 'prod':
                    subt_summary = self.ginfo_extractor.summarize_sub_tasks(
                        self.reqspec_model.states_valuable_history[WeakReasonerState.task_clarifying]['general_qa'],
                        self.reqspec_model.specification_struct.general.goal)
                else:
                    raise ValueError
                
                self.reqspec_model.specification_struct.general.sub_tasks = subt_summary

            # Генерация секции ТЗ с описанием интеграционных моментов по проекту
            elif self.STATE.iextr_state == TGCInfoExtractingState.integr_extr_process:
                integr_summary = None
                if self.mode == 'stub':
                    integr_summary = "Заглушка с описанием интеграционных моментов в рамках проекта."
                elif self.mode == 'prod':
                    integr_summary = self.ginfo_extractor.summarize_integration(
                        self.reqspec_model.states_valuable_history[WeakReasonerState.task_clarifying]['general_qa'],
                        self.reqspec_model.specification_struct.general.goal)
                else:
                    raise ValueError
                
                self.reqspec_model.specification_struct.general.integration = integr_summary
        
        else:
            ba_response = tmp_state_response.ba_response
            reasoner_newstatus = tmp_state_response.reasoner_newstatus
            self.STATE = tmp_state_response.stage_newstate

        
        return ba_response, reasoner_newstatus, done_state

    def process_response(self, user_response: UserResponse) -> None:
        
        # Переходим в состояние по классификации типа ТЗ при получении сигнала 
        # во время QA-сессии с пользователем на общие темы/вопросы 
        if user_response.signal is not None and user_response.signal == WeakGlobalSignal.next_stage:
            self.STATE.base_state = TaskGeneralCommunicatorState.task_classifying

        # Получение/обработка ответа пользователя на общий вопрос от AI бизнес-аналитика
        elif self.STATE.base_state == TaskGeneralCommunicatorState.clarifying:
            new_qapair = [Response(role='ba', text=TASK_GENERAL_QUESTIONS[self.CURRENT_QUESTION_IDX]), Response(role='user', text=user_response.user_text)]
            self.reqspec_model.states_valuable_history[WeakReasonerState.task_clarifying]['general_qa'].sequence += new_qapair
            
        else:
            raise ValueError

    def reset(self):
        self.init_state()
        gc.collect
