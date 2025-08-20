from dataclasses import dataclass, field
from typing import Tuple, Union
from copy import deepcopy
from time import time
import random
import gc

from .config import USCOMMUNICATOR_MAIN_LOG_PATH, BAUSC_RESPONSE_CONFIG
from .utils import USExtractingState, USAddState, USEditState, USDeleteState, USClarifierState, USClarifierCurrentState
from .llm_pipelines import UserStoriesExtractor, UserStoriesExtractorConfig
from ...utils import AbstractWeakModule, UserResponse, BAResponse, \
    WeakReasonerState, WeakReasonerStatus, WeakStateSignal, WeakGlobalSignal
from .....specification_model import ReqSpecificationModel
from .....specification_model.utils import UserStory
from .....db_drivers.kv_driver import KeyValueDriverConfig
from .....utils.data_structs import create_id
from .....utils import Logger


@dataclass
class UserStoriesCommunicatorConfig:
    """Конфигурация UserStoriesCommunicator-стадии в рамках WeakBAReasoner-стратегии общения с пользователем по формированию технического задания.
    
    :param us_extractor_config: Конфигурация LLM-пайплайна по генерации/валидаци user-историй.
    :type us_extractor_config: UserStoriesExtractorConfig
    :param extracted_us_limit: Максимальное количество user-историй, которое может быть автоматически сгенерировано.Значение по умолчанию 5.
    :type extracted_us_limit: int
    :param log: Отладочный класс для журналирования/мониторинга поведения инициализируемой компоненты. Значение по умолчанию Logger(TCLARIFIER_MAIN_LOG_PATH).
    :type log: Logger
    :param verbose: Если True, то информация о поведении класса будет сохраняться в stdout и файл-журналирования (log), иначе только в файл. Значение по умолчанию False.
    :type verbose: bool
    """

    us_extractor_config: UserStoriesExtractorConfig = field(default_factory=lambda: UserStoriesExtractorConfig())

    extracted_us_limit: int = -1 #5

    log: Logger = field(default_factory=lambda: Logger(USCOMMUNICATOR_MAIN_LOG_PATH))
    verbose: bool = False

