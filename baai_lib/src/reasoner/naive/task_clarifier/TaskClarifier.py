from dataclasses import dataclass, field
from typing import Tuple
from ....utils import Logger, AgentTaskSolverConfig, AgentTaskSolver, ReturnStatus
from ....agents import AgentDriver, AgentDriverConfig
from ....db_drivers.kv_driver import KeyValueDriverConfig
from ..utils import AbstractNaiveModule, NaiveReasonerStatus, NaiveGlobalSignal
from ...utils import BAResponse, UserResponse, Response, DialogueHistory
from .config import BA_TASKCLAR_NOTICE, BA_MESSAGE_WITH_STOP_QCLARIFICATION_NOTICE, DEFAULT_CQG_TASK_CONFIG
from ..config import NBAR_GLOBAL_SIGNALSINFO
from .utils import TaskClarifierState

TCLARIFIER_MAIN_LOG_PATH = 'log/reasoner/naive/t_clarifier/main'

@dataclass
class TaskClarifierConfig:
    clarify_questions_limit: int = 10

    lang: str = "ru"
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    condqgen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_CQG_TASK_CONFIG)

    log: Logger = field(default_factory=lambda: Logger(TCLARIFIER_MAIN_LOG_PATH))
    verbose: bool = False

class TaskClarifier(AbstractNaiveModule):
    def __init__(self, dialogue_history: DialogueHistory, config: TaskClarifierConfig = TaskClarifierConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.dialogue_history = dialogue_history
        self.mode = mode

        self.init_module_state()

        self.agent = AgentDriver.connect(config.adriver_config)
        self.condqgen_solver = AgentTaskSolver(
            self.agent, self.config.condqgen_task_config, cache_kvdriver_config)
        
        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_module_state(self):
        self.state = TaskClarifierState.greetings
        self.asked_questions_counter = 0
        self.next_stage = False

    def prepare_response(self) -> Tuple[BAResponse, NaiveReasonerStatus]:
        ba_response, new_status = None, None
        if self.state == TaskClarifierState.greetings:
            ba_response = BAResponse(ba_text=BA_TASKCLAR_NOTICE)
            self.state = TaskClarifierState.clarifying
            new_status = NaiveReasonerStatus.waiting_interaction

        elif self.state == TaskClarifierState.clarifying:
            if self.asked_questions_counter <= self.config.clarify_questions_limit:
                if self.mode == 'prod':
                    clarify_question, status = self.condqgen_solver.solve(lang=self.config.lang, dialogue_history=self.dialogue_history)
                    if status != ReturnStatus.success:
                        # TODO: Предложить обработчик ошибки парсинга ответа LLM
                        raise ValueError
                elif self.mode == 'stub':
                    clarify_question = 'Заглушка с уточняющим вопросом.'
                else:
                    raise ValueError

                cur_global_signals = [NBAR_GLOBAL_SIGNALSINFO['next_stage']] if self.asked_questions_counter > 0 else []
                ba_response = BAResponse(ba_text=clarify_question, available_state_signals=cur_global_signals)

                self.dialogue_history.sequence.append(Response(role='ba', text=ba_response.ba_text))
                new_status = NaiveReasonerStatus.waiting_response
                self.asked_questions_counter += 1

            else:
                ba_response = BAResponse(ba_text=BA_MESSAGE_WITH_STOP_QCLARIFICATION_NOTICE)
                new_status = NaiveReasonerStatus.done
                self.state = TaskClarifierState.done
        else:
            raise AttributeError


        return ba_response, new_status

    def process_response(self, user_response: UserResponse) -> NaiveReasonerStatus:
        new_status = None
        if self.state == TaskClarifierState.clarifying:
            if user_response.signal is not None:
                self.next_stage = user_response.signal == NaiveGlobalSignal.next_stage
                if self.next_stage:
                    self.state = TaskClarifierState.done
                    new_status = NaiveReasonerStatus.done
                else:
                    raise ValueError
                
            elif user_response.user_text is not None:
                 self.dialogue_history.sequence.append(Response(role='user', text=user_response.user_text))
                 new_status = NaiveReasonerStatus.waiting_interaction
            else:
                raise ValueError
            
        else:
            raise AttributeError
        
        return new_status
        
    def reset(self):
        self.init_module_state()