class UserStoriesCommunicator(AbstractWeakModule):
    """Класс реализует сценарий общения с пользователем в рамках стадии по уточнению user-историй. 
    На основе коммуникации (уточняющих вопросов) в рамках предыдущих стадий будет автоматически сформировано базовый наборе user-историй. 
    Пользователю будет доступен функционал по ручному добавлению новых user-историй, а также их удалению и редактированию. 
    При добавлении или редактировании user-истории выполняется её валидация на предмет соответствия заданным критериям. 
    """
    
    def __init__(self, reqspec_model: ReqSpecificationModel, config: UserStoriesCommunicatorConfig = UserStoriesCommunicatorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.cache_kvdriver_config = cache_kvdriver_config
        self.mode = mode

        self.us_extractor = UserStoriesExtractor(self.config.us_extractor_config, cache_kvdriver_config)

        self.init_state()

    def init_state(self):
        self.STATE = USClarifierCurrentState()
        self.EDITING_US_ID = None
        self.IS_US_VALID_FLAG = None
        self.IS_USID_VALID_FLAG = None

    def prepare_response(self) -> Tuple[BAResponse, WeakReasonerStatus, Union[None,WeakReasonerState]]:
        tmp_state_response = deepcopy(BAUSC_RESPONSE_CONFIG[self.STATE.base_state])
        done_state = None

        if self.STATE.base_state == USClarifierState.us_extracting:
            tmp_state_response = tmp_state_response[self.STATE.usextr_state]
            
            if self.STATE.usextr_state == USExtractingState.done:
                user_stories = None
                if self.mode == 'prod':
                    task_goal = self.reqspec_model.specification_struct.general.goal
                    base_dhistory = self.reqspec_model.states_valuable_history[WeakReasonerState.task_clarifying]['general_qa']
                    detailed_dhistory = self.reqspec_model.states_valuable_history[WeakReasonerState.bp_clarifying]['detailed_qa']
                    user_stories = self.us_extractor.extract_userstories(
                        task_goal, base_dhistory, detailed_dhistory, us_limit=self.config.extracted_us_limit)
                    
                elif self.mode == 'stub':
                    user_stories = [UserStory(id='1', statement="User-история #1"), UserStory(id='2', statement="User-история #2")]
                else: 
                    raise ValueError

                self.reqspec_model.specification_struct.user_stories = {us.id: us for us in user_stories}

                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

                ba_response.ba_text = ba_response.ba_text.format(us_amount=len(user_stories))
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

        elif self.STATE.base_state == USClarifierState.add:
            tmp_state_response = tmp_state_response[self.STATE.usadd_state]

            if self.STATE.usadd_state == USAddState.validating:
                response_keyword = None
                if self.IS_US_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_US_VALID_FLAG = None
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate
  
        elif self.STATE.base_state == USClarifierState.delete:
            tmp_state_response = tmp_state_response[self.STATE.usdelete_state]

            if self.STATE.usdelete_state == USDeleteState.usid_validating:
                response_keyword = None
                if self.IS_USID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_USID_VALID_FLAG = None
            else:
                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate
            
        elif self.STATE.base_state == USClarifierState.edit:
            tmp_state_response = tmp_state_response[self.STATE.usedit_state]

            if self.STATE.usedit_state == USEditState.usid_validating:
                response_keyword = None
                if self.IS_USID_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_USID_VALID_FLAG = None

            elif self.STATE.usedit_state == USEditState.editing_us:
                tmp_state_response.ba_response.user_base_answer = self.reqspec_model.specification_struct.user_stories[self.EDITING_US_ID].statement

                ba_response = tmp_state_response.ba_response
                reasoner_newstatus = tmp_state_response.reasoner_newstatus
                self.STATE = tmp_state_response.stage_newstate

            elif self.STATE.usedit_state == USEditState.validating:
                response_keyword = None
                if self.IS_US_VALID_FLAG:
                    response_keyword = 'good'
                else:
                    response_keyword = 'bad'

                ba_response = tmp_state_response[response_keyword].ba_response
                reasoner_newstatus = tmp_state_response[response_keyword].reasoner_newstatus
                self.STATE = tmp_state_response[response_keyword].stage_newstate
                self.IS_USID_VALID_FLAG = None

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
        if self.STATE.base_state == USClarifierState.select_act:
            if user_response.signal is None:
                raise ValueError
            
            if user_response.signal == WeakGlobalSignal.next_stage:
                self.STATE.base_state = USClarifierState.done

            elif user_response.signal == WeakStateSignal.add:
                self.STATE.base_state = USClarifierState.add
                self.STATE.usadd_state = USAddState.init
            
            elif user_response.signal == WeakStateSignal.delete:
                self.STATE.base_state = USClarifierState.delete
                self.STATE.usdelete_state = USDeleteState.init
            
            elif user_response.signal == WeakStateSignal.edit:
                self.STATE.base_state = USClarifierState.edit
                self.STATE.usedit_state = USEditState.init
            
            else:
                raise ValueError

        elif self.STATE.base_state == USClarifierState.add:
    
            if self.STATE.usadd_state == USAddState.adding_us:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.usadd_state = USAddState.done
                else:
                    if self.mode == 'prod':
                        task_goal = self.reqspec_model.specification_struct.general.goal
                        #self.IS_US_VALID_FLAG = self.us_extractor.is_userstory_valid(task_goal, user_story=user_response.user_text)
                        self.IS_US_VALID_FLAG = True
                    elif self.mode == 'stub':
                        self.IS_US_VALID_FLAG = random.sample([True,False],1)[0]
                        #self.IS_US_VALID_FLAG = True
                    else:
                        raise ValueError

                    if self.IS_US_VALID_FLAG:
                        new_userstory = UserStory(id=create_id(str(time())), statement=user_response.user_text)
                        self.reqspec_model.specification_struct.user_stories[new_userstory.id] = new_userstory

                    self.STATE.usadd_state = USAddState.validating

            else:
                raise ValueError
            
        elif self.STATE.base_state == USClarifierState.delete:
            
            if self.STATE.usdelete_state == USDeleteState.us_selecting:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.usdelete_state = USDeleteState.done
                else:
                    us_id = user_response.user_text
                    self.IS_USID_VALID_FLAG = us_id in list(self.reqspec_model.specification_struct.user_stories.keys())
                    self.STATE.usdelete_state = USDeleteState.usid_validating
                    if self.IS_USID_VALID_FLAG:
                      del self.reqspec_model.specification_struct.user_stories[us_id]  
            else:
                raise ValueError
            
        elif self.STATE.base_state == USClarifierState.edit:

            if self.STATE.usedit_state == USEditState.us_selecting:

                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.usedit_state = USEditState.done
                else:
                    us_id = user_response.user_text
                    self.IS_USID_VALID_FLAG = us_id in list(self.reqspec_model.specification_struct.user_stories.keys())
                    self.STATE.usedit_state = USEditState.usid_validating
                    if self.IS_USID_VALID_FLAG:
                        self.EDITING_US_ID = user_response.user_text
               
            elif self.STATE.usedit_state == USEditState.editing_us:
                if user_response.signal == WeakStateSignal.cancel_operation:
                    self.STATE.usedit_state = USEditState.done
                else:
                    if self.mode == 'prod':
                        #self.IS_US_VALID_FLAG = self.us_extractor.is_userstory_valid(self.reqspec_model, user_story=user_response.user_text)
                        self.IS_US_VALID_FLAG = True
                    elif self.mode == 'stub':
                        self.IS_US_VALID_FLAG = random.sample([True,False],1)[0]
                        #self.IS_US_VALID_FLAG = True
                    else:
                        raise ValueError

                    if self.IS_US_VALID_FLAG:
                        self.reqspec_model.specification_struct.user_stories[self.EDITING_US_ID] = UserStory(id=self.EDITING_US_ID, statement=user_response.user_text)

                    self.STATE.usedit_state = USEditState.validating
                    
            else:
                raise ValueError
        else:
            raise ValueError
    
    def reset(self):
        self.init_state()
        gc.collect()